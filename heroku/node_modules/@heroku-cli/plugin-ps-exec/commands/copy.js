'use strict';

const cli = require('heroku-cli-util');
const exec = require('heroku-exec-util');
const co = require('co');
const path = require('path');
const fs = require('fs');

module.exports = function(topic, command) {
  return {
    topic: topic,
    command: command,
    description: 'Copy a file from a dyno to the local filesystem',
    help: `Example:

    $ heroku ps:copy FILENAME --app murmuring-headland-14719`,
    args: [ {name: 'file'} ],
    flags: [
      { name: 'dyno', char: 'd', hasValue: true, description: 'specify the dyno to connect to' },
      { name: 'output', char: 'o', hasValue: true, description: 'the name of the output file' }],
    needsApp: true,
    needsAuth: true,
    run: cli.command(co.wrap(run))
  }
};

function * run(context, heroku) {
  var src = context.args.file
  var dest = context.flags.output ? context.flags.output : path.basename(src)

  cli.log(`Copying ${cli.color.white.bold(src)} to ${cli.color.white.bold(dest)}`)
  if (fs.existsSync(dest)) {
    cli.error(`The local file ${cli.color.white.bold(dest)} already exists!`)
  } else {
    yield exec.initFeature(context, heroku, function *(configVars) {
      yield exec.updateClientKey(context, heroku, configVars, function(privateKey, dyno, response) {
        var message = `Connecting to ${cli.color.cyan.bold(dyno)} on ${cli.color.app(context.app)}`
        cli.action(message, {success: false}, co(function* () {
          cli.hush(response.body);
          var json = JSON.parse(response.body);
          exec.scp(context, json['tunnel_host'], json['client_user'], privateKey, json['proxy_public_key'], src, dest)
        }))
      })
    });
  }
  return new Promise(resolve => {})
}
