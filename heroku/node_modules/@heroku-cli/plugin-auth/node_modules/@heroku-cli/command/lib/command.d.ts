import { Command as Base } from '@oclif/command';
import { APIClient } from './api-client';
export declare abstract class Command extends Base {
    base: string;
    _heroku: APIClient;
    _legacyHerokuClient: any;
    get heroku(): APIClient;
    get legacyHerokuClient(): any;
    get cli(): any;
    get out(): any;
}
