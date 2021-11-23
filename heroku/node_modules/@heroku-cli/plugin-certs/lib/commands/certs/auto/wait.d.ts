import { Command } from '@oclif/command';
export default class CertsAutoWait extends Command {
    static description: string;
    static hidden: boolean;
    static flags: {
        help: import("@oclif/parser/lib/flags").IBooleanFlag<void>;
    };
    run(): Promise<void>;
}
