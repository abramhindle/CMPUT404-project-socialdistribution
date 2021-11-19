import { Command, flags } from '@oclif/command';
export default class Index extends Command {
    static description: string;
    static aliases: string[];
    static args: {
        name: string;
        required: boolean;
    }[];
    static examples: string[];
    static flags: {
        procfile: flags.IOptionFlag<string | undefined>;
        env: flags.IOptionFlag<string | undefined>;
        port: flags.IOptionFlag<string | undefined>;
        restart: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
        concurrency: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
