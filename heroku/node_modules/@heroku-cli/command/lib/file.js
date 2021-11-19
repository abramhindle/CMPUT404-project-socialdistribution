"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const fs = tslib_1.__importStar(require("fs"));
const util_1 = require("util");
let _debug;
function debug(...args) {
    if (_debug)
        _debug = require('debug')('@heroku-cli/command:file');
    _debug(...args);
}
function exists(f) {
    // tslint:disable-next-line
    return util_1.promisify(fs.exists)(f);
}
exports.exists = exists;
function readdir(f) {
    debug('readdir', f);
    return util_1.promisify(fs.readdir)(f);
}
exports.readdir = readdir;
function readFile(f) {
    debug('readFile', f);
    return util_1.promisify(fs.readFile)(f);
}
exports.readFile = readFile;
