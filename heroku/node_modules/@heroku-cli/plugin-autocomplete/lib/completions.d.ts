import { flags } from '@heroku-cli/command';
import * as Config from '@oclif/config';
export declare const oneDay: number;
export declare const herokuGet: (resource: string, ctx: {
    config: Config.IConfig;
}) => Promise<string[]>;
export declare const AppCompletion: flags.ICompletion;
export declare const AppAddonCompletion: flags.ICompletion;
export declare const AppDynoCompletion: flags.ICompletion;
export declare const BuildpackCompletion: flags.ICompletion;
export declare const DynoSizeCompletion: flags.ICompletion;
export declare const FileCompletion: flags.ICompletion;
export declare const PipelineCompletion: flags.ICompletion;
export declare const ProcessTypeCompletion: flags.ICompletion;
export declare const RegionCompletion: flags.ICompletion;
export declare const RemoteCompletion: flags.ICompletion;
export declare const RoleCompletion: flags.ICompletion;
export declare const ScopeCompletion: flags.ICompletion;
export declare const SpaceCompletion: flags.ICompletion;
export declare const StackCompletion: flags.ICompletion;
export declare const StageCompletion: flags.ICompletion;
export declare const TeamCompletion: flags.ICompletion;
export declare const CompletionMapping: {
    [key: string]: flags.ICompletion;
};
export declare class CompletionLookup {
    private readonly cmdId;
    private readonly name;
    private readonly description?;
    private get key();
    private readonly blocklistMap;
    private readonly keyAliasMap;
    private readonly commandArgsMap;
    constructor(cmdId: string, name: string, description?: string | undefined);
    run(): flags.ICompletion | undefined;
    private argAlias;
    private keyAlias;
    private descriptionAlias;
    private blocklisted;
}
