import { Command, flags as Flags } from '@heroku-cli/command';
export default class Clear extends Command {
    static description: string;
    static flags: {
        app: Flags.IOptionFlag<string>;
        remote: Flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
