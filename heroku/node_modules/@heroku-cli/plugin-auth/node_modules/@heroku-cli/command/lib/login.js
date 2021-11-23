"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const http_call_1 = tslib_1.__importDefault(require("http-call"));
const netrc_parser_1 = tslib_1.__importDefault(require("netrc-parser"));
const open = require("open");
const os = tslib_1.__importStar(require("os"));
const api_client_1 = require("./api-client");
const vars_1 = require("./vars");
const debug = require('debug')('heroku-cli-command');
const hostname = os.hostname();
const thirtyDays = 60 * 60 * 24 * 30;
const headers = (token) => ({ headers: { accept: 'application/vnd.heroku+json; version=3', authorization: `Bearer ${token}` } });
class Login {
    constructor(config, heroku) {
        this.config = config;
        this.heroku = heroku;
        this.loginHost = process.env.HEROKU_LOGIN_HOST || 'https://cli-auth.heroku.com';
    }
    async login(opts = {}) {
        let loggedIn = false;
        try {
            // timeout after 10 minutes
            setTimeout(() => {
                if (!loggedIn)
                    cli_ux_1.default.error('timed out');
            }, 1000 * 60 * 10).unref();
            if (process.env.HEROKU_API_KEY)
                cli_ux_1.default.error('Cannot log in with HEROKU_API_KEY set');
            if (opts.expiresIn && opts.expiresIn > thirtyDays)
                cli_ux_1.default.error('Cannot set an expiration longer than thirty days');
            await netrc_parser_1.default.load();
            const previousEntry = netrc_parser_1.default.machines['api.heroku.com'];
            let input = opts.method;
            if (!input) {
                if (opts.expiresIn) {
                    // can't use browser with --expires-in
                    input = 'interactive';
                }
                else if (process.env.HEROKU_LEGACY_SSO === '1') {
                    input = 'sso';
                }
                else {
                    await cli_ux_1.default.anykey(`heroku: Press any key to open up the browser to login or ${color_1.default.yellow('q')} to exit`);
                    input = 'browser';
                }
            }
            try {
                if (previousEntry && previousEntry.password)
                    await this.logout(previousEntry.password);
            }
            catch (err) {
                cli_ux_1.default.warn(err);
            }
            let auth;
            switch (input) {
                case 'b':
                case 'browser':
                    auth = await this.browser(opts.browser);
                    break;
                case 'i':
                case 'interactive':
                    auth = await this.interactive(previousEntry && previousEntry.login, opts.expiresIn);
                    break;
                case 's':
                case 'sso':
                    auth = await this.sso();
                    break;
                default:
                    return this.login(opts);
            }
            await this.saveToken(auth);
        }
        catch (err) {
            throw new api_client_1.HerokuAPIError(err);
        }
        finally {
            loggedIn = true;
        }
    }
    async logout(token = this.heroku.auth) {
        if (!token)
            return debug('no credentials to logout');
        const requests = [];
        // for SSO logins we delete the session since those do not show up in
        // authorizations because they are created a trusted client
        requests.push(http_call_1.default.delete(`${vars_1.vars.apiUrl}/oauth/sessions/~`, headers(token))
            .catch(err => {
            if (!err.http)
                throw err;
            if (err.http.statusCode === 404 && err.http.body && err.http.body.id === 'not_found' && err.http.body.resource === 'session') {
                return;
            }
            if (err.http.statusCode === 401 && err.http.body && err.http.body.id === 'unauthorized') {
                return;
            }
            throw err;
        }));
        // grab all the authorizations so that we can delete the token they are
        // using in the CLI.  we have to do this rather than delete ~ because
        // the ~ is the API Key, not the authorization that is currently requesting
        requests.push(http_call_1.default.get(`${vars_1.vars.apiUrl}/oauth/authorizations`, headers(token))
            .then(async ({ body: authorizations }) => {
            // grab the default authorization because that is the token shown in the
            // dashboard as API Key and they may be using it for something else and we
            // would unwittingly break an integration that they are depending on
            const d = await this.defaultToken();
            if (d === token)
                return;
            return Promise.all(authorizations
                .filter(a => a.access_token && a.access_token.token === this.heroku.auth)
                .map(a => http_call_1.default.delete(`${vars_1.vars.apiUrl}/oauth/authorizations/${a.id}`, headers(token))));
        })
            .catch(err => {
            if (!err.http)
                throw err;
            if (err.http.statusCode === 401 && err.http.body && err.http.body.id === 'unauthorized') {
                return [];
            }
            throw err;
        }));
        await Promise.all(requests);
    }
    async browser(browser) {
        const { body: urls } = await http_call_1.default.post(`${this.loginHost}/auth`, {
            body: { description: `Heroku CLI login from ${hostname}` },
        });
        const url = `${this.loginHost}${urls.browser_url}`;
        process.stderr.write(`Opening browser to ${url}\n`);
        let urlDisplayed = false;
        const showUrl = () => {
            if (!urlDisplayed)
                cli_ux_1.default.warn('Cannot open browser.');
            urlDisplayed = true;
        };
        // ux.warn(`If browser does not open, visit ${color.greenBright(url)}`)
        const cp = await open(url, { app: browser, wait: false });
        cp.on('error', err => {
            cli_ux_1.default.warn(err);
            showUrl();
        });
        if (process.env.HEROKU_TESTING_HEADLESS_LOGIN === '1')
            showUrl();
        cp.on('close', code => {
            if (code !== 0)
                showUrl();
        });
        cli_ux_1.default.action.start('heroku: Waiting for login');
        const fetchAuth = async (retries = 3) => {
            try {
                const { body: auth } = await http_call_1.default.get(`${this.loginHost}${urls.cli_url}`, {
                    headers: { authorization: `Bearer ${urls.token}` }
                });
                return auth;
            }
            catch (err) {
                if (retries > 0 && err.http && err.http.statusCode > 500)
                    return fetchAuth(retries - 1);
                throw err;
            }
        };
        const auth = await fetchAuth();
        if (auth.error)
            cli_ux_1.default.error(auth.error);
        this.heroku.auth = auth.access_token;
        cli_ux_1.default.action.start('Logging in');
        const { body: account } = await http_call_1.default.get(`${vars_1.vars.apiUrl}/account`, headers(auth.access_token));
        cli_ux_1.default.action.stop();
        return {
            login: account.email,
            password: auth.access_token,
        };
    }
    async interactive(login, expiresIn) {
        process.stderr.write('heroku: Enter your login credentials\n');
        login = await cli_ux_1.default.prompt('Email', { default: login });
        let password = await cli_ux_1.default.prompt('Password', { type: 'hide' });
        let auth;
        try {
            auth = await this.createOAuthToken(login, password, { expiresIn });
        }
        catch (err) {
            if (err.body && err.body.id === 'device_trust_required') {
                err.body.message = 'The interactive flag requires Two-Factor Authentication to be enabled on your account. Please use heroku login.';
                throw err;
            }
            if (!err.body || err.body.id !== 'two_factor') {
                throw err;
            }
            let secondFactor = await cli_ux_1.default.prompt('Two-factor code', { type: 'mask' });
            auth = await this.createOAuthToken(login, password, { expiresIn, secondFactor });
        }
        this.heroku.auth = auth.password;
        return auth;
    }
    async createOAuthToken(username, password, opts = {}) {
        function basicAuth(username, password) {
            let auth = [username, password].join(':');
            auth = Buffer.from(auth).toString('base64');
            return `Basic ${auth}`;
        }
        let headers = {
            accept: 'application/vnd.heroku+json; version=3',
            authorization: basicAuth(username, password)
        };
        if (opts.secondFactor)
            headers['Heroku-Two-Factor-Code'] = opts.secondFactor;
        const { body: auth } = await http_call_1.default.post(`${vars_1.vars.apiUrl}/oauth/authorizations`, {
            headers,
            body: {
                scope: ['global'],
                description: `Heroku CLI login from ${hostname}`,
                expires_in: opts.expiresIn || thirtyDays
            }
        });
        return { password: auth.access_token.token, login: auth.user.email };
    }
    async saveToken(entry) {
        const hosts = [vars_1.vars.apiHost, vars_1.vars.httpGitHost];
        hosts.forEach(host => {
            if (!netrc_parser_1.default.machines[host])
                netrc_parser_1.default.machines[host] = {};
            netrc_parser_1.default.machines[host].login = entry.login;
            netrc_parser_1.default.machines[host].password = entry.password;
            delete netrc_parser_1.default.machines[host].method;
            delete netrc_parser_1.default.machines[host].org;
        });
        if (netrc_parser_1.default.machines._tokens) {
            netrc_parser_1.default.machines._tokens.forEach((token) => {
                if (hosts.includes(token.host)) {
                    token.internalWhitespace = '\n  ';
                }
            });
        }
        await netrc_parser_1.default.save();
    }
    async defaultToken() {
        try {
            const { body: authorization } = await http_call_1.default.get(`${vars_1.vars.apiUrl}/oauth/authorizations/~`, headers(this.heroku.auth));
            return authorization.access_token && authorization.access_token.token;
        }
        catch (err) {
            if (!err.http)
                throw err;
            if (err.http.statusCode === 404 && err.http.body && err.http.body.id === 'not_found' && err.body.resource === 'authorization')
                return;
            if (err.http.statusCode === 401 && err.http.body && err.http.body.id === 'unauthorized')
                return;
            throw err;
        }
    }
    async sso() {
        let url = process.env.SSO_URL;
        let org = process.env.HEROKU_ORGANIZATION;
        if (!url) {
            if (org) {
                org = await cli_ux_1.default.prompt('Organization name', { default: org });
            }
            else {
                org = await cli_ux_1.default.prompt('Organization name');
            }
            url = `https://sso.heroku.com/saml/${encodeURIComponent(org)}/init?cli=true`;
        }
        // TODO: handle browser
        debug(`opening browser to ${url}`);
        process.stderr.write(`Opening browser to:\n${url}\n`);
        process.stderr.write(color_1.default.gray('If the browser fails to open or you’re authenticating on a ' +
            'remote machine, please manually open the URL above in your ' +
            'browser.\n'));
        await open(url, { wait: false });
        const password = await cli_ux_1.default.prompt('Access token', { type: 'mask' });
        cli_ux_1.default.action.start('Validating token');
        this.heroku.auth = password;
        const { body: account } = await http_call_1.default.get(`${vars_1.vars.apiUrl}/account`, headers(password));
        return { password, login: account.email };
    }
}
exports.Login = Login;
