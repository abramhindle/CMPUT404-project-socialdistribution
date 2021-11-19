"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
async function getCISettings(yes, organization) {
    const settings = {
        ci: true,
        organization: undefined,
    };
    if (yes) {
        delete settings.organization;
        return settings;
    }
    settings.ci = await cli_ux_1.default.confirm('Enable automatic Heroku CI test runs?');
    if (settings.ci && organization) {
        settings.organization = organization;
    }
    return settings;
}
exports.default = getCISettings;
