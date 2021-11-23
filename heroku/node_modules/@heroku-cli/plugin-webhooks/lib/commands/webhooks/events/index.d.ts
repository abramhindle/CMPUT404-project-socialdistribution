import { flags } from '@heroku-cli/command';
import BaseCommand from '../../../base';
export default class EventsIndex extends BaseCommand {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        pipeline: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
