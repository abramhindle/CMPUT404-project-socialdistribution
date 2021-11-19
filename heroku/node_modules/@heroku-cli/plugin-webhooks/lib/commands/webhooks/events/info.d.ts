import { flags } from '@heroku-cli/command';
import BaseCommand from '../../../base';
export default class Info extends BaseCommand {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        pipeline: flags.IOptionFlag<string | undefined>;
    };
    static args: {
        name: string;
        required: boolean;
    }[];
    run(): Promise<void>;
}
