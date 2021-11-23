"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
exports.org = command_1.flags.build({
    char: 'o',
    default: () => process.env.HEROKU_ORGANIZATION,
    description: 'name of org',
    hidden: true,
});
