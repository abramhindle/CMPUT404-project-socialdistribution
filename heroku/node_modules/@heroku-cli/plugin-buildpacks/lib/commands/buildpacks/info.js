"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const true_myth_1 = require("true-myth");
const buildpack_registry_1 = require("@heroku/buildpack-registry");
class Info extends command_1.Command {
    async run() {
        const { args } = this.parse(Info);
        const registry = new buildpack_registry_1.BuildpackRegistry();
        true_myth_1.Result.match({
            // eslint-disable-next-line @typescript-eslint/no-empty-function
            Ok: _ => { },
            Err: err => {
                this.error(`Could not publish the buildpack.\n${err}`);
            },
        }, buildpack_registry_1.BuildpackRegistry.isValidBuildpackSlug(args.buildpack));
        const result = await registry.info(args.buildpack);
        true_myth_1.Result.match({
            Ok: buildpack => {
                cli_ux_1.cli.styledHeader(args.buildpack);
                cli_ux_1.cli.styledObject(buildpack, ['description', 'category', 'license', 'support', 'source', 'readme']);
            },
            Err: err => {
                if (err.status === 404) {
                    cli_ux_1.cli.error(`Could not find the buildpack '${args.buildpack}'`);
                }
                else {
                    cli_ux_1.cli.error(`Problems finding buildpack info: ${err.description}`);
                }
            },
        }, result);
    }
}
exports.default = Info;
Info.description = 'fetch info about a buildpack';
Info.args = [
    {
        name: 'buildpack',
        required: true,
        description: 'namespace/name of the buildpack',
    },
];
