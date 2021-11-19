"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const disambiguate_1 = tslib_1.__importDefault(require("../../disambiguate"));
class Open extends command_1.Command {
    async run() {
        const { args } = this.parse(Open);
        const pipeline = await disambiguate_1.default(this.heroku, args.pipeline);
        await cli_ux_1.default.open(`https://dashboard.heroku.com/pipelines/${pipeline.id}`);
    }
}
exports.default = Open;
Open.description = 'open a pipeline in dashboard';
Open.examples = ['$ heroku pipelines:open my-pipeline'];
Open.args = [{
        name: 'pipeline', description: 'name of pipeline', required: true,
    }];
