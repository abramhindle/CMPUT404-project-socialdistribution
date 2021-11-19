"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@heroku-cli/color");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const distanceInWordsToNow = require("date-fns/distance_in_words_to_now");
const http_call_1 = require("http-call");
const util_1 = require("../util");
class Status extends command_1.Command {
    async run() {
        const { flags } = this.parse(Status);
        const apiPath = '/api/v4/current-status';
        const capitalize = (str) => str.substr(0, 1).toUpperCase() + str.substr(1);
        const printStatus = (status) => {
            const colorize = color_1.default[status];
            let message = capitalize(status);
            if (status === 'green') {
                message = 'No known issues at this time.';
            }
            return colorize(message);
        };
        const host = process.env.HEROKU_STATUS_HOST || 'https://status.heroku.com';
        const { body } = await http_call_1.default.get(host + apiPath);
        if (flags.json) {
            cli_ux_1.default.styledJSON(body);
            return;
        }
        for (const item of body.status) {
            const message = printStatus(item.status);
            this.log(`${(item.system + ':').padEnd(11)}${message}`);
        }
        for (const incident of body.incidents) {
            cli_ux_1.default.log();
            cli_ux_1.default.styledHeader(`${incident.title} ${color_1.default.yellow(incident.created_at)} ${color_1.default.cyan(incident.full_url)}`);
            const padding = util_1.maxBy(incident.updates, (i) => i.update_type.length).update_type.length + 0;
            for (const u of incident.updates) {
                cli_ux_1.default.log(`${color_1.default.yellow(u.update_type.padEnd(padding))} ${new Date(u.updated_at).toISOString()} (${distanceInWordsToNow(new Date(u.updated_at))} ago)`);
                cli_ux_1.default.log(`${u.contents}\n`);
            }
        }
    }
}
exports.default = Status;
Status.description = 'display current status of the Heroku platform';
Status.flags = {
    json: command_1.flags.boolean({ description: 'output in json format' }),
};
