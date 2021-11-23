"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const color_1 = require("@heroku-cli/color");
const cli_ux_1 = require("cli-ux");
const https_1 = require("https");
const phoenix_1 = require("phoenix");
const util_1 = require("util");
const uuid_1 = require("uuid");
const WebSocket = require("ws");
const debug = require('debug')('ci');
const ansiEscapes = require('ansi-escapes');
const HEROKU_CI_WEBSOCKET_URL = process.env.HEROKU_CI_WEBSOCKET_URL || 'wss://particleboard.heroku.com/socket';
function logStream(url, fn) {
    return https_1.get(url, fn);
}
function stream(url) {
    return new Promise((resolve, reject) => {
        const request = logStream(url, output => {
            output.on('data', data => {
                if (data.toString() === Buffer.from('').toString()) {
                    request.abort();
                    resolve();
                }
            });
            output.on('end', () => resolve());
            output.on('error', e => reject(e));
            output.pipe(process.stdout);
        });
    });
}
function statusIcon({ status }) {
    if (!status) {
        return color_1.default.yellow('-');
    }
    switch (status) {
        case 'pending':
        case 'creating':
        case 'building':
        case 'running':
        case 'debugging':
            return color_1.default.yellow('-');
        case 'errored':
            return color_1.default.red('!');
        case 'failed':
            return color_1.default.red('✗');
        case 'succeeded':
            return color_1.default.green('✓');
        case 'cancelled':
            return color_1.default.yellow('!');
        default:
            return color_1.default.yellow('?');
    }
}
const BUILDING = 'building';
const RUNNING = 'running';
const ERRORED = 'errored';
const FAILED = 'failed';
const SUCCEEDED = 'succeeded';
const CANCELLED = 'cancelled';
const TERMINAL_STATES = [SUCCEEDED, FAILED, ERRORED, CANCELLED];
const RUNNING_STATES = [RUNNING].concat(TERMINAL_STATES);
const BUILDING_STATES = [BUILDING, RUNNING].concat(TERMINAL_STATES);
function printLine(testRun) {
    return `${statusIcon(testRun)} #${testRun.number} ${testRun.commit_branch}:${testRun.commit_sha.slice(0, 7)} ${testRun.status}`;
}
function printLineTestNode(testNode) {
    return `${statusIcon(testNode)} #${testNode.index} ${testNode.status}`;
}
function processExitCode(command, testNode) {
    if (testNode.exit_code && testNode.exit_code !== 0) {
        command.exit(testNode.exit_code);
    }
}
function handleTestRunEvent(newTestRun, testRuns) {
    const previousTestRun = testRuns.find(({ id }) => id === newTestRun.id);
    if (previousTestRun) {
        const previousTestRunIndex = testRuns.indexOf(previousTestRun);
        testRuns.splice(previousTestRunIndex, 1);
    }
    testRuns.push(newTestRun);
    return testRuns;
}
function sort(testRuns) {
    return testRuns.sort((a, b) => a.number < b.number ? 1 : -1);
}
function draw(testRuns, watchOption = false, jsonOption = false, count = 15) {
    const latestTestRuns = sort(testRuns).slice(0, count);
    if (jsonOption) {
        cli_ux_1.default.styledJSON(latestTestRuns);
        return;
    }
    if (watchOption) {
        process.stdout.write(ansiEscapes.eraseDown);
    }
    const data = [];
    latestTestRuns.forEach(testRun => {
        data.push({
            iconStatus: `${statusIcon(testRun)}`,
            number: testRun.number,
            branch: testRun.commit_branch,
            sha: testRun.commit_sha.slice(0, 7),
            status: testRun.status,
        });
    });
    cli_ux_1.default.table(data, {
        printHeader: undefined,
        columns: [
            { key: 'iconStatus', width: 1, label: '' },
            { key: 'number', label: '' },
            { key: 'branch' },
            { key: 'sha' },
            { key: 'status' },
        ],
    });
    if (watchOption) {
        process.stdout.write(ansiEscapes.cursorUp(latestTestRuns.length));
    }
}
async function renderList(command, testRuns, pipeline, watchOption, jsonOption) {
    const watchable = (Boolean(watchOption && !jsonOption));
    if (!jsonOption) {
        const header = `${watchOption ? 'Watching' : 'Showing'} latest test runs for the ${pipeline.name} pipeline`;
        cli_ux_1.default.styledHeader(header);
    }
    draw(testRuns, watchOption, jsonOption);
    if (!watchable) {
        return;
    }
    const socket = new phoenix_1.Socket(HEROKU_CI_WEBSOCKET_URL, {
        transport: WebSocket,
        params: {
            token: command.heroku.auth,
            tab_id: `heroku-cli-${uuid_1.v4()}`,
        },
        logger: (kind, msg, data) => debug(`${kind}: ${msg}\n${util_1.inspect(data)}`),
    });
    socket.connect();
    const channel = socket.channel(`events:pipelines/${pipeline.id}/test-runs`, {});
    channel.on('create', ({ data }) => {
        testRuns = handleTestRunEvent(data, testRuns);
        draw(testRuns, watchOption);
    });
    channel.on('update', ({ data }) => {
        testRuns = handleTestRunEvent(data, testRuns);
        draw(testRuns, watchOption);
    });
    channel.join();
}
exports.renderList = renderList;
async function renderNodeOutput(command, testRun, testNode) {
    if (!testNode) {
        command.error(`Test run ${testRun.number} was ${testRun.status}. No Heroku CI runs found for this pipeline.`);
    }
    await stream(testNode.setup_stream_url);
    await stream(testNode.output_stream_url);
    command.log();
    command.log(printLine(testRun));
}
async function waitForStates(states, testRun, command) {
    let newTestRun = testRun;
    while (!states.includes(newTestRun.status.toString())) {
        // eslint-disable-next-line no-await-in-loop
        const { body: bodyTestRun } = await command.heroku.get(`/pipelines/${testRun.pipeline.id}/test-runs/${testRun.number}`);
        newTestRun = bodyTestRun;
    }
    return newTestRun;
}
async function display(pipeline, number, command) {
    let { body: testRun } = await command.heroku.get(`/pipelines/${pipeline.id}/test-runs/${number}`);
    if (testRun) {
        cli_ux_1.default.action.start('Waiting for build to start');
        testRun = await waitForStates(BUILDING_STATES, testRun, command);
        cli_ux_1.default.action.stop();
        const { body: testNodes } = await command.heroku.get(`/test-runs/${testRun.id}/test-nodes`);
        let firstTestNode = testNodes[0];
        if (firstTestNode) {
            await stream(firstTestNode.setup_stream_url);
        }
        if (testRun) {
            testRun = await waitForStates(RUNNING_STATES, testRun, command);
        }
        if (firstTestNode) {
            await stream(firstTestNode.output_stream_url);
        }
        if (testRun) {
            testRun = await waitForStates(TERMINAL_STATES, testRun, command);
        }
        // At this point, we know that testRun has a finished status,
        // and we can check for exit_code from firstTestNode
        if (testRun) {
            const { body: newTestNodes } = await command.heroku.get(`/test-runs/${testRun.id}/test-nodes`);
            firstTestNode = newTestNodes[0];
            command.log();
            command.log(printLine(testRun));
        }
        return firstTestNode;
    }
}
async function displayAndExit(pipeline, number, command) {
    const testNode = await display(pipeline, number, command);
    testNode ? processExitCode(command, testNode) : command.exit(1);
}
exports.displayAndExit = displayAndExit;
async function displayTestRunInfo(command, testRun, testNodes, nodeArg) {
    let testNode;
    if (nodeArg) {
        const nodeIndex = parseInt(nodeArg, 2);
        testNode = testNodes.length > 1 ? testNodes[nodeIndex] : testNodes[0];
        await renderNodeOutput(command, testRun, testNode);
        if (testNodes.length === 1) {
            command.log();
            command.warn('This pipeline doesn\'t have parallel test runs, but you specified a node');
            command.warn('See https://devcenter.heroku.com/articles/heroku-ci-parallel-test-runs for more info');
        }
        processExitCode(command, testNode);
    }
    else if (testNodes.length > 1) {
        command.log(printLine(testRun));
        command.log();
        testNodes.forEach(testNode => {
            command.log(printLineTestNode(testNode));
        });
    }
    else {
        testNode = testNodes[0];
        await renderNodeOutput(command, testRun, testNode);
        processExitCode(command, testNode);
    }
}
exports.displayTestRunInfo = displayTestRunInfo;
