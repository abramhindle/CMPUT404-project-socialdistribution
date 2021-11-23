export default class Git {
    exec(args: string[]): Promise<string>;
    spawn(args: string[]): Promise<unknown>;
    remoteFromGitConfig(): Promise<string | void>;
    sshGitUrl(app: string): string;
    httpGitUrl(app: string): string;
    remoteUrl(name: string): Promise<string>;
    url(app: string, ssh: boolean): string;
}
