import { Command, flags } from '@heroku-cli/command';
export default class Disable extends Command {
    static description: string;
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
