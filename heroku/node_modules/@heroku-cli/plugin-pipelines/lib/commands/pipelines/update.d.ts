import { Command, flags } from '@heroku-cli/command';
export default class PipelinesUpdate extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        stage: flags.IOptionFlag<string>;
    };
    run(): Promise<void>;
}
