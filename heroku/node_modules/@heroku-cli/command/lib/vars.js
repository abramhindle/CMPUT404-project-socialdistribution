"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const url = tslib_1.__importStar(require("url"));
class Vars {
    get host() {
        return this.envHost || 'heroku.com';
    }
    get apiUrl() {
        return this.host.startsWith('http') ? this.host : `https://api.${this.host}`;
    }
    get apiHost() {
        if (this.host.startsWith('http')) {
            const u = url.parse(this.host);
            if (u.host)
                return u.host;
        }
        return `api.${this.host}`;
    }
    get envHost() {
        return process.env.HEROKU_HOST;
    }
    get envGitHost() {
        return process.env.HEROKU_GIT_HOST;
    }
    get gitHost() {
        if (this.envGitHost)
            return this.envGitHost;
        if (this.host.startsWith('http')) {
            const u = url.parse(this.host);
            if (u.host)
                return u.host;
        }
        return this.host;
    }
    get httpGitHost() {
        if (this.envGitHost)
            return this.envGitHost;
        if (this.host.startsWith('http')) {
            const u = url.parse(this.host);
            if (u.host)
                return u.host;
        }
        return `git.${this.host}`;
    }
    get gitPrefixes() {
        return [`git@${this.gitHost}:`, `ssh://git@${this.gitHost}/`, `https://${this.httpGitHost}/`];
    }
}
exports.Vars = Vars;
exports.vars = new Vars();
