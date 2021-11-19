import { Command, flags } from '@heroku-cli/command';
export declare class ConfigUnset extends Command {
    static aliases: string[];
    static description: string;
    static examples: string[];
    static strict: boolean;
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
