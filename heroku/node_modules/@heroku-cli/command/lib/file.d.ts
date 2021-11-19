/// <reference types="node" />
export declare function exists(f: string): Promise<boolean>;
export declare function readdir(f: string): Promise<string[]>;
export declare function readFile(f: string): Promise<Buffer>;
