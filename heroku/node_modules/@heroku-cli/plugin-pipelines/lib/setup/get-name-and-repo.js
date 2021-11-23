"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const cli_ux_1 = tslib_1.__importDefault(require("cli-ux"));
const validate_1 = require("./validate");
function filter(obj) {
    const ret = {};
    Object.keys(obj)
        .filter((key) => obj[key] !== undefined)
        .forEach((key) => {
        ret[key] = obj[key];
    });
    return ret;
}
async function getNameAndRepo(args) {
    const answer = {
        name: '',
        repo: '',
    };
    if (!args.name) {
        const name = await cli_ux_1.default.prompt('Pipeline name', {
            required: true,
        });
        const [valid, msg] = validate_1.pipelineName(name);
        if (valid) {
            answer.name = name;
        }
        else {
            cli_ux_1.default.error(msg);
        }
    }
    if (!args.repo) {
        const repo = await cli_ux_1.default.prompt('GitHub repository to connect to (e.g. rails/rails)', {
            required: true,
        });
        const [valid, msg] = validate_1.repoName(repo);
        if (valid) {
            answer.repo = repo;
        }
        else {
            cli_ux_1.default.error(msg);
        }
    }
    const reply = Object.assign(filter(answer), filter(args));
    reply.name = reply.name.toLowerCase().replace(/\s/g, '-');
    return reply;
}
exports.default = getNameAndRepo;
