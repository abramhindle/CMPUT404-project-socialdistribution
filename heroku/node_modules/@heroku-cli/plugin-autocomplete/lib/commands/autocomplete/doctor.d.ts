import { AutocompleteBase } from '../../base';
export default class Doctor extends AutocompleteBase {
    static hidden: boolean;
    static description: string;
    static args: {
        name: string;
        description: string;
        required: boolean;
    }[];
    static flags: {
        verbose: import("@oclif/parser/lib/flags").IBooleanFlag<boolean>;
    };
    run(): Promise<void>;
    private printList;
}
