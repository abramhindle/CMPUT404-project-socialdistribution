import { Command } from '@heroku-cli/command';
export default class Status extends Command {
    static description: string;
    static flags: {
        json: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
