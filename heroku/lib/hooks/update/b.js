"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const child_process_1 = require("child_process");
const path = tslib_1.__importStar(require("path"));
const fs = tslib_1.__importStar(require("../../file"));
const debug = require('debug')('heroku:brewhook');
function brew(args, opts = {}) {
    debug('brew %o', args);
    return child_process_1.spawnSync('brew', args, Object.assign(Object.assign({ stdio: 'inherit' }, opts), { encoding: 'utf8' }));
}
exports.brewHook = async function () {
    if (this.config.platform !== 'darwin')
        return;
    const brewRoot = path.join(process.env.HOMEBREW_PREFIX || '/usr/local');
    let binPath;
    try {
        binPath = fs.realpathSync(path.join(brewRoot, 'bin/heroku'));
    }
    catch (error) {
        if (error.code === 'ENOENT')
            return;
        throw error;
    }
    let cellarPath;
    if (binPath && binPath.startsWith(path.join(brewRoot, 'Cellar'))) {
        cellarPath = path.resolve(binPath, path.dirname(path.relative(binPath, path.join(brewRoot, 'Cellar/heroku'))));
    }
    const fetchInstallReceipt = async () => {
        if (!cellarPath)
            return;
        return fs.readJSON(path.join(cellarPath, 'INSTALL_RECEIPT.json'));
    };
    const needsMigrate = async () => {
        const receipt = await fetchInstallReceipt();
        if (!receipt)
            return false;
        return receipt.source.tap === 'homebrew/core';
    };
    if (!await needsMigrate())
        return;
    debug('migrating from brew');
    // not on private tap, move to it
    brew(['uninstall', 'heroku']);
    brew(['install', 'heroku/brew/heroku']);
};
