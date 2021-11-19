export interface IGitRemote {
    name: string;
    url: string;
}
export declare class Git {
    get remotes(): IGitRemote[];
    exec(cmd: string): string;
}
export declare function configRemote(): string | undefined;
export interface IGitRemotes {
    remote: string;
    app: string;
}
export declare function getGitRemotes(onlyRemote: string | undefined): IGitRemotes[];
