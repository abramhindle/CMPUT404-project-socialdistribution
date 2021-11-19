"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const _ = tslib_1.__importStar(require("lodash"));
const quote_1 = require("../../quote");
class ConfigIndex extends command_1.Command {
    async run() {
        const { flags } = this.parse(ConfigIndex);
        const { body: config } = await this.heroku.get(`/apps/${flags.app}/config-vars`);
        if (flags.shell) {
            Object.entries(config)
                .forEach(([k, v]) => cli_ux_1.default.log(`${k}=${quote_1.quote(v)}`));
        }
        else if (flags.json) {
            cli_ux_1.default.styledJSON(config);
        }
        else {
            cli_ux_1.default.styledHeader(`${flags.app} Config Vars`);
            cli_ux_1.default.styledObject(_.mapKeys(config, (_, k) => color_1.default.configVar(k)));
        }
    }
}
exports.ConfigIndex = ConfigIndex;
ConfigIndex.description = 'display the config vars for an app';
ConfigIndex.flags = {
    app: command_1.flags.app({ required: true }),
    remote: command_1.flags.remote(),
    shell: command_1.flags.boolean({ char: 's', description: 'output config vars in shell format' }),
    json: command_1.flags.boolean({ char: 'j', description: 'output config vars in json format' }),
};
