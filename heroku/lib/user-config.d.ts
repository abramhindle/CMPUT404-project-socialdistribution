import * as Config from '@oclif/config';
export interface ConfigJSON {
    schema: 1;
    install?: string;
    skipAnalytics?: boolean;
}
export default class UserConfig {
    private readonly config;
    private needsSave;
    private body;
    private mtime?;
    private saving?;
    private _init;
    constructor(config: Config.IConfig);
    get install(): string;
    set install(install: string);
    get skipAnalytics(): boolean;
    init(): Promise<void>;
    private get debug();
    private get file();
    private save;
    private read;
    private migrate;
    private canWrite;
    private getLastUpdated;
    private genInstall;
}
