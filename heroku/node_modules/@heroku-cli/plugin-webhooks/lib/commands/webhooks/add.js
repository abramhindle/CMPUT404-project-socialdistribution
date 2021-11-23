"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const base_1 = require("../../base");
class WebhooksAdd extends base_1.default {
    async run() {
        const { flags } = this.parse(WebhooksAdd);
        const { path, display } = this.webhookType(flags);
        cli_ux_1.cli.action.start(`Adding webhook to ${display}`);
        const response = await this.webhooksClient.post(`${path}/webhooks`, {
            body: {
                include: flags.include.split(',').map(s => s.trim()),
                level: flags.level,
                secret: flags.secret,
                url: flags.url,
                authorization: flags.authorization,
            },
        });
        const secret = response.headers && response.headers['heroku-webhook-secret'];
        cli_ux_1.cli.action.stop();
        if (secret) {
            cli_ux_1.cli.styledHeader('Webhooks Signing Secret');
            this.log(secret);
        }
        else {
            cli_ux_1.cli.warn('no secret found');
        }
    }
}
exports.default = WebhooksAdd;
WebhooksAdd.description = 'add a webhook to an app';
WebhooksAdd.examples = [
    '$ heroku webhooks:add -i api:dyno -l notify -u https://example.com/hooks',
];
WebhooksAdd.flags = {
    app: command_1.flags.app(),
    remote: command_1.flags.remote(),
    pipeline: command_1.flags.pipeline({ char: 'p', description: 'pipeline on which to list', hidden: true }),
    include: command_1.flags.string({ char: 'i', description: 'comma delimited event types your server will receive ', required: true }),
    level: command_1.flags.string({ char: 'l', description: 'notify does not retry, sync will retry until successful or timeout', required: true }),
    secret: command_1.flags.string({ char: 's', description: 'value to sign delivery with in Heroku-Webhook-Hmac-SHA256 header' }),
    authorization: command_1.flags.string({ char: 't', description: 'authoriation header to send with webhooks' }),
    url: command_1.flags.string({ char: 'u', description: 'URL for receiver', required: true }),
};
