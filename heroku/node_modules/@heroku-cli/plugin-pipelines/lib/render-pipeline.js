"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const lodash_sortby_1 = tslib_1.__importDefault(require("lodash.sortby"));
const ownership_1 = require("./ownership");
async function renderPipeline(heroku, pipeline, pipelineApps, { withOwners, showOwnerWarning } = { withOwners: false, showOwnerWarning: false }) {
    cli_ux_1.default.styledHeader(pipeline.name);
    let owner;
    if (pipeline.owner) {
        owner = await ownership_1.getOwner(heroku, pipelineApps, pipeline);
        cli_ux_1.default.log(`owner: ${owner}`);
    }
    cli_ux_1.default.log('');
    const columns = {
        name: {
            header: 'app name',
            get(row) {
                return color_1.default.app(row.name || '');
            },
        },
        'coupling.stage': {
            header: 'stage',
            get(row) {
                return row.coupling.stage;
            },
        },
    };
    if (withOwners) {
        columns['owner.email'] = {
            header: 'owner',
            get(row) {
                const email = row.owner && row.owner.email;
                if (email) {
                    return email.endsWith('@herokumanager.com') ? `${row.split('@')[0]} (team)` : email;
                }
            },
        };
    }
    const developmentApps = lodash_sortby_1.default(pipelineApps.filter(app => app.coupling.stage === 'development'), ['name']);
    const reviewApps = lodash_sortby_1.default(pipelineApps.filter(app => app.coupling.stage === 'review'), ['name']);
    const stagingApps = lodash_sortby_1.default(pipelineApps.filter(app => app.coupling.stage === 'staging'), ['name']);
    const productionApps = lodash_sortby_1.default(pipelineApps.filter(app => app.coupling.stage === 'production'), ['name']);
    const apps = developmentApps.concat(reviewApps).concat(stagingApps).concat(productionApps);
    cli_ux_1.default.table(apps, columns);
    if (showOwnerWarning && pipeline.owner) {
        ownership_1.warnMixedOwnership(pipelineApps, pipeline, owner);
    }
}
exports.default = renderPipeline;
