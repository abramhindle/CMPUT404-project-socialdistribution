"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const api_1 = require("../../api");
const github_api_1 = tslib_1.__importDefault(require("../../github-api"));
const kolkrabbi_api_1 = tslib_1.__importDefault(require("../../kolkrabbi-api"));
const get_github_token_1 = tslib_1.__importDefault(require("../../setup/get-github-token"));
const get_name_and_repo_1 = tslib_1.__importDefault(require("../../setup/get-name-and-repo"));
const get_repo_1 = tslib_1.__importDefault(require("../../setup/get-repo"));
const validate_1 = require("../../setup/validate");
class Connect extends command_1.Command {
    async run() {
        const { args, flags } = this.parse(Connect);
        const combinedInputs = {
            name: args.name,
            repo: flags.repo,
        };
        const errors = validate_1.nameAndRepo({ repo: flags.repo });
        if (errors.length !== 0) {
            this.error(errors.join(', '));
            return;
        }
        const kolkrabbi = new kolkrabbi_api_1.default(this.config.userAgent, () => this.heroku.auth);
        const github = new github_api_1.default(this.config.userAgent, await get_github_token_1.default(kolkrabbi));
        const { name: pipelineName, repo: repoName, } = await get_name_and_repo_1.default(combinedInputs);
        const repo = await get_repo_1.default(github, repoName);
        const pipeline = await api_1.getPipeline(this.heroku, pipelineName);
        cli_ux_1.default.action.start('Linking to repo');
        await kolkrabbi.createPipelineRepository(pipeline.body.id, repo.id);
        cli_ux_1.default.action.stop();
    }
}
exports.default = Connect;
Connect.description = 'connect a github repo to an existing pipeline';
Connect.examples = [
    '$ heroku pipelines:connect my-pipeline -r githuborg/reponame',
];
Connect.flags = {
    repo: command_1.flags.string({
        name: 'repo',
        char: 'r',
        description: 'the GitHub repository to connect to',
        required: true,
    }),
};
Connect.args = [{
        name: 'name',
        description: 'name of pipeline',
        required: true,
    }];
