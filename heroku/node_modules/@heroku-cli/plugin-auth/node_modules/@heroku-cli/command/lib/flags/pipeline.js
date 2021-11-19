"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
exports.pipeline = command_1.flags.build({
    char: 'p',
    description: 'name of pipeline',
});
