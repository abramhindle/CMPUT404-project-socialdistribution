"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
class Logout extends command_1.Command {
    async run() {
        cli_ux_1.default.action.start('Logging out');
        await this.heroku.logout();
        await this.config.runHook('recache', { type: 'logout' });
    }
}
exports.default = Logout;
Logout.description = 'clears local login credentials and invalidates API session';
Logout.aliases = ['logout'];
