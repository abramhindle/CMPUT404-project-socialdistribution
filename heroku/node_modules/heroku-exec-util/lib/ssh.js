'use strict'

const child = require('child_process');
const cli = require('heroku-cli-util');
const Client = require('ssh2').Client;
const crypto = require('crypto');
const tty = require('tty')
const stream = require('stream')
const fs = require('fs')
const socks = require('@heroku/socksv5');
const progress = require('smooth-progress')
const temp = require('temp')

function connect(context, addonHost, dynoUser, privateKey, proxyKey, callback) {
  return new Promise((resolve, reject) => {
    var conn = new Client();
    cli.hush("[cli-ssh] created")
    conn.on('ready', function() {
      cli.hush("[cli-ssh] ready")
      cli.action.done('up')
      if (context.args.length > 0 && context.args != 'bash') {
        let cmd = _buildCommand(context.args)
        cli.hush(`[cli-ssh] command: ${cmd}`)
        conn.exec(cmd, function(err, stream) {
          cli.hush("[cli-ssh] exec")
          if (err) {
            cli.hush(`[cli-ssh] err: ${err}`)
            throw err;
          }
          stream.on('close', function(code, signal) {
            cli.hush("[cli-ssh] close")
            conn.end();
            resolve();
            if (callback) callback();
          })
          .on('data', _readData(stream))
          .on('error', reject);
          process.once('SIGINT', () => conn.end())
        });
      } else {
        cli.hush("[cli-ssh] bash")
        conn.shell(function(err, stream) {
          cli.hush("[cli-ssh] shell")
          if (err) {
            cli.hush(`[cli-ssh] err: ${err}`)
            return _logConnectionError(err);
          }
          stream.on('close', function() {
            cli.hush("[cli-ssh] close")
            conn.end();
            resolve();
          })
          .on('data', _readData(stream))
          .on('error', function (err) {
            cli.hush(err)
            cli.error("There was a networking error! Please try connecting again.")
            reject
          })
          process.once('SIGINT', () => conn.end())
        });
      }
    }).on('error', function(err) {
      cli.hush(err)
      if (err.message === "Keepalive timeout") {
        cli.error("Connection to the dyno timed out!")
      } else {
        cli.error("There was an error connecting to the dyno!")
      }
      reject
    }).connect({
      ..._connectionDefaults(proxyKey),
      host: addonHost,
      username: dynoUser,
      privateKey: privateKey,
      keepaliveInterval: 10000,
      keepaliveCountMax: 3,
      debug: cli.hush
    });
  });
}

function ssh(context, addonHost, dynoUser, privateKey, proxyKey) {
  cli.hush("[cli-ssh] native")
  return new Promise((resolve, reject) => {
    temp.track();
    temp.open('heroku-exec-key', function(err, info) {
      if (!err) {
        fs.writeSync(info.fd, privateKey);
        fs.close(info.fd, function(err) {
          fs.chmodSync(`${info.path}`, "0700")
          temp.open('heroku-exec-proxy-key', function(err, proxyKeyFile) {
            if (!err) {
              fs.writeSync(proxyKeyFile.fd, `[${addonHost}]:80 ${proxyKey}`);
              fs.close(proxyKeyFile.fd, function(err) {
                let sshCommand = "ssh " +
                  `-o UserKnownHostsFile=${proxyKeyFile.path} ` +
                  "-o ServerAliveInterval=10 " +
                  "-o ServerAliveCountMax=3 " +
                  "-p 80 " +
                  `-i ${info.path} ` +
                  `${dynoUser}@${addonHost} `

                if (context.args.length > 0 && context.args != 'bash') {
                  sshCommand = `${sshCommand} ${_buildCommand(context.args)}`
                }

                try {
                  child.execSync(sshCommand, { stdio: ['inherit', 'inherit', 'ignore' ] }
                  )
                } catch (e) {
                  if (e.stderr) cli.hush(e.stderr)
                  cli.hush(`[cli-ssh] exit: ${e.status}, ${e.message}`)
                }
              });
            }
          });
        });
      }
    });
  });
}

function scp(context, addonHost, dynoUser, privateKey, proxyKey, src, dest) {
  return new Promise((resolve, reject) => {
    var conn = new Client();
    conn.on('ready', function() {
      cli.action.done('up')
      conn.sftp(function(err, sftp) {
        if (err) {
          return _logConnectionError(err);
        }

        var bar = false;
        var progressCallback = function (totalTransferred, chunk, totalFile) {
          if (!bar) {
            bar = progress({
              tmpl: 'Downloading... :bar :percent :eta',
              width: 25,
              total: totalFile
            })
          }
          bar.tick(chunk, totalTransferred)
        };

        sftp.fastGet(src, dest, {
          step: function (totalTransferred, chunk, totalFile) {
            progressCallback(totalTransferred, chunk, totalFile);
          }
        }, function(error) {
          if (error) {
            cli.hush(error)
            cli.error("ERROR: Could not transfer the file!");
            cli.error("Make sure the filename is correct.");
          }
          conn.end();
          resolve();
        });
      });
    }).on('error', reject).connect({
      ..._connectionDefaults(proxyKey),
      host: addonHost,
      username: dynoUser,
      privateKey: privateKey
    });
  });
}

function _logConnectionError(err) {
  cli.error("ERROR: Could not connect to the dyno!");
  cli.error(`Check that the dyno is active by running ${cli.color.white.bold("heroku ps")}`);
  return err;
}

function _readData (c) {
  let firstLine = true
  return function(data) {
    if (firstLine) {
      firstLine = false
      _readStdin(c)
    }
    if (data) {
      data = data.toString().replace(' \r', '\n')
      process.stdout.write(data)
    }
  }
}

function _readStdin (c) {
  let stdin = process.stdin
  stdin.setEncoding('utf8')
  if (stdin.unref) stdin.unref()
  if (tty.isatty(0)) {
    stdin.setRawMode(true)
    stdin.pipe(c)
    let sigints = []
    stdin.on('data', function (c) {
      if (c === '\u0003') sigints.push(new Date())
      sigints = sigints.filter(d => d > new Date() - 1000)
      if (sigints.length >= 4) {
        cli.error('forcing dyno disconnect')
        process.exit(1)
      }
    })
  } else {
    stdin.pipe(new stream.Transform({
      objectMode: true,
      transform: (chunk, _, next) => c.write(chunk, next),
      flush: done => c.write('\x04', done)
    }))
  }
}

function socksv5(context, addonHost, dynoUser, privateKey, proxyKey, callback) {
  var socksPort = 1080;
  socks.createServer(function(info, accept, deny) {
    var conn = new Client();
    conn.on('ready', function() {
      conn.forwardOut(info.srcAddr,
                      info.srcPort,
                      info.dstAddr,
                      info.dstPort,
                      function(err, stream) {
        if (err) {
          conn.end();
          return deny();
        }

        var clientSocket;
        if (clientSocket = accept(true)) {
          stream.pipe(clientSocket).pipe(stream).on('close', function() {
            conn.end();
          });
        } else
          conn.end();
      });
    }).on('error', function(err) {
      deny();
    }).connect({
      ..._connectionDefaults(proxyKey),
      host: addonHost,
      username: dynoUser,
      privateKey: privateKey
    });
  }).listen(socksPort, 'localhost', function() {
    console.log(`SOCKSv5 proxy server started on port ${cli.color.white.bold(socksPort)}`);
    if (callback) callback(socksPort);
  }).useAuth(socks.auth.None());
}

function _buildCommand (args) {
  if (args.length === 1) {
    // do not add quotes around arguments if there is only one argument
    // `heroku run "rake test"` should work like `heroku run rake test`
    return args[0]
  }
  let cmd = ''
  for (let arg of args) {
    if (arg.indexOf(' ') !== -1 || arg.indexOf('"') !== -1) {
      arg = '"' + arg.replace(/"/g, '\\"') + '"'
    }
    cmd = cmd + ' ' + arg
  }
  return cmd.trim()
}

function _connectionDefaults(proxyKey) {
  return {
    port: 80,
    hostHash: 'sha256',
    hostVerifier: function(hashedKey) {
      var hasher = crypto.createHash('sha256');
      hasher.update(Buffer.from(proxyKey.split(' ')[1], 'base64'));
      return hasher.digest('hex') === hashedKey
    }
  }
}

module.exports = {
  ssh,
  socksv5,
  connect,
  scp
}
