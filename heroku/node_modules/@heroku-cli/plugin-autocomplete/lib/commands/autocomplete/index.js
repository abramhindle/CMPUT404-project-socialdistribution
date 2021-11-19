"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const completions_1 = require("@heroku-cli/command/lib/completions");
const chalk_1 = require("chalk");
const cli_ux_1 = require("cli-ux");
const path = require("path");
const base_1 = require("../../base");
const cache_1 = require("../../cache");
const create_1 = require("./create");
class Index extends base_1.AutocompleteBase {
    async run() {
        const { args, flags } = this.parse(Index);
        const shell = args.shell || this.config.shell;
        this.errorIfNotSupportedShell(shell);
        cli_ux_1.cli.action.start(`${chalk_1.default.bold('Building the autocomplete cache')}`);
        await create_1.default.run([], this.config);
        await this.updateCache(completions_1.AppCompletion, 'app');
        await this.updateCache(completions_1.PipelineCompletion, 'pipeline');
        await this.updateCache(completions_1.SpaceCompletion, 'space');
        await this.updateCache(completions_1.TeamCompletion, 'team');
        cli_ux_1.cli.action.stop();
        if (!flags['refresh-cache']) {
            const bin = this.config.bin;
            const bashNote = 'If your terminal starts as a login shell you may need to print the init script into ~/.bash_profile or ~/.profile.';
            const zshNote = `After sourcing, you can run \`${chalk_1.default.cyan('$ compaudit -D')}\` to ensure no permissions conflicts are present`;
            const note = shell === 'zsh' ? zshNote : bashNote;
            const tabStr = shell === 'bash' ? '<TAB><TAB>' : '<TAB>';
            this.log(`
${chalk_1.default.bold(`Setup Instructions for ${bin.toUpperCase()} CLI Autocomplete ---`)}

1) Add the autocomplete env var to your ${shell} profile and source it
${chalk_1.default.cyan(`$ printf "$(${bin} autocomplete:script ${shell})" >> ~/.${shell}rc; source ~/.${shell}rc`)}

NOTE: ${note}

2) Test it out, e.g.:
${chalk_1.default.cyan(`$ ${bin} ${tabStr}`)}                 # Command completion
${chalk_1.default.cyan(`$ ${bin} apps:info --${tabStr}`)}     # Flag completion
${chalk_1.default.cyan(`$ ${bin} apps:info --app=${tabStr}`)} # Flag option completion

Visit the autocomplete Dev Center doc at https://devcenter.heroku.com/articles/heroku-cli-autocomplete

Enjoy!
`);
        }
    }
    async updateCache(completion, cacheKey) {
        const cachePath = path.join(this.completionsCacheDir, cacheKey);
        const options = await completion.options({ config: this.config });
        await cache_1.updateCache(cachePath, options);
    }
}
exports.default = Index;
Index.description = 'display autocomplete installation instructions';
Index.args = [{ name: 'shell', description: 'shell type', required: false }];
Index.flags = {
    'refresh-cache': command_1.flags.boolean({ description: 'refresh cache only (ignores displaying instructions)', char: 'r' }),
};
Index.examples = [
    '$ heroku autocomplete',
    '$ heroku autocomplete bash',
    '$ heroku autocomplete zsh',
    '$ heroku autocomplete --refresh-cache',
];
