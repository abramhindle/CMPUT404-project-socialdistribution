"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const base_1 = require("../../base");
class WebhooksInfo extends base_1.default {
    async run() {
        const { flags, args } = this.parse(WebhooksInfo);
        const { path } = this.webhookType(flags);
        const { body: webhook } = await this.webhooksClient.get(`${path}/webhooks/${args.id}`);
        const obj = {
            'Webhook ID': webhook.id,
            URL: webhook.url,
            Include: webhook.include.join(','),
            Level: webhook.level,
        };
        cli_ux_1.cli.styledHeader(webhook.id);
        cli_ux_1.cli.styledObject(obj);
    }
}
exports.default = WebhooksInfo;
WebhooksInfo.description = 'info for a webhook on an app';
WebhooksInfo.example = ['$ heroku webhooks:info 99999999-9999-9999-9999-999999999999'];
WebhooksInfo.flags = {
    app: command_1.flags.app(),
    remote: command_1.flags.remote(),
    pipeline: command_1.flags.pipeline({ char: 'p', description: 'pipeline on which to list', hidden: true }),
};
WebhooksInfo.args = [{ name: 'id', required: true }];
