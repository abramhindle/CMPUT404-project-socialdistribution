"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const color_1 = tslib_1.__importDefault(require("@heroku-cli/color"));
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const debug_1 = tslib_1.__importDefault(require("debug"));
const api_1 = require("../../api");
const github_api_1 = tslib_1.__importDefault(require("../../github-api"));
const kolkrabbi_api_1 = tslib_1.__importDefault(require("../../kolkrabbi-api"));
const create_apps_1 = tslib_1.__importDefault(require("../../setup/create-apps"));
const get_ci_settings_1 = tslib_1.__importDefault(require("../../setup/get-ci-settings"));
const get_github_token_1 = tslib_1.__importDefault(require("../../setup/get-github-token"));
const get_name_and_repo_1 = tslib_1.__importDefault(require("../../setup/get-name-and-repo"));
const get_repo_1 = tslib_1.__importDefault(require("../../setup/get-repo"));
const get_settings_1 = tslib_1.__importDefault(require("../../setup/get-settings"));
const poll_app_setups_1 = tslib_1.__importDefault(require("../../setup/poll-app-setups"));
const setup_pipeline_1 = tslib_1.__importDefault(require("../../setup/setup-pipeline"));
const validate_1 = require("../../setup/validate");
// eslint-disable-next-line new-cap
const debug = debug_1.default('pipelines:setup');
class Setup extends command_1.Command {
    async run() {
        const { args, flags } = this.parse(Setup);
        const errors = validate_1.nameAndRepo(args);
        if (errors.length !== 0) {
            this.error(errors.join(', '));
            return;
        }
        const kolkrabbi = new kolkrabbi_api_1.default(this.config.userAgent, () => this.heroku.auth);
        const github = new github_api_1.default(this.config.userAgent, await get_github_token_1.default(kolkrabbi));
        const team = flags.team;
        const { name: pipelineName, repo: repoName } = await get_name_and_repo_1.default(args);
        const stagingAppName = pipelineName + validate_1.STAGING_APP_INDICATOR;
        const repo = await get_repo_1.default(github, repoName);
        const settings = await get_settings_1.default(flags.yes, repo.default_branch);
        const ciSettings = await get_ci_settings_1.default(flags.yes, team);
        const ownerType = team ? 'team' : 'user';
        // If team or org is not specified, we assign ownership to the user creating
        const { body: { id: ownerID }, } = team ? await api_1.getTeam(this.heroku, team) : await api_1.getAccountInfo(this.heroku);
        const owner = { id: ownerID, type: ownerType };
        cli_ux_1.default.action.start('Creating pipeline');
        const { body: pipeline } = await api_1.createPipeline(this.heroku, pipelineName, owner);
        cli_ux_1.default.action.stop();
        cli_ux_1.default.action.start('Linking to repo');
        await kolkrabbi.createPipelineRepository(pipeline.id, repo.id);
        cli_ux_1.default.action.stop();
        const archiveURL = await kolkrabbi.getArchiveURL(repoName, repo.default_branch);
        const appSetupsResult = await create_apps_1.default(this.heroku, archiveURL, pipeline, pipelineName, stagingAppName, team);
        const appSetups = appSetupsResult.map((result) => result.body);
        cli_ux_1.default.action.start(`Creating production and staging apps (${color_1.default.app(pipelineName)} and ${color_1.default.app(stagingAppName)})`);
        await poll_app_setups_1.default(this.heroku, appSetups);
        cli_ux_1.default.action.stop();
        const stagingApp = appSetups.find((appSetup) => appSetup.app.name === stagingAppName).app;
        const setup = setup_pipeline_1.default(kolkrabbi, stagingApp.id, settings, pipeline.id, ciSettings);
        cli_ux_1.default.action.start('Configuring pipeline');
        try {
            await setup;
            await cli_ux_1.default.open(`https://dashboard.heroku.com/pipelines/${pipeline.id}`);
        }
        catch (error) {
            debug(error);
            cli_ux_1.default.error(error);
        }
        finally {
            cli_ux_1.default.action.stop();
        }
    }
}
exports.default = Setup;
Setup.description = 'bootstrap a new pipeline with common settings and create a production and staging app (requires a fully formed app.json in the repo)';
Setup.examples = ['$ heroku pipelines:setup my-pipeline githuborg/reponame -t my-team'];
Setup.flags = {
    team: command_1.flags.team({
        description: 'the team to assign pipeline ownership to (defaults to current user)',
    }),
    yes: command_1.flags.boolean({
        char: 'y',
        description: 'accept all default settings without prompting',
    }),
};
Setup.args = [
    {
        name: 'name',
        description: 'name of pipeline',
        required: false,
    },
    {
        name: 'repo',
        description: 'a GitHub repository to connect the pipeline to',
        required: false,
    },
];
