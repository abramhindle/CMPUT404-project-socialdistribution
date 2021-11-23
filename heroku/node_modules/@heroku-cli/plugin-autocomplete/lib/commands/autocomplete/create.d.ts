import { AutocompleteBase } from '../../base';
export default class Create extends AutocompleteBase {
    static hidden: boolean;
    static description: string;
    private _commands?;
    run(): Promise<void>;
    private ensureDirs;
    private createFiles;
    private get bashSetupScriptPath();
    private get bashCommandsListPath();
    private get zshSetupScriptPath();
    private get zshCompletionSettersPath();
    private get skipEllipsis();
    private get commands();
    private get bashCommandsList();
    private get zshCompletionSetters();
    private get zshCommandsSetter();
    private get zshCommandsFlagsSetters();
    private genCmdPublicFlags;
    private genCmdWithDescription;
    private genZshCmdFlagsSetter;
    private genZshAllCmdsListSetter;
    private get envAnalyticsDir();
    private get envCommandsPath();
    private get bashSetupScript();
    private get zshSetupScript();
    private get completionDotsFunc();
    private wantsLocalFiles;
}
