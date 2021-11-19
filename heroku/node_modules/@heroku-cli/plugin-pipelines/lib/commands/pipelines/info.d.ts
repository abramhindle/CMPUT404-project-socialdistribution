import { Command } from '@heroku-cli/command';
export default class PipelinesInfo extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        json: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        'with-owners': import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    static args: {
        name: string;
        description: string;
        required: boolean;
    }[];
    run(): Promise<void>;
}
