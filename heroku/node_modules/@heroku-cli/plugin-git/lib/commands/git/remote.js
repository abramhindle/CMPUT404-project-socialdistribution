"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@heroku-cli/color");
const command_1 = require("@heroku-cli/command");
const git_1 = require("../../git");
class GitRemote extends command_1.Command {
    async run() {
        const { argv, flags } = this.parse(GitRemote);
        const git = new git_1.default();
        const appName = flags.app || argv.shift() || process.env.HEROKU_APP;
        if (!appName) {
            this.error('Specify an app with --app');
        }
        const { body: app } = await this.heroku.get(`/apps/${appName}`);
        const remote = flags.remote || (await git.remoteFromGitConfig()) || 'heroku';
        const remotes = await git.exec(['remote']);
        const url = git.url(app.name, flags['ssh-git']);
        if (remotes.split('\n').includes(remote)) {
            await git.exec(['remote', 'set-url', remote, url].concat(argv));
        }
        else {
            await git.exec(['remote', 'add', remote, url].concat(argv));
        }
        const newRemote = await git.remoteUrl(remote);
        this.log(`set git remote ${color_1.default.cyan(remote)} to ${color_1.default.cyan(newRemote)}`);
    }
}
exports.GitRemote = GitRemote;
GitRemote.description = `adds a git remote to an app repo
extra arguments will be passed to git remote add
`;
GitRemote.example = `# set git remote heroku to https://git.heroku.com/example.git
    $ heroku git:remote -a example

    # set git remote heroku-staging to https://git.heroku.com/example.git
    $ heroku git:remote --remote heroku-staging -a example`;
GitRemote.flags = {
    app: command_1.flags.string({ char: 'a', description: 'the Heroku app to use' }),
    remote: command_1.flags.string({ char: 'r', description: 'the git remote to create' }),
    'ssh-git': command_1.flags.boolean({ description: 'use SSH git protocol' }),
};
GitRemote.strict = false;
