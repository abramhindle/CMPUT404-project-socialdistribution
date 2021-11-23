"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const path = tslib_1.__importStar(require("path"));
const fs = tslib_1.__importStar(require("fs-extra"));
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
function checkTos(options) {
    const tosPath = path.join(options.config.cacheDir, 'terms-of-service');
    const viewedBanner = fs.pathExistsSync(tosPath);
    const message = 'Our terms of service have changed: https://dashboard.heroku.com/terms-of-service';
    if (!viewedBanner) {
        cli_ux_1.default.warn(message);
        fs.createFile(tosPath);
    }
}
exports.checkTos = checkTos;
const hook = async function (options) {
    checkTos(options);
};
exports.default = hook;
