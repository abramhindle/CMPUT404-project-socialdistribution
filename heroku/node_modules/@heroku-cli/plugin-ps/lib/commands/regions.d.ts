import { Command } from '@heroku-cli/command';
export default class Regions extends Command {
    static topic: string;
    static description: string;
    static flags: {
        json: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        private: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        common: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
