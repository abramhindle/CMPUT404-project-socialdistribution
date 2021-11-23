import { Command, flags } from '@heroku-cli/command';
export default class PipelinesTransfer extends Command {
    static description: string;
    static examples: string[];
    static args: {
        name: string;
        description: string;
        required: boolean;
    }[];
    static flags: {
        pipeline: flags.IOptionFlag<string>;
        confirm: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
