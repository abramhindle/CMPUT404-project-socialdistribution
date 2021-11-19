import { Command, flags } from '@heroku-cli/command';
export default class Setup extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        team: flags.IOptionFlag<string | undefined>;
        yes: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    static args: {
        name: string;
        description: string;
        required: boolean;
    }[];
    run(): Promise<void>;
}
