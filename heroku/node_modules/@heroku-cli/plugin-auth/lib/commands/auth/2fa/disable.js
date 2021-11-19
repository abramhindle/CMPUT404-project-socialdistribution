"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
class Auth2faGenerate extends command_1.Command {
    async run() {
        cli_ux_1.default.error('this command has been removed, in favor of disabling MFA in your Account Settings in a browser: https://dashboard.heroku.com/account');
        cli_ux_1.default.exit(1);
    }
}
exports.default = Auth2faGenerate;
Auth2faGenerate.description = 'disables 2fa on account';
Auth2faGenerate.example = '$ heroku auth:2fa:disable';
Auth2faGenerate.aliases = [
    'twofactor:disable',
    '2fa:disable',
];
