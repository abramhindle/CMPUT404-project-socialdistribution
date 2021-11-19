"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const path = tslib_1.__importStar(require("path"));
const deps_1 = tslib_1.__importDefault(require("./deps"));
class UserConfig {
    // eslint-disable-next-line no-useless-constructor
    constructor(config) {
        this.config = config;
        this.needsSave = false;
    }
    get install() {
        return this.body.install || this.genInstall();
    }
    set install(install) {
        this.body.install = install;
        this.needsSave = true;
    }
    get skipAnalytics() {
        if (this.config.scopedEnvVar('SKIP_ANALYTICS') === '1')
            return true;
        if (typeof this.body.skipAnalytics !== 'boolean') {
            this.body.skipAnalytics = false;
            this.needsSave = true;
        }
        return this.body.skipAnalytics;
    }
    async init() {
        await this.saving;
        if (this._init)
            return this._init;
        this._init = (async () => {
            this.debug('init');
            this.body = (await this.read()) || { schema: 1 };
            if (!this.body.schema) {
                this.body.schema = 1;
                this.needsSave = true;
            }
            else if (this.body.schema !== 1)
                this.body = { schema: 1 };
            // tslint:disable-next-line
            this.install;
            // tslint:disable-next-line
            this.skipAnalytics;
            if (this.needsSave)
                await this.save();
        })();
        return this._init;
    }
    get debug() {
        return require('debug')('heroku:user_config');
    }
    get file() {
        return path.join(this.config.dataDir, 'config.json');
    }
    async save() {
        if (!this.needsSave)
            return;
        this.needsSave = false;
        this.saving = (async () => {
            this.debug('saving');
            if (!await this.canWrite()) {
                throw new Error('file modified, cannot save');
            }
            await deps_1.default.file.outputJSON(this.file, this.body);
        })();
    }
    async read() {
        await this.migrate();
        try {
            this.mtime = await this.getLastUpdated();
            const body = await deps_1.default.file.readJSON(this.file);
            return body;
        }
        catch (error) {
            if (error.code !== 'ENOENT')
                throw error;
            this.debug('not found');
        }
    }
    async migrate() {
        if (await deps_1.default.file.exists(this.file))
            return;
        const old = path.join(this.config.configDir, 'config.json');
        if (!await deps_1.default.file.exists(old))
            return;
        this.debug('moving config into new place');
        await deps_1.default.file.rename(old, this.file);
    }
    async canWrite() {
        if (!this.mtime)
            return true;
        return (await this.getLastUpdated()) === this.mtime;
    }
    async getLastUpdated() {
        try {
            const stat = await deps_1.default.file.stat(this.file);
            return stat.mtime.getTime();
        }
        catch (error) {
            if (error.code !== 'ENOENT')
                throw error;
        }
    }
    genInstall() {
        const uuid = require('uuid/v4');
        this.install = uuid();
        return this.install;
    }
}
exports.default = UserConfig;
