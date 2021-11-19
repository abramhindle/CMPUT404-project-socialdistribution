"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const completions_1 = require("@heroku-cli/command/lib/completions");
const command_1 = require("@oclif/command");
const fork_foreman_1 = require("../../fork-foreman");
class Run extends command_1.Command {
    async run() {
        const execArgv = ['run'];
        const { argv, flags } = this.parse(Run);
        if (argv.length === 0) {
            const errorMessage = 'Usage: heroku local:run [COMMAND]\nMust specify command to run';
            this.error(errorMessage, { exit: -1 });
        }
        if (flags.env)
            execArgv.push('--env', flags.env);
        if (flags.port)
            execArgv.push('--port', flags.port);
        execArgv.push('--'); // disable node-foreman flag parsing
        execArgv.push(...argv);
        await fork_foreman_1.fork(execArgv);
    }
}
Run.description = 'run a one-off command';
Run.examples = [
    '$ heroku local:run bin/migrate',
];
Run.strict = false;
Run.flags = {
    env: command_1.flags.string({
        char: 'e',
        completion: completions_1.FileCompletion,
    }),
    port: command_1.flags.string({
        char: 'p',
    }),
};
exports.default = Run;
