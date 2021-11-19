"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../../api");
const disambiguate_1 = tslib_1.__importDefault(require("../../disambiguate"));
class PipelinesRename extends command_1.Command {
    async run() {
        const { args } = this.parse(PipelinesRename);
        const pipeline = await disambiguate_1.default(this.heroku, args.pipeline);
        cli_ux_1.default.action.start(`Renaming ${color_1.default.pipeline(pipeline.name)} pipeline to ${color_1.default.pipeline(args.name)}`);
        await api_1.updatePipeline(this.heroku, pipeline.id, {
            name: args.name,
        });
        cli_ux_1.default.action.stop();
    }
}
exports.default = PipelinesRename;
PipelinesRename.description = 'rename a pipeline';
PipelinesRename.examples = [
    '$ heroku pipelines:rename my-pipeline new-pipeline-name',
];
PipelinesRename.args = [
    {
        name: 'pipeline',
        description: 'current name of pipeline',
        required: true,
    },
    {
        name: 'name',
        description: 'new name of pipeline',
        required: true,
    },
];
