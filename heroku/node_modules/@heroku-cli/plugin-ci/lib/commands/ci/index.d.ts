import { Command, flags } from '@heroku-cli/command';
export default class CiIndex extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        watch: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        pipeline: flags.IOptionFlag<string | undefined>;
        json: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
