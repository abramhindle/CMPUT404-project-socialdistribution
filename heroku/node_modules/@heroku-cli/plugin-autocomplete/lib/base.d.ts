import Command, { flags } from '@heroku-cli/command';
export declare abstract class AutocompleteBase extends Command {
    errorIfWindows(): void;
    errorIfNotSupportedShell(shell: string): void;
    get autocompleteCacheDir(): string;
    get completionsCacheDir(): string;
    get acLogfilePath(): string;
    writeLogFile(msg: string): void;
    protected findCompletion(cmdId: string, name: string, description?: string): flags.ICompletion | undefined;
}
