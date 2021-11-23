/// <reference types="node" />
import * as FS from 'fs-extra';
export declare function exists(f: string): Promise<boolean>;
export declare function stat(file: string): Promise<FS.Stats>;
export declare function rename(from: string, to: string): Promise<void>;
export declare function remove(file: string): Promise<void>;
export declare function ls(dir: string): Promise<{
    path: string;
    stat: FS.Stats;
}[]>;
export declare function removeEmptyDirs(dir: string): Promise<void>;
export declare function readJSON(file: string): Promise<any>;
export declare function outputJSON(file: string, data: any, options?: FS.WriteOptions): Promise<void>;
export declare function realpathSync(p: string): string;
