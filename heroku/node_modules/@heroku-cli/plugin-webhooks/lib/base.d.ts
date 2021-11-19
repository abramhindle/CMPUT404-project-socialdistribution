import { APIClient, Command } from '@heroku-cli/command';
import { IConfig } from '@oclif/config';
export default abstract class extends Command {
    webhooksClient: APIClient;
    protected constructor(argv: string[], config: IConfig);
    webhookType(context: {
        pipeline?: string;
        app?: string;
    }): {
        path: string;
        display: string;
    };
}
