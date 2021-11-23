import { Command, flags } from '@heroku-cli/command';
export default class Connect extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        repo: flags.IOptionFlag<string>;
    };
    static args: {
        name: string;
        description: string;
        required: boolean;
    }[];
    run(): Promise<void>;
}
