"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@heroku-cli/command");
const netrc_parser_1 = tslib_1.__importDefault(require("netrc-parser"));
const path = tslib_1.__importStar(require("path"));
const deps_1 = tslib_1.__importDefault(require("./deps"));
const debug = require('debug')('heroku:analytics');
class AnalyticsCommand {
    constructor(config) {
        this.config = config;
        this.http = deps_1.default.HTTP.create({
            headers: { 'user-agent': config.userAgent },
        });
    }
    async record(opts) {
        await this.init();
        const plugin = opts.Command.plugin;
        if (!plugin) {
            debug('no plugin found for analytics');
            return;
        }
        if (this.userConfig.skipAnalytics)
            return;
        const analyticsData = {
            source: 'cli',
            event: opts.Command.id,
            properties: {
                cli: this.config.name,
                command: opts.Command.id,
                completion: await this._acAnalytics(opts.Command.id),
                version: this.config.version,
                plugin: plugin.name,
                plugin_version: plugin.version,
                os: this.config.platform,
                shell: this.config.shell,
                valid: true,
                language: 'node',
                install_id: this.userConfig.install,
            },
        };
        const data = Buffer.from(JSON.stringify(analyticsData)).toString('base64');
        if (this.authorizationToken) {
            return this.http.get(`${this.url}?data=${data}`, { headers: { authorization: `Bearer ${this.authorizationToken}` } }).catch(error => debug(error));
        }
        return this.http.get(`${this.url}?data=${data}`).catch(error => debug(error));
    }
    get url() {
        return process.env.HEROKU_ANALYTICS_URL || 'https://backboard.heroku.com/hamurai';
    }
    get authorizationToken() {
        return process.env.HEROKU_API_KEY || this.netrcToken;
    }
    get netrcToken() {
        return netrc_parser_1.default.machines[command_1.vars.apiHost] && netrc_parser_1.default.machines[command_1.vars.apiHost].password;
    }
    get usingHerokuAPIKey() {
        const k = process.env.HEROKU_API_KEY;
        return Boolean(k && k.length > 0);
    }
    get netrcLogin() {
        return netrc_parser_1.default.machines[command_1.vars.apiHost] && netrc_parser_1.default.machines[command_1.vars.apiHost].login;
    }
    get user() {
        if (this.usingHerokuAPIKey)
            return;
        return this.netrcLogin;
    }
    async _acAnalytics(id) {
        if (id === 'autocomplete:options')
            return 0;
        const root = path.join(this.config.cacheDir, 'autocomplete', 'completion_analytics');
        const meta = {
            cmd: deps_1.default.file.exists(path.join(root, 'command')),
            flag: deps_1.default.file.exists(path.join(root, 'flag')),
            value: deps_1.default.file.exists(path.join(root, 'value')),
        };
        let score = 0;
        if (await meta.cmd)
            score += 1;
        if (await meta.flag)
            score += 2;
        if (await meta.value)
            score += 4;
        if (await deps_1.default.file.exists(root))
            await deps_1.default.file.remove(root);
        return score;
    }
    async init() {
        await netrc_parser_1.default.load();
        this.userConfig = new deps_1.default.UserConfig(this.config);
        await this.userConfig.init();
    }
}
exports.default = AnalyticsCommand;
