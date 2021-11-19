"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@oclif/color");
const command_1 = require("@oclif/command");
const cli_ux_1 = require("cli-ux");
const spawn = require("cross-spawn");
const fs = require("fs-extra");
const _ = require("lodash");
const path = require("path");
const tar_1 = require("../tar");
const util_1 = require("../util");
class UpdateCommand extends command_1.default {
    constructor() {
        super(...arguments);
        this.clientRoot = this.config.scopedEnvVar('OCLIF_CLIENT_HOME') || path.join(this.config.dataDir, 'client');
        this.clientBin = path.join(this.clientRoot, 'bin', this.config.windows ? `${this.config.bin}.cmd` : this.config.bin);
    }
    async run() {
        const { args, flags } = this.parse(UpdateCommand);
        this.autoupdate = !!flags.autoupdate;
        if (this.autoupdate)
            await this.debounce();
        cli_ux_1.default.action.start(`${this.config.name}: Updating CLI`);
        this.channel = args.channel || this.config.channel || 'stable';
        await this.config.runHook('preupdate', { channel: this.channel });
        const manifest = await this.fetchManifest();
        let reason = await this.skipUpdate();
        if (reason)
            cli_ux_1.default.action.stop(reason || 'done');
        else
            await this.update(manifest);
        this.debug('tidy');
        await this.tidy();
        await this.config.runHook('update', { channel: this.channel });
        this.debug('done');
        cli_ux_1.default.action.stop();
    }
    async fetchManifest() {
        const http = require('http-call').HTTP;
        try {
            const url = this.config.s3Url(this.config.s3Key('manifest', {
                channel: this.channel,
                platform: this.config.platform,
                arch: this.config.arch
            }));
            let { body } = await http.get(url);
            // in case the content-type is not set, parse as a string
            // this will happen if uploading without `oclif-dev publish`
            if (typeof body === 'string') {
                return JSON.parse(body);
            }
            else {
                return body;
            }
        }
        catch (err) {
            if (err.statusCode === 403)
                throw new Error(`HTTP 403: Invalid channel ${this.channel}`);
            throw err;
        }
    }
    async update(manifest) {
        const { version, channel } = manifest;
        cli_ux_1.default.action.start(`${this.config.name}: Updating CLI from ${color_1.default.green(this.config.version)} to ${color_1.default.green(version)}${channel === 'stable' ? '' : ' (' + color_1.default.yellow(channel) + ')'}`);
        const http = require('http-call').HTTP;
        const filesize = (n) => {
            const [num, suffix] = require('filesize')(n, { output: 'array' });
            return num.toFixed(1) + ` ${suffix}`;
        };
        await this.ensureClientDir();
        const output = path.join(this.clientRoot, version);
        const gzUrl = manifest.gz || this.config.s3Url(this.config.s3Key('versioned', {
            version,
            channel,
            bin: this.config.bin,
            platform: this.config.platform,
            arch: this.config.arch,
            ext: 'gz'
        }));
        const { response: stream } = await http.stream(gzUrl);
        stream.pause();
        const baseDir = manifest.baseDir || this.config.s3Key('baseDir', {
            version,
            channel,
            bin: this.config.bin,
            platform: this.config.platform,
            arch: this.config.arch,
        });
        let extraction = tar_1.extract(stream, baseDir, output, manifest.sha256gz);
        // TODO: use cli.action.type
        if (cli_ux_1.default.action.frames) {
            // if spinner action
            let total = parseInt(stream.headers['content-length'], 10);
            let current = 0;
            const updateStatus = _.throttle((newStatus) => { cli_ux_1.default.action.status = newStatus; }, 250, { leading: true, trailing: false });
            stream.on('data', data => {
                current += data.length;
                updateStatus(`${filesize(current)}/${filesize(total)}`);
            });
        }
        stream.resume();
        await extraction;
        await this.createBin(version);
        await this.touch();
        await this.reexec();
    }
    async skipUpdate() {
        if (!this.config.binPath) {
            const instructions = this.config.scopedEnvVar('UPDATE_INSTRUCTIONS');
            if (instructions)
                this.warn(instructions);
            return 'not updatable';
        }
        const manifest = await this.fetchManifest();
        if (this.config.version === manifest.version) {
            if (this.config.scopedEnvVar('HIDE_UPDATED_MESSAGE'))
                return 'done';
            return `already on latest version: ${this.config.version}`;
        }
        return false;
    }
    async logChop() {
        try {
            this.debug('log chop');
            const logChopper = require('log-chopper').default;
            await logChopper.chop(this.config.errlog);
        }
        catch (e) {
            this.debug(e.message);
        }
    }
    async mtime(f) {
        const { mtime } = await fs.stat(f);
        return mtime;
    }
    // when autoupdating, wait until the CLI isn't active
    async debounce() {
        let output = false;
        const lastrunfile = path.join(this.config.cacheDir, 'lastrun');
        const m = await this.mtime(lastrunfile);
        m.setHours(m.getHours() + 1);
        if (m > new Date()) {
            const msg = `waiting until ${m.toISOString()} to update`;
            if (output) {
                this.debug(msg);
            }
            else {
                await cli_ux_1.default.log(msg);
                output = true;
            }
            await util_1.wait(60 * 1000); // wait 1 minute
            return this.debounce();
        }
        cli_ux_1.default.log('time to update');
    }
    // removes any unused CLIs
    async tidy() {
        try {
            let root = this.clientRoot;
            if (!await fs.pathExists(root))
                return;
            let files = await util_1.ls(root);
            let promises = files.map(async (f) => {
                if (['bin', 'current', this.config.version].includes(path.basename(f.path)))
                    return;
                const mtime = f.stat.mtime;
                mtime.setHours(mtime.getHours() + 14 * 24);
                if (mtime < new Date()) {
                    await fs.remove(f.path);
                }
            });
            for (let p of promises)
                await p;
            await this.logChop();
        }
        catch (err) {
            cli_ux_1.default.warn(err);
        }
    }
    async touch() {
        // touch the client so it won't be tidied up right away
        try {
            const p = path.join(this.clientRoot, this.config.version);
            this.debug('touching client at', p);
            if (!await fs.pathExists(p))
                return;
            await fs.utimes(p, new Date(), new Date());
        }
        catch (err) {
            this.warn(err);
        }
    }
    async reexec() {
        cli_ux_1.default.action.stop();
        return new Promise((_, reject) => {
            this.debug('restarting CLI after update', this.clientBin);
            spawn(this.clientBin, ['update'], {
                stdio: 'inherit',
                env: Object.assign({}, process.env, { [this.config.scopedEnvVarKey('HIDE_UPDATED_MESSAGE')]: '1' }),
            })
                .on('error', reject)
                .on('close', (status) => {
                try {
                    this.exit(status);
                }
                catch (err) {
                    reject(err);
                }
            });
        });
    }
    async createBin(version) {
        const dst = this.clientBin;
        const { bin } = this.config;
        const binPathEnvVar = this.config.scopedEnvVarKey('BINPATH');
        const redirectedEnvVar = this.config.scopedEnvVarKey('REDIRECTED');
        if (this.config.windows) {
            let body = `@echo off
setlocal enableextensions
set ${redirectedEnvVar}=1
set ${binPathEnvVar}=%~dp0${bin}
"%~dp0..\\${version}\\bin\\${bin}.cmd" %*
`;
            await fs.outputFile(dst, body);
        }
        else {
            let body = `#!/usr/bin/env bash
set -e
get_script_dir () {
  SOURCE="\${BASH_SOURCE[0]}"
  # While $SOURCE is a symlink, resolve it
  while [ -h "$SOURCE" ]; do
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$( readlink "$SOURCE" )"
    # If $SOURCE was a relative symlink (so no "/" as prefix, need to resolve it relative to the symlink base directory
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  done
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  echo "$DIR"
}
DIR=$(get_script_dir)
${binPathEnvVar}="\$DIR/${bin}" ${redirectedEnvVar}=1 "$DIR/../${version}/bin/${bin}" "$@"
`;
            await fs.remove(dst);
            await fs.outputFile(dst, body);
            await fs.chmod(dst, 0o755);
            await fs.remove(path.join(this.clientRoot, 'current'));
            await fs.symlink(`./${version}`, path.join(this.clientRoot, 'current'));
        }
    }
    async ensureClientDir() {
        try {
            await fs.mkdirp(this.clientRoot);
        }
        catch (err) {
            if (err.code === 'EEXIST') {
                // for some reason the client directory is sometimes a file
                // if so, this happens. Delete it and recreate
                await fs.remove(this.clientRoot);
                await fs.mkdirp(this.clientRoot);
            }
            else {
                throw err;
            }
        }
    }
}
UpdateCommand.description = 'update the <%= config.bin %> CLI';
UpdateCommand.args = [{ name: 'channel', optional: true }];
UpdateCommand.flags = {
    autoupdate: command_1.flags.boolean({ hidden: true }),
};
exports.default = UpdateCommand;
