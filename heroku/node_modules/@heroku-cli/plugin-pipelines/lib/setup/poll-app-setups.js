"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const api = tslib_1.__importStar(require("../api"));
const cli = require('heroku-cli-util');
function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
function pollAppSetup(heroku, appSetup) {
    return api.getAppSetup(heroku, appSetup.id).then(({ body: setup }) => {
        if (setup.status === 'succeeded') {
            return setup;
        }
        if (setup.status === 'failed') {
            throw new Error(`Couldn't create application ${cli.color.app(setup.app.name)}: ${setup.failure_message}`);
        }
        return wait(1000).then(() => pollAppSetup(heroku, appSetup));
    }).catch((error) => {
        return cli.exit(1, error);
    });
}
function pollAppSetups(heroku, appSetups) {
    return Promise.all(appSetups.map((appSetup) => pollAppSetup(heroku, appSetup)));
}
exports.default = pollAppSetups;
