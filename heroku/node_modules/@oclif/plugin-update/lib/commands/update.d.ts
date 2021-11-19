import Command from '@oclif/command';
export default class UpdateCommand extends Command {
    static description: string;
    static args: {
        name: string;
        optional: boolean;
    }[];
    static flags: {
        autoupdate: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    private autoupdate;
    private channel;
    private readonly clientRoot;
    private readonly clientBin;
    run(): Promise<void>;
    private fetchManifest;
    private update;
    private skipUpdate;
    private logChop;
    private mtime;
    private debounce;
    private tidy;
    private touch;
    private reexec;
    private createBin;
    private ensureClientDir;
}
