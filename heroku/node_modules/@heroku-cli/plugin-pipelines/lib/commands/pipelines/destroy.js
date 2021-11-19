"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../../api");
const disambiguate_1 = tslib_1.__importDefault(require("../../disambiguate"));
class PipelinesDestroy extends command_1.Command {
    async run() {
        const { args } = this.parse(PipelinesDestroy);
        const pipeline = await disambiguate_1.default(this.heroku, args.pipeline);
        cli_ux_1.default.action.start(`Destroying ${color_1.default.pipeline(pipeline.name)} pipeline`);
        await api_1.destroyPipeline(this.heroku, pipeline.name, pipeline.id);
        cli_ux_1.default.action.stop();
    }
}
exports.default = PipelinesDestroy;
PipelinesDestroy.description = 'destroy a pipeline';
PipelinesDestroy.examples = [
    '$ heroku pipelines:destroy my-pipeline',
];
PipelinesDestroy.args = [{
        name: 'pipeline',
        description: 'name of pipeline',
        required: true,
    }];
