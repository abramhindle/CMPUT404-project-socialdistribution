"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@heroku-cli/color");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const base_1 = require("../../base");
class Webhooks extends base_1.default {
    async run() {
        const { flags } = this.parse(Webhooks);
        const { path, display } = this.webhookType(flags);
        const { body: webhooks } = await this.webhooksClient.get(`${path}/webhooks`);
        if (webhooks.length === 0) {
            this.log(`${display} has no webhooks\nUse ${color_1.default.cmd('heroku webhooks:add')} to add one.`);
            return;
        }
        webhooks.sort((a, b) => Date.parse(a.created_at) - Date.parse(b.created_at));
        cli_ux_1.cli.table(webhooks, {
            id: {
                header: 'Webhook ID',
            },
            url: {
                header: 'URL',
            },
            include: {
                get: (row) => row.include.join(','),
            },
            level: {},
        }, {
            printLine: this.log,
        });
    }
}
exports.default = Webhooks;
Webhooks.description = 'list webhooks on an app';
Webhooks.examples = ['$ heroku webhooks'];
Webhooks.flags = {
    app: command_1.flags.app(),
    remote: command_1.flags.remote(),
    pipeline: command_1.flags.pipeline({
        char: 'p',
        description: 'pipeline on which to list',
        hidden: true,
    }),
};
