"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const base_1 = require("../../../base");
class EventsIndex extends base_1.default {
    async run() {
        const { flags } = this.parse(EventsIndex);
        const { path, display } = this.webhookType(flags);
        cli_ux_1.cli.warn('heroku webhooks:event is deprecated, please use heroku webhooks:deliveries');
        const { body: events } = await this.webhooksClient.get(`${path}/webhook-events`);
        if (events.length === 0) {
            this.log(`${display} has no events`);
        }
        else {
            events.sort((a, b) => Date.parse(a.created_at) - Date.parse(b.created_at));
            cli_ux_1.cli.table(events, {
                id: {
                    header: 'Event ID',
                },
                resource: {
                    get: (w) => w.payload.resource,
                },
                action: {
                    get: (w) => w.payload.action,
                },
                published_at: {
                    header: 'Published At', get: (w) => w.payload.published_at,
                },
            }, {
                printLine: this.log,
            });
        }
    }
}
exports.default = EventsIndex;
EventsIndex.description = 'list webhook events on an app';
EventsIndex.examples = [
    '$ heroku webhooks:events',
];
EventsIndex.flags = {
    app: command_1.flags.app(),
    remote: command_1.flags.remote(),
    pipeline: command_1.flags.pipeline({ char: 'p', description: 'pipeline on which to list', hidden: true }),
};
