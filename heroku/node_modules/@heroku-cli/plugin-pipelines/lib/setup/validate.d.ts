export declare const STAGING_APP_INDICATOR = "-staging";
export declare function pipelineName(name: any): ValidatedResponse;
export declare function repoName(repo: any): ValidatedResponse;
export declare function nameAndRepo({ name, repo }: {
    name?: string;
    repo?: string;
}): (string | undefined)[];
declare type ValidatedResponse = [true] | [false, string];
export {};
