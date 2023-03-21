"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");
Object.defineProperty(exports, "__esModule", {
  value: true
});
var _exportNames = {
  snackbarUnstyledClasses: true
};
Object.defineProperty(exports, "default", {
  enumerable: true,
  get: function () {
    return _SnackbarUnstyled.default;
  }
});
Object.defineProperty(exports, "snackbarUnstyledClasses", {
  enumerable: true,
  get: function () {
    return _snackbarUnstyledClasses.default;
  }
});
var _SnackbarUnstyled = _interopRequireDefault(require("./SnackbarUnstyled"));
var _SnackbarUnstyled2 = require("./SnackbarUnstyled.types");
Object.keys(_SnackbarUnstyled2).forEach(function (key) {
  if (key === "default" || key === "__esModule") return;
  if (Object.prototype.hasOwnProperty.call(_exportNames, key)) return;
  if (key in exports && exports[key] === _SnackbarUnstyled2[key]) return;
  Object.defineProperty(exports, key, {
    enumerable: true,
    get: function () {
      return _SnackbarUnstyled2[key];
    }
  });
});
var _snackbarUnstyledClasses = _interopRequireWildcard(require("./snackbarUnstyledClasses"));
Object.keys(_snackbarUnstyledClasses).forEach(function (key) {
  if (key === "default" || key === "__esModule") return;
  if (Object.prototype.hasOwnProperty.call(_exportNames, key)) return;
  if (key in exports && exports[key] === _snackbarUnstyledClasses[key]) return;
  Object.defineProperty(exports, key, {
    enumerable: true,
    get: function () {
      return _snackbarUnstyledClasses[key];
    }
  });
});
function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }
function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }