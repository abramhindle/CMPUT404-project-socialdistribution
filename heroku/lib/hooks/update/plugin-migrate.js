"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const fs = tslib_1.__importStar(require("fs-extra"));
const path = tslib_1.__importStar(require("path"));
const exec = (cmd, args) => {
    const execa = require('execa');
    return execa(cmd, args, { stdio: 'inherit' });
};
exports.migrate = async function () {
    if (process.argv[2] && process.argv[2].startsWith('plugins'))
        return;
    const pluginsDir = path.join(this.config.dataDir, 'plugins');
    const yarnLockFilePath = path.join(this.config.dataDir, 'yarn.lock');
    const removeYarnLockFile = async () => {
        if (await fs.existsSync(yarnLockFilePath)) {
            const yarnLockFile = await fs.readFileSync(yarnLockFilePath);
            if (yarnLockFile.toString().includes('cli-npm.heroku.com')) {
                await fs.remove(yarnLockFilePath);
            }
        }
    };
    const migrateV6Plugins = async () => {
        if (!await fs.pathExists(pluginsDir))
            return;
        process.stderr.write('heroku: migrating plugins\n');
        try {
            const p = path.join(pluginsDir, 'user.json');
            if (await fs.pathExists(p)) {
                const { manifest } = await fs.readJSON(p);
                for (const plugin of Object.keys(manifest.plugins)) {
                    process.stderr.write(`heroku-cli: migrating ${plugin}\n`);
                    // eslint-disable-next-line no-await-in-loop
                    await exec('heroku', ['plugins:install', plugin]);
                }
            }
        }
        catch (error) {
            this.warn(error);
        }
        try {
            const p = path.join(pluginsDir, 'link.json');
            if (await fs.pathExists(p)) {
                const { manifest } = await fs.readJSON(path.join(pluginsDir, 'link.json'));
                for (const { root } of Object.values(manifest.plugins)) {
                    process.stderr.write(`heroku-cli: migrating ${root}\n`);
                    // eslint-disable-next-line no-await-in-loop
                    await exec('heroku', ['plugins:link', root]);
                }
            }
        }
        catch (error) {
            this.warn(error);
        }
        await fs.remove(pluginsDir);
        process.stderr.write('heroku: done migrating plugins\n');
    };
    await removeYarnLockFile();
    await migrateV6Plugins();
};
