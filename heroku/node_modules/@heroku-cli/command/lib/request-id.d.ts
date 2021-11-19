export declare const requestIdHeader = "Request-Id";
export declare class RequestId {
    static ids: string[];
    static track(...ids: string[]): string[];
    static create(): string[];
    static empty(): void;
    static get headerValue(): string;
    static _generate(): string;
}
