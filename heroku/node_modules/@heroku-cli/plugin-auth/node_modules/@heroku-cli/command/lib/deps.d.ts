/// <reference types="node" />
import CLI = require('cli-ux');
import HTTP = require('http-call');
import netrc = require('netrc-parser');
import apiClient = require('./api-client');
import file = require('./file');
import flags = require('./flags');
import git = require('./git');
import mutex = require('./mutex');
export declare const deps: {
    readonly cli: {
        config: CLI.Config;
        warn: typeof import("@oclif/errors").warn;
        error: typeof import("@oclif/errors").error;
        exit: typeof import("@oclif/errors").exit;
        readonly prompt: typeof import("cli-ux/lib/prompt").prompt;
        readonly anykey: typeof import("cli-ux/lib/prompt").anykey;
        readonly confirm: typeof import("cli-ux/lib/prompt").confirm;
        readonly action: CLI.ActionBase;
        styledObject(obj: any, keys?: string[] | undefined): void;
        readonly styledHeader: typeof import("cli-ux/lib/styled/header").default;
        readonly styledJSON: typeof import("cli-ux/lib/styled/json").default;
        readonly table: typeof CLI.Table.default;
        readonly tree: typeof import("cli-ux/lib/styled/tree").default;
        readonly open: typeof import("cli-ux/lib/open").default;
        readonly wait: (ms?: number | undefined) => Promise<{}>;
        done(): Promise<void>;
        trace(format: string, ...args: string[]): void;
        debug(format: string, ...args: string[]): void;
        info(format: string, ...args: string[]): void;
        log(format?: string | undefined, ...args: string[]): void;
        url(text: string, uri: string, params?: {} | undefined): void;
        annotation(text: string, annotation: string): void;
        flush(): Promise<void>;
    };
    readonly HTTP: typeof HTTP;
    readonly netrc: netrc.Netrc;
    readonly Mutex: typeof mutex.Mutex;
    readonly yubikey: {
        disable: () => void;
        enable: () => void;
        platform: NodeJS.Platform;
    };
    readonly APIClient: typeof apiClient.APIClient;
    readonly file: typeof file;
    readonly flags: typeof flags;
    readonly Git: typeof git.Git;
};
export default deps;
