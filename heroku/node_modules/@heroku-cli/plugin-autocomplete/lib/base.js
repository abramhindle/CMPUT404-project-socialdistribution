"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const fs = require("fs-extra");
const path = require("path");
const completions_1 = require("./completions");
class AutocompleteBase extends command_1.default {
    errorIfWindows() {
        if (this.config.windows) {
            throw new Error('Autocomplete is not currently supported in Windows');
        }
    }
    errorIfNotSupportedShell(shell) {
        if (!shell) {
            this.error('Missing required argument shell');
        }
        this.errorIfWindows();
        if (!['bash', 'zsh'].includes(shell)) {
            throw new Error(`${shell} is not a supported shell for autocomplete`);
        }
    }
    get autocompleteCacheDir() {
        return path.join(this.config.cacheDir, 'autocomplete');
    }
    get completionsCacheDir() {
        return path.join(this.config.cacheDir, 'autocomplete', 'completions');
    }
    get acLogfilePath() {
        return path.join(this.config.cacheDir, 'autocomplete.log');
    }
    writeLogFile(msg) {
        const now = new Date();
        const entry = `[${now}] ${msg}\n`;
        const fd = fs.openSync(this.acLogfilePath, 'a');
        // eslint-disable-next-line
        // @ts-ignore
        fs.write(fd, entry);
    }
    findCompletion(cmdId, name, description = '') {
        return new completions_1.CompletionLookup(cmdId, name, description).run();
    }
}
exports.AutocompleteBase = AutocompleteBase;
