"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const path = tslib_1.__importStar(require("path"));
const deps_1 = tslib_1.__importDefault(require("./deps"));
const debug = require('debug')('heroku-cli:file');
function exists(f) {
    return deps_1.default.fs.pathExists(f);
}
exports.exists = exists;
async function stat(file) {
    // debug('stat', file)
    return deps_1.default.fs.stat(file);
}
exports.stat = stat;
async function rename(from, to) {
    debug('rename', from, to);
    return deps_1.default.fs.rename(from, to);
}
exports.rename = rename;
async function remove(file) {
    if (!await exists(file))
        return;
    debug('remove', file);
    return deps_1.default.fs.remove(file);
}
exports.remove = remove;
async function ls(dir) {
    const files = await deps_1.default.fs.readdir(dir);
    const paths = files.map(f => path.join(dir, f));
    return Promise.all(paths.map(path => deps_1.default.fs.stat(path).then(stat => ({ path, stat }))));
}
exports.ls = ls;
async function removeEmptyDirs(dir) {
    let files;
    try {
        files = await ls(dir);
    }
    catch (error) {
        if (error.code === 'ENOENT')
            return;
        throw error;
    }
    const dirs = files.filter(f => f.stat.isDirectory()).map(f => f.path);
    // eslint-disable-next-line no-await-in-loop
    for (const p of dirs.map(removeEmptyDirs))
        await p;
    files = await ls(dir);
    if (files.length === 0)
        await remove(dir);
}
exports.removeEmptyDirs = removeEmptyDirs;
async function readJSON(file) {
    debug('readJSON', file);
    return deps_1.default.fs.readJSON(file);
}
exports.readJSON = readJSON;
async function outputJSON(file, data, options = {}) {
    debug('outputJSON', file);
    return deps_1.default.fs.outputJSON(file, data, Object.assign({ spaces: 2 }, options));
}
exports.outputJSON = outputJSON;
function realpathSync(p) {
    return deps_1.default.fs.realpathSync(p);
}
exports.realpathSync = realpathSync;
