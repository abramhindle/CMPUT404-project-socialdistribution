import { flags } from '@heroku-cli/command';
import BaseCommand from '../../base';
export default class WebhooksUpdate extends BaseCommand {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        pipeline: flags.IOptionFlag<string | undefined>;
        include: flags.IOptionFlag<string>;
        level: flags.IOptionFlag<string>;
        secret: flags.IOptionFlag<string | undefined>;
        authorization: flags.IOptionFlag<string | undefined>;
        url: flags.IOptionFlag<string>;
    };
    static args: {
        name: string;
        required: boolean;
    }[];
    run(): Promise<void>;
}
