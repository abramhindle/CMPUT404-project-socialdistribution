"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const true_myth_1 = require("true-myth");
const buildpack_registry_1 = require("@heroku/buildpack-registry");
class Versions extends command_1.Command {
    async run() {
        const { args } = this.parse(Versions);
        const herokuAuth = this.heroku.auth || '';
        if (herokuAuth === '') {
            this.error('You need to be logged in to run this command.');
        }
        const registry = new buildpack_registry_1.BuildpackRegistry();
        true_myth_1.Result.match({
            // eslint-disable-next-line @typescript-eslint/no-empty-function
            Ok: _ => { },
            Err: err => {
                this.error(`Could not find the buildpack.\n${err}`);
            },
        }, buildpack_registry_1.BuildpackRegistry.isValidBuildpackSlug(args.buildpack));
        const result = await registry.listVersions(args.buildpack);
        true_myth_1.Result.match({
            Ok: versions => {
                cli_ux_1.cli.table(versions.sort((a, b) => {
                    return a.release > b.release ? -1 : 1;
                }), {
                    columns: [
                        { key: 'release', label: 'Version' },
                        { key: 'created_at', label: 'Released At' },
                        { key: 'status', label: 'Status' },
                    ],
                });
            },
            Err: err => {
                if (err.status === 404) {
                    this.error(`Could not find '${args.buildpack}'`);
                }
                else {
                    this.error(`Problem fetching versions, ${err.status}: ${err.description}`);
                }
            },
        }, result);
    }
}
exports.default = Versions;
Versions.description = 'list versions of a buildpack';
Versions.args = [
    {
        name: 'buildpack',
        required: true,
        description: 'namespace/name of the buildpack',
    },
];
