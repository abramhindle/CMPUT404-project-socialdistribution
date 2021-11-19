import { Command, flags } from '@heroku-cli/command';
export declare const sleep: (time: number) => Promise<unknown>;
export default class Promote extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
        to: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
