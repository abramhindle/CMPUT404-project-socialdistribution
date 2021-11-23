"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const analytics_1 = tslib_1.__importDefault(require("../../analytics"));
exports.analytics = async function (options) {
    const analytics = new analytics_1.default(this.config);
    await analytics.record(options);
};
