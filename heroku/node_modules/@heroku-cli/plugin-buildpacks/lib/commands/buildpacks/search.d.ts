import { Command, flags as Flags } from '@heroku-cli/command';
export default class Search extends Command {
    static description: string;
    static flags: {
        namespace: Flags.IOptionFlag<string | undefined>;
        name: Flags.IOptionFlag<string | undefined>;
        description: Flags.IOptionFlag<string | undefined>;
    };
    static args: {
        name: string;
        description: string;
    }[];
    run(): Promise<void>;
}
