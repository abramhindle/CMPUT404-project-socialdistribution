import { Command, flags } from '@heroku-cli/command';
export declare class GitRemote extends Command {
    static description: string;
    static example: string;
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        'ssh-git': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    static strict: boolean;
    run(): Promise<void>;
}
