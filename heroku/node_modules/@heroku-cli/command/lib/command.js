"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@oclif/command");
const util_1 = require("util");
const deps_1 = tslib_1.__importDefault(require("./deps"));
const pjson = require('../package.json');
const deprecatedCLI = util_1.deprecate(() => {
    return require('cli-ux').cli;
}, 'this.out and this.cli is deprecated. Please import the "cli-ux" module directly instead.');
class Command extends command_1.Command {
    constructor() {
        super(...arguments);
        this.base = `${pjson.name}@${pjson.version}`;
    }
    get heroku() {
        if (this._heroku)
            return this._heroku;
        this._heroku = new deps_1.default.APIClient(this.config);
        return this._heroku;
    }
    get legacyHerokuClient() {
        if (this._legacyHerokuClient)
            return this._legacyHerokuClient;
        const HerokuClient = require('heroku-client');
        let options = {
            debug: this.config.debug,
            host: `${this.heroku.defaults.protocol || 'https:'}//${this.heroku.defaults.host ||
                'api.heroku.com'}`,
            token: this.heroku.auth,
            userAgent: this.heroku.defaults.headers['user-agent'],
        };
        this._legacyHerokuClient = new HerokuClient(options);
        return this._legacyHerokuClient;
    }
    get cli() {
        return deprecatedCLI();
    }
    get out() {
        return deprecatedCLI();
    }
}
exports.Command = Command;
