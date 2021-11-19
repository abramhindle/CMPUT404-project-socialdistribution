"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const edit = require('edit-string');
// This indirection exists to give tests
// a way to stub calls to `edit(...)`
class Editor {
    edit(input, options = {}) {
        return edit(input, options);
    }
}
exports.Editor = Editor;
