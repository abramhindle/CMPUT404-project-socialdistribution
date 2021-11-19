"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const tmp = require("tmp");
const execa = require("execa");
const _ = require("lodash");
const debug = require('debug')('edit-string');
function tmpFile(opts) {
    return new Promise((resolve, reject) => {
        tmp.file(opts, (err, name, fd, cleanup) => {
            if (err)
                return reject(err);
            resolve({ name, fd, cleanup });
        });
    });
}
function edit(name, editor) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        debug(editor, [name]);
        let msg = `Waiting for ${editor}... `;
        process.stderr.write(msg);
        yield execa(editor, [name], { stdio: 'inherit' });
        process.stderr.write(`\r${msg.replace(/./g, ' ')}\r`);
    });
}
module.exports = function (input, options = {}) {
    return tslib_1.__awaiter(this, void 0, void 0, function* () {
        const { promisify } = require('util');
        const FS = require('fs');
        const fs = {
            write: promisify(FS.write),
            readFile: promisify(FS.readFile)
        };
        const { name, fd, cleanup } = yield tmpFile(options);
        yield fs.write(fd, input);
        const editors = _.compact([process.env.VISUAL || process.env.EDITOR, 'pico', 'nano', 'vi']);
        for (let editor of editors) {
            try {
                yield edit(name, editor);
                let output = yield fs.readFile(name, 'utf8');
                cleanup();
                return output;
            }
            catch (err) {
                if (err.code !== 'ENOENT') {
                    console.error(err);
                    continue;
                }
                throw err;
            }
        }
        throw new Error('No $VISUAL or $EDITOR set');
    });
};
