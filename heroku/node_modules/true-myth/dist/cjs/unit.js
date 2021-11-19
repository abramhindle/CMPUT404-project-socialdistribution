"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("./utils");
/**
  The `Unit` type exists for the cases where you want a type-safe equivalent of
  `undefined` or `null`. It's a concrete instance, which won't blow up on you,
  and you can safely use it with e.g. [`Result`](../modules/_result_.html)
  without being concerned that you'll accidentally introduce `null` or
  `undefined` back into your application.
 */
exports.Unit = new utils_1._Brand('unit');
exports.default = exports.Unit;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidW5pdC5qcyIsInNvdXJjZVJvb3QiOiIuLyIsInNvdXJjZXMiOlsidW5pdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUFBLG1DQUFpQztBQUVqQzs7Ozs7O0dBTUc7QUFDVSxRQUFBLElBQUksR0FBRyxJQUFJLGNBQU0sQ0FBQyxNQUFNLENBQUMsQ0FBQztBQUV2QyxrQkFBZSxZQUFJLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBfQnJhbmQgfSBmcm9tICcuL3V0aWxzJztcblxuLyoqXG4gIFRoZSBgVW5pdGAgdHlwZSBleGlzdHMgZm9yIHRoZSBjYXNlcyB3aGVyZSB5b3Ugd2FudCBhIHR5cGUtc2FmZSBlcXVpdmFsZW50IG9mXG4gIGB1bmRlZmluZWRgIG9yIGBudWxsYC4gSXQncyBhIGNvbmNyZXRlIGluc3RhbmNlLCB3aGljaCB3b24ndCBibG93IHVwIG9uIHlvdSxcbiAgYW5kIHlvdSBjYW4gc2FmZWx5IHVzZSBpdCB3aXRoIGUuZy4gW2BSZXN1bHRgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwpXG4gIHdpdGhvdXQgYmVpbmcgY29uY2VybmVkIHRoYXQgeW91J2xsIGFjY2lkZW50YWxseSBpbnRyb2R1Y2UgYG51bGxgIG9yXG4gIGB1bmRlZmluZWRgIGJhY2sgaW50byB5b3VyIGFwcGxpY2F0aW9uLlxuICovXG5leHBvcnQgY29uc3QgVW5pdCA9IG5ldyBfQnJhbmQoJ3VuaXQnKTtcbmV4cG9ydCB0eXBlIFVuaXQgPSB0eXBlb2YgVW5pdDtcbmV4cG9ydCBkZWZhdWx0IFVuaXQ7XG4iXX0=