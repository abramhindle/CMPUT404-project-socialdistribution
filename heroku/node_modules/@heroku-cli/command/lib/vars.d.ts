export declare class Vars {
    get host(): string;
    get apiUrl(): string;
    get apiHost(): string;
    get envHost(): string | undefined;
    get envGitHost(): string | undefined;
    get gitHost(): string;
    get httpGitHost(): string;
    get gitPrefixes(): string[];
}
export declare const vars: Vars;
