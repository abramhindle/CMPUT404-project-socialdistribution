"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs-extra");
async function updateCache(cachePath, cache) {
    await fs.ensureFile(cachePath);
    await fs.writeJSON(cachePath, cache);
}
exports.updateCache = updateCache;
function _mtime(f) {
    return fs.statSync(f).mtime;
}
function _isStale(cachePath, cacheDuration) {
    const past = new Date();
    past.setSeconds(past.getSeconds() - cacheDuration);
    return past.getTime() > _mtime(cachePath).getTime();
}
async function fetchCache(cachePath, cacheDuration, options) {
    const cachePresent = fs.existsSync(cachePath);
    if (cachePresent && !_isStale(cachePath, cacheDuration)) {
        return fs.readJSON(cachePath);
    }
    const cache = await options.cacheFn();
    // to-do: move this to a fork
    await updateCache(cachePath, cache);
    return cache;
}
exports.fetchCache = fetchCache;
