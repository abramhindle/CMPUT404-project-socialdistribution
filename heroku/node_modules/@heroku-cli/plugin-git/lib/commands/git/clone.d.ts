import { Command, flags } from '@heroku-cli/command';
export declare class GitClone extends Command {
    static description: string;
    static example: string;
    static args: {
        name: string;
        optional: boolean;
        description: string;
    }[];
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        'ssh-git': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
