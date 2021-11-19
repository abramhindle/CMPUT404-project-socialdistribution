"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const git = require("../../utils/git");
const pipelines_1 = require("../../utils/pipelines");
const source_1 = require("../../utils/source");
const test_run_1 = require("../../utils/test-run");
class CiRun extends command_1.Command {
    async run() {
        const { flags } = this.parse(CiRun);
        const pipeline = await pipelines_1.getPipeline(flags, this);
        const commit = await git.readCommit('HEAD');
        cli_ux_1.default.action.start('Preparing source');
        const sourceBlobUrl = await source_1.createSourceBlob(commit.ref, this);
        cli_ux_1.default.action.stop();
        cli_ux_1.default.action.start('Starting test run');
        const { body: pipelineRepository } = await this.heroku.get(`https://kolkrabbi.heroku.com/pipelines/${pipeline.id}/repository`);
        const organization = pipelineRepository.organization && pipelineRepository.organization.name;
        const { body: testRun } = await this.heroku.post('/test-runs', { body: {
                commit_branch: commit.branch,
                commit_message: commit.message,
                commit_sha: commit.ref,
                pipeline: pipeline.id,
                organization,
                source_blob_url: sourceBlobUrl,
            },
        });
        cli_ux_1.default.action.stop();
        await test_run_1.displayAndExit(pipeline, testRun.number, this);
    }
}
exports.default = CiRun;
CiRun.description = 'run tests against current directory';
CiRun.examples = [
    `$ heroku ci:run --app murmuring-headland-14719
`,
];
CiRun.flags = {
    app: command_1.flags.string({ char: 'a', description: 'app name' }),
    pipeline: command_1.flags.pipeline({ required: false }),
};
