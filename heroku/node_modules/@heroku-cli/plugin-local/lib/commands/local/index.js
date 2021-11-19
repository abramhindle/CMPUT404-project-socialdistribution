"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const completions_1 = require("@heroku-cli/command/lib/completions");
const command_1 = require("@oclif/command");
const fork_foreman_1 = require("../../fork-foreman");
// eslint-disable-next-line node/no-missing-require
const Procfile = require('../../load-foreman-procfile');
class Index extends command_1.Command {
    async run() {
        const execArgv = ['start'];
        const { args, flags } = this.parse(Index);
        if (flags.restart) {
            this.error('--restart is no longer available\nUse forego instead: https://github.com/ddollar/forego');
        }
        if (flags.concurrency) {
            this.error('--concurrency is no longer available\nUse forego instead: https://github.com/ddollar/forego');
        }
        if (flags.procfile)
            execArgv.push('--procfile', flags.procfile);
        if (flags.env)
            execArgv.push('--env', flags.env);
        if (flags.port)
            execArgv.push('--port', flags.port);
        if (args.processname) {
            execArgv.push(args.processname);
        }
        else {
            const procfile = flags.procfile || 'Procfile';
            const procHash = Procfile.loadProc(procfile);
            const processes = Object.keys(procHash).filter(x => x !== 'release');
            execArgv.push(processes.join(','));
        }
        await fork_foreman_1.fork(execArgv);
    }
}
// \n splits the description between the title shown in the help
// and the DESCRIPTION section shown in the help
Index.description = 'run heroku app locally\nStart the application specified by a Procfile (defaults to ./Procfile)';
Index.aliases = ['local:start'];
Index.args = [{ name: 'processname', required: false }];
Index.examples = [
    `$ heroku local
$ heroku local web
$ heroku local web=2
$ heroku local web=1,worker=2`,
];
Index.flags = {
    procfile: command_1.flags.string({
        char: 'f',
        description: 'use a different Procfile',
        completion: completions_1.FileCompletion,
    }),
    env: command_1.flags.string({
        char: 'e',
        description: 'location of env file (defaults to .env)',
        completion: completions_1.FileCompletion,
    }),
    port: command_1.flags.string({
        char: 'p',
        description: 'port to listen on',
    }),
    restart: command_1.flags.boolean({
        char: 'r',
        description: 'restart process if it dies',
        hidden: true,
    }),
    concurrency: command_1.flags.string({
        char: 'c',
        description: 'number of processes to start',
        hidden: true,
    }),
};
exports.default = Index;
