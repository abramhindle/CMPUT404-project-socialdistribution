import { Command, flags } from '@oclif/command';
export default class Run extends Command {
    static description: string;
    static examples: string[];
    static strict: boolean;
    static flags: {
        env: flags.IOptionFlag<string | undefined>;
        port: flags.IOptionFlag<string | undefined>;
    };
    run(): Promise<void>;
}
