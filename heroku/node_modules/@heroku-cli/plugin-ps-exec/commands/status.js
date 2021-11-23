'use strict';

const cli = require('heroku-cli-util');
const exec = require('heroku-exec-util');
const co = require('co');

module.exports = function(topic, command) {
  return {
    topic: topic,
    command: command,
    description: 'Check the status of your heroku-exec add-on',
    help: `Example:

    $ heroku ps:status --app murmuring-headland-14719`,
    args: [],
    needsApp: true,
    needsAuth: true,
    run: cli.command(co.wrap(run))
  }
};

function * run(context, heroku) {
  yield exec.initFeature(context, heroku, function *(configVars) {
    yield exec.checkStatus(context, heroku, configVars);
  });
}
