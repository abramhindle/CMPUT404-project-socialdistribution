"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
class Pipelines extends command_1.Command {
    async run() {
        const { flags } = this.parse(Pipelines);
        const { body: pipelines } = await this.heroku.get('/pipelines');
        if (flags.json) {
            cli_ux_1.default.styledJSON(pipelines);
        }
        else {
            cli_ux_1.default.styledHeader('My Pipelines');
            for (const pipeline of pipelines) {
                cli_ux_1.default.log(pipeline.name);
            }
        }
    }
}
exports.default = Pipelines;
Pipelines.description = 'list pipelines you have access to';
Pipelines.examples = [
    '$ heroku pipelines',
];
Pipelines.flags = {
    json: command_1.flags.boolean({ description: 'output in json format' }),
};
