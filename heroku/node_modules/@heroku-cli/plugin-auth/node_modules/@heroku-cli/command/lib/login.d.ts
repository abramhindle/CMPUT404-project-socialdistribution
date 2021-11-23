import * as Config from '@oclif/config';
import { APIClient } from './api-client';
export declare namespace Login {
    interface Options {
        expiresIn?: number;
        method?: 'interactive' | 'sso' | 'browser';
        browser?: string;
    }
}
export declare class Login {
    private readonly config;
    private readonly heroku;
    loginHost: string;
    constructor(config: Config.IConfig, heroku: APIClient);
    login(opts?: Login.Options): Promise<void>;
    logout(token?: string | undefined): Promise<any>;
    private browser;
    private interactive;
    private createOAuthToken;
    private saveToken;
    private defaultToken;
    private sso;
}
