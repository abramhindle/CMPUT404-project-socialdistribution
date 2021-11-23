"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const path = tslib_1.__importStar(require("path"));
const deps_1 = tslib_1.__importDefault(require("./deps"));
const git_1 = require("./git");
exports.oneDay = 60 * 60 * 24;
exports.herokuGet = async (resource, ctx) => {
    const heroku = new deps_1.default.APIClient(ctx.config);
    let { body: resources } = await heroku.get(`/${resource}`);
    if (typeof resources === 'string')
        resources = JSON.parse(resources);
    return resources.map((a) => a.name).sort();
};
exports.AppCompletion = {
    cacheDuration: exports.oneDay,
    options: async (ctx) => {
        let apps = await exports.herokuGet('apps', ctx);
        return apps;
    },
};
exports.AppAddonCompletion = {
    cacheDuration: exports.oneDay,
    cacheKey: async (ctx) => {
        return ctx.flags && ctx.flags.app ? `${ctx.flags.app}_addons` : '';
    },
    options: async (ctx) => {
        let addons = ctx.flags && ctx.flags.app ? await exports.herokuGet(`apps/${ctx.flags.app}/addons`, ctx) : [];
        return addons;
    },
};
exports.AppDynoCompletion = {
    cacheDuration: exports.oneDay,
    cacheKey: async (ctx) => {
        return ctx.flags && ctx.flags.app ? `${ctx.flags.app}_dynos` : '';
    },
    options: async (ctx) => {
        let dynos = ctx.flags && ctx.flags.app ? await exports.herokuGet(`apps/${ctx.flags.app}/dynos`, ctx) : [];
        return dynos;
    },
};
exports.BuildpackCompletion = {
    skipCache: true,
    options: async () => {
        return [
            'heroku/ruby',
            'heroku/nodejs',
            'heroku/clojure',
            'heroku/python',
            'heroku/java',
            'heroku/gradle',
            'heroku/scala',
            'heroku/php',
            'heroku/go',
        ];
    },
};
exports.DynoSizeCompletion = {
    cacheDuration: exports.oneDay * 90,
    options: async (ctx) => {
        let sizes = await exports.herokuGet('dyno-sizes', ctx);
        return sizes;
    },
};
exports.FileCompletion = {
    skipCache: true,
    options: async () => {
        let files = await deps_1.default.file.readdir(process.cwd());
        return files;
    },
};
exports.PipelineCompletion = {
    cacheDuration: exports.oneDay,
    options: async (ctx) => {
        let pipelines = await exports.herokuGet('pipelines', ctx);
        return pipelines;
    },
};
exports.ProcessTypeCompletion = {
    skipCache: true,
    options: async () => {
        let types = [];
        let procfile = path.join(process.cwd(), 'Procfile');
        try {
            let buff = await deps_1.default.file.readFile(procfile);
            types = buff
                .toString()
                .split('\n')
                .map(s => {
                if (!s)
                    return false;
                let m = s.match(/^([A-Za-z0-9_-]+)/);
                return m ? m[0] : false;
            })
                .filter(t => t);
        }
        catch (err) {
            if (err.code !== 'ENOENT')
                throw err;
        }
        return types;
    },
};
exports.RegionCompletion = {
    cacheDuration: exports.oneDay * 7,
    options: async (ctx) => {
        let regions = await exports.herokuGet('regions', ctx);
        return regions;
    },
};
exports.RemoteCompletion = {
    skipCache: true,
    options: async () => {
        let remotes = git_1.getGitRemotes(git_1.configRemote());
        return remotes.map(r => r.remote);
    },
};
exports.RoleCompletion = {
    skipCache: true,
    options: async () => {
        return ['admin', 'collaborator', 'member', 'owner'];
    },
};
exports.ScopeCompletion = {
    skipCache: true,
    options: async () => {
        return ['global', 'identity', 'read', 'write', 'read-protected', 'write-protected'];
    },
};
exports.SpaceCompletion = {
    cacheDuration: exports.oneDay,
    options: async (ctx) => {
        let spaces = await exports.herokuGet('spaces', ctx);
        return spaces;
    },
};
exports.StackCompletion = {
    cacheDuration: exports.oneDay,
    options: async (ctx) => {
        let stacks = await exports.herokuGet('stacks', ctx);
        return stacks;
    },
};
exports.StageCompletion = {
    skipCache: true,
    options: async () => {
        return ['test', 'review', 'development', 'staging', 'production'];
    },
};
exports.TeamCompletion = {
    cacheDuration: exports.oneDay,
    options: async (ctx) => {
        let teams = await exports.herokuGet('teams', ctx);
        return teams;
    },
};
