"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Mutex {
    constructor() {
        this.busy = false;
        this.queue = [];
    }
    synchronize(task) {
        return new Promise((resolve, reject) => {
            this.queue.push([task, resolve, reject]);
            if (!this.busy) {
                this.dequeue();
            }
        });
    }
    dequeue() {
        this.busy = true;
        let next = this.queue.shift();
        if (next) {
            return this.execute(next);
        }
        else {
            this.busy = false;
        }
    }
    execute(record) {
        let [task, resolve, reject] = record;
        return task()
            .then(resolve, reject)
            .then(() => {
            this.dequeue();
        });
    }
}
exports.Mutex = Mutex;
