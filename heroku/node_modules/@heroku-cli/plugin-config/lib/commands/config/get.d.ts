import { Command, flags } from '@heroku-cli/command';
export declare class ConfigGet extends Command {
    static usage: string;
    static description: string;
    static example: string;
    static strict: boolean;
    static args: {
        name: string;
        required: boolean;
    }[];
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        shell: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
