"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.brewHook = async function () {
    // autocomplete is now in core, skip windows
    if (this.config.windows)
        return;
    await this.config.runHook('recache', { type: 'update' });
};
