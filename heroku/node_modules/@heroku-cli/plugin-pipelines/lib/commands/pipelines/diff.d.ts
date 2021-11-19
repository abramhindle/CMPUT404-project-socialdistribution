import { Command, flags } from '@heroku-cli/command';
import KolkrabbiAPI from '../../kolkrabbi-api';
interface AppInfo {
    name: string;
    repo?: string;
    hash?: string;
}
export default class PipelinesDiff extends Command {
    static description: string;
    static examples: string[];
    static flags: {
        app: flags.IOptionFlag<string>;
        remote: flags.IOptionFlag<string | undefined>;
    };
    kolkrabbi: KolkrabbiAPI;
    getAppInfo: (appName: string, appId: string) => Promise<AppInfo>;
    run(): Promise<undefined>;
}
export {};
