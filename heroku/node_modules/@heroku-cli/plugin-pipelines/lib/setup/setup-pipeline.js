"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
function setupPipeline(kolkrabbi, app, settings, pipelineID, ciSettings = {}) {
    const promises = [kolkrabbi.updateAppLink(app, settings)];
    if (ciSettings.ci) {
        promises.push(kolkrabbi.updatePipelineRepository(pipelineID, ciSettings));
    }
    return Promise.all(promises).then(([appLink]) => {
        return appLink;
    }, error => {
        cli_ux_1.default.error(error.body.message || error.message);
    });
}
exports.default = setupPipeline;
