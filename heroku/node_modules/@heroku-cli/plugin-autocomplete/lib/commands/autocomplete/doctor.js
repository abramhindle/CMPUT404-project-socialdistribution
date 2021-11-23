"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const fs = require("fs-extra");
const path = require("path");
const base_1 = require("../../base");
class Doctor extends base_1.AutocompleteBase {
    async run() {
        const { args, flags } = this.parse(Doctor);
        const shell = args.shell || this.config.shell;
        this.errorIfNotSupportedShell(shell);
        const data = [];
        // cli version
        data.push({ name: 'cli version', value: this.config.version });
        // plugin version
        const pjson = require(path.resolve(__dirname, '..', '..', '..', 'package.json'));
        data.push({ name: 'plugin version', value: pjson.version });
        // check shell shim source env var
        // i.e. HEROKU_AC_<shell>_SETUP_PATH
        const shellProfilePath = path.join(process.env.HOME || '', shell === 'zsh' ? '.zshrc' : '.bashrc');
        const shellProfile = fs.readFileSync(shellProfilePath);
        const regex = /AC_\w+_SETUP_PATH/;
        const shimVlaue = regex.exec(shellProfile.toString()) ? 'present' : 'missing';
        data.push({ name: `~/${shell === 'zsh' ? '.zshrc' : '.bashrc'} shimmed`, value: shimVlaue });
        // check shell shim
        const shellCompletion = path.join(this.autocompleteCacheDir, `${shell}_setup`);
        const shellCompletionValue = fs.existsSync(shellCompletion) ? 'present' : 'missing';
        data.push({ name: `${shell} shim file`, value: shellCompletionValue });
        // check shell command cache
        const shellCmdCache = path.join(this.autocompleteCacheDir, shell === 'zsh' ? 'commands_setters' : 'commands');
        const shellCmdCacheValue = fs.existsSync(shellCmdCache) ? 'present' : 'missing';
        data.push({ name: `${shell} commands cache`, value: shellCmdCacheValue });
        // check app completion cache
        const appsCache = path.join(this.completionsCacheDir, 'app');
        let appsCacheValue;
        if (fs.existsSync(appsCache)) {
            const length = fs.readJSONSync(appsCache).length;
            appsCacheValue = length || 'empty';
        }
        else {
            appsCacheValue = 'missing';
        }
        data.push({ name: 'apps completion cache', value: appsCacheValue });
        cli_ux_1.ux.table(data, {
            printHeader: undefined,
            columns: [
                { key: 'name' },
                { key: 'value' },
            ],
        });
        if (flags.verbose)
            this.printList();
    }
    printList() {
        this.log();
        const header = 'Completable Commands';
        this.log(header);
        this.log('='.repeat(header.length));
        this.config.plugins.forEach(p => {
            p.commands.forEach(c => {
                try {
                    if (c.hidden) {
                        this.log(`${c.id} (hidden)`);
                    }
                    else {
                        const results = Object.keys(c.flags).map((f) => {
                            let out = `--${f}`;
                            const flag = c.flags[f];
                            if (flag.type === 'option')
                                out += '=';
                            const hasCompletion = 'completion' in flag || this.findCompletion(c.id, f, flag.description);
                            if (hasCompletion) {
                                out += '(c)';
                            }
                            if (flag.hidden)
                                out += '(h)';
                            return out;
                        });
                        if (results.length > 0)
                            this.log(`${c.id} -> ${results}`);
                    }
                }
                catch (_a) {
                    this.log(`Error creating autocomplete for command ${c.id}`);
                }
            });
        });
    }
}
exports.default = Doctor;
Doctor.hidden = true;
Doctor.description = 'autocomplete diagnostic';
Doctor.args = [
    { name: 'shell', description: 'shell type', required: false },
];
Doctor.flags = {
    verbose: command_1.flags.boolean({ description: 'list completable commands' }),
};
