"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
const errors_1 = require("@oclif/errors");
const completions_1 = require("../completions");
const git_1 = require("../git");
class MultipleRemotesError extends errors_1.CLIError {
    constructor(gitRemotes) {
        super(`Multiple apps in git remotes
  Usage: --remote ${gitRemotes[1].remote}
     or: --app ${gitRemotes[1].app}
  Your local git repository has more than 1 app referenced in git remotes.
  Because of this, we can't determine which app you want to run this command against.
  Specify the app you want with --app or --remote.
  Heroku remotes in repo:
  ${gitRemotes.map(r => `${r.app} (${r.remote})`).join('\n')}

  https://devcenter.heroku.com/articles/multiple-environments`);
    }
}
exports.app = command_1.flags.build({
    char: 'a',
    completion: completions_1.AppCompletion,
    description: 'app to run command against',
    default: ({ options, flags }) => {
        const envApp = process.env.HEROKU_APP;
        if (envApp)
            return envApp;
        let gitRemotes = git_1.getGitRemotes(flags.remote || git_1.configRemote());
        if (gitRemotes.length === 1)
            return gitRemotes[0].app;
        if (flags.remote && gitRemotes.length === 0) {
            errors_1.error(`remote ${flags.remote} not found in git remotes`);
        }
        if (gitRemotes.length > 1 && options.required) {
            throw new MultipleRemotesError(gitRemotes);
        }
    },
});
exports.remote = command_1.flags.build({
    char: 'r',
    completion: completions_1.RemoteCompletion,
    description: 'git remote of app to use',
});
