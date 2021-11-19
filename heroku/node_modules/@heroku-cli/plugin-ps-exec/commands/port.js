'use strict';

const cli = require('heroku-cli-util');
const exec = require('heroku-exec-util');
const co = require('co');
const socks = require('@heroku/socksv5')
var net = require("net");

module.exports = function(topic, command) {
  return {
    topic: topic,
    command: command,
    description: 'Forward traffic on a local port to a dyno',
    help: `Provide a port or comma-separated list of ports to forward.

    For example, "4000,9000:9001" will forward port 4000 to port 4000 and
    port 9000 to port 9001.

    Example:

    $ heroku ps:forward 8080 --app murmuring-headland-14719`,
    args: [{name: 'port', optional: false}],
    flags: [
      { name: 'dyno', char: 'd', hasValue: true, description: 'specify the dyno to connect to' },
      { name: 'localPort', char: 'p', hasValue: true, hidden: true, description: 'the local port to use' } ],
    needsApp: true,
    needsAuth: true,
    run: cli.command(co.wrap(run))
  }
};

function * run(context, heroku) {
  yield exec.initFeature(context, heroku, function *(configVars) {
    const portMappings = context.args.port.split(',').map(function(portMapping) {
      const ports = portMapping.split(':')

      // this will error out if localPort is used with multiple ports, but
      // that's ok because localPort is only here for backwards compat
      return [ports[0], ports[1] || context.flags.localPort || ports[0]]
    })

    yield exec.createSocksProxy(context, heroku, configVars, function(dynoIp, dynoName, socksPort) {
      portMappings.forEach(function(portMapping) {
        const localPort = portMapping[0]
        const remotePort = portMapping[1]

        cli.log(`Listening on ${cli.color.white.bold(localPort)} and forwarding to ${cli.color.white.bold(`${dynoName}:${remotePort}`)}`)

        net.createServer(function(connIn) {
          socks.connect({
            host: '0.0.0.0',
            port: remotePort,
            proxyHost: '127.0.0.1',
            proxyPort: socksPort,
            auths: [ socks.auth.None() ]
          }, function(socket) {
            connIn.pipe(socket);
            socket.pipe(connIn);
          });
        }).listen(localPort);
      })

      cli.log(`Use ${cli.color.magenta('CTRL+C')} to stop port fowarding`)
    });
  });
  return new Promise(resolve => {})
}
