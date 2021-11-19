import { Command, flags } from '@heroku-cli/command';
export default class CiRun extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        pipeline: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
