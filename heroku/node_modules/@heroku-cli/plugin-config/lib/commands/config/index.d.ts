import { Command, flags } from '@heroku-cli/command';
export declare class ConfigIndex extends Command {
    static description: string;
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        shell: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        json: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
