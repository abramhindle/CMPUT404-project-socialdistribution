"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cp = require("child_process");
const cli_ux_1 = require("cli-ux");
const util_1 = require("util");
const execFile = util_1.promisify(cp.execFile);
const debug = require('debug')('git');
class Git {
    async exec(args) {
        debug('exec: git %o', args);
        try {
            const { stdout, stderr } = await execFile('git', args);
            if (stderr)
                process.stderr.write(stderr);
            return stdout.trim();
        }
        catch (error) {
            if (error.code === 'ENOENT') {
                cli_ux_1.default.error('Git must be installed to use the Heroku CLI.  See instructions here: https://git-scm.com');
            }
            throw error;
        }
    }
    spawn(args) {
        return new Promise((resolve, reject) => {
            debug('spawn: git %o', args);
            const s = cp.spawn('git', args, { stdio: [0, 1, 2] });
            s.on('error', (err) => {
                if (err.code === 'ENOENT') {
                    cli_ux_1.default.error('Git must be installed to use the Heroku CLI.  See instructions here: https://git-scm.com');
                }
                else
                    reject(err);
            });
            s.on('close', resolve);
        });
    }
    remoteFromGitConfig() {
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        return this.exec(['config', 'heroku.remote']).catch(() => { });
    }
    sshGitUrl(app) {
        return `git@${command_1.vars.gitHost}:${app}.git`;
    }
    httpGitUrl(app) {
        return `https://${command_1.vars.httpGitHost}/${app}.git`;
    }
    async remoteUrl(name) {
        const remotes = await this.exec(['remote', '-v']);
        return remotes.split('\n')
            .map(r => r.split('\t'))
            .find(r => r[0] === name)[1]
            .split(' ')[0];
    }
    url(app, ssh) {
        return ssh ? this.sshGitUrl(app) : this.httpGitUrl(app);
    }
}
exports.default = Git;
