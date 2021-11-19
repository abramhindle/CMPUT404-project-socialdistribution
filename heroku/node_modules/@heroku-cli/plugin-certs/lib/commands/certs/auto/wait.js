"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@oclif/command");
class CertsAutoWait extends command_1.Command {
    async run() {
        this.parse(CertsAutoWait);
    }
}
CertsAutoWait.description = 'waits for the certificate to be activated';
CertsAutoWait.hidden = true;
CertsAutoWait.flags = {
    help: command_1.flags.help({ char: 'h' }),
};
exports.default = CertsAutoWait;
