import { Command, flags } from '@heroku-cli/command';
export default class Login extends Command {
    static description: string;
    static aliases: string[];
    static flags: {
        browser: flags.IOptionFlag<string | undefined>;
        sso: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        interactive: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'expires-in': import("@oclif/parser/lib/flags").IOptionFlag<number | undefined>;
    };
    run(): Promise<void>;
}
