import { Command, flags as Flags } from '@heroku-cli/command';
export default class Remove extends Command {
    static description: string;
    static flags: {
        app: Flags.IOptionFlag<string>;
        remote: Flags.IOptionFlag<string | undefined>;
        index: import("@oclif/parser/lib/flags").IOptionFlag<number | undefined>;
    };
    static args: {
        name: string;
        description: string;
    }[];
    run(): Promise<void>;
}
