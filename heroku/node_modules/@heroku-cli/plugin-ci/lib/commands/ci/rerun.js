"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const command_1 = require("@heroku-cli/command");
const cli_ux_1 = require("cli-ux");
const pipelines_1 = require("../../utils/pipelines");
const source_1 = require("../../utils/source");
const test_run_1 = require("../../utils/test-run");
class CiReRun extends command_1.Command {
    async run() {
        const { flags, args } = this.parse(CiReRun);
        const pipeline = await pipelines_1.getPipeline(flags, this);
        let sourceTestRun;
        if (args.number) {
            const testRunResponse = await this.heroku.get(`/pipelines/${pipeline.id}/test-runs/${args.number}`);
            sourceTestRun = testRunResponse.body;
        }
        else {
            const { body: testRuns } = await this.heroku.get(`/pipelines/${pipeline.id}/test-runs`, { headers: { Range: 'number ..; order=desc,max=1' } });
            sourceTestRun = testRuns[0];
        }
        this.log(`Rerunning test run #${sourceTestRun.number}...`);
        cli_ux_1.default.action.start('Preparing source');
        const sourceBlobUrl = await source_1.createSourceBlob(sourceTestRun.commit_sha, this);
        cli_ux_1.default.action.stop();
        const { body: pipelineRepository } = await this.heroku.get(`https://kolkrabbi.heroku.com/pipelines/${pipeline.id}/repository`);
        cli_ux_1.default.action.start('Starting test run');
        const organization = pipelineRepository.organization && pipelineRepository.organization.name;
        const { body: testRun } = await this.heroku.post('/test-runs', { body: {
                commit_branch: sourceTestRun.commit_branch,
                commit_message: sourceTestRun.commit_message,
                commit_sha: sourceTestRun.commit_sha,
                pipeline: pipeline.id,
                organization,
                source_blob_url: sourceBlobUrl,
            },
        });
        cli_ux_1.default.action.stop();
        await test_run_1.displayAndExit(pipeline, testRun.number, this);
    }
}
exports.default = CiReRun;
CiReRun.description = 'rerun tests against current directory';
CiReRun.examples = [
    `$ heroku ci:rerun 985 --app murmuring-headland-14719
`,
];
CiReRun.flags = {
    app: command_1.flags.string({ char: 'a', description: 'app name' }),
    pipeline: command_1.flags.pipeline({ required: false }),
};
CiReRun.args = [{ name: 'number', required: false }];
