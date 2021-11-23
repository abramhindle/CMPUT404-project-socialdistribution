"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deps = {
    // remote
    get cli() { return fetch('cli-ux').default; },
    get HTTP() { return fetch('http-call'); },
    get netrc() { return fetch('netrc-parser').default; },
    // local
    get Mutex() { return fetch('./mutex').Mutex; },
    get yubikey() { return fetch('./yubikey').yubikey; },
    get APIClient() { return fetch('./api-client').APIClient; },
    get file() { return fetch('./file'); },
    get flags() { return fetch('./flags'); },
    get Git() { return fetch('./git').Git; },
};
const cache = {};
function fetch(s) {
    if (!cache[s]) {
        cache[s] = require(s);
    }
    return cache[s];
}
exports.default = exports.deps;
