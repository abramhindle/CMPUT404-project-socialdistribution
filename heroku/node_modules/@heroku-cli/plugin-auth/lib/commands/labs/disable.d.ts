import { Command, flags } from '@heroku-cli/command';
export default class LabsDisable extends Command {
    static description: string;
    static args: {
        name: string;
    }[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        confirm: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
    disableFeature(feature: string, app?: string): Promise<any>;
}
