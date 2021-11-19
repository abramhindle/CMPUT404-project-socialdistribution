import { Command, flags } from '@heroku-cli/command';
export default class Wait extends Command {
    static description: string;
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        type: flags.IOptionFlag<string | undefined>;
        'wait-interval': import("@oclif/parser/lib/flags").IOptionFlag<number>;
        'with-run': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
