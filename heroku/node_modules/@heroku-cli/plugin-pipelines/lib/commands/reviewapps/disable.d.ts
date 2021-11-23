import { Command, flags } from '@heroku-cli/command';
export default class ReviewappsDisable extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string | undefined>;
        remote: flags.IOptionFlag<string | undefined>;
        pipeline: flags.IOptionFlag<string>;
        autodeploy: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        autodestroy: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'wait-for-ci': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'no-autodeploy': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'no-autodestroy': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'no-wait-for-ci': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
