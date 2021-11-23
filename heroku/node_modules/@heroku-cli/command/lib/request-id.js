"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const uuid = tslib_1.__importStar(require("uuid"));
exports.requestIdHeader = 'Request-Id';
// tslint:disable-next-line: no-unnecessary-class
class RequestId {
    static track(...ids) {
        const tracked = RequestId.ids;
        ids = ids.filter(id => !(tracked.includes(id)));
        RequestId.ids = [...ids, ...tracked];
        return RequestId.ids;
    }
    static create() {
        const tracked = RequestId.ids;
        const generatedId = RequestId._generate();
        RequestId.ids = [generatedId, ...tracked];
        return RequestId.ids;
    }
    static empty() {
        RequestId.ids = [];
    }
    static get headerValue() {
        return RequestId.ids.join(',');
    }
    static _generate() {
        return uuid.v4();
    }
}
exports.RequestId = RequestId;
RequestId.ids = [];
