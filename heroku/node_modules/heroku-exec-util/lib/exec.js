'use strict'

const cli = require('heroku-cli-util')
const path = require('path');
const child = require('child_process');
const url = require('url');
const co = require('co');
const keypair = require('keypair');
const forge = require('node-forge');
const socks = require('@heroku/socksv5');
const ssh = require('./ssh')
const wait = require('co-wait')

function * checkStatus(context, heroku, configVars) {
  let dynos = yield heroku.request({path: `/apps/${context.app}/dynos`})

  var execUrl = _execUrl(context, configVars)

  return cli.got(`https://${execUrl.host}`, {
    auth: execUrl.auth,
    path: _execApiPath(configVars),
    headers: _execHeaders(),
    method: 'GET'
  }).then(response => {

    var reservations = JSON.parse(response.body);

    cli.styledHeader(`Heroku Exec ${cli.color.app(context.app)}`)

    if (reservations.length == 0) {
      cli.error("Heroku Exec is not running!")
      cli.error("Check dyno status with `heroku ps'")
    } else {

      var statuses = []

      for (var i in reservations) {
        var name = reservations[i]['dyno_name']
        var dyno = dynos.find(d => d.name === name)

        statuses.push({
          dyno_name: cli.color.white.bold(name),
          proxy_status: 'running',
          dyno_status: !dyno ? cli.color.red('missing!') : (dyno.state === 'up' ? cli.color.green(dyno.state) : cli.color.yellow(dyno.state))
        })
      }
      cli.table(statuses, {
        columns: [
          {key: 'dyno_name', label: 'Dyno'},
          {key: 'proxy_status', label: 'Proxy Status'},
          {key: 'dyno_status', label: 'Dyno Status'},
        ]
      });
    }
  }).catch(error => {
    cli.error(error);
  });;
}

function * initFeature(context, heroku, callback) {
  var buildpackUrls = ["https://github.com/heroku/exec-buildpack", "urn:buildpack:heroku/exec"]
  let promises = {
    app: heroku.get(`/apps/${context.app}`),
    feature: heroku.get(`/apps/${context.app}/features/runtime-heroku-exec`),
    config: heroku.get(`/apps/${context.app}/config-vars`),
    buildpacks: heroku.request({
      path: `/apps/${context.app}/buildpack-installations`,
      headers: {Range: ''}
    })
  }

  let data = yield promises
  let feature = data.feature
  let configVars = data.config
  let buildpacks = data.buildpacks

  if (data.app['space'] != null) {
    if (data.app['space']['shield'] === true) {
      cli.error(`This feature is restricted for Shield Private Spaces`)
      cli.exit(1);
    } else if (buildpacks.length === 0) {
      cli.error(`${context.app} has no Buildpack URL set. You must deploy your application first!`)
      cli.exit(1);
    } else if (!(_hasExecBuildpack(buildpacks, buildpackUrls))) {
      yield _enableFeature(context, heroku)
      cli.log(`Adding the Heroku Exec buildpack to ${context.app}`)
      child.execSync(`heroku buildpacks:add -i 1 heroku/exec -a ${context.app}`)
      cli.log('')
      cli.log('Run the following commands to redeploy your app, then Heroku Exec will be ready to use:')
      cli.log(cli.color.magenta('  git commit -m "Heroku Exec initialization" --allow-empty'))
      cli.log(cli.color.magenta('  git push heroku master'))
      cli.exit(0);
    }
  } else if (_hasExecBuildpack(buildpacks, buildpackUrls)) {
    cli.warn(`The Heroku Exec buildpack is no longer required for this app,\n` +
             `and may interfer with the 'heroku run' command. Please run the\n` +
             `following command to remove it:\n  ` +
             cli.color.magenta('heroku buildpacks:remove https://github.com/heroku/exec-buildpack'))
  }

  var addonUrl = configVars['HEROKU_EXEC_URL']
  if (addonUrl) {
    cli.error("It looks like you're using the Heroku Exec addon, which is no longer required\n" +
              "to use this feature. Please run the following command to remove the addon\n" +
              "and then try using Heroku Exec again:\n" +
              cli.color.magenta('  heroku addons:destroy heroku-exec'));
    cli.exit();
  } else if (!feature.enabled) {
    cli.log(`Running this command for the first time requires a dyno restart.`)
    let answer = yield cli.prompt('Do you want to continue? [y/n]', {});

    if (answer.trim().toLowerCase() !== 'y') {
      cli.exit();
    }

    yield _enableFeature(context, heroku)

    yield cli.action(`Restarting dynos`, co(function * () {
      yield wait(2000)
      yield heroku.request({method: 'DELETE', path: `/apps/${context.app}/dynos`});
    }))

    let dynoName = _dyno(context)
    let state = 'down'
    yield cli.action(`Waiting for ${cli.color.cyan(dynoName)} to start`, co(function * () {
      while (state != 'up') {
        yield wait(3000)
        let d = yield heroku.request({path: `/apps/${context.app}/dynos/${dynoName}`})
        state = d.state
        if (state === 'crashed') {
          throw new Error(`The dyno crashed`)
        }
      }
    }))
  }

  yield callback(configVars);
}

function updateClientKey(context, heroku, configVars, callback) {
  return cli.action("Establishing credentials", {success: false}, co(function* () {
    var key = keypair();
    var privkeypem = key.private;
    var publicKey = forge.pki.publicKeyFromPem(key.public);
    var pubkeypem = forge.ssh.publicKeyToOpenSSH(publicKey, '');
    cli.hush(pubkeypem)

    var execUrl = _execUrl(context, configVars)
    var dyno = _dyno(context)

    return cli.got(`https://${execUrl.host}`, {
      auth: execUrl.auth,
      path: `${_execApiPath(configVars)}/${dyno}`,
      method: 'PUT',
      headers: {..._execHeaders(), 'content-type': 'application/json'},
      body: JSON.stringify({client_key: pubkeypem})
    }).then(function (response) {
      cli.action.done('done')
      callback(privkeypem, dyno, response);
    }).catch(error => {
      cli.action.done('error');
      cli.hush(error);
      cli.error('Could not connect to dyno!\nCheck if the dyno is running with `heroku ps\'')
    });;
  }))
}


function createSocksProxy(context, heroku, configVars, callback) {
  return updateClientKey(context, heroku, configVars, function(privateKey, dyno, response) {
    cli.hush(response.body);
    var json = JSON.parse(response.body);

    ssh.socksv5(context, json['tunnel_host'], json['client_user'], privateKey, json['proxy_public_key'], function(socks_port) {
      if (callback) callback(json['dyno_ip'], dyno, socks_port)
      else cli.log(`Use ${cli.color.magenta('CTRL+C')} to stop the proxy`)
    });
  })
}

function _execApiPath(configVars) {
  if (configVars['HEROKU_EXEC_URL']) {
    return '/api/v1';
  } else {
    return '/api/v2'
  }
}

function _execUrl(context, configVars) {
  var urlString = configVars['HEROKU_EXEC_URL']
  if (urlString) {
    return url.parse(urlString);
  } else {
    if (process.env.HEROKU_EXEC_URL === undefined) {
      urlString = "https://exec-manager.heroku.com/"
    } else {
      urlString = process.env.HEROKU_EXEC_URL
    }
    var execUrl = url.parse(urlString)
    execUrl.auth = `${context.app}:${process.env.HEROKU_API_KEY || context.auth.password}`
    return execUrl
  }
}

function _dyno(context) {
  return context.flags.dyno || 'web.1'
}

function _hasExecBuildpack(buildpacks, urls) {
  for (let b of buildpacks) {
    for (let u of urls) {
      if (b['buildpack']['url'].indexOf(u) === 0) return true
    }
  }
  return false
}

function _enableFeature(context, heroku) {
  return cli.action('Initializing feature', co(function* () {
    yield heroku.request({
      method: 'PATCH',
      path: `/apps/${context.app}/features/runtime-heroku-exec`,
      body: {'enabled' : true}
    });
  }));
}

function _execHeaders() {
  if (process.env.HEROKU_HEADERS) {
    cli.hush(`using headers: ${process.env.HEROKU_HEADERS}`)
    return JSON.parse(process.env.HEROKU_HEADERS)
  } else {
    return {}
  }
}

module.exports = {
  createSocksProxy,
  checkStatus,
  initFeature,
  updateClientKey
}
