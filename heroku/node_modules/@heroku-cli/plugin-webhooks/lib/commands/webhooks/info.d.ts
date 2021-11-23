import { flags } from '@heroku-cli/command';
import BaseCommand from '../../base';
export default class WebhooksInfo extends BaseCommand {
    static description: string;
    static example: string[];
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
