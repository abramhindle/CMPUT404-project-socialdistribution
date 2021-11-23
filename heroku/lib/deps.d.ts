import { HTTP } from 'http-call';
import UserConfig from './user-config';
import FS = require('fs-extra');
import file = require('./file');
declare const _default: {
    readonly fs: typeof FS;
    readonly HTTP: typeof HTTP;
    readonly file: typeof file;
    readonly UserConfig: typeof UserConfig;
};
export default _default;
