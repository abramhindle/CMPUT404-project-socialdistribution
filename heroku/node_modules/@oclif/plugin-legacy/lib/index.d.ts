import * as Config from '@oclif/config';
export declare class PluginLegacy extends Config.Plugin implements Config.IPlugin {
    config: Config.IConfig;
    base: Config.IPlugin;
    _base: string;
    protected _moduleCommands?: Config.Command.Class[];
    protected _moduleTopics?: Config.Topic[];
    constructor(config: Config.IConfig, base: Config.IPlugin);
    get topics(): Config.Topic[];
    get commandIDs(): string[];
    findCommand(id: string, opts: {
        must: true;
    }): Config.Command.Class;
    findCommand(id: string, opts?: {
        must?: boolean;
    }): Config.Command.Class | undefined;
    protected get moduleCommands(): Config.Command.Class[];
    protected get moduleTopics(): Config.Topic[];
    private convertCommand;
    private convertFromICommand;
    private convertFromFlow;
    private convertFromV5;
    private isICommand;
    private isV5Command;
    private isFlowCommand;
}
