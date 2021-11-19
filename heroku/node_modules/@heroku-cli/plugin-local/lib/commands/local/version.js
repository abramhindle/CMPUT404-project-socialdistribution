"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
const fork_foreman_1 = require("../../fork-foreman");
class Version extends command_1.Command {
    async run() {
        this.parse(Version);
        const execArgv = ['--version'];
        await fork_foreman_1.fork(execArgv);
    }
}
Version.description = 'display node-foreman version';
exports.default = Version;
