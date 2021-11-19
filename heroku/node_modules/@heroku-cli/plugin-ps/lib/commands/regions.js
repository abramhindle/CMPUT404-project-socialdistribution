"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@heroku-cli/color");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const _ = require("lodash");
class Regions extends command_1.Command {
    async run() {
        const { flags } = this.parse(Regions);
        let { body: regions } = await this.heroku.get('/regions');
        if (flags.private) {
            regions = regions.filter((region) => region.private_capable);
        }
        else if (flags.common) {
            regions = regions.filter((region) => !region.private_capable);
        }
        regions = _.sortBy(regions, ['private_capable', 'name']);
        if (flags.json) {
            cli_ux_1.cli.styledJSON(regions);
        }
        else {
            cli_ux_1.cli.table(regions, {
                columns: [
                    { key: 'name', label: 'ID', format: (n) => color_1.default.green(n) },
                    { key: 'description', label: 'Location' },
                    { key: 'private_capable', label: 'Runtime', format: (c) => c ? 'Private Spaces' : 'Common Runtime' },
                ],
            });
        }
    }
}
exports.default = Regions;
Regions.topic = 'regions';
Regions.description = 'list available regions for deployment';
Regions.flags = {
    json: command_1.flags.boolean({ description: 'output in json format' }),
    private: command_1.flags.boolean({ description: 'show regions for private spaces' }),
    common: command_1.flags.boolean({ description: 'show regions for common runtime' }),
};
