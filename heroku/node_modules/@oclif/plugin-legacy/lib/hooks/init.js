"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const __1 = require("..");
const util_1 = require("../util");
exports.init = async function (opts) {
    await Promise.all(opts.config.plugins.map(async (p, i) => {
        if (p.valid)
            return;
        try {
            const plugin = new __1.PluginLegacy(opts.config, p);
            await plugin.load();
            opts.config.plugins[i] = plugin; // eslint-disable-line require-atomic-updates
        }
        catch (error) {
            error.name = `@oclif/plugin-legacy: Plugin ${p.name}: ${error.name}`;
            error.detail = util_1.compact([error.detail, p.root]).join(' ');
            process.emitWarning(error);
        }
    }));
};
