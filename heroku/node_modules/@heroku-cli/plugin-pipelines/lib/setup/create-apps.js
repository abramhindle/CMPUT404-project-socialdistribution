"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../api");
function createApp(heroku, { archiveURL, name, organization, pipeline, stage }) {
    const params = {
        source_blob: { url: archiveURL },
        app: { name },
        pipeline_coupling: {
            stage,
            pipeline: pipeline.id,
        },
    };
    if (organization) {
        params.app.organization = organization;
    }
    else {
        params.app.personal = true;
    }
    return api_1.createAppSetup(heroku, params).then(setup => setup);
}
function createApps(heroku, archiveURL, pipeline, pipelineName, stagingAppName, organization) {
    const prodAppSetupPromise = createApp(heroku, {
        archiveURL,
        pipeline,
        name: pipelineName,
        stage: 'production',
        organization,
    });
    const stagingAppSetupPromise = createApp(heroku, {
        archiveURL,
        pipeline,
        name: stagingAppName,
        stage: 'staging',
        organization,
    });
    const promises = [prodAppSetupPromise, stagingAppSetupPromise];
    return Promise.all(promises).then(appSetups => {
        return appSetups;
    }, error => {
        cli_ux_1.default.error(error, { exit: 1 });
    });
}
exports.default = createApps;
