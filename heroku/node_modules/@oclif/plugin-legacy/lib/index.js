"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Config = require("@oclif/config");
const path = require("path");
const util_1 = require("util");
const util_2 = require("./util");
const debug = require('debug')('@oclif/plugin-legacy');
const pjson = require('../package.json');
function convertFlagsFromV5(Flags, flags) {
    if (!flags)
        return {};
    if (!Array.isArray(flags))
        return flags;
    return flags.reduce((flags, flag) => {
        const opts = {
            char: flag.char,
            description: flag.description,
            hidden: flag.hidden,
            required: flag.required || flag.optional === false,
            parse: flag.parse,
            completion: flag.completion,
            default: flag.default,
        };
        for (const [k, v] of Object.entries(opts)) {
            if (v === undefined)
                delete opts[k];
        }
        if (!opts.parse)
            delete opts.parse;
        flags[flag.name] = flag.hasValue ? Flags.string(opts) : Flags.boolean(opts);
        return flags;
    }, {});
}
class PluginLegacy extends Config.Plugin {
    constructor(config, base) {
        super(base);
        this.config = config;
        this.base = base;
        this._base = `${pjson.name}@${pjson.version}`;
        debug('loading legacy plugin', base.root);
    }
    get topics() {
        return super.topics
            .concat(this.moduleTopics);
    }
    get commandIDs() {
        return super.commandIDs
            .concat(this.moduleCommands.map(c => c.id));
    }
    findCommand(id, opts = {}) {
        let cmd = super.findCommand(id);
        if (cmd)
            return this.convertCommand(cmd);
        cmd = this.moduleCommands.find(c => c.id === id);
        if (cmd) {
            cmd.plugin = this;
            return this.convertCommand(cmd);
        }
        if (opts.must)
            throw new Error(`command ${id} not found`);
    }
    get moduleCommands() {
        if (this._moduleCommands)
            return this._moduleCommands;
        const main = this.pjson.main;
        if (!main)
            return [];
        const module = require(path.join(this.root, main));
        if (!module.commands)
            return [];
        debug('loading module commands', this.root);
        this._moduleCommands = module.commands
            .map((c) => this.convertCommand(c));
        return this._moduleCommands;
    }
    get moduleTopics() {
        if (this.pjson.oclif.topics)
            return [];
        if (this._moduleTopics)
            return this._moduleTopics;
        const main = this.pjson.main;
        if (!main)
            return [];
        const module = require(path.join(this.root, main));
        if (!module.commands)
            return [];
        debug('loading module topics', this.root);
        this._moduleTopics = module.topics;
        return this._moduleTopics;
    }
    convertCommand(c) {
        if (this.isICommand(c))
            return this.convertFromICommand(c);
        if (this.isV5Command(c))
            return this.convertFromV5(c);
        if (this.isFlowCommand(c))
            return this.convertFromFlow(c);
        debug(c);
        throw new Error(`Invalid command: ${util_1.inspect(c)}`);
    }
    convertFromICommand(c) {
        if (!c.id)
            c.id = util_2.compact([c.topic, c.command]).join(':');
        return c;
    }
    convertFromFlow(c) {
        if (!c.id)
            c.id = util_2.compact([c.topic, c.command]).join(':');
        c._version = c._version || '0.0.0';
        return c;
    }
    convertFromV5(c) {
        const { Command, flags: Flags, vars } = require('@heroku-cli/command');
        class V5 extends Command {
            async run() {
                const color = require('@oclif/color').default;
                const { flags, argv, args } = this.parse(this.constructor);
                const ctx = {
                    version: this.config.userAgent,
                    supportsColor: color.enabled,
                    auth: {},
                    debug: Boolean(this.config.debug),
                    debugHeaders: this.config.debug > 1 || ['1', 'true'].includes(process.env.HEROKU_DEBUG_HEADERS),
                    flags,
                    args: c.variableArgs ? argv : args,
                    app: flags.app,
                    org: flags.org,
                    team: flags.team,
                    config: this.config,
                    apiUrl: vars.apiUrl,
                    herokuDir: this.config.cacheDir,
                    apiToken: this.heroku.auth,
                    apiHost: vars.apiHost,
                    gitHost: vars.gitHost,
                    httpGitHost: vars.httpGitHost,
                    cwd: process.cwd(),
                };
                ctx.auth.password = ctx.apiToken;
                const ansi = require('ansi-escapes');
                process.once('exit', () => {
                    if (process.stderr.isTTY) {
                        process.stderr.write(ansi.cursorShow);
                    }
                });
                return c.run(ctx);
            }
        }
        V5.id = util_2.compact([c.topic, c.command]).join(':');
        V5.description = [c.description, c.help].join('\n');
        V5.hidden = Boolean(c.hidden);
        V5.args = (c.args || []).map((a) => (Object.assign(Object.assign({}, a), { required: a.required !== false && !a.optional })));
        V5.flags = convertFlagsFromV5(Flags, c.flags);
        V5.strict = c.strict || !c.variableArgs;
        V5.help = c.help;
        V5.aliases = c.aliases || [];
        V5.usage = c.usage;
        V5.examples = c.examples || c.example;
        if (c.needsApp || c.wantsApp) {
            V5.flags.app = Flags.app({ required: Boolean(c.needsApp) });
            V5.flags.remote = Flags.remote();
        }
        if (c.needsOrg || c.wantsOrg) {
            const opts = { required: Boolean(c.needsOrg), hidden: false, description: 'team to use' };
            V5.flags.team = Flags.team(opts);
            V5.flags.org = Flags.team({ char: 'o', hidden: true });
        }
        return V5;
    }
    isICommand(c) {
        const semver = require('semver');
        if (!c._version)
            return false;
        return semver.gte(c._version, '11.0.0');
    }
    isV5Command(command) {
        const c = command;
        return Boolean(typeof c === 'object');
    }
    isFlowCommand(command) {
        const c = command;
        return typeof c === 'function';
        // if (c._version && deps.semver.lt(c._version, '11.0.0')) return true
    }
}
exports.PluginLegacy = PluginLegacy;
