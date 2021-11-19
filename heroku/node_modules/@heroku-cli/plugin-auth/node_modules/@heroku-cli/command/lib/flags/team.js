"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
const completions_1 = require("../completions");
exports.team = command_1.flags.build({
    char: 't',
    completion: completions_1.TeamCompletion,
    description: 'team to use',
    default: ({ flags }) => {
        let { HEROKU_ORGANIZATION: org, HEROKU_TEAM: team } = process.env;
        if (flags.org)
            return flags.org;
        if (team)
            return team;
        if (org)
            return org;
    }
});
