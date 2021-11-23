import { Command, flags } from '@heroku-cli/command';
export default class Enable extends Command {
    static description: string;
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        min: import("@oclif/parser/lib/flags").IOptionFlag<number>;
        max: import("@oclif/parser/lib/flags").IOptionFlag<number>;
        p95: import("@oclif/parser/lib/flags").IOptionFlag<number | undefined>;
        notifications: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
