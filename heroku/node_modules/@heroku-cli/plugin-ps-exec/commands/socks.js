'use strict';

const cli = require('heroku-cli-util');
const exec = require('heroku-exec-util');
const co = require('co');

module.exports = function(topic, command) {
  return {
    topic: topic,
    command: command,
    description: 'Launch a SOCKS proxy into a dyno',
    help: `Example:

    $ heroku ps:socks --app murmuring-headland-14719
    Establishing credentials... done
    SOCKSv5 proxy server started on port 1080
    Use CTRL+C to stop the proxy`,
    args: [],
    flags: [{ name: 'dyno', char: 'd', hasValue: true, description: 'specify the dyno to connect to' }],
    needsApp: true,
    needsAuth: true,
    run: cli.command(co.wrap(run))
  }
};

function * run(context, heroku) {
  yield exec.initFeature(context, heroku, function *(configVars) {
    yield exec.createSocksProxy(context, heroku, configVars)
  });
  return new Promise(resolve => {})
}
