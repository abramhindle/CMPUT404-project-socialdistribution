export declare type PromiseResolve<T> = (value: T | PromiseLike<T> | undefined) => void;
export declare type PromiseReject = (reason?: any) => void;
export declare type Task<T> = () => Promise<T>;
export declare type Record<T> = [Task<T>, PromiseResolve<T>, PromiseReject];
export declare class Mutex<T> {
    private busy;
    private readonly queue;
    synchronize(task: Task<T>): Promise<T>;
    dequeue(): Promise<void> | undefined;
    execute(record: Record<T>): Promise<void>;
}
