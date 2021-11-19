"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const errors_1 = require("@oclif/errors");
const netrc_parser_1 = tslib_1.__importDefault(require("netrc-parser"));
const url = tslib_1.__importStar(require("url"));
const deps_1 = tslib_1.__importDefault(require("./deps"));
const login_1 = require("./login");
const request_id_1 = require("./request-id");
const vars_1 = require("./vars");
class HerokuAPIError extends errors_1.CLIError {
    constructor(httpError) {
        if (!httpError)
            throw new Error('invalid error');
        let options = httpError.body;
        if (!options || !options.message)
            throw httpError;
        let info = [];
        if (options.id)
            info.push(`Error ID: ${options.id}`);
        if (options.app && options.app.name)
            info.push(`App: ${options.app.name}`);
        if (options.url)
            info.push(`See ${options.url} for more information.`);
        if (info.length)
            super([options.message, ''].concat(info).join('\n'));
        else
            super(options.message);
        this.http = httpError;
        this.body = options;
    }
}
exports.HerokuAPIError = HerokuAPIError;
class APIClient {
    constructor(config, options = {}) {
        this.config = config;
        this.options = options;
        this._login = new login_1.Login(this.config, this);
        this.config = config;
        if (options.required === undefined)
            options.required = true;
        options.preauth = options.preauth !== false;
        this.options = options;
        let apiUrl = url.URL ? new url.URL(vars_1.vars.apiUrl) : url.parse(vars_1.vars.apiUrl);
        let envHeaders = JSON.parse(process.env.HEROKU_HEADERS || '{}');
        this.preauthPromises = {};
        let self = this;
        const opts = {
            host: apiUrl.hostname,
            port: apiUrl.port,
            protocol: apiUrl.protocol,
            headers: Object.assign({ accept: 'application/vnd.heroku+json; version=3', 'user-agent': `heroku-cli/${self.config.version} ${self.config.platform}` }, envHeaders),
        };
        this.http = class APIHTTPClient extends deps_1.default.HTTP.HTTP.create(opts) {
            static async twoFactorRetry(err, url, opts = {}, retries = 3) {
                const app = err.body.app ? err.body.app.name : null;
                if (!app || !options.preauth) {
                    opts.headers = opts.headers || {};
                    opts.headers['Heroku-Two-Factor-Code'] = await self.twoFactorPrompt();
                    return this.request(url, opts, retries);
                }
                else {
                    // if multiple requests are run in parallel for the same app, we should
                    // only preauth for the first so save the fact we already preauthed
                    if (!self.preauthPromises[app]) {
                        self.preauthPromises[app] = self.twoFactorPrompt().then((factor) => self.preauth(app, factor));
                    }
                    await self.preauthPromises[app];
                    return this.request(url, opts, retries);
                }
            }
            static trackRequestIds(response) {
                const responseRequestIdHeader = response.headers[request_id_1.requestIdHeader];
                if (responseRequestIdHeader) {
                    const requestIds = Array.isArray(responseRequestIdHeader) ? responseRequestIdHeader : responseRequestIdHeader.split(',');
                    request_id_1.RequestId.track(...requestIds);
                }
            }
            static async request(url, opts = {}, retries = 3) {
                opts.headers = opts.headers || {};
                opts.headers[request_id_1.requestIdHeader] = request_id_1.RequestId.create() && request_id_1.RequestId.headerValue;
                if (!Object.keys(opts.headers).find(h => h.toLowerCase() === 'authorization')) {
                    opts.headers.authorization = `Bearer ${self.auth}`;
                }
                retries--;
                try {
                    const response = await super.request(url, opts);
                    this.trackRequestIds(response);
                    return response;
                }
                catch (err) {
                    if (!(err instanceof deps_1.default.HTTP.HTTPError))
                        throw err;
                    if (retries > 0) {
                        if (opts.retryAuth !== false && err.http.statusCode === 401 && err.body.id === 'unauthorized') {
                            if (process.env.HEROKU_API_KEY) {
                                throw new Error('The token provided to HEROKU_API_KEY is invalid. Please double-check that you have the correct token, or run `heroku login` without HEROKU_API_KEY set.');
                            }
                            if (!self.authPromise)
                                self.authPromise = self.login();
                            await self.authPromise;
                            opts.headers.authorization = `Bearer ${self.auth}`;
                            return this.request(url, opts, retries);
                        }
                        if (err.http.statusCode === 403 && err.body.id === 'two_factor') {
                            return this.twoFactorRetry(err, url, opts, retries);
                        }
                    }
                    throw new HerokuAPIError(err);
                }
            }
        };
    }
    get twoFactorMutex() {
        if (!this._twoFactorMutex) {
            this._twoFactorMutex = new deps_1.default.Mutex();
        }
        return this._twoFactorMutex;
    }
    get auth() {
        if (!this._auth) {
            if (process.env.HEROKU_API_TOKEN && !process.env.HEROKU_API_KEY)
                deps_1.default.cli.warn('HEROKU_API_TOKEN is set but you probably meant HEROKU_API_KEY');
            this._auth = process.env.HEROKU_API_KEY;
            if (!this._auth) {
                deps_1.default.netrc.loadSync();
                this._auth = deps_1.default.netrc.machines[vars_1.vars.apiHost] && deps_1.default.netrc.machines[vars_1.vars.apiHost].password;
            }
        }
        return this._auth;
    }
    set auth(token) {
        delete this.authPromise;
        this._auth = token;
    }
    twoFactorPrompt() {
        deps_1.default.yubikey.enable();
        return this.twoFactorMutex.synchronize(async () => {
            try {
                let factor = await deps_1.default.cli.prompt('Two-factor code', { type: 'mask' });
                deps_1.default.yubikey.disable();
                return factor;
            }
            catch (err) {
                deps_1.default.yubikey.disable();
                throw err;
            }
        });
    }
    preauth(app, factor) {
        return this.put(`/apps/${app}/pre-authorizations`, {
            headers: { 'Heroku-Two-Factor-Code': factor },
        });
    }
    get(url, options = {}) {
        return this.http.get(url, options);
    }
    post(url, options = {}) {
        return this.http.post(url, options);
    }
    put(url, options = {}) {
        return this.http.put(url, options);
    }
    patch(url, options = {}) {
        return this.http.patch(url, options);
    }
    delete(url, options = {}) {
        return this.http.delete(url, options);
    }
    stream(url, options = {}) {
        return this.http.stream(url, options);
    }
    request(url, options = {}) {
        return this.http.request(url, options);
    }
    login(opts = {}) {
        return this._login.login(opts);
    }
    async logout() {
        try {
            await this._login.logout();
        }
        catch (err) {
            errors_1.warn(err);
        }
        delete netrc_parser_1.default.machines['api.heroku.com'];
        delete netrc_parser_1.default.machines['git.heroku.com'];
        await netrc_parser_1.default.save();
    }
    get defaults() {
        return this.http.defaults;
    }
}
exports.APIClient = APIClient;
