import * as Config from '@oclif/config';
import { CLIError } from '@oclif/errors';
import { HTTP, HTTPError, HTTPRequestOptions } from 'http-call';
import { Login } from './login';
import { Mutex } from './mutex';
export declare namespace APIClient {
    interface Options extends HTTPRequestOptions {
        retryAuth?: boolean;
    }
}
export interface IOptions {
    required?: boolean;
    preauth?: boolean;
}
export interface IHerokuAPIErrorOptions {
    resource?: string;
    app?: {
        id: string;
        name: string;
    };
    id?: string;
    message?: string;
    url?: string;
}
export declare class HerokuAPIError extends CLIError {
    http: HTTPError;
    body: IHerokuAPIErrorOptions;
    constructor(httpError: HTTPError);
}
export declare class APIClient {
    protected config: Config.IConfig;
    options: IOptions;
    preauthPromises: {
        [k: string]: Promise<HTTP<any>>;
    };
    authPromise?: Promise<HTTP<any>>;
    http: typeof HTTP;
    private readonly _login;
    private _twoFactorMutex;
    private _auth?;
    constructor(config: Config.IConfig, options?: IOptions);
    get twoFactorMutex(): Mutex<string>;
    get auth(): string | undefined;
    set auth(token: string | undefined);
    twoFactorPrompt(): Promise<string>;
    preauth(app: string, factor: string): Promise<HTTP<unknown>>;
    get<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    post<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    put<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    patch<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    delete<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    stream(url: string, options?: APIClient.Options): Promise<HTTP<unknown>>;
    request<T>(url: string, options?: APIClient.Options): Promise<HTTP<T>>;
    login(opts?: Login.Options): Promise<void>;
    logout(): Promise<void>;
    get defaults(): typeof HTTP.defaults;
}
