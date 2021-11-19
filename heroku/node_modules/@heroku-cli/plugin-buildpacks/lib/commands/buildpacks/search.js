"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const lodash_1 = require("lodash");
const buildpack_registry_1 = require("@heroku/buildpack-registry");
class Search extends command_1.Command {
    async run() {
        const { args, flags } = this.parse(Search);
        let searchResults;
        const registry = new buildpack_registry_1.BuildpackRegistry();
        if (args.term) {
            const uniqueBuildpacks = new Map();
            const array = ((await registry.search(args.term, undefined, undefined)).unwrapOr([]))
                .concat((await registry.search(undefined, args.term, undefined)).unwrapOr([]))
                .concat((await registry.search(undefined, undefined, args.term)).unwrapOr([]));
            array
                .forEach((element) => {
                uniqueBuildpacks.set(`${element.namespace}/${element.name}`, element);
            });
            searchResults = [...uniqueBuildpacks.values()];
        }
        else {
            searchResults = (await registry.search(flags.namespace, flags.name, flags.description)).unwrapOr([]);
        }
        const buildpacks = searchResults.map((buildpack) => {
            return {
                buildpack: `${buildpack.namespace}/${buildpack.name}`,
                category: buildpack.category,
                description: buildpack.description,
            };
        });
        const trunc = (value, _) => lodash_1.truncate(value, { length: 35, omission: '…' });
        const displayTable = (buildpacks) => {
            cli_ux_1.cli.table(buildpacks, {
                columns: [
                    { key: 'buildpack', label: 'Buildpack' },
                    { key: 'category', label: 'Category' },
                    { key: 'description', label: 'Description', format: trunc },
                ],
            });
        };
        if (buildpacks.length === 0) {
            cli_ux_1.cli.log('No buildpacks found');
        }
        else if (buildpacks.length === 1) {
            displayTable(buildpacks);
            cli_ux_1.cli.log('\n1 buildpack found');
        }
        else {
            displayTable(buildpacks);
            cli_ux_1.cli.log(`\n${buildpacks.length} buildpacks found`);
        }
    }
}
exports.default = Search;
Search.description = 'search for buildpacks';
Search.flags = {
    namespace: command_1.flags.string({ description: 'buildpack namespaces to filter on using a comma separated list' }),
    name: command_1.flags.string({ description: 'buildpack names to filter on using a comma separated list ' }),
    description: command_1.flags.string({ description: 'buildpack description to filter on' }),
};
Search.args = [
    {
        name: 'term',
        description: 'search term that searches across name, namespace, and description',
    },
];
