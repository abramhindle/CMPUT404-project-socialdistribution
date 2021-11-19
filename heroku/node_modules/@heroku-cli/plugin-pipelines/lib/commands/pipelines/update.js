"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const command_1 = require("@heroku-cli/command");
const completions_1 = require("@heroku-cli/command/lib/completions");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../../api");
class PipelinesUpdate extends command_1.Command {
    async run() {
        const { flags } = this.parse(PipelinesUpdate);
        const app = flags.app;
        const stage = flags.stage;
        cli_ux_1.default.action.start(`Changing ${color_1.default.app(app)} to ${stage}`);
        await api_1.updateCoupling(this.heroku, app, stage);
        cli_ux_1.default.action.stop();
    }
}
exports.default = PipelinesUpdate;
PipelinesUpdate.description = 'update the app\'s stage in a pipeline';
PipelinesUpdate.examples = [
    '$ heroku pipelines:update -s staging -a my-app',
];
PipelinesUpdate.flags = {
    app: command_1.flags.app({ required: true }),
    remote: command_1.flags.remote(),
    stage: command_1.flags.string({
        char: 's',
        description: 'new stage of app',
        completion: completions_1.StageCompletion,
        required: true,
    }),
};
