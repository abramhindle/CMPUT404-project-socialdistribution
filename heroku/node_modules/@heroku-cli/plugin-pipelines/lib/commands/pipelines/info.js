"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../../api");
const disambiguate_1 = tslib_1.__importDefault(require("../../disambiguate"));
const render_pipeline_1 = tslib_1.__importDefault(require("../../render-pipeline"));
class PipelinesInfo extends command_1.Command {
    async run() {
        const { args, flags } = this.parse(PipelinesInfo);
        const pipeline = await disambiguate_1.default(this.heroku, args.pipeline);
        const pipelineApps = await api_1.listPipelineApps(this.heroku, pipeline.id);
        if (flags.json) {
            cli_ux_1.default.styledJSON({ pipeline, apps: pipelineApps });
        }
        else {
            await render_pipeline_1.default(this.heroku, pipeline, pipelineApps, {
                withOwners: flags['with-owners'],
                showOwnerWarning: true,
            });
        }
    }
}
exports.default = PipelinesInfo;
PipelinesInfo.description = 'show list of apps in a pipeline';
PipelinesInfo.examples = [
    '$ heroku pipelines:info my-pipeline',
];
PipelinesInfo.flags = {
    json: command_1.flags.boolean({
        description: 'output in json format',
    }),
    'with-owners': command_1.flags.boolean({
        description: 'shows owner of every app',
        hidden: true,
    }),
};
PipelinesInfo.args = [{
        name: 'pipeline',
        description: 'pipeline to show list of apps for',
        required: true,
    }];
