"use strict";
/** [[include:doc/result.md]] */
Object.defineProperty(exports, "__esModule", { value: true });
/** (keep typedoc from getting confused by the import) */
const maybe_1 = require("./maybe");
const unit_1 = require("./unit");
const utils_1 = require("./utils");
// So that it doesn't appear unused but can be exported.
utils_1._Brand; // tslint:disable-line:no-unused-expression
/**
  Discriminant for `Ok` and `Err` variants of `Result` type.

  You can use the discriminant via the `variant` property of `Result` instances
  if you need to match explicitly on it.
 */
var Variant;
(function (Variant) {
    Variant["Ok"] = "Ok";
    Variant["Err"] = "Err";
})(Variant = exports.Variant || (exports.Variant = {}));
/**
  An `Ok` instance is the *successful* variant instance of the
  [`Result`](../modules/_result_.html#result) type, representing a successful
  outcome from an operation which may fail. For a full discussion, see [the
  module docs](../modules/_result_.html).

  @typeparam T The type wrapped in this `Ok` variant of `Result`.
  @typeparam E The type which would be wrapped in an `Err` variant of `Result`.
 */
class Ok {
    /**
      Create an instance of `Result.Ok` with `new`.
  
      Note: While you *may* create the `Result` type via normal
      JavaScript class construction, it is not recommended for the functional
      style for which the library is intended. Instead, use [`Result.ok`].
  
      [`Result.ok`]: ../modules/_result_.html#ok
  
      ```ts
      // Avoid:
      const aString = new Result.Ok('characters');
  
      // Prefer:
      const aString = Result.ok('characters);
      ```
  
      Note that you may explicitly pass `Unit` to the `Ok` constructor to create
      a `Result<Unit, E>`. However, you may *not* call the `Ok` constructor with
      `null` or `undefined` to get that result (the type system won't allow you to
      construct it that way). Instead, for convenience, you can simply call
      `Result.ok()`, which will construct the type correctly.
  
      @param value
      The value to wrap in a `Result.Ok`.
  
      Note: `null` and `undefined` are allowed by the type signature so that the
      constructor may `throw` on those rather than constructing a type like
      `Result<undefined>`.
  
      @throws If you pass `null`.
     */
    constructor(value) {
        /** `Ok` is always [`Variant.Ok`](../enums/_result_.variant#ok). */
        this.variant = Variant.Ok;
        if (utils_1.isVoid(value)) {
            throw new Error('Tried to construct `Ok` with `null` or `undefined`. Maybe you want `Maybe.Nothing`?');
        }
        this.value = value;
    }
    /**
      Unwrap the contained value. A convenience method for functional idioms.
  
      A common scenario where you might want to use this is in a pipeline of
      functions:
  
      ```ts
      import Result, { Ok } from 'true-myth/result';
  
      function getLengths(results: Array<Result<string, string>>): Array<number> {
        return results
          .filter(Result.isOk)
          .map(Ok.unwrap)
          .map(s => s.length);
      }
      ```
     */
    static unwrap(theOk) {
        return theOk.value;
    }
    /** Method variant for [`Result.isOk`](../modules/_result_.html#isok) */
    isOk() {
        return true;
    }
    /** Method variant for [`Result.isErr`](../modules/_result_.html#iserr) */
    isErr() {
        return false;
    }
    /** Method variant for [`Result.map`](../modules/_result_.html#map) */
    map(mapFn) {
        return map(mapFn, this);
    }
    /** Method variant for [`Result.mapOr`](../modules/_result_.html#mapor) */
    mapOr(orU, mapFn) {
        return mapOr(orU, mapFn, this);
    }
    /** Method variant for [`Result.mapOrElse`](../modules/_result_.html#maporelse) */
    mapOrElse(orElseFn, mapFn) {
        return mapOrElse(orElseFn, mapFn, this);
    }
    /** Method variant for [`Result.match`](../modules/_result_.html#match) */
    match(matcher) {
        return match(matcher, this);
    }
    /** Method variant for [`Result.mapErr`](../modules/_result_.html#maperr) */
    mapErr(mapErrFn) {
        return mapErr(mapErrFn, this);
    }
    /** Method variant for [`Result.or`](../modules/_result_.html#or) */
    or(orResult) {
        return or(orResult, this);
    }
    /** Method variant for [`Result.orElse`](../modules/_result_.html#orelse) */
    orElse(orElseFn) {
        return orElse(orElseFn, this);
    }
    /** Method variant for [`Result.and`](../modules/_result_.html#and) */
    and(mAnd) {
        return and(mAnd, this);
    }
    /** Method variant for [`Result.andThen`](../modules/_result_.html#andthen) */
    andThen(andThenFn) {
        return andThen(andThenFn, this);
    }
    /** Method variant for [`Result.chain`](../modules/_result_.html#chain) */
    chain(chainFn) {
        return exports.chain(chainFn, this);
    }
    /** Method variant for [`Result.flatMap`](../modules/_result_.html#flatmap) */
    flatMap(flatMapFn) {
        return exports.flatMap(flatMapFn, this);
    }
    /** Method variant for [`Result.unwrap`](../modules/_result_.html#unwrap) */
    unsafelyUnwrap() {
        return this.value;
    }
    /** Method variant for [`Result.unwrapErr`](../modules/_result_.html#unwraperr) */
    unsafelyUnwrapErr() {
        throw new Error('Tried to `unsafelyUnwrapErr` an `Ok`');
    }
    /** Method variant for [`Result.unwrapOr`](../modules/_result_.html#unwrapor) */
    unwrapOr(defaultValue) {
        return unwrapOr(defaultValue, this);
    }
    /** Method variant for [`Result.unwrapOrElse`](../modules/_result_.html#unwrapOrElse) */
    unwrapOrElse(elseFn) {
        return unwrapOrElse(elseFn, this);
    }
    /** Method variant for [`Result.toMaybe`](../modules/_result_.html#tomaybe) */
    toMaybe() {
        return toMaybe(this);
    }
    /** Method variant for [`Result.toString`](../modules/_result_.html#tostring) */
    toString() {
        return exports.toString(this);
    }
    /** Method variant for [`Result.equals`](../modules/_result_.html#equals) */
    equals(comparison) {
        return equals(comparison, this);
    }
    /** Method variant for [`Result.ap`](../modules/_result_.html#ap) */
    ap(r) {
        return ap(this, r);
    }
}
exports.Ok = Ok;
/**
  An `Err` instance is the *failure* variant instance of the
  [`Result`](../modules/_result_.html#result) type, representing a failure
  outcome from an operation which may fail. For a full discussion, see [the
  module docs](../modules/_result_.html).

  @typeparam T The type which would be wrapped in an `Ok` variant of `Result`.
  @typeparam E The type wrapped in this `Err` variant of `Result`.
  */
class Err {
    /**
      Create an instance of `Result.Err` with `new`.
  
      Note: While you *may* create the `Result` type via normal
      JavaScript class construction, it is not recommended for the functional
      style for which the library is intended. Instead, use [`Result.err`].
  
      [`Result.err`]: ../modules/_result_.html#err
  
      ```ts
      // Avoid:
      const anErr = new Result.Err('alas, failure');
  
      // Prefer:
      const anErr = Result.err('alas, failure');
      ```
  
      Note that you may explicitly pass `Unit` to the `Err` constructor to create
      a `Result<T, Unit>`. However, you may *not* call the `Err` constructor with
      `null` or `undefined` to get that result (the type system won't allow you to
      construct it that way). Instead, for convenience, you can simply call
      `Result.err()`, which will construct the type correctly.
  
      @param error
      The value to wrap in a `Result.Err`.
  
      `Note: null` and `undefined` are allowed by the type signature so that the
      constructor may `throw` on those rather than constructing a type like
      `Result<number, undefined>`.
  
      @throws If you pass `null` or `undefined`.
     */
    constructor(error) {
        /** `Err` is always [`Variant.Err`](../enums/_result_.variant#err). */
        this.variant = Variant.Err;
        if (utils_1.isVoid(error)) {
            throw new Error('Tried to construct `Err` with `null` or `undefined`. Maybe you want `Maybe.Nothing`?');
        }
        this.error = error;
    }
    /**
      Unwrap the contained error . A convenience method for functional idioms.
  
      A common scenario where you might want to use this is in a pipeline of
      functions:
  
      ```ts
      import Result, { Ok } from 'true-myth/result';
  
      function getMessages(results: Array<Result<string, Error>>): Array<number> {
        return maybeStrings
          .filter(Result.isErr)
          .map(Err.unwrapErr)
          .map(e => e.message);
      }
      ```
     */
    static unwrapErr(theErr) {
        return theErr.error;
    }
    /** Method variant for [`Result.isOk`](../modules/_result_.html#isok) */
    isOk() {
        return false;
    }
    /** Method variant for [`Result.isErr`](../modules/_result_.html#iserr) */
    isErr() {
        return true;
    }
    /** Method variant for [`Result.map`](../modules/_result_.html#map) */
    map(mapFn) {
        return map(mapFn, this);
    }
    /** Method variant for [`Result.mapOr`](../modules/_result_.html#mapor) */
    mapOr(orU, mapFn) {
        return mapOr(orU, mapFn, this);
    }
    /** Method variant for [`Result.mapOrElse`](../modules/_result_.html#maporelse) */
    mapOrElse(orElseFn, mapFn) {
        return mapOrElse(orElseFn, mapFn, this);
    }
    /** Method variant for [`Result.match`](../modules/_result_.html#match) */
    match(matchObj) {
        return match(matchObj, this);
    }
    /** Method variant for [`Result.mapErr`](../modules/_result_.html#maperr) */
    mapErr(mapErrFn) {
        return mapErr(mapErrFn, this);
    }
    /** Method variant for [`Result.or`](../modules/_result_.html#or) */
    or(orResult) {
        return or(orResult, this);
    }
    /** Method variant for [`Result.orElse`](../modules/_result_.html#orelse) */
    orElse(orElseFn) {
        return orElse(orElseFn, this);
    }
    /** Method variant for [`Result.and`](../modules/_result_.html#and) */
    and(mAnd) {
        return and(mAnd, this);
    }
    /** Method variant for [`Result.andThen`](../modules/_result_.html#andthen) */
    andThen(andThenFn) {
        return andThen(andThenFn, this);
    }
    /** Method variant for [`Result.chain`](../modules/_result_.html#chain) */
    chain(chainFn) {
        return this.andThen(chainFn);
    }
    /** Method variant for [`Result.flatMap`](../modules/_result_.html#flatmap) */
    flatMap(flatMapFn) {
        return this.andThen(flatMapFn);
    }
    /** Method variant for [`Result.unsafelyUnwrap`](../modules/_result_.html#unsafelyunwrap) */
    unsafelyUnwrap() {
        throw new Error('Tried to `unsafelyUnwrap an Err`');
    }
    /** Method variant for [`Result.unsafelyUnwrapErr`](../modules/_result_.html#unsafelyunwraperr) */
    unsafelyUnwrapErr() {
        return this.error;
    }
    /** Method variant for [`Result.unwrapOr`](../modules/_result_.html#unwrapor) */
    unwrapOr(defaultValue) {
        return unwrapOr(defaultValue, this);
    }
    /** Method variant for [`Result.unwrapOrElse`](../modules/_result_.html#unwraporelse) */
    unwrapOrElse(elseFn) {
        return unwrapOrElse(elseFn, this);
    }
    /** Method variant for [`Result.toMaybe`](../modules/_result_.html#tomaybe) */
    toMaybe() {
        return toMaybe(this);
    }
    /** Method variant for [`Result.toString`](../modules/_result_.html#tostring) */
    toString() {
        return exports.toString(this);
    }
    /** Method variant for [`Result.equals`](../modules/_result_.html#equals) */
    equals(comparison) {
        return equals(comparison, this);
    }
    /** Method variant for [`Result.ap`](../modules/_result_.html#ap) */
    ap(r) {
        return ap(this, r);
    }
}
exports.Err = Err;
/**
  Is this `Result` an `Ok` instance?

  In TypeScript, narrows the type from `Result<T, E>` to `Ok<T, E>`.
 */
function isOk(result) {
    return result.variant === Variant.Ok;
}
exports.isOk = isOk;
/**
  Is this `Result` an `Err` instance?

  In TypeScript, narrows the type from `Result<T, E>` to `Err<T, E>`.
 */
function isErr(result) {
    return result.variant === Variant.Err;
}
exports.isErr = isErr;
function ok(value) {
    return value === undefined ? new Ok(unit_1.default) : new Ok(value);
}
exports.ok = ok;
/** `Result.of` is an alias for `Result.ok`. */
exports.of = ok;
function err(error) {
    return utils_1.isVoid(error) ? new Err(unit_1.default) : new Err(error);
}
exports.err = err;
function tryOr(error, callback) {
    const op = (cb) => {
        try {
            return exports.Result.ok(cb());
        }
        catch (_a) {
            return exports.Result.err(error);
        }
    };
    return utils_1.curry1(op, callback);
}
exports.tryOr = tryOr;
function tryOrElse(onError, callback) {
    const op = (cb) => {
        try {
            return exports.Result.ok(cb());
        }
        catch (e) {
            return exports.Result.err(onError(e));
        }
    };
    return utils_1.curry1(op, callback);
}
exports.tryOrElse = tryOrElse;
function map(mapFn, result) {
    const op = (r) => (isOk(r) ? ok(mapFn(r.value)) : r);
    return utils_1.curry1(op, result);
}
exports.map = map;
function mapOr(orU, mapFn, result) {
    function fullOp(fn, r) {
        return isOk(r) ? fn(r.value) : orU;
    }
    function partialOp(fn, curriedResult) {
        return curriedResult !== undefined
            ? fullOp(fn, curriedResult)
            : (extraCurriedResult) => fullOp(fn, extraCurriedResult);
    }
    return mapFn === undefined
        ? partialOp
        : result === undefined
            ? partialOp(mapFn)
            : partialOp(mapFn, result);
}
exports.mapOr = mapOr;
function mapOrElse(orElseFn, mapFn, result) {
    function fullOp(fn, r) {
        return isOk(r) ? fn(r.value) : orElseFn(r.error);
    }
    function partialOp(fn, curriedResult) {
        return curriedResult !== undefined
            ? fullOp(fn, curriedResult)
            : (extraCurriedResult) => fullOp(fn, extraCurriedResult);
    }
    return mapFn === undefined
        ? partialOp
        : result === undefined
            ? partialOp(mapFn)
            : partialOp(mapFn, result);
}
exports.mapOrElse = mapOrElse;
function mapErr(mapErrFn, result) {
    const op = (r) => (isOk(r) ? r : err(mapErrFn(r.error)));
    return utils_1.curry1(op, result);
}
exports.mapErr = mapErr;
function and(andResult, result) {
    const op = (r) => (isOk(r) ? andResult : r);
    return utils_1.curry1(op, result);
}
exports.and = and;
function andThen(thenFn, result) {
    const op = (r) => (isOk(r) ? thenFn(r.value) : r);
    return utils_1.curry1(op, result);
}
exports.andThen = andThen;
/** Alias for [`andThen`](#andthen). */
exports.chain = andThen;
/** Alias for [`andThen`](#andthen). */
exports.flatMap = andThen;
function or(defaultResult, result) {
    const op = (r) => (isOk(r) ? r : defaultResult);
    return utils_1.curry1(op, result);
}
exports.or = or;
function orElse(elseFn, result) {
    const op = (r) => (isOk(r) ? r : elseFn(r.unsafelyUnwrapErr()));
    return utils_1.curry1(op, result);
}
exports.orElse = orElse;
/**
  Get the value out of the `Result`.

  Returns the content of an `Ok`, but **throws if the `Result` is `Err`.**
  Prefer to use [`unwrapOr`](#unwrapor) or [`unwrapOrElse`](#unwraporelse).

  @throws If the `Result` instance is `Nothing`.
 */
function unsafelyUnwrap(result) {
    return result.unsafelyUnwrap();
}
exports.unsafelyUnwrap = unsafelyUnwrap;
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
exports.unsafelyGet = unsafelyUnwrap;
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
exports.unsafeGet = unsafelyUnwrap;
/**
  Get the error value out of the [`Result`](#result).

  Returns the content of an `Err`, but **throws if the `Result` is `Ok`**.
  Prefer to use [`unwrapOrElse`](#unwraporelse).

  @param result
  @throws Error If the `Result` instance is `Nothing`.
 */
function unsafelyUnwrapErr(result) {
    return result.unsafelyUnwrapErr();
}
exports.unsafelyUnwrapErr = unsafelyUnwrapErr;
/** Alias for [`unsafelyUnwrapErr`](#unsafelyunwraperr) */
exports.unsafelyGetErr = unsafelyUnwrapErr;
function unwrapOr(defaultValue, result) {
    const op = (r) => (isOk(r) ? r.value : defaultValue);
    return utils_1.curry1(op, result);
}
exports.unwrapOr = unwrapOr;
/** Alias for [`unwrapOr`](#unwrapor) */
exports.getOr = unwrapOr;
function unwrapOrElse(orElseFn, result) {
    const op = (r) => (isOk(r) ? r.value : orElseFn(r.error));
    return utils_1.curry1(op, result);
}
exports.unwrapOrElse = unwrapOrElse;
/** Alias for [`unwrapOrElse`](#unwraporelse) */
exports.getOrElse = unwrapOrElse;
/**
  Convert a [`Result`](#result) to a [`Maybe`](../modules/_maybe_.html#maybe).

  The converted type will be [`Just`] if the `Result` is [`Ok`] or [`Nothing`]
  if the `Result` is [`Err`]; the wrapped error value will be discarded.

  [`Just`]: ../classes/_maybe_.just.html
  [`Nothing`]: ../classes/_maybe_.nothing.html
  [`Ok`]: ../classes/_result_.ok.html
  [`Err`]: ../classes/_result_.err.html

  @param result The `Result` to convert to a `Maybe`
  @returns      `Just` the value in `result` if it is `Ok`; otherwise `Nothing`
 */
function toMaybe(result) {
    return isOk(result) ? maybe_1.just(result.value) : maybe_1.nothing();
}
exports.toMaybe = toMaybe;
function fromMaybe(errValue, maybe) {
    const op = (m) => (maybe_1.isJust(m) ? ok(maybe_1.default.unsafelyUnwrap(m)) : err(errValue));
    return utils_1.curry1(op, maybe);
}
exports.fromMaybe = fromMaybe;
/**
  Create a `String` representation of a `result` instance.

  An `Ok` instance will be printed as `Ok(<representation of the value>)`, and
  an `Err` instance will be printed as `Err(<representation of the error>)`,
  where the representation of the value or error is simply the value or error's
  own `toString` representation. For example:

                call                |         output
  --------------------------------- | ----------------------
  `toString(ok(42))`                | `Ok(42)`
  `toString(ok([1, 2, 3]))`         | `Ok(1,2,3)`
  `toString(ok({ an: 'object' }))`  | `Ok([object Object])`n
  `toString(err(42))`               | `Err(42)`
  `toString(err([1, 2, 3]))`        | `Err(1,2,3)`
  `toString(err({ an: 'object' }))` | `Err([object Object])`

  @typeparam T The type of the wrapped value; its own `.toString` will be used
               to print the interior contents of the `Just` variant.
  @param maybe The value to convert to a string.
  @returns     The string representation of the `Maybe`.
 */
exports.toString = (result) => {
    const body = (isOk(result) ? result.value : result.error).toString();
    return `${result.variant.toString()}(${body})`;
};
function match(matcher, result) {
    const op = (r) => mapOrElse(matcher.Err, matcher.Ok, r);
    return utils_1.curry1(op, result);
}
exports.match = match;
/** Alias for [`match`](#match) */
exports.cata = match;
function equals(resultB, resultA) {
    return resultA !== undefined
        ? resultA.match({
            Err: () => isErr(resultB),
            Ok: a => isOk(resultB) && resultB.unsafelyUnwrap() === a,
        })
        : (curriedResultA) => curriedResultA.match({
            Err: () => isErr(resultB),
            Ok: a => isOk(resultB) && resultB.unsafelyUnwrap() === a,
        });
}
exports.equals = equals;
function ap(resultFn, result) {
    const op = (r) => r.match({
        Ok: val => resultFn.map(fn => fn(val)),
        Err: e => exports.Result.err(e),
    });
    return utils_1.curry1(op, result);
}
exports.ap = ap;
/**
  Determine whether an item is an instance of `Just` or `Nothing`.

  @param item The item to check.
 */
function isInstance(item) {
    return item instanceof Ok || item instanceof Err;
}
exports.isInstance = isInstance;
exports.Result = {
    Variant,
    Ok,
    Err,
    isOk,
    isErr,
    ok,
    err,
    tryOr,
    tryOrElse,
    map,
    mapOr,
    mapOrElse,
    mapErr,
    and,
    andThen,
    chain: exports.chain,
    flatMap: exports.flatMap,
    or,
    orElse,
    unsafelyUnwrap,
    unsafelyGet: exports.unsafelyGet,
    unsafeGet: exports.unsafeGet,
    unsafelyUnwrapErr,
    unsafelyGetErr: exports.unsafelyGetErr,
    unwrapOr,
    getOr: exports.getOr,
    unwrapOrElse,
    getOrElse: exports.getOrElse,
    toMaybe,
    fromMaybe,
    toString: exports.toString,
    match,
    cata: exports.cata,
    equals,
    ap,
    isInstance,
};
exports.default = exports.Result;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVzdWx0LmpzIiwic291cmNlUm9vdCI6Ii4vIiwic291cmNlcyI6WyJyZXN1bHQudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBLGdDQUFnQzs7QUFFaEMseURBQXlEO0FBQ3pELG1DQUF1RDtBQUN2RCxpQ0FBMEI7QUFDMUIsbUNBQWlEO0FBRWpELHdEQUF3RDtBQUN4RCxjQUFNLENBQUMsQ0FBQywyQ0FBMkM7QUFFbkQ7Ozs7O0dBS0c7QUFDSCxJQUFZLE9BR1g7QUFIRCxXQUFZLE9BQU87SUFDakIsb0JBQVMsQ0FBQTtJQUNULHNCQUFXLENBQUE7QUFDYixDQUFDLEVBSFcsT0FBTyxHQUFQLGVBQU8sS0FBUCxlQUFPLFFBR2xCO0FBdUVEOzs7Ozs7OztHQVFHO0FBQ0gsTUFBYSxFQUFFO0lBNEJiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O09BK0JHO0lBQ0gsWUFBWSxLQUFnQjtRQXRDNUIsbUVBQW1FO1FBQzFELFlBQU8sR0FBZSxPQUFPLENBQUMsRUFBRSxDQUFDO1FBc0N4QyxJQUFJLGNBQU0sQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUNqQixNQUFNLElBQUksS0FBSyxDQUNiLHFGQUFxRixDQUN0RixDQUFDO1NBQ0g7UUFFRCxJQUFJLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQztJQUNyQixDQUFDO0lBbkVEOzs7Ozs7Ozs7Ozs7Ozs7O09BZ0JHO0lBQ0gsTUFBTSxDQUFDLE1BQU0sQ0FBSSxLQUFpQjtRQUNoQyxPQUFPLEtBQUssQ0FBQyxLQUFLLENBQUM7SUFDckIsQ0FBQztJQWtERCx3RUFBd0U7SUFDeEUsSUFBSTtRQUNGLE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztJQUVELDBFQUEwRTtJQUMxRSxLQUFLO1FBQ0gsT0FBTyxLQUFLLENBQUM7SUFDZixDQUFDO0lBRUQsc0VBQXNFO0lBQ3RFLEdBQUcsQ0FBd0IsS0FBa0I7UUFDM0MsT0FBTyxHQUFHLENBQUMsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQzFCLENBQUM7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QUk7SUFDSixLQUFLO0lBQ0wsRUFBRTtJQUNGLEdBQUc7SUFDSCxLQUFLO0lBQ0wsU0FBUztJQUNULEdBQUc7SUFDSCxLQUFLO0lBQ0wsU0FBUztJQUNULE1BQU07SUFDTixHQUFHO0lBQ0gsT0FBTztJQUNQLEtBQUssRUFBTCxhQUFLO0lBQ0wsT0FBTyxFQUFQLGVBQU87SUFDUCxFQUFFO0lBQ0YsTUFBTTtJQUNOLGNBQWM7SUFDZCxXQUFXLEVBQVgsbUJBQVc7SUFDWCxTQUFTLEVBQVQsaUJBQVM7SUFDVCxpQkFBaUI7SUFDakIsY0FBYyxFQUFkLHNCQUFjO0lBQ2QsUUFBUTtJQUNSLEtBQUssRUFBTCxhQUFLO0lBQ0wsWUFBWTtJQUNaLFNBQVMsRUFBVCxpQkFBUztJQUNULE9BQU87SUFDUCxTQUFTO0lBQ1QsUUFBUSxFQUFSLGdCQUFRO0lBQ1IsS0FBSztJQUNMLElBQUksRUFBSixZQUFJO0lBQ0osTUFBTTtJQUNOLEVBQUU7SUFDRixVQUFVO0NBQ1gsQ0FBQztBQUVGLGtCQUFlLGNBQU0sQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbIi8qKiBbW2luY2x1ZGU6ZG9jL3Jlc3VsdC5tZF1dICovXG5cbi8qKiAoa2VlcCB0eXBlZG9jIGZyb20gZ2V0dGluZyBjb25mdXNlZCBieSB0aGUgaW1wb3J0KSAqL1xuaW1wb3J0IE1heWJlLCB7IGlzSnVzdCwganVzdCwgbm90aGluZyB9IGZyb20gJy4vbWF5YmUnO1xuaW1wb3J0IFVuaXQgZnJvbSAnLi91bml0JztcbmltcG9ydCB7IF9CcmFuZCwgY3VycnkxLCBpc1ZvaWQgfSBmcm9tICcuL3V0aWxzJztcblxuLy8gU28gdGhhdCBpdCBkb2Vzbid0IGFwcGVhciB1bnVzZWQgYnV0IGNhbiBiZSBleHBvcnRlZC5cbl9CcmFuZDsgLy8gdHNsaW50OmRpc2FibGUtbGluZTpuby11bnVzZWQtZXhwcmVzc2lvblxuXG4vKipcbiAgRGlzY3JpbWluYW50IGZvciBgT2tgIGFuZCBgRXJyYCB2YXJpYW50cyBvZiBgUmVzdWx0YCB0eXBlLlxuXG4gIFlvdSBjYW4gdXNlIHRoZSBkaXNjcmltaW5hbnQgdmlhIHRoZSBgdmFyaWFudGAgcHJvcGVydHkgb2YgYFJlc3VsdGAgaW5zdGFuY2VzXG4gIGlmIHlvdSBuZWVkIHRvIG1hdGNoIGV4cGxpY2l0bHkgb24gaXQuXG4gKi9cbmV4cG9ydCBlbnVtIFZhcmlhbnQge1xuICBPayA9ICdPaycsXG4gIEVyciA9ICdFcnInLFxufVxuXG4vKiogU2ltcGx5IGRlZmluZXMgdGhlIGNvbW1vbiBzaGFwZSBmb3IgYE9rYCBhbmQgYEVycmAuICovXG5leHBvcnQgaW50ZXJmYWNlIFJlc3VsdFNoYXBlPFQsIEU+IHtcbiAgLyoqIERpc3Rpbmd1aXNoIGJldHdlZW4gdGhlIGBPa2AgYW5kIGBFcnJgIHZhcmlhbnRzLiAqL1xuICByZWFkb25seSB2YXJpYW50OiBWYXJpYW50O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuaXNPa2BdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNpc29rKSAqL1xuICBpc09rKHRoaXM6IFJlc3VsdDxULCBFPik6IHRoaXMgaXMgT2s8VCwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5pc0VycmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNpc2VycikgKi9cbiAgaXNFcnIodGhpczogUmVzdWx0PFQsIEU+KTogdGhpcyBpcyBFcnI8VCwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjbWFwKSAqL1xuICBtYXA8VT4odGhpczogUmVzdWx0PFQsIEU+LCBtYXBGbjogKHQ6IFQpID0+IFUpOiBSZXN1bHQ8VSwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBPcmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNtYXBvcikgKi9cbiAgbWFwT3I8VT4odGhpczogUmVzdWx0PFQsIEU+LCBvclU6IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFU7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBPckVsc2VgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjbWFwb3JlbHNlKSAqL1xuICBtYXBPckVsc2U8VT4odGhpczogUmVzdWx0PFQsIEU+LCBvckVsc2VGbjogKGVycjogRSkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVTtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm1hdGNoYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI21hdGNoKSAqL1xuICBtYXRjaDxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG1hdGNoZXI6IE1hdGNoZXI8VCwgRSwgVT4pOiBVO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQubWFwRXJyYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI21hcGVycikgKi9cbiAgbWFwRXJyPEY+KHRoaXM6IFJlc3VsdDxULCBFPiwgbWFwRXJyRm46IChlOiBFKSA9PiBGKTogUmVzdWx0PFQsIEY+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQub3JgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjb3IpICovXG4gIG9yPEY+KHRoaXM6IFJlc3VsdDxULCBFPiwgb3JSZXN1bHQ6IFJlc3VsdDxULCBGPik6IFJlc3VsdDxULCBGPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm9yRWxzZWBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNvcmVsc2UpICovXG4gIG9yRWxzZTxGPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG9yRWxzZUZuOiAoZXJyOiBFKSA9PiBSZXN1bHQ8VCwgRj4pOiBSZXN1bHQ8VCwgRj47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5hbmRgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjYW5kKSAqL1xuICBhbmQ8VT4odGhpczogUmVzdWx0PFQsIEU+LCBtQW5kOiBSZXN1bHQ8VSwgRT4pOiBSZXN1bHQ8VSwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5hbmRUaGVuYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2FuZHRoZW4pICovXG4gIGFuZFRoZW48VT4odGhpczogUmVzdWx0PFQsIEU+LCBhbmRUaGVuRm46ICh0OiBUKSA9PiBSZXN1bHQ8VSwgRT4pOiBSZXN1bHQ8VSwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5jaGFpbmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNjaGFpbikgKi9cbiAgY2hhaW48VT4odGhpczogUmVzdWx0PFQsIEU+LCBjaGFpbkZuOiAodDogVCkgPT4gUmVzdWx0PFUsIEU+KTogUmVzdWx0PFUsIEU+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuZmxhdE1hcGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNmbGF0bWFwKSAqL1xuICBmbGF0TWFwPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgY2hhaW5GbjogKHQ6IFQpID0+IFJlc3VsdDxVLCBFPik6IFJlc3VsdDxVLCBFPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVud3JhcGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN1bndyYXApICovXG4gIHVuc2FmZWx5VW53cmFwKCk6IFQgfCBuZXZlcjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVud3JhcEVycmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN1bndyYXBlcnIpICovXG4gIHVuc2FmZWx5VW53cmFwRXJyKCk6IEUgfCBuZXZlcjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVud3JhcE9yYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Vud3JhcG9yKSAqL1xuICB1bndyYXBPcih0aGlzOiBSZXN1bHQ8VCwgRT4sIGRlZmF1bHRWYWx1ZTogVCk6IFQ7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC51bndyYXBPckVsc2VgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjdW53cmFwT3JFbHNlKSAqL1xuICB1bndyYXBPckVsc2UodGhpczogUmVzdWx0PFQsIEU+LCBlbHNlRm46IChlcnJvcjogRSkgPT4gVCk6IFQ7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC50b01heWJlYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3RvbWF5YmUpICovXG4gIHRvTWF5YmUodGhpczogUmVzdWx0PFQsIEU+KTogTWF5YmU8VD47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC50b1N0cmluZ2BdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN0b3N0cmluZykgKi9cbiAgdG9TdHJpbmcodGhpczogUmVzdWx0PFQsIEU+KTogc3RyaW5nO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuZXF1YWxzYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2VxdWFscykgKi9cbiAgZXF1YWxzKHRoaXM6IFJlc3VsdDxULCBFPiwgY29tcGFyaXNvbjogUmVzdWx0PFQsIEU+KTogYm9vbGVhbjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmFwYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2FwKSAqL1xuICBhcDxBLCBCPih0aGlzOiBSZXN1bHQ8KGE6IEEpID0+IEIsIEU+LCByOiBSZXN1bHQ8QSwgRT4pOiBSZXN1bHQ8QiwgRT47XG59XG5cbi8qKlxuICBBbiBgT2tgIGluc3RhbmNlIGlzIHRoZSAqc3VjY2Vzc2Z1bCogdmFyaWFudCBpbnN0YW5jZSBvZiB0aGVcbiAgW2BSZXN1bHRgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjcmVzdWx0KSB0eXBlLCByZXByZXNlbnRpbmcgYSBzdWNjZXNzZnVsXG4gIG91dGNvbWUgZnJvbSBhbiBvcGVyYXRpb24gd2hpY2ggbWF5IGZhaWwuIEZvciBhIGZ1bGwgZGlzY3Vzc2lvbiwgc2VlIFt0aGVcbiAgbW9kdWxlIGRvY3NdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCkuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIHdyYXBwZWQgaW4gdGhpcyBgT2tgIHZhcmlhbnQgb2YgYFJlc3VsdGAuXG4gIEB0eXBlcGFyYW0gRSBUaGUgdHlwZSB3aGljaCB3b3VsZCBiZSB3cmFwcGVkIGluIGFuIGBFcnJgIHZhcmlhbnQgb2YgYFJlc3VsdGAuXG4gKi9cbmV4cG9ydCBjbGFzcyBPazxULCBFPiBpbXBsZW1lbnRzIFJlc3VsdFNoYXBlPFQsIEU+IHtcbiAgLyoqXG4gICAgVW53cmFwIHRoZSBjb250YWluZWQgdmFsdWUuIEEgY29udmVuaWVuY2UgbWV0aG9kIGZvciBmdW5jdGlvbmFsIGlkaW9tcy5cblxuICAgIEEgY29tbW9uIHNjZW5hcmlvIHdoZXJlIHlvdSBtaWdodCB3YW50IHRvIHVzZSB0aGlzIGlzIGluIGEgcGlwZWxpbmUgb2ZcbiAgICBmdW5jdGlvbnM6XG5cbiAgICBgYGB0c1xuICAgIGltcG9ydCBSZXN1bHQsIHsgT2sgfSBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcblxuICAgIGZ1bmN0aW9uIGdldExlbmd0aHMocmVzdWx0czogQXJyYXk8UmVzdWx0PHN0cmluZywgc3RyaW5nPj4pOiBBcnJheTxudW1iZXI+IHtcbiAgICAgIHJldHVybiByZXN1bHRzXG4gICAgICAgIC5maWx0ZXIoUmVzdWx0LmlzT2spXG4gICAgICAgIC5tYXAoT2sudW53cmFwKVxuICAgICAgICAubWFwKHMgPT4gcy5sZW5ndGgpO1xuICAgIH1cbiAgICBgYGBcbiAgICovXG4gIHN0YXRpYyB1bndyYXA8Tz4odGhlT2s6IE9rPE8sIGFueT4pOiBPIHtcbiAgICByZXR1cm4gdGhlT2sudmFsdWU7XG4gIH1cblxuICAvKiogYE9rYCBpcyBhbHdheXMgW2BWYXJpYW50Lk9rYF0oLi4vZW51bXMvX3Jlc3VsdF8udmFyaWFudCNvaykuICovXG4gIHJlYWRvbmx5IHZhcmlhbnQ6IFZhcmlhbnQuT2sgPSBWYXJpYW50Lk9rO1xuXG4gIC8qKiBUaGUgd3JhcHBlZCB2YWx1ZS4gKi9cbiAgcmVhZG9ubHkgdmFsdWU6IFQ7XG5cbiAgLyoqXG4gICAgQ3JlYXRlIGFuIGluc3RhbmNlIG9mIGBSZXN1bHQuT2tgIHdpdGggYG5ld2AuXG5cbiAgICBOb3RlOiBXaGlsZSB5b3UgKm1heSogY3JlYXRlIHRoZSBgUmVzdWx0YCB0eXBlIHZpYSBub3JtYWxcbiAgICBKYXZhU2NyaXB0IGNsYXNzIGNvbnN0cnVjdGlvbiwgaXQgaXMgbm90IHJlY29tbWVuZGVkIGZvciB0aGUgZnVuY3Rpb25hbFxuICAgIHN0eWxlIGZvciB3aGljaCB0aGUgbGlicmFyeSBpcyBpbnRlbmRlZC4gSW5zdGVhZCwgdXNlIFtgUmVzdWx0Lm9rYF0uXG5cbiAgICBbYFJlc3VsdC5va2BdOiAuLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjb2tcblxuICAgIGBgYHRzXG4gICAgLy8gQXZvaWQ6XG4gICAgY29uc3QgYVN0cmluZyA9IG5ldyBSZXN1bHQuT2soJ2NoYXJhY3RlcnMnKTtcblxuICAgIC8vIFByZWZlcjpcbiAgICBjb25zdCBhU3RyaW5nID0gUmVzdWx0Lm9rKCdjaGFyYWN0ZXJzKTtcbiAgICBgYGBcblxuICAgIE5vdGUgdGhhdCB5b3UgbWF5IGV4cGxpY2l0bHkgcGFzcyBgVW5pdGAgdG8gdGhlIGBPa2AgY29uc3RydWN0b3IgdG8gY3JlYXRlXG4gICAgYSBgUmVzdWx0PFVuaXQsIEU+YC4gSG93ZXZlciwgeW91IG1heSAqbm90KiBjYWxsIHRoZSBgT2tgIGNvbnN0cnVjdG9yIHdpdGhcbiAgICBgbnVsbGAgb3IgYHVuZGVmaW5lZGAgdG8gZ2V0IHRoYXQgcmVzdWx0ICh0aGUgdHlwZSBzeXN0ZW0gd29uJ3QgYWxsb3cgeW91IHRvXG4gICAgY29uc3RydWN0IGl0IHRoYXQgd2F5KS4gSW5zdGVhZCwgZm9yIGNvbnZlbmllbmNlLCB5b3UgY2FuIHNpbXBseSBjYWxsXG4gICAgYFJlc3VsdC5vaygpYCwgd2hpY2ggd2lsbCBjb25zdHJ1Y3QgdGhlIHR5cGUgY29ycmVjdGx5LlxuXG4gICAgQHBhcmFtIHZhbHVlXG4gICAgVGhlIHZhbHVlIHRvIHdyYXAgaW4gYSBgUmVzdWx0Lk9rYC5cblxuICAgIE5vdGU6IGBudWxsYCBhbmQgYHVuZGVmaW5lZGAgYXJlIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgdGhlXG4gICAgY29uc3RydWN0b3IgbWF5IGB0aHJvd2Agb24gdGhvc2UgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gICAgYFJlc3VsdDx1bmRlZmluZWQ+YC5cblxuICAgIEB0aHJvd3MgSWYgeW91IHBhc3MgYG51bGxgLlxuICAgKi9cbiAgY29uc3RydWN0b3IodmFsdWU/OiBUIHwgbnVsbCkge1xuICAgIGlmIChpc1ZvaWQodmFsdWUpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoXG4gICAgICAgICdUcmllZCB0byBjb25zdHJ1Y3QgYE9rYCB3aXRoIGBudWxsYCBvciBgdW5kZWZpbmVkYC4gTWF5YmUgeW91IHdhbnQgYE1heWJlLk5vdGhpbmdgPydcbiAgICAgICk7XG4gICAgfVxuXG4gICAgdGhpcy52YWx1ZSA9IHZhbHVlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5pc09rYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2lzb2spICovXG4gIGlzT2sodGhpczogUmVzdWx0PFQsIEU+KTogdGhpcyBpcyBPazxULCBFPiB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmlzRXJyYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2lzZXJyKSAqL1xuICBpc0Vycih0aGlzOiBSZXN1bHQ8VCwgRT4pOiB0aGlzIGlzIEVycjxULCBFPiB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjbWFwKSAqL1xuICBtYXA8VT4odGhpczogUmVzdWx0PFQsIEU+LCBtYXBGbjogKHQ6IFQpID0+IFUpOiBSZXN1bHQ8VSwgRT4ge1xuICAgIHJldHVybiBtYXAobWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBPcmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNtYXBvcikgKi9cbiAgbWFwT3I8VT4odGhpczogUmVzdWx0PFQsIEU+LCBvclU6IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFUge1xuICAgIHJldHVybiBtYXBPcihvclUsIG1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQubWFwT3JFbHNlYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI21hcG9yZWxzZSkgKi9cbiAgbWFwT3JFbHNlPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgb3JFbHNlRm46IChlcnI6IEUpID0+IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFUge1xuICAgIHJldHVybiBtYXBPckVsc2Uob3JFbHNlRm4sIG1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQubWF0Y2hgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjbWF0Y2gpICovXG4gIG1hdGNoPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgbWF0Y2hlcjogTWF0Y2hlcjxULCBFLCBVPik6IFUge1xuICAgIHJldHVybiBtYXRjaChtYXRjaGVyLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQubWFwRXJyYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI21hcGVycikgKi9cbiAgbWFwRXJyPEY+KHRoaXM6IFJlc3VsdDxULCBFPiwgbWFwRXJyRm46IChlOiBFKSA9PiBGKTogUmVzdWx0PFQsIEY+IHtcbiAgICByZXR1cm4gbWFwRXJyKG1hcEVyckZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQub3JgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjb3IpICovXG4gIG9yPEY+KHRoaXM6IFJlc3VsdDxULCBFPiwgb3JSZXN1bHQ6IFJlc3VsdDxULCBGPik6IFJlc3VsdDxULCBGPiB7XG4gICAgcmV0dXJuIG9yKG9yUmVzdWx0LCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQub3JFbHNlYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI29yZWxzZSkgKi9cbiAgb3JFbHNlPEY+KHRoaXM6IFJlc3VsdDxULCBFPiwgb3JFbHNlRm46IChlcnI6IEUpID0+IFJlc3VsdDxULCBGPik6IFJlc3VsdDxULCBGPiB7XG4gICAgcmV0dXJuIG9yRWxzZShvckVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmFuZGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNhbmQpICovXG4gIGFuZDxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG1BbmQ6IFJlc3VsdDxVLCBFPik6IFJlc3VsdDxVLCBFPiB7XG4gICAgcmV0dXJuIGFuZChtQW5kLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuYW5kVGhlbmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNhbmR0aGVuKSAqL1xuICBhbmRUaGVuPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgYW5kVGhlbkZuOiAodDogVCkgPT4gUmVzdWx0PFUsIEU+KTogUmVzdWx0PFUsIEU+IHtcbiAgICByZXR1cm4gYW5kVGhlbihhbmRUaGVuRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5jaGFpbmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNjaGFpbikgKi9cbiAgY2hhaW48VT4odGhpczogUmVzdWx0PFQsIEU+LCBjaGFpbkZuOiAodDogVCkgPT4gUmVzdWx0PFUsIEU+KTogUmVzdWx0PFUsIEU+IHtcbiAgICByZXR1cm4gY2hhaW4oY2hhaW5GbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmZsYXRNYXBgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjZmxhdG1hcCkgKi9cbiAgZmxhdE1hcDxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIGZsYXRNYXBGbjogKHQ6IFQpID0+IFJlc3VsdDxVLCBFPik6IFJlc3VsdDxVLCBFPiB7XG4gICAgcmV0dXJuIGZsYXRNYXAoZmxhdE1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQudW53cmFwYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Vud3JhcCkgKi9cbiAgdW5zYWZlbHlVbndyYXAoKTogVCB7XG4gICAgcmV0dXJuIHRoaXMudmFsdWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVud3JhcEVycmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN1bndyYXBlcnIpICovXG4gIHVuc2FmZWx5VW53cmFwRXJyKCk6IG5ldmVyIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ1RyaWVkIHRvIGB1bnNhZmVseVVud3JhcEVycmAgYW4gYE9rYCcpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC51bndyYXBPcmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN1bndyYXBvcikgKi9cbiAgdW53cmFwT3IodGhpczogUmVzdWx0PFQsIEU+LCBkZWZhdWx0VmFsdWU6IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3IoZGVmYXVsdFZhbHVlLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQudW53cmFwT3JFbHNlYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Vud3JhcE9yRWxzZSkgKi9cbiAgdW53cmFwT3JFbHNlKHRoaXM6IFJlc3VsdDxULCBFPiwgZWxzZUZuOiAoZXJyb3I6IEUpID0+IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3JFbHNlKGVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnRvTWF5YmVgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjdG9tYXliZSkgKi9cbiAgdG9NYXliZSh0aGlzOiBSZXN1bHQ8VCwgRT4pOiBNYXliZTxUPiB7XG4gICAgcmV0dXJuIHRvTWF5YmUodGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnRvU3RyaW5nYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Rvc3RyaW5nKSAqL1xuICB0b1N0cmluZyh0aGlzOiBSZXN1bHQ8VCwgRT4pOiBzdHJpbmcge1xuICAgIHJldHVybiB0b1N0cmluZyh0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuZXF1YWxzYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2VxdWFscykgKi9cbiAgZXF1YWxzKHRoaXM6IFJlc3VsdDxULCBFPiwgY29tcGFyaXNvbjogUmVzdWx0PFQsIEU+KTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGVxdWFscyhjb21wYXJpc29uLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuYXBgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjYXApICovXG4gIGFwPEEsIEI+KHRoaXM6IFJlc3VsdDwoYTogQSkgPT4gQiwgRT4sIHI6IFJlc3VsdDxBLCBFPik6IFJlc3VsdDxCLCBFPiB7XG4gICAgcmV0dXJuIGFwKHRoaXMsIHIpO1xuICB9XG59XG5cbi8qKlxuICBBbiBgRXJyYCBpbnN0YW5jZSBpcyB0aGUgKmZhaWx1cmUqIHZhcmlhbnQgaW5zdGFuY2Ugb2YgdGhlXG4gIFtgUmVzdWx0YF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Jlc3VsdCkgdHlwZSwgcmVwcmVzZW50aW5nIGEgZmFpbHVyZVxuICBvdXRjb21lIGZyb20gYW4gb3BlcmF0aW9uIHdoaWNoIG1heSBmYWlsLiBGb3IgYSBmdWxsIGRpc2N1c3Npb24sIHNlZSBbdGhlXG4gIG1vZHVsZSBkb2NzXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwpLlxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSB3aGljaCB3b3VsZCBiZSB3cmFwcGVkIGluIGFuIGBPa2AgdmFyaWFudCBvZiBgUmVzdWx0YC5cbiAgQHR5cGVwYXJhbSBFIFRoZSB0eXBlIHdyYXBwZWQgaW4gdGhpcyBgRXJyYCB2YXJpYW50IG9mIGBSZXN1bHRgLlxuICAqL1xuZXhwb3J0IGNsYXNzIEVycjxULCBFPiBpbXBsZW1lbnRzIFJlc3VsdFNoYXBlPFQsIEU+IHtcbiAgLyoqXG4gICAgVW53cmFwIHRoZSBjb250YWluZWQgZXJyb3IgLiBBIGNvbnZlbmllbmNlIG1ldGhvZCBmb3IgZnVuY3Rpb25hbCBpZGlvbXMuXG5cbiAgICBBIGNvbW1vbiBzY2VuYXJpbyB3aGVyZSB5b3UgbWlnaHQgd2FudCB0byB1c2UgdGhpcyBpcyBpbiBhIHBpcGVsaW5lIG9mXG4gICAgZnVuY3Rpb25zOlxuXG4gICAgYGBgdHNcbiAgICBpbXBvcnQgUmVzdWx0LCB7IE9rIH0gZnJvbSAndHJ1ZS1teXRoL3Jlc3VsdCc7XG5cbiAgICBmdW5jdGlvbiBnZXRNZXNzYWdlcyhyZXN1bHRzOiBBcnJheTxSZXN1bHQ8c3RyaW5nLCBFcnJvcj4+KTogQXJyYXk8bnVtYmVyPiB7XG4gICAgICByZXR1cm4gbWF5YmVTdHJpbmdzXG4gICAgICAgIC5maWx0ZXIoUmVzdWx0LmlzRXJyKVxuICAgICAgICAubWFwKEVyci51bndyYXBFcnIpXG4gICAgICAgIC5tYXAoZSA9PiBlLm1lc3NhZ2UpO1xuICAgIH1cbiAgICBgYGBcbiAgICovXG4gIHN0YXRpYyB1bndyYXBFcnI8Rj4odGhlRXJyOiBFcnI8RiwgYW55Pik6IEYge1xuICAgIHJldHVybiB0aGVFcnIuZXJyb3I7XG4gIH1cblxuICAvKiogYEVycmAgaXMgYWx3YXlzIFtgVmFyaWFudC5FcnJgXSguLi9lbnVtcy9fcmVzdWx0Xy52YXJpYW50I2VycikuICovXG4gIHJlYWRvbmx5IHZhcmlhbnQ6IFZhcmlhbnQuRXJyID0gVmFyaWFudC5FcnI7XG5cbiAgLyoqIFRoZSB3cmFwcGVkIGVycm9yIHZhbHVlLiAqL1xuICByZWFkb25seSBlcnJvcjogRTtcblxuICAvKipcbiAgICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYFJlc3VsdC5FcnJgIHdpdGggYG5ld2AuXG5cbiAgICBOb3RlOiBXaGlsZSB5b3UgKm1heSogY3JlYXRlIHRoZSBgUmVzdWx0YCB0eXBlIHZpYSBub3JtYWxcbiAgICBKYXZhU2NyaXB0IGNsYXNzIGNvbnN0cnVjdGlvbiwgaXQgaXMgbm90IHJlY29tbWVuZGVkIGZvciB0aGUgZnVuY3Rpb25hbFxuICAgIHN0eWxlIGZvciB3aGljaCB0aGUgbGlicmFyeSBpcyBpbnRlbmRlZC4gSW5zdGVhZCwgdXNlIFtgUmVzdWx0LmVycmBdLlxuXG4gICAgW2BSZXN1bHQuZXJyYF06IC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNlcnJcblxuICAgIGBgYHRzXG4gICAgLy8gQXZvaWQ6XG4gICAgY29uc3QgYW5FcnIgPSBuZXcgUmVzdWx0LkVycignYWxhcywgZmFpbHVyZScpO1xuXG4gICAgLy8gUHJlZmVyOlxuICAgIGNvbnN0IGFuRXJyID0gUmVzdWx0LmVycignYWxhcywgZmFpbHVyZScpO1xuICAgIGBgYFxuXG4gICAgTm90ZSB0aGF0IHlvdSBtYXkgZXhwbGljaXRseSBwYXNzIGBVbml0YCB0byB0aGUgYEVycmAgY29uc3RydWN0b3IgdG8gY3JlYXRlXG4gICAgYSBgUmVzdWx0PFQsIFVuaXQ+YC4gSG93ZXZlciwgeW91IG1heSAqbm90KiBjYWxsIHRoZSBgRXJyYCBjb25zdHJ1Y3RvciB3aXRoXG4gICAgYG51bGxgIG9yIGB1bmRlZmluZWRgIHRvIGdldCB0aGF0IHJlc3VsdCAodGhlIHR5cGUgc3lzdGVtIHdvbid0IGFsbG93IHlvdSB0b1xuICAgIGNvbnN0cnVjdCBpdCB0aGF0IHdheSkuIEluc3RlYWQsIGZvciBjb252ZW5pZW5jZSwgeW91IGNhbiBzaW1wbHkgY2FsbFxuICAgIGBSZXN1bHQuZXJyKClgLCB3aGljaCB3aWxsIGNvbnN0cnVjdCB0aGUgdHlwZSBjb3JyZWN0bHkuXG5cbiAgICBAcGFyYW0gZXJyb3JcbiAgICBUaGUgdmFsdWUgdG8gd3JhcCBpbiBhIGBSZXN1bHQuRXJyYC5cblxuICAgIGBOb3RlOiBudWxsYCBhbmQgYHVuZGVmaW5lZGAgYXJlIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgdGhlXG4gICAgY29uc3RydWN0b3IgbWF5IGB0aHJvd2Agb24gdGhvc2UgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gICAgYFJlc3VsdDxudW1iZXIsIHVuZGVmaW5lZD5gLlxuXG4gICAgQHRocm93cyBJZiB5b3UgcGFzcyBgbnVsbGAgb3IgYHVuZGVmaW5lZGAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihlcnJvcjogRSB8IG51bGwpIHtcbiAgICBpZiAoaXNWb2lkKGVycm9yKSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFxuICAgICAgICAnVHJpZWQgdG8gY29uc3RydWN0IGBFcnJgIHdpdGggYG51bGxgIG9yIGB1bmRlZmluZWRgLiBNYXliZSB5b3Ugd2FudCBgTWF5YmUuTm90aGluZ2A/J1xuICAgICAgKTtcbiAgICB9XG5cbiAgICB0aGlzLmVycm9yID0gZXJyb3I7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmlzT2tgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjaXNvaykgKi9cbiAgaXNPayh0aGlzOiBSZXN1bHQ8VCwgRT4pOiB0aGlzIGlzIE9rPFQsIEU+IHtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmlzRXJyYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI2lzZXJyKSAqL1xuICBpc0Vycih0aGlzOiBSZXN1bHQ8VCwgRT4pOiB0aGlzIGlzIEVycjxULCBFPiB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm1hcGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNtYXApICovXG4gIG1hcDxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG1hcEZuOiAodDogVCkgPT4gVSk6IFJlc3VsdDxVLCBFPiB7XG4gICAgcmV0dXJuIG1hcChtYXBGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm1hcE9yYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI21hcG9yKSAqL1xuICBtYXBPcjxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yKG9yVSwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXBPckVsc2VgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjbWFwb3JlbHNlKSAqL1xuICBtYXBPckVsc2U8VT4odGhpczogUmVzdWx0PFQsIEU+LCBvckVsc2VGbjogKGVycjogRSkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yRWxzZShvckVsc2VGbiwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5tYXRjaGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNtYXRjaCkgKi9cbiAgbWF0Y2g8VT4odGhpczogUmVzdWx0PFQsIEU+LCBtYXRjaE9iajogTWF0Y2hlcjxULCBFLCBVPik6IFUge1xuICAgIHJldHVybiBtYXRjaChtYXRjaE9iaiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm1hcEVycmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNtYXBlcnIpICovXG4gIG1hcEVycjxGPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG1hcEVyckZuOiAoZTogRSkgPT4gRik6IFJlc3VsdDxULCBGPiB7XG4gICAgcmV0dXJuIG1hcEVycihtYXBFcnJGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm9yYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI29yKSAqL1xuICBvcjxGPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG9yUmVzdWx0OiBSZXN1bHQ8VCwgRj4pOiBSZXN1bHQ8VCwgRj4ge1xuICAgIHJldHVybiBvcihvclJlc3VsdCwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0Lm9yRWxzZWBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNvcmVsc2UpICovXG4gIG9yRWxzZTxGPih0aGlzOiBSZXN1bHQ8VCwgRT4sIG9yRWxzZUZuOiAoZXJyOiBFKSA9PiBSZXN1bHQ8VCwgRj4pOiBSZXN1bHQ8VCwgRj4ge1xuICAgIHJldHVybiBvckVsc2Uob3JFbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5hbmRgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjYW5kKSAqL1xuICBhbmQ8VT4odGhpczogUmVzdWx0PFQsIEU+LCBtQW5kOiBSZXN1bHQ8VSwgRT4pOiBSZXN1bHQ8VSwgRT4ge1xuICAgIHJldHVybiBhbmQobUFuZCwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LmFuZFRoZW5gXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjYW5kdGhlbikgKi9cbiAgYW5kVGhlbjxVPih0aGlzOiBSZXN1bHQ8VCwgRT4sIGFuZFRoZW5GbjogKHQ6IFQpID0+IFJlc3VsdDxVLCBFPik6IFJlc3VsdDxVLCBFPiB7XG4gICAgcmV0dXJuIGFuZFRoZW4oYW5kVGhlbkZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuY2hhaW5gXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjY2hhaW4pICovXG4gIGNoYWluPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgY2hhaW5GbjogKHQ6IFQpID0+IFJlc3VsdDxVLCBFPik6IFJlc3VsdDxVLCBFPiB7XG4gICAgcmV0dXJuIHRoaXMuYW5kVGhlbihjaGFpbkZuKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQuZmxhdE1hcGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNmbGF0bWFwKSAqL1xuICBmbGF0TWFwPFU+KHRoaXM6IFJlc3VsdDxULCBFPiwgZmxhdE1hcEZuOiAodDogVCkgPT4gUmVzdWx0PFUsIEU+KTogUmVzdWx0PFUsIEU+IHtcbiAgICByZXR1cm4gdGhpcy5hbmRUaGVuKGZsYXRNYXBGbik7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVuc2FmZWx5VW53cmFwYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Vuc2FmZWx5dW53cmFwKSAqL1xuICB1bnNhZmVseVVud3JhcCgpOiBuZXZlciB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCdUcmllZCB0byBgdW5zYWZlbHlVbndyYXAgYW4gRXJyYCcpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC51bnNhZmVseVVud3JhcEVycmBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN1bnNhZmVseXVud3JhcGVycikgKi9cbiAgdW5zYWZlbHlVbndyYXBFcnIoKTogRSB7XG4gICAgcmV0dXJuIHRoaXMuZXJyb3I7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgUmVzdWx0LnVud3JhcE9yYF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Vud3JhcG9yKSAqL1xuICB1bndyYXBPcih0aGlzOiBSZXN1bHQ8VCwgRT4sIGRlZmF1bHRWYWx1ZTogVCk6IFQge1xuICAgIHJldHVybiB1bndyYXBPcihkZWZhdWx0VmFsdWUsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC51bndyYXBPckVsc2VgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjdW53cmFwb3JlbHNlKSAqL1xuICB1bndyYXBPckVsc2UodGhpczogUmVzdWx0PFQsIEU+LCBlbHNlRm46IChlcnJvcjogRSkgPT4gVCk6IFQge1xuICAgIHJldHVybiB1bndyYXBPckVsc2UoZWxzZUZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQudG9NYXliZWBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCN0b21heWJlKSAqL1xuICB0b01heWJlKHRoaXM6IFJlc3VsdDxULCBFPik6IE1heWJlPFQ+IHtcbiAgICByZXR1cm4gdG9NYXliZSh0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BSZXN1bHQudG9TdHJpbmdgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjdG9zdHJpbmcpICovXG4gIHRvU3RyaW5nKHRoaXM6IFJlc3VsdDxULCBFPik6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRvU3RyaW5nKHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5lcXVhbHNgXSguLi9tb2R1bGVzL19yZXN1bHRfLmh0bWwjZXF1YWxzKSAqL1xuICBlcXVhbHModGhpczogUmVzdWx0PFQsIEU+LCBjb21wYXJpc29uOiBSZXN1bHQ8VCwgRT4pOiBib29sZWFuIHtcbiAgICByZXR1cm4gZXF1YWxzKGNvbXBhcmlzb24sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYFJlc3VsdC5hcGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNhcCkgKi9cbiAgYXA8QSwgQj4odGhpczogUmVzdWx0PChhOiBBKSA9PiBCLCBFPiwgcjogUmVzdWx0PEEsIEU+KTogUmVzdWx0PEIsIEU+IHtcbiAgICByZXR1cm4gYXAodGhpcywgcik7XG4gIH1cbn1cblxuLyoqXG4gIElzIHRoaXMgYFJlc3VsdGAgYW4gYE9rYCBpbnN0YW5jZT9cblxuICBJbiBUeXBlU2NyaXB0LCBuYXJyb3dzIHRoZSB0eXBlIGZyb20gYFJlc3VsdDxULCBFPmAgdG8gYE9rPFQsIEU+YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzT2s8VCwgRT4ocmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiByZXN1bHQgaXMgT2s8VCwgRT4ge1xuICByZXR1cm4gcmVzdWx0LnZhcmlhbnQgPT09IFZhcmlhbnQuT2s7XG59XG5cbi8qKlxuICBJcyB0aGlzIGBSZXN1bHRgIGFuIGBFcnJgIGluc3RhbmNlP1xuXG4gIEluIFR5cGVTY3JpcHQsIG5hcnJvd3MgdGhlIHR5cGUgZnJvbSBgUmVzdWx0PFQsIEU+YCB0byBgRXJyPFQsIEU+YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzRXJyPFQsIEU+KHJlc3VsdDogUmVzdWx0PFQsIEU+KTogcmVzdWx0IGlzIEVycjxULCBFPiB7XG4gIHJldHVybiByZXN1bHQudmFyaWFudCA9PT0gVmFyaWFudC5FcnI7XG59XG5cbi8qKlxuICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYFJlc3VsdC5Pa2AuXG5cbiAgSWYgeW91IG5lZWQgdG8gY3JlYXRlIGFuIGluc3RhbmNlIHdpdGggYSBzcGVjaWZpYyB0eXBlIChhcyB5b3UgZG8gd2hlbmV2ZXIgeW91XG4gIGFyZSBub3QgY29uc3RydWN0aW5nIGltbWVkaWF0ZWx5IGZvciBhIGZ1bmN0aW9uIHJldHVybiBvciBhcyBhbiBhcmd1bWVudCB0byBhXG4gIGZ1bmN0aW9uKSwgeW91IGNhbiB1c2UgYSB0eXBlIHBhcmFtZXRlcjpcblxuICBgYGB0c1xuICBjb25zdCB5YXlOdW1iZXIgPSBSZXN1bHQub2s8bnVtYmVyLCBzdHJpbmc+KDEyKTtcbiAgYGBgXG5cbiAgTm90ZTogYG51bGxgIGlzIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgc28gdGhhdCB0aGUgZnVuY3Rpb25cbiAgbWF5IGJlIHVzZWQgdG8gIGB0aHJvd2Agb24gcGFzc2luZyBgbnVsbGAgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gIGBSZXN1bHQ8bnVsbCwgc3RyaW5nPmAuIGB1bmRlZmluZWRgIGlzIGFsbG93ZWQgYXMgYSBjb252ZW5pZW5jZSBtZXRob2QgZm9yXG4gIGNvbnN0cnVjdGluZyBhIGBSZXN1bHQ8VW5pdCwgRT5gLlxuXG4gIGBgYHRzXG4gIGNvbnN0IG5vcm1hbFJlc3VsdCA9IFJlc3VsdC5vazxudW1iZXIsIHN0cmluZz4oNDIpO1xuICBjb25zdCBleHBsaWNpdFVuaXQgPSBSZXN1bHQub2s8VW5pdCwgc3RyaW5nPihVbml0KTtcbiAgY29uc3QgaW1wbGljaXRVbml0ID0gUmVzdWx0Lm9rPFVuaXQsIHN0cmluZz4oKTtcbiAgYGBgXG5cbiAgSW4gdGhlIGNvbnRleHQgb2YgYW4gaW1tZWRpYXRlIGZ1bmN0aW9uIHJldHVybiwgb3IgYW4gYXJyb3cgZnVuY3Rpb24gd2l0aCBhXG4gIHNpbmdsZSBleHByZXNzaW9uIHZhbHVlLCB5b3UgZG8gbm90IGhhdmUgdG8gc3BlY2lmeSB0aGUgdHlwZXMsIHNvIHRoaXMgY2FuIGJlXG4gIHF1aXRlIGNvbnZlbmllbnQuXG5cbiAgYGBgdHNcbiAgdHlwZSBTb21lRGF0YSA9IHtcbiAgICAvLy4uLlxuICB9O1xuXG4gIGNvbnN0IGlzVmFsaWQgPSAoZGF0YTogU29tZURhdGEpOiBib29sZWFuID0+IHtcbiAgICAvLyB0cnVlIG9yIGZhbHNlLi4uXG4gIH1cblxuICBjb25zdCBhcnJvd1ZhbGlkYXRlID0gKGRhdGE6IFNvbWVEYXRhKTogUmVzdWx0PFVuaXQsIHN0cmluZz4gPT5cbiAgICBpc1ZhbGlkKGRhdGEpID8gUmVzdWx0Lm9rKCkgOiBSZXN1bHQuZXJyKCdzb21ldGhpbmcgd2FzIHdyb25nIScpO1xuXG4gIGZ1bmN0aW9uIGZuVmFsaWRhdGUoZGF0YTogc29tZURhdGEpOiBSZXN1bHQ8VW5pdCwgc3RyaW5nPiB7XG4gICAgcmV0dXJuIGlzVmFsaWQoZGF0YSkgPyBSZXN1bHQub2soKSA6IFJlc3VsdC5lcnIoJ3NvbWV0aGluZyB3YXMgd3JvbmcnKTtcbiAgfVxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIGl0ZW0gY29udGFpbmVkIGluIHRoZSBgUmVzdWx0YC5cbiAgQHBhcmFtIHZhbHVlIFRoZSB2YWx1ZSB0byB3cmFwIGluIGEgYFJlc3VsdC5Pa2AuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBvazxULCBFPigpOiBSZXN1bHQ8VW5pdCwgRT47XG5leHBvcnQgZnVuY3Rpb24gb2s8VCwgRT4odmFsdWU6IFQpOiBSZXN1bHQ8VCwgRT47XG5leHBvcnQgZnVuY3Rpb24gb2s8VCwgRT4odmFsdWU/OiBUKTogUmVzdWx0PFVuaXQsIEU+IHwgUmVzdWx0PFQsIEU+IHtcbiAgcmV0dXJuIHZhbHVlID09PSB1bmRlZmluZWQgPyBuZXcgT2soVW5pdCkgOiBuZXcgT2sodmFsdWUpO1xufVxuXG4vKiogYFJlc3VsdC5vZmAgaXMgYW4gYWxpYXMgZm9yIGBSZXN1bHQub2tgLiAqL1xuZXhwb3J0IGNvbnN0IG9mID0gb2s7XG5cbi8qKlxuICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYFJlc3VsdC5FcnJvcmAuXG5cbiAgSWYgeW91IG5lZWQgdG8gY3JlYXRlIGFuIGluc3RhbmNlIHdpdGggYSBzcGVjaWZpYyB0eXBlIChhcyB5b3UgZG8gd2hlbmV2ZXIgeW91XG4gIGFyZSBub3QgY29uc3RydWN0aW5nIGltbWVkaWF0ZWx5IGZvciBhIGZ1bmN0aW9uIHJldHVybiBvciBhcyBhbiBhcmd1bWVudCB0byBhXG4gIGZ1bmN0aW9uKSwgeW91IGNhbiB1c2UgYSB0eXBlIHBhcmFtZXRlcjpcblxuICBgYGB0c1xuICBjb25zdCBub3RTdHJpbmcgPSBSZXN1bHQuZXJyPG51bWJlciwgc3RyaW5nPignc29tZXRoaW5nIHdlbnQgd3JvbmcnKTtcbiAgYGBgXG5cbiAgTm90ZTogYG51bGxgIGlzIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgc28gdGhhdCB0aGUgZnVuY3Rpb25cbiAgbWF5IGJlIHVzZWQgdG8gIGB0aHJvd2Agb24gcGFzc2luZyBgbnVsbGAgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gIGBSZXN1bHQ8bnVsbCwgc3RyaW5nPmAuIGB1bmRlZmluZWRgIGlzIGFsbG93ZWQgYXMgYSBjb252ZW5pZW5jZSBtZXRob2QgZm9yXG4gIGNvbnN0cnVjdGluZyBhIGBSZXN1bHQ8VW5pdCwgRT5gLlxuXG4gIGBgYHRzXG4gIGNvbnN0IG5vcm1hbFJlc3VsdCA9IFJlc3VsdC5lcnI8bnVtYmVyLCBzdHJpbmc+KCdvaCBubycpO1xuICBjb25zdCBleHBsaWNpdFVuaXQgPSBSZXN1bHQuZXJyPG51bWJlciwgVW5pdD4oVW5pdCk7XG4gIGNvbnN0IGltcGxpY2l0VW5pdCA9IFJlc3VsdC5lcnI8bnVtYmVyLCBVbml0PigpO1xuICBgYGBcblxuICBJbiB0aGUgY29udGV4dCBvZiBhbiBpbW1lZGlhdGUgZnVuY3Rpb24gcmV0dXJuLCBvciBhbiBhcnJvdyBmdW5jdGlvbiB3aXRoIGFcbiAgc2luZ2xlIGV4cHJlc3Npb24gdmFsdWUsIHlvdSBkbyBub3QgaGF2ZSB0byBzcGVjaWZ5IHRoZSB0eXBlcywgc28gdGhpcyBjYW4gYmVcbiAgcXVpdGUgY29udmVuaWVudC5cblxuICBgYGB0c1xuICB0eXBlIFNvbWVEYXRhID0ge1xuICAgIC8vLi4uXG4gIH07XG5cbiAgY29uc3QgaXNWYWxpZCA9IChkYXRhOiBTb21lRGF0YSk6IGJvb2xlYW4gPT4ge1xuICAgIC8vIHRydWUgb3IgZmFsc2UuLi5cbiAgfVxuXG4gIGNvbnN0IGFycm93VmFsaWRhdGUgPSAoZGF0YTogU29tZURhdGEpOiBSZXN1bHQ8bnVtYmVyLCBVbml0PiA9PlxuICAgIGlzVmFsaWQoZGF0YSkgPyBSZXN1bHQub2soNDIpIDogUmVzdWx0LmVycigpO1xuXG4gIGZ1bmN0aW9uIGZuVmFsaWRhdGUoZGF0YTogc29tZURhdGEpOiBSZXN1bHQ8bnVtYmVyLCBVbml0PiB7XG4gICAgcmV0dXJuIGlzVmFsaWQoZGF0YSkgPyBSZXN1bHQub2soNDIpIDogUmVzdWx0LmVycigpO1xuICB9XG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgaXRlbSBjb250YWluZWQgaW4gdGhlIGBSZXN1bHRgLlxuICBAcGFyYW0gRSBUaGUgZXJyb3IgdmFsdWUgdG8gd3JhcCBpbiBhIGBSZXN1bHQuRXJyYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGVycjxULCBFPigpOiBSZXN1bHQ8VCwgVW5pdD47XG5leHBvcnQgZnVuY3Rpb24gZXJyPFQsIEU+KGVycm9yOiBFKTogUmVzdWx0PFQsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIGVycjxULCBFPihlcnJvcj86IEUpOiBSZXN1bHQ8VCwgVW5pdD4gfCBSZXN1bHQ8VCwgRT4ge1xuICByZXR1cm4gaXNWb2lkKGVycm9yKSA/IG5ldyBFcnIoVW5pdCkgOiBuZXcgRXJyKGVycm9yKTtcbn1cblxuLyoqXG4gIEV4ZWN1dGUgdGhlIHByb3ZpZGVkIGNhbGxiYWNrLCB3cmFwcGluZyB0aGUgcmV0dXJuIHZhbHVlIGluIGBSZXN1bHQuT2tgIG9yXG4gIGBSZXN1bHQuRXJyKGVycm9yKWAgaWYgdGhlcmUgaXMgYW4gZXhjZXB0aW9uLlxuXG4gIGBgYHRzXG4gIGNvbnN0IGFTdWNjZXNzZnVsT3BlcmF0aW9uID0gKCkgPT4gMiArIDI7XG5cbiAgY29uc3QgYW5Pa1Jlc3VsdCA9IFJlc3VsdC50cnlPcignT2ggbm9lcyEhMScsICgpID0+IHtcbiAgICBhU3VjY2Vzc2Z1bE9wZXJhdGlvbigpXG4gIH0pOyAvLyA9PiBPayg0KVxuXG4gIGNvbnN0IHRoaXNPcGVyYXRpb25UaHJvd3MgPSAoKSA9PiB0aHJvdyBuZXcgRXJyb3IoJ0J1bW1lcicpO1xuXG4gIGNvbnN0IGFuRXJyUmVzdWx0ID0gUmVzdWx0LnRyeU9yKCdPaCBub2VzISExJywgKCkgPT4ge1xuICAgIHRoaXNPcGVyYXRpb25UaHJvd3MoKTtcbiAgfSk7IC8vID0+IEVycignT2ggbm9lcyEhMScpXG4gYGBgXG5cbiAgQHBhcmFtIGVycm9yIFRoZSBlcnJvciB2YWx1ZSBpbiBjYXNlIG9mIGFuIGV4Y2VwdGlvblxuICBAcGFyYW0gY2FsbGJhY2sgVGhlIGNhbGxiYWNrIHRvIHRyeSBleGVjdXRpbmdcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHRyeU9yPFQsIEU+KGVycm9yOiBFLCBjYWxsYmFjazogKCkgPT4gVCk6IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0cnlPcjxULCBFPihlcnJvcjogRSk6IChjYWxsYmFjazogKCkgPT4gVCkgPT4gUmVzdWx0PFQsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIHRyeU9yPFQsIEU+KFxuICBlcnJvcjogRSxcbiAgY2FsbGJhY2s/OiAoKSA9PiBUXG4pOiBSZXN1bHQ8VCwgRT4gfCAoKGNhbGxiYWNrOiAoKSA9PiBUKSA9PiBSZXN1bHQ8VCwgRT4pIHtcbiAgY29uc3Qgb3AgPSAoY2I6ICgpID0+IFQpID0+IHtcbiAgICB0cnkge1xuICAgICAgcmV0dXJuIFJlc3VsdC5vazxULCBFPihjYigpKTtcbiAgICB9IGNhdGNoIHtcbiAgICAgIHJldHVybiBSZXN1bHQuZXJyPFQsIEU+KGVycm9yKTtcbiAgICB9XG4gIH07XG5cbiAgcmV0dXJuIGN1cnJ5MShvcCwgY2FsbGJhY2spO1xufVxuXG4vKipcbiAgRXhlY3V0ZSB0aGUgcHJvdmlkZWQgY2FsbGJhY2ssIHdyYXBwaW5nIHRoZSByZXR1cm4gdmFsdWUgaW4gYFJlc3VsdC5Pa2AuXG4gIElmIHRoZXJlIGlzIGFuIGV4Y2VwdGlvbiwgcmV0dXJuIGEgYFJlc3VsdC5FcnJgIG9mIHdoYXRldmVyIHRoZSBgb25FcnJvcmBcbiAgZnVuY3Rpb24gcmV0dXJucy5cblxuICBgYGB0c1xuICBjb25zdCBhU3VjY2Vzc2Z1bE9wZXJhdGlvbiA9ICgpID0+IDIgKyAyO1xuXG4gIGNvbnN0IGFuT2tSZXN1bHQgPSBSZXN1bHQudHJ5T3JFbHNlKFxuICAgIChlKSA9PiBlLFxuICAgIGFTdWNjZXNzZnVsT3BlcmF0aW9uXG4gICk7IC8vID0+IE9rKDQpXG5cbiAgY29uc3QgdGhpc09wZXJhdGlvblRocm93cyA9ICgpID0+IHRocm93ICdCdW1tZXInXG5cbiAgY29uc3QgYW5FcnJSZXN1bHQgPSBSZXN1bHQudHJ5T3JFbHNlKChlKSA9PiBlLCAoKSA9PiB7XG4gICAgdGhpc09wZXJhdGlvblRocm93cygpO1xuICB9KTsgLy8gPT4gRXJyKCdCdW1tZXInKVxuIGBgYFxuXG4gIEBwYXJhbSBvbkVycm9yIEEgZnVuY3Rpb24gdGhhdCB0YWtlcyBgZWAgZXhjZXB0aW9uIGFuZCByZXR1cm5zIHdoYXQgd2lsbFxuICBiZSB3cmFwcGVkIGluIGEgYFJlc3VsdC5FcnJgXG4gIEBwYXJhbSBjYWxsYmFjayBUaGUgY2FsbGJhY2sgdG8gdHJ5IGV4ZWN1dGluZ1xuICovXG5leHBvcnQgZnVuY3Rpb24gdHJ5T3JFbHNlPFQsIEU+KG9uRXJyb3I6IChlOiB1bmtub3duKSA9PiBFLCBjYWxsYmFjazogKCkgPT4gVCk6IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0cnlPckVsc2U8VCwgRT4ob25FcnJvcjogKGU6IHVua25vd24pID0+IEUpOiAoY2FsbGJhY2s6ICgpID0+IFQpID0+IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0cnlPckVsc2U8VCwgRT4oXG4gIG9uRXJyb3I6IChlOiB1bmtub3duKSA9PiBFLFxuICBjYWxsYmFjaz86ICgpID0+IFRcbik6IFJlc3VsdDxULCBFPiB8ICgoY2FsbGJhY2s6ICgpID0+IFQpID0+IFJlc3VsdDxULCBFPikge1xuICBjb25zdCBvcCA9IChjYjogKCkgPT4gVCkgPT4ge1xuICAgIHRyeSB7XG4gICAgICByZXR1cm4gUmVzdWx0Lm9rPFQsIEU+KGNiKCkpO1xuICAgIH0gY2F0Y2ggKGUpIHtcbiAgICAgIHJldHVybiBSZXN1bHQuZXJyPFQsIEU+KG9uRXJyb3IoZSkpO1xuICAgIH1cbiAgfTtcblxuICByZXR1cm4gY3VycnkxKG9wLCBjYWxsYmFjayk7XG59XG5cbi8qKlxuICBNYXAgb3ZlciBhIGBSZXN1bHRgIGluc3RhbmNlOiBhcHBseSB0aGUgZnVuY3Rpb24gdG8gdGhlIHdyYXBwZWQgdmFsdWUgaWYgdGhlXG4gIGluc3RhbmNlIGlzIGBPa2AsIGFuZCByZXR1cm4gdGhlIHdyYXBwZWQgZXJyb3IgdmFsdWUgd3JhcHBlZCBhcyBhIG5ldyBgRXJyYCBvZlxuICB0aGUgY29ycmVjdCB0eXBlIChgUmVzdWx0PFUsIEU+YCkgaWYgdGhlIGluc3RhbmNlIGlzIGBFcnJgLlxuXG4gIGBSZXN1bHQubWFwYCB3b3JrcyBhIGxvdCBsaWtlIGBBcnJheS5wcm90b3R5cGUubWFwYCwgYnV0IHdpdGggb25lIGltcG9ydGFudFxuICBkaWZmZXJlbmNlLiBCb3RoIGBSZXN1bHRgIGFuZCBgQXJyYXlgIGFyZSBjb250YWluZXJzIGZvciBvdGhlciBraW5kcyBvZiBpdGVtcyxcbiAgYnV0IHdoZXJlIGBBcnJheS5wcm90b3R5cGUubWFwYCBoYXMgMCB0byBfbl8gaXRlbXMsIGEgYFJlc3VsdGAgYWx3YXlzIGhhc1xuICBleGFjdGx5IG9uZSBpdGVtLCB3aGljaCBpcyAqZWl0aGVyKiBhIHN1Y2Nlc3Mgb3IgYW4gZXJyb3IgaW5zdGFuY2UuXG5cbiAgV2hlcmUgYEFycmF5LnByb3RvdHlwZS5tYXBgIHdpbGwgYXBwbHkgdGhlIG1hcHBpbmcgZnVuY3Rpb24gdG8gZXZlcnkgaXRlbSBpblxuICB0aGUgYXJyYXkgKGlmIHRoZXJlIGFyZSBhbnkpLCBgUmVzdWx0Lm1hcGAgd2lsbCBvbmx5IGFwcGx5IHRoZSBtYXBwaW5nXG4gIGZ1bmN0aW9uIHRvIHRoZSAoc2luZ2xlKSBlbGVtZW50IGlmIGFuIGBPa2AgaW5zdGFuY2UsIGlmIHRoZXJlIGlzIG9uZS5cblxuICBJZiB5b3UgaGF2ZSBubyBpdGVtcyBpbiBhbiBhcnJheSBvZlxuICBudW1iZXJzIG5hbWVkIGBmb29gIGFuZCBjYWxsIGBmb28ubWFwKHggPT4geCArIDEpYCwgeW91J2xsIHN0aWxsIHNvbWUgaGF2ZSBhblxuICBhcnJheSB3aXRoIG5vdGhpbmcgaW4gaXQuIEJ1dCBpZiB5b3UgaGF2ZSBhbnkgaXRlbXMgaW4gdGhlIGFycmF5IChgWzIsIDNdYCksXG4gIGFuZCB5b3UgY2FsbCBgZm9vLm1hcCh4ID0+IHggKyAxKWAgb24gaXQsIHlvdSdsbCBnZXQgYSBuZXcgYXJyYXkgd2l0aCBlYWNoIG9mXG4gIHRob3NlIGl0ZW1zIGluc2lkZSB0aGUgYXJyYXkgXCJjb250YWluZXJcIiB0cmFuc2Zvcm1lZCAoYFszLCA0XWApLlxuXG4gIFdpdGggYFJlc3VsdC5tYXBgLCB0aGUgYEVycmAgdmFyaWFudCBpcyB0cmVhdGVkICpieSB0aGUgYG1hcGAgZnVuY3Rpb24qIGtpbmRcbiAgb2YgdGhlIHNhbWUgd2F5IGFzIHRoZSBlbXB0eSBhcnJheSBjYXNlOiBpdCdzIGp1c3QgaWdub3JlZCwgYW5kIHlvdSBnZXQgYmFjayBhXG4gIG5ldyBgUmVzdWx0YCB0aGF0IGlzIHN0aWxsIGp1c3QgdGhlIHNhbWUgYEVycmAgaW5zdGFuY2UuIEJ1dCBpZiB5b3UgaGF2ZSBhblxuICBgT2tgIHZhcmlhbnQsIHRoZSBtYXAgZnVuY3Rpb24gaXMgYXBwbGllZCB0byBpdCwgYW5kIHlvdSBnZXQgYmFjayBhIG5ld1xuICBgUmVzdWx0YCB3aXRoIHRoZSB2YWx1ZSB0cmFuc2Zvcm1lZCwgYW5kIHN0aWxsIHdyYXBwZWQgaW4gYW4gYE9rYC5cblxuICAjIyMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsgb2ssIGVyciwgbWFwLCB0b1N0cmluZyB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuICBjb25zdCBkb3VibGUgPSBuID0+IG4gKiAyO1xuXG4gIGNvbnN0IGFuT2sgPSBvaygxMik7XG4gIGNvbnN0IG1hcHBlZE9rID0gbWFwKGRvdWJsZSwgYW5Payk7XG4gIGNvbnNvbGUubG9nKHRvU3RyaW5nKG1hcHBlZE9rKSk7IC8vIE9rKDI0KVxuXG4gIGNvbnN0IGFuRXJyID0gZXJyKFwibm90aGluZyBoZXJlIVwiKTtcbiAgY29uc3QgbWFwcGVkRXJyID0gbWFwKGRvdWJsZSwgYW5FcnIpO1xuICBjb25zb2xlLmxvZyh0b1N0cmluZyhtYXBwZWRPaykpOyAvLyBFcnIobm90aGluZyBoZXJlISlcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiBhbiBgT2tgIGluc3RhbmNlLCBhbmQgdGFrZW4gYXNcbiAgICAgICAgICAgICAgICB0aGUgYXJndW1lbnQgdG8gdGhlIGBtYXBGbmAuXG4gIEB0eXBlcGFyYW0gVSAgVGhlIHR5cGUgb2YgdGhlIHZhbHVlIHdyYXBwZWQgaW4gdGhlIG5ldyBgT2tgIGluc3RhbmNlIGFmdGVyXG4gICAgICAgICAgICAgICAgYXBwbHlpbmcgYG1hcEZuYCwgdGhhdCBpcywgdGhlIHR5cGUgcmV0dXJuZWQgYnkgYG1hcEZuYC5cbiAgQHR5cGVwYXJhbSBFICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiBhbiBgRXJyYCBpbnN0YW5jZS5cbiAgQHBhcmFtIG1hcEZuICBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdGhlIHZhbHVlIHRvIGlmIGByZXN1bHRgIGlzIGBPa2AuXG4gIEBwYXJhbSByZXN1bHQgVGhlIGBSZXN1bHRgIGluc3RhbmNlIHRvIG1hcCBvdmVyLlxuICBAcmV0dXJucyAgICAgIEEgbmV3IGBSZXN1bHRgIHdpdGggdGhlIHJlc3VsdCBvZiBhcHBseWluZyBgbWFwRm5gIHRvIHRoZSB2YWx1ZVxuICAgICAgICAgICAgICAgIGluIGFuIGBPa2AsIG9yIGVsc2UgdGhlIG9yaWdpbmFsIGBFcnJgIHZhbHVlIHdyYXBwZWQgaW4gdGhlIG5ld1xuICAgICAgICAgICAgICAgIGluc3RhbmNlLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWFwPFQsIFUsIEU+KG1hcEZuOiAodDogVCkgPT4gVSwgcmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBSZXN1bHQ8VSwgRT47XG5leHBvcnQgZnVuY3Rpb24gbWFwPFQsIFUsIEU+KG1hcEZuOiAodDogVCkgPT4gVSk6IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gUmVzdWx0PFUsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIG1hcDxULCBVLCBFPihcbiAgbWFwRm46ICh0OiBUKSA9PiBVLFxuICByZXN1bHQ/OiBSZXN1bHQ8VCwgRT5cbik6IFJlc3VsdDxVLCBFPiB8ICgocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxVLCBFPikge1xuICBjb25zdCBvcCA9IChyOiBSZXN1bHQ8VCwgRT4pID0+IChpc09rKHIpID8gb2sobWFwRm4oci52YWx1ZSkpIDogcikgYXMgUmVzdWx0PFUsIEU+O1xuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKipcbiAgTWFwIG92ZXIgYSBgUmVzdWx0YCBpbnN0YW5jZSBhcyBpbiBbYG1hcGBdKCNtYXApIGFuZCBnZXQgb3V0IHRoZSB2YWx1ZVxuICBpZiBgcmVzdWx0YCBpcyBhbiBgT2tgLCBvciByZXR1cm4gYSBkZWZhdWx0IHZhbHVlIGlmIGByZXN1bHRgIGlzIGFuIGBFcnJgLlxuXG4gICMjIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBpbXBvcnQgeyBvaywgZXJyLCBtYXBPciB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuXG4gIGNvbnN0IGxlbmd0aCA9IChzOiBzdHJpbmcpID0+IHMubGVuZ3RoO1xuXG4gIGNvbnN0IGFuT2tTdHJpbmcgPSBvaygnYSBzdHJpbmcnKTtcbiAgY29uc3QgdGhlU3RyaW5nTGVuZ3RoID0gbWFwT3IoMCwgYW5Pa1N0cmluZyk7XG4gIGNvbnNvbGUubG9nKHRoZVN0cmluZ0xlbmd0aCk7ICAvLyA4XG5cbiAgY29uc3QgYW5FcnIgPSBlcnIoJ3VoIG9oJyk7XG4gIGNvbnN0IGFuRXJyTWFwcGVkID0gbWFwT3IoMCwgYW5FcnIpO1xuICBjb25zb2xlLmxvZyhhbkVyck1hcHBlZCk7ICAvLyAwXG4gIGBgYFxuXG4gIEBwYXJhbSBvclUgVGhlIGRlZmF1bHQgdmFsdWUgdG8gdXNlIGlmIGByZXN1bHRgIGlzIGFuIGBFcnJgLlxuICBAcGFyYW0gbWFwRm4gVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IHRoZSB2YWx1ZSB0byBpZiBgcmVzdWx0YCBpcyBhbiBgT2tgLlxuICBAcGFyYW0gcmVzdWx0IFRoZSBgUmVzdWx0YCBpbnN0YW5jZSB0byBtYXAgb3Zlci5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFUsIEU+KG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVLCByZXN1bHQ6IFJlc3VsdDxULCBFPik6IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3I8VCwgVSwgRT4ob3JVOiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3I8VCwgVSwgRT4ob3JVOiBVKTogKG1hcEZuOiAodDogVCkgPT4gVSkgPT4gKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFUsIEU+KFxuICBvclU6IFUsXG4gIG1hcEZuPzogKHQ6IFQpID0+IFUsXG4gIHJlc3VsdD86IFJlc3VsdDxULCBFPlxuKTogVSB8ICgocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFUpIHwgKChtYXBGbjogKHQ6IFQpID0+IFUpID0+IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gVSkge1xuICBmdW5jdGlvbiBmdWxsT3AoZm46ICh0OiBUKSA9PiBVLCByOiBSZXN1bHQ8VCwgRT4pOiBVIHtcbiAgICByZXR1cm4gaXNPayhyKSA/IGZuKHIudmFsdWUpIDogb3JVO1xuICB9XG5cbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSk6IChtYXliZTogUmVzdWx0PFQsIEU+KSA9PiBVO1xuICBmdW5jdGlvbiBwYXJ0aWFsT3AoZm46ICh0OiBUKSA9PiBVLCBjdXJyaWVkUmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBVO1xuICBmdW5jdGlvbiBwYXJ0aWFsT3AoXG4gICAgZm46ICh0OiBUKSA9PiBVLFxuICAgIGN1cnJpZWRSZXN1bHQ/OiBSZXN1bHQ8VCwgRT5cbiAgKTogVSB8ICgobWF5YmU6IFJlc3VsdDxULCBFPikgPT4gVSkge1xuICAgIHJldHVybiBjdXJyaWVkUmVzdWx0ICE9PSB1bmRlZmluZWRcbiAgICAgID8gZnVsbE9wKGZuLCBjdXJyaWVkUmVzdWx0KVxuICAgICAgOiAoZXh0cmFDdXJyaWVkUmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IGZ1bGxPcChmbiwgZXh0cmFDdXJyaWVkUmVzdWx0KTtcbiAgfVxuXG4gIHJldHVybiBtYXBGbiA9PT0gdW5kZWZpbmVkXG4gICAgPyBwYXJ0aWFsT3BcbiAgICA6IHJlc3VsdCA9PT0gdW5kZWZpbmVkXG4gICAgICA/IHBhcnRpYWxPcChtYXBGbilcbiAgICAgIDogcGFydGlhbE9wKG1hcEZuLCByZXN1bHQpO1xufVxuXG4vKipcbiAgTWFwIG92ZXIgYSBgUmVzdWx0YCBpbnN0YW5jZSBhcyBpbiBbYG1hcGBdKCNtYXApIGFuZCBnZXQgb3V0IHRoZSB2YWx1ZSBpZlxuICBgcmVzdWx0YCBpcyBgT2tgLCBvciBhcHBseSBhIGZ1bmN0aW9uIChgb3JFbHNlRm5gKSB0byB0aGUgdmFsdWUgd3JhcHBlZCBpblxuICB0aGUgYEVycmAgdG8gZ2V0IGEgZGVmYXVsdCB2YWx1ZS5cblxuICBMaWtlIFtgbWFwT3JgXSgjbWFwb3IpIGJ1dCB1c2luZyBhIGZ1bmN0aW9uIHRvIHRyYW5zZm9ybSB0aGUgZXJyb3IgaW50byBhXG4gIHVzYWJsZSB2YWx1ZSBpbnN0ZWFkIG9mIHNpbXBseSB1c2luZyBhIGRlZmF1bHQgdmFsdWUuXG5cbiAgIyMjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGltcG9ydCB7IG9rLCBlcnIsIG1hcE9yRWxzZSB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuXG4gIGNvbnN0IHN1bW1hcml6ZSA9IChzOiBzdHJpbmcpID0+IGBUaGUgcmVzcG9uc2Ugd2FzOiAnJHtzfSdgO1xuICBjb25zdCBnZXRSZWFzb24gPSAoZXJyOiB7IGNvZGU6IG51bWJlciwgcmVhc29uOiBzdHJpbmcgfSkgPT4gZXJyLnJlYXNvbjtcblxuICBjb25zdCBva1Jlc3BvbnNlID0gb2soXCJUaGluZ3MgYXJlIGdyYW5kIGhlcmUuXCIpO1xuICBjb25zdCBtYXBwZWRPa0FuZFVud3JhcHBlZCA9IG1hcE9yRWxzZShnZXRSZWFzb24sIHN1bW1hcml6ZSwgb2tSZXNwb25zZSk7XG4gIGNvbnNvbGUubG9nKG1hcHBlZE9rQW5kVW53cmFwcGVkKTsgIC8vIFRoZSByZXNwb25zZSB3YXM6ICdUaGluZ3MgYXJlIGdyYW5kIGhlcmUuJ1xuXG4gIGNvbnN0IGVyclJlc3BvbnNlID0gZXJyKHsgY29kZTogNTAwLCByZWFzb246ICdOb3RoaW5nIGF0IHRoaXMgZW5kcG9pbnQhJyB9KTtcbiAgY29uc3QgbWFwcGVkRXJyQW5kVW53cmFwcGVkID0gbWFwT3JFbHNlKGdldFJlYXNvbiwgc3VtbWFyaXplLCBlcnJSZXNwb25zZSk7XG4gIGNvbnNvbGUubG9nKG1hcHBlZEVyckFuZFVud3JhcHBlZCk7ICAvLyBOb3RoaW5nIGF0IHRoaXMgZW5kcG9pbnQhXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCBgT2tgIHZhbHVlLlxuICBAdHlwZXBhcmFtIFUgICAgVGhlIHR5cGUgb2YgdGhlIHJlc3VsdGluZyB2YWx1ZSBmcm9tIGFwcGx5aW5nIGBtYXBGbmAgdG8gdGhlXG4gICAgICAgICAgICAgICAgICBgT2tgIHZhbHVlIG9yIGBvckVsc2VGbmAgdG8gdGhlIGBFcnJgIHZhbHVlLlxuICBAdHlwZXBhcmFtIEUgICAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgYEVycmAgdmFsdWUuXG4gIEBwYXJhbSBvckVsc2VGbiBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdG8gdGhlIHdyYXBwZWQgYEVycmAgdmFsdWUgdG8gZ2V0IGFcbiAgICAgICAgICAgICAgICAgIHVzYWJsZSB2YWx1ZSBpZiBgcmVzdWx0YCBpcyBhbiBgRXJyYC5cbiAgQHBhcmFtIG1hcEZuICAgIFRoZSBmdW5jdGlvbiB0byBhcHBseSB0byB0aGUgd3JhcHBlZCBgT2tgIHZhbHVlIGlmIGByZXN1bHRgIGlzXG4gICAgICAgICAgICAgICAgICBhbiBgT2tgLlxuICBAcGFyYW0gcmVzdWx0ICAgVGhlIGBSZXN1bHRgIGluc3RhbmNlIHRvIG1hcCBvdmVyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWFwT3JFbHNlPFQsIFUsIEU+KFxuICBvckVsc2VGbjogKGVycjogRSkgPT4gVSxcbiAgbWFwRm46ICh0OiBUKSA9PiBVLFxuICByZXN1bHQ6IFJlc3VsdDxULCBFPlxuKTogVTtcbmV4cG9ydCBmdW5jdGlvbiBtYXBPckVsc2U8VCwgVSwgRT4oXG4gIG9yRWxzZUZuOiAoZXJyOiBFKSA9PiBVLFxuICBtYXBGbjogKHQ6IFQpID0+IFVcbik6IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gVTtcbmV4cG9ydCBmdW5jdGlvbiBtYXBPckVsc2U8VCwgVSwgRT4oXG4gIG9yRWxzZUZuOiAoZXJyOiBFKSA9PiBVXG4pOiAobWFwRm46ICh0OiBUKSA9PiBVKSA9PiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3JFbHNlPFQsIFUsIEU+KFxuICBvckVsc2VGbjogKGVycjogRSkgPT4gVSxcbiAgbWFwRm4/OiAodDogVCkgPT4gVSxcbiAgcmVzdWx0PzogUmVzdWx0PFQsIEU+XG4pOiBVIHwgKChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gVSkgfCAoKG1hcEZuOiAodDogVCkgPT4gVSkgPT4gKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBVKSB7XG4gIGZ1bmN0aW9uIGZ1bGxPcChmbjogKHQ6IFQpID0+IFUsIHI6IFJlc3VsdDxULCBFPikge1xuICAgIHJldHVybiBpc09rKHIpID8gZm4oci52YWx1ZSkgOiBvckVsc2VGbihyLmVycm9yKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHBhcnRpYWxPcChmbjogKHQ6IFQpID0+IFUpOiAobWF5YmU6IFJlc3VsdDxULCBFPikgPT4gVTtcbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSwgY3VycmllZFJlc3VsdDogUmVzdWx0PFQsIEU+KTogVTtcbiAgZnVuY3Rpb24gcGFydGlhbE9wKFxuICAgIGZuOiAodDogVCkgPT4gVSxcbiAgICBjdXJyaWVkUmVzdWx0PzogUmVzdWx0PFQsIEU+XG4gICk6IFUgfCAoKG1heWJlOiBSZXN1bHQ8VCwgRT4pID0+IFUpIHtcbiAgICByZXR1cm4gY3VycmllZFJlc3VsdCAhPT0gdW5kZWZpbmVkXG4gICAgICA/IGZ1bGxPcChmbiwgY3VycmllZFJlc3VsdClcbiAgICAgIDogKGV4dHJhQ3VycmllZFJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBmdWxsT3AoZm4sIGV4dHJhQ3VycmllZFJlc3VsdCk7XG4gIH1cblxuICByZXR1cm4gbWFwRm4gPT09IHVuZGVmaW5lZFxuICAgID8gcGFydGlhbE9wXG4gICAgOiByZXN1bHQgPT09IHVuZGVmaW5lZFxuICAgICAgPyBwYXJ0aWFsT3AobWFwRm4pXG4gICAgICA6IHBhcnRpYWxPcChtYXBGbiwgcmVzdWx0KTtcbn1cblxuLyoqXG4gIE1hcCBvdmVyIGEgYFJlc3VsdGAsIGV4YWN0bHkgYXMgaW4gW2BtYXBgXSgjbWFwKSwgYnV0IG9wZXJhdGluZyBvbiB0aGUgdmFsdWVcbiAgd3JhcHBlZCBpbiBhbiBgRXJyYCBpbnN0ZWFkIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgT2tgLiBUaGlzIGlzIGhhbmR5XG4gIGZvciB3aGVuIHlvdSBuZWVkIHRvIGxpbmUgdXAgYSBidW5jaCBvZiBkaWZmZXJlbnQgdHlwZXMgb2YgZXJyb3JzLCBvciBpZiB5b3VcbiAgbmVlZCBhbiBlcnJvciBvZiBvbmUgc2hhcGUgdG8gYmUgaW4gYSBkaWZmZXJlbnQgc2hhcGUgdG8gdXNlIHNvbWV3aGVyZSBlbHNlIGluXG4gIHlvdXIgY29kZWJhc2UuXG5cbiAgIyMjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGltcG9ydCB7IG9rLCBlcnIsIG1hcEVyciwgdG9TdHJpbmcgfSBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcblxuICBjb25zdCByZWFzb24gPSAoZXJyOiB7IGNvZGU6IG51bWJlciwgcmVhc29uOiBzdHJpbmcgfSkgPT4gZXJyLnJlYXNvbjtcblxuICBjb25zdCBhbk9rID0gb2soMTIpO1xuICBjb25zdCBtYXBwZWRPayA9IG1hcEVycihyZWFzb24sIGFuT2spO1xuICBjb25zb2xlLmxvZyh0b1N0cmluZyhtYXBwZWRPaykpOyAgLy8gT2soMTIpXG5cbiAgY29uc3QgYW5FcnIgPSBlcnIoeyBjb2RlOiAxMDEsIHJlYXNvbjogJ2JhZCBmaWxlJyB9KTtcbiAgY29uc3QgbWFwcGVkRXJyID0gbWFwRXJyKHJlYXNvbiwgYW5FcnIpO1xuICBjb25zb2xlLmxvZyh0b1N0cmluZyhtYXBwZWRFcnIpKTsgIC8vIEVycihiYWQgZmlsZSlcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUICAgIFRoZSB0eXBlIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgT2tgIG9mIHRoZSBgUmVzdWx0YC5cbiAgQHR5cGVwYXJhbSBFICAgIFRoZSB0eXBlIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgRXJyYCBvZiB0aGUgYFJlc3VsdGAuXG4gIEB0eXBlcGFyYW0gRiAgICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiB0aGUgYEVycmAgb2YgYSBuZXcgYFJlc3VsdGAsXG4gICAgICAgICAgICAgICAgICByZXR1cm5lZCBieSB0aGUgYG1hcEVyckZuYC5cbiAgQHBhcmFtIG1hcEVyckZuIFRoZSBmdW5jdGlvbiB0byBhcHBseSB0byB0aGUgdmFsdWUgd3JhcHBlZCBpbiBgRXJyYCBpZiBgcmVzdWx0YCBpcyBhbiBgRXJyYC5cbiAgQHBhcmFtIHJlc3VsdCAgIFRoZSBgUmVzdWx0YCBpbnN0YW5jZSB0byBtYXAgb3ZlciBhbiBlcnJvciBjYXNlIGZvci5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hcEVycjxULCBFLCBGPihtYXBFcnJGbjogKGU6IEUpID0+IEYsIHJlc3VsdDogUmVzdWx0PFQsIEU+KTogUmVzdWx0PFQsIEY+O1xuZXhwb3J0IGZ1bmN0aW9uIG1hcEVycjxULCBFLCBGPihtYXBFcnJGbjogKGU6IEUpID0+IEYpOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxULCBGPjtcbmV4cG9ydCBmdW5jdGlvbiBtYXBFcnI8VCwgRSwgRj4oXG4gIG1hcEVyckZuOiAoZTogRSkgPT4gRixcbiAgcmVzdWx0PzogUmVzdWx0PFQsIEU+XG4pOiBSZXN1bHQ8VCwgRj4gfCAoKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBSZXN1bHQ8VCwgRj4pIHtcbiAgY29uc3Qgb3AgPSAocjogUmVzdWx0PFQsIEU+KSA9PiAoaXNPayhyKSA/IHIgOiBlcnIobWFwRXJyRm4oci5lcnJvcikpKSBhcyBSZXN1bHQ8VCwgRj47XG4gIHJldHVybiBjdXJyeTEob3AsIHJlc3VsdCk7XG59XG5cbi8qKlxuICBZb3UgY2FuIHRoaW5rIG9mIHRoaXMgbGlrZSBhIHNob3J0LWNpcmN1aXRpbmcgbG9naWNhbCBcImFuZFwiIG9wZXJhdGlvbiBvbiBhXG4gIGBSZXN1bHRgIHR5cGUuIElmIGByZXN1bHRgIGlzIGBPa2AsIHRoZW4gdGhlIHJlc3VsdCBpcyB0aGUgYGFuZFJlc3VsdGAuIElmXG4gIGByZXN1bHRgIGlzIGBFcnJgLCB0aGUgcmVzdWx0IGlzIHRoZSBgRXJyYC5cblxuICBUaGlzIGlzIHVzZWZ1bCB3aGVuIHlvdSBoYXZlIGFub3RoZXIgYFJlc3VsdGAgdmFsdWUgeW91IHdhbnQgdG8gcHJvdmlkZSBpZlxuICBhbmQgKm9ubHkgaWYqIHlvdSBoYXZlIGFuIGBPa2Ag4oCTIHRoYXQgaXMsIHdoZW4geW91IG5lZWQgdG8gbWFrZSBzdXJlIHRoYXQgaWYgeW91XG4gIGBFcnJgLCB3aGF0ZXZlciBlbHNlIHlvdSdyZSBoYW5kaW5nIGEgYFJlc3VsdGAgdG8gKmFsc28qIGdldHMgdGhhdCBgRXJyYC5cblxuICBOb3RpY2UgdGhhdCwgdW5saWtlIGluIFtgbWFwYF0oI21hcCkgb3IgaXRzIHZhcmlhbnRzLCB0aGUgb3JpZ2luYWwgYHJlc3VsdGAgaXNcbiAgbm90IGludm9sdmVkIGluIGNvbnN0cnVjdGluZyB0aGUgbmV3IGBSZXN1bHRgLlxuXG4gICMjIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBpbXBvcnQgeyBhbmQsIG9rLCBlcnIsIHRvU3RyaW5nIH0gZnJvbSAndHJ1ZS1teXRoL3Jlc3VsdCc7XG5cbiAgY29uc3Qgb2tBID0gb2soJ0EnKTtcbiAgY29uc3Qgb2tCID0gb2soJ0InKTtcbiAgY29uc3QgYW5FcnIgPSBlcnIoeyBzbzogJ2JhZCcgfSk7XG5cbiAgY29uc29sZS5sb2codG9TdHJpbmcoYW5kKG9rQiwgb2tBKSkpOyAgLy8gT2soQilcbiAgY29uc29sZS5sb2codG9TdHJpbmcoYW5kKG9rQiwgYW5FcnIpKSk7ICAvLyBFcnIoW29iamVjdCBPYmplY3RdKVxuICBjb25zb2xlLmxvZyh0b1N0cmluZyhhbmQoYW5FcnIsIG9rQSkpKTsgIC8vIEVycihbb2JqZWN0IE9iamVjdF0pXG4gIGNvbnNvbGUubG9nKHRvU3RyaW5nKGFuZChhbkVyciwgYW5FcnIpKSk7ICAvLyBFcnIoW29iamVjdCBPYmplY3RdKVxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgICAgIFRoZSB0eXBlIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgT2tgIG9mIHRoZSBgUmVzdWx0YC5cbiAgQHR5cGVwYXJhbSBVICAgICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiB0aGUgYE9rYCBvZiB0aGUgYGFuZFJlc3VsdGAsXG4gICAgICAgICAgICAgICAgICAgaS5lLiB0aGUgc3VjY2VzcyB0eXBlIG9mIHRoZSBgUmVzdWx0YCBwcmVzZW50IGlmIHRoZSBjaGVja2VkXG4gICAgICAgICAgICAgICAgICAgYFJlc3VsdGAgaXMgYE9rYC5cbiAgQHR5cGVwYXJhbSBFICAgICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiB0aGUgYEVycmAgb2YgdGhlIGBSZXN1bHRgLlxuICBAcGFyYW0gYW5kUmVzdWx0IFRoZSBgUmVzdWx0YCBpbnN0YW5jZSB0byByZXR1cm4gaWYgYHJlc3VsdGAgaXMgYEVycmAuXG4gIEBwYXJhbSByZXN1bHQgICAgVGhlIGBSZXN1bHRgIGluc3RhbmNlIHRvIGNoZWNrLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYW5kPFQsIFUsIEU+KGFuZFJlc3VsdDogUmVzdWx0PFUsIEU+LCByZXN1bHQ6IFJlc3VsdDxULCBFPik6IFJlc3VsdDxVLCBFPjtcbmV4cG9ydCBmdW5jdGlvbiBhbmQ8VCwgVSwgRT4oYW5kUmVzdWx0OiBSZXN1bHQ8VSwgRT4pOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxVLCBFPjtcbmV4cG9ydCBmdW5jdGlvbiBhbmQ8VCwgVSwgRT4oXG4gIGFuZFJlc3VsdDogUmVzdWx0PFUsIEU+LFxuICByZXN1bHQ/OiBSZXN1bHQ8VCwgRT5cbik6IFJlc3VsdDxVLCBFPiB8ICgocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxVLCBFPikge1xuICBjb25zdCBvcCA9IChyOiBSZXN1bHQ8VCwgRT4pID0+IChpc09rKHIpID8gYW5kUmVzdWx0IDogKHIgYXMgRXJyPGFueSwgRT4pKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgcmVzdWx0KTtcbn1cblxuLyoqXG4gIEFwcGx5IGEgZnVuY3Rpb24gdG8gdGhlIHdyYXBwZWQgdmFsdWUgaWYgYE9rYCBhbmQgcmV0dXJuIGEgbmV3IGBPa2BcbiAgY29udGFpbmluZyB0aGUgcmVzdWx0aW5nIHZhbHVlOyBvciBpZiBpdCBpcyBgRXJyYCByZXR1cm4gaXQgdW5tb2RpZmllZC5cblxuICBUaGlzIGRpZmZlcnMgZnJvbSBgbWFwYCBpbiB0aGF0IGB0aGVuRm5gIHJldHVybnMgYW5vdGhlciBgUmVzdWx0YC4gWW91IGNhbiB1c2VcbiAgYGFuZFRoZW5gIHRvIGNvbWJpbmUgdHdvIGZ1bmN0aW9ucyB3aGljaCAqYm90aCogY3JlYXRlIGEgYFJlc3VsdGAgZnJvbSBhblxuICB1bndyYXBwZWQgdHlwZS5cblxuICBZb3UgbWF5IGZpbmQgdGhlIGAudGhlbmAgbWV0aG9kIG9uIGFuIEVTNiBgUHJvbWlzZWAgaGVscGZ1bCBmb3IgY29tcGFyaXNvbjogaWZcbiAgeW91IGhhdmUgYSBgUHJvbWlzZWAsIHlvdSBjYW4gcGFzcyBpdHMgYHRoZW5gIG1ldGhvZCBhIGNhbGxiYWNrIHdoaWNoXG4gIHJldHVybnMgYW5vdGhlciBgUHJvbWlzZWAsIGFuZCB0aGUgcmVzdWx0IHdpbGwgbm90IGJlIGEgKm5lc3RlZCogcHJvbWlzZSwgYnV0XG4gIGEgc2luZ2xlIGBQcm9taXNlYC4gVGhlIGRpZmZlcmVuY2UgaXMgdGhhdCBgUHJvbWlzZSN0aGVuYCB1bndyYXBzICphbGwqXG4gIGxheWVycyB0byBvbmx5IGV2ZXIgcmV0dXJuIGEgc2luZ2xlIGBQcm9taXNlYCB2YWx1ZSwgd2hlcmVhcyBgUmVzdWx0LmFuZFRoZW5gXG4gIHdpbGwgbm90IHVud3JhcCBuZXN0ZWQgYFJlc3VsdGBzLlxuXG4gIFRoaXMgaXMgYWxzbyBjb21tb25seSBrbm93biBhcyAoYW5kIHRoZXJlZm9yZSBhbGlhc2VkIGFzKSBbYGZsYXRNYXBgXSBvclxuICBbYGNoYWluYF0uIEl0IGlzIHNvbWV0aW1lcyBhbHNvIGtub3duIGFzIGBiaW5kYCwgYnV0ICpub3QqIGFsaWFzZWQgYXMgc3VjaFxuICBiZWNhdXNlIFtgYmluZGAgYWxyZWFkeSBtZWFucyBzb21ldGhpbmcgaW4gSmF2YVNjcmlwdF1bYmluZF0uXG5cbiAgW2BmbGF0TWFwYF06ICNmbGF0bWFwXG4gIFtgY2hhaW5gXTogI2NoYWluXG4gIFtiaW5kXTogaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvSmF2YVNjcmlwdC9SZWZlcmVuY2UvR2xvYmFsX09iamVjdHMvRnVuY3Rpb24vYmluZFxuXG4gICMjIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBpbXBvcnQgeyBvaywgZXJyLCBhbmRUaGVuLCB0b1N0cmluZyB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuXG4gIGNvbnN0IHRvTGVuZ3RoQXNSZXN1bHQgPSAoczogc3RyaW5nKSA9PiBvayhzLmxlbmd0aCk7XG5cbiAgY29uc3QgYW5PayA9IG9rKCdqdXN0IGEgc3RyaW5nJyk7XG4gIGNvbnN0IGxlbmd0aEFzUmVzdWx0ID0gYW5kVGhlbih0b0xlbmd0aEFzUmVzdWx0LCBhbk9rKTtcbiAgY29uc29sZS5sb2codG9TdHJpbmcobGVuZ3RoQXNSZXN1bHQpKTsgIC8vIE9rKDEzKVxuXG4gIGNvbnN0IGFuRXJyID0gZXJyKFsnc3JzbHknLCAnd2hhdGV2ZXInXSk7XG4gIGNvbnN0IG5vdExlbmd0aEFzUmVzdWx0ID0gYW5kVGhlbih0b0xlbmd0aEFzUmVzdWx0LCBhbkVycik7XG4gIGNvbnNvbGUubG9nKHRvU3RyaW5nKG5vdExlbmd0aEFzUmVzdWx0KSk7ICAvLyBFcnIoc3JzbHksd2hhdGV2ZXIpXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgIFRoZSB0eXBlIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgT2tgIG9mIHRoZSBgUmVzdWx0YC5cbiAgQHR5cGVwYXJhbSBVICAgVGhlIHR5cGUgb2YgdGhlIHZhbHVlIHdyYXBwZWQgaW4gdGhlIGBPa2Agb2YgdGhlIGBSZXN1bHRgXG4gICAgICAgICAgICAgICAgIHJldHVybmVkIGJ5IHRoZSBgdGhlbkZuYC5cbiAgQHR5cGVwYXJhbSBFICAgVGhlIHR5cGUgb2YgdGhlIHZhbHVlIHdyYXBwZWQgaW4gdGhlIGBFcnJgIG9mIHRoZSBgUmVzdWx0YC5cbiAgQHBhcmFtIHRoZW5GbiAgVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IHRvIHRoZSB3cmFwcGVkIGBUYCBpZiBgbWF5YmVgIGlzIGBKdXN0YC5cbiAgQHBhcmFtIHJlc3VsdCAgVGhlIGBNYXliZWAgdG8gZXZhbHVhdGUgYW5kIHBvc3NpYmx5IGFwcGx5IGEgZnVuY3Rpb24gdG8uXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhbmRUaGVuPFQsIFUsIEU+KFxuICB0aGVuRm46ICh0OiBUKSA9PiBSZXN1bHQ8VSwgRT4sXG4gIHJlc3VsdDogUmVzdWx0PFQsIEU+XG4pOiBSZXN1bHQ8VSwgRT47XG5leHBvcnQgZnVuY3Rpb24gYW5kVGhlbjxULCBVLCBFPihcbiAgdGhlbkZuOiAodDogVCkgPT4gUmVzdWx0PFUsIEU+XG4pOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxVLCBFPjtcbmV4cG9ydCBmdW5jdGlvbiBhbmRUaGVuPFQsIFUsIEU+KFxuICB0aGVuRm46ICh0OiBUKSA9PiBSZXN1bHQ8VSwgRT4sXG4gIHJlc3VsdD86IFJlc3VsdDxULCBFPlxuKTogUmVzdWx0PFUsIEU+IHwgKChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gUmVzdWx0PFUsIEU+KSB7XG4gIGNvbnN0IG9wID0gKHI6IFJlc3VsdDxULCBFPikgPT4gKGlzT2socikgPyB0aGVuRm4oci52YWx1ZSkgOiAociBhcyBFcnI8YW55LCBFPikpO1xuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgYW5kVGhlbmBdKCNhbmR0aGVuKS4gKi9cbmV4cG9ydCBjb25zdCBjaGFpbiA9IGFuZFRoZW47XG5cbi8qKiBBbGlhcyBmb3IgW2BhbmRUaGVuYF0oI2FuZHRoZW4pLiAqL1xuZXhwb3J0IGNvbnN0IGZsYXRNYXAgPSBhbmRUaGVuO1xuXG4vKipcbiAgUHJvdmlkZSBhIGZhbGxiYWNrIGZvciBhIGdpdmVuIGBSZXN1bHRgLiBCZWhhdmVzIGxpa2UgYSBsb2dpY2FsIGBvcmA6IGlmIHRoZVxuICBgcmVzdWx0YCB2YWx1ZSBpcyBhbiBgT2tgLCByZXR1cm5zIHRoYXQgYHJlc3VsdGA7IG90aGVyd2lzZSwgcmV0dXJucyB0aGVcbiAgYGRlZmF1bHRSZXN1bHRgIHZhbHVlLlxuXG4gIFRoaXMgaXMgdXNlZnVsIHdoZW4geW91IHdhbnQgdG8gbWFrZSBzdXJlIHRoYXQgc29tZXRoaW5nIHdoaWNoIHRha2VzIGFcbiAgYFJlc3VsdGAgYWx3YXlzIGVuZHMgdXAgZ2V0dGluZyBhbiBgT2tgIHZhcmlhbnQsIGJ5IHN1cHBseWluZyBhIGRlZmF1bHQgdmFsdWVcbiAgZm9yIHRoZSBjYXNlIHRoYXQgeW91IGN1cnJlbnRseSBoYXZlIGFuIGBFcnJgLlxuXG4gIGBgYHRzXG4gIGltcG9ydCB7IG9rLCBlcnIsIFJlc3VsdCwgb3IgfSBmcm9tICd0cnVlLXV0aWxzL3Jlc3VsdCc7XG5cbiAgY29uc3Qgb2tBID0gb2s8c3RyaW5nLCBzdHJpbmc+KCdhJyk7XG4gIGNvbnN0IG9rQiA9IG9rPHN0cmluZywgc3RyaW5nPignYicpO1xuICBjb25zdCBhbkVyciA9IGVycjxzdHJpbmcsIHN0cmluZz4oJzp3YXQ6Jyk7XG4gIGNvbnN0IGFub3RoZXJFcnIgPSBlcnI8c3RyaW5nLCBzdHJpbmc+KCc6aGVhZGRlc2s6Jyk7XG5cbiAgY29uc29sZS5sb2cob3Iob2tCLCBva0EpLnRvU3RyaW5nKCkpOyAgLy8gT2soQSlcbiAgY29uc29sZS5sb2cob3IoYW5FcnIsIG9rQSkudG9TdHJpbmcoKSk7ICAvLyBPayhBKVxuICBjb25zb2xlLmxvZyhvcihva0IsIGFuRXJyKS50b1N0cmluZygpKTsgIC8vIE9rKEIpXG4gIGNvbnNvbGUubG9nKG9yKGFub3RoZXJFcnIsIGFuRXJyKS50b1N0cmluZygpKTsgIC8vIEVycig6aGVhZGRlc2s6KVxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgICAgICAgICAgVGhlIHR5cGUgd3JhcHBlZCBpbiB0aGUgYE9rYCBjYXNlIG9mIGByZXN1bHRgLlxuICBAdHlwZXBhcmFtIEUgICAgICAgICAgVGhlIHR5cGUgd3JhcHBlZCBpbiB0aGUgYEVycmAgY2FzZSBvZiBgcmVzdWx0YC5cbiAgQHR5cGVwYXJhbSBGICAgICAgICAgIFRoZSB0eXBlIHdyYXBwZWQgaW4gdGhlIGBFcnJgIGNhc2Ugb2YgYGRlZmF1bHRSZXN1bHRgLlxuICBAcGFyYW0gZGVmYXVsdFJlc3VsdCAgVGhlIGBSZXN1bHRgIHRvIHVzZSBpZiBgcmVzdWx0YCBpcyBhbiBgRXJyYC5cbiAgQHBhcmFtIHJlc3VsdCAgICAgICAgIFRoZSBgUmVzdWx0YCBpbnN0YW5jZSB0byBjaGVjay5cbiAgQHJldHVybnMgICAgICAgICAgICAgIGByZXN1bHRgIGlmIGl0IGlzIGFuIGBPa2AsIG90aGVyd2lzZSBgZGVmYXVsdFJlc3VsdGAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBvcjxULCBFLCBGPihkZWZhdWx0UmVzdWx0OiBSZXN1bHQ8VCwgRj4sIHJlc3VsdDogUmVzdWx0PFQsIEU+KTogUmVzdWx0PFQsIEY+O1xuZXhwb3J0IGZ1bmN0aW9uIG9yPFQsIEUsIEY+KGRlZmF1bHRSZXN1bHQ6IFJlc3VsdDxULCBGPik6IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gUmVzdWx0PFQsIEY+O1xuZXhwb3J0IGZ1bmN0aW9uIG9yPFQsIEUsIEY+KFxuICBkZWZhdWx0UmVzdWx0OiBSZXN1bHQ8VCwgRj4sXG4gIHJlc3VsdD86IFJlc3VsdDxULCBFPlxuKTogUmVzdWx0PFQsIEY+IHwgKChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gUmVzdWx0PFQsIEY+KSB7XG4gIGNvbnN0IG9wID0gKHI6IFJlc3VsdDxULCBFPikgPT4gKGlzT2socikgPyAociBhcyBPazxULCBhbnk+KSA6IGRlZmF1bHRSZXN1bHQpO1xuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKipcbiAgTGlrZSBgb3JgLCBidXQgdXNpbmcgYSBmdW5jdGlvbiB0byBjb25zdHJ1Y3QgdGhlIGFsdGVybmF0aXZlIGBSZXN1bHRgLlxuXG4gIFNvbWV0aW1lcyB5b3UgbmVlZCB0byBwZXJmb3JtIGFuIG9wZXJhdGlvbiB1c2luZyBvdGhlciBkYXRhIGluIHRoZSBlbnZpcm9ubWVudFxuICB0byBjb25zdHJ1Y3QgdGhlIGZhbGxiYWNrIHZhbHVlLiBJbiB0aGVzZSBzaXR1YXRpb25zLCB5b3UgY2FuIHBhc3MgYSBmdW5jdGlvblxuICAod2hpY2ggbWF5IGJlIGEgY2xvc3VyZSkgYXMgdGhlIGBlbHNlRm5gIHRvIGdlbmVyYXRlIHRoZSBmYWxsYmFjayBgUmVzdWx0PFQ+YC5cbiAgSXQgY2FuIHRoZW4gdHJhbnNmb3JtIHRoZSBkYXRhIGluIHRoZSBgRXJyYCB0byBzb21ldGhpbmcgdXNhYmxlIGFzIGFuIGBPa2AsIG9yXG4gIGdlbmVyYXRlIGEgbmV3IGBFcnJgIGluc3RhbmNlIGFzIGFwcHJvcHJpYXRlLlxuXG4gIFVzZWZ1bCBmb3IgdHJhbnNmb3JtaW5nIGZhaWx1cmVzIHRvIHVzYWJsZSBkYXRhLlxuXG4gIEBwYXJhbSBlbHNlRm4gVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IHRvIHRoZSBjb250ZW50cyBvZiB0aGUgYEVycmAgaWYgYHJlc3VsdGBcbiAgICAgICAgICAgICAgICBpcyBhbiBgRXJyYCwgdG8gY3JlYXRlIGEgbmV3IGBSZXN1bHRgLlxuICBAcGFyYW0gcmVzdWx0IFRoZSBgUmVzdWx0YCB0byB1c2UgaWYgaXQgaXMgYW4gYE9rYC5cbiAgQHJldHVybnMgICAgICBUaGUgYHJlc3VsdGAgaWYgaXQgaXMgYE9rYCwgb3IgdGhlIGBSZXN1bHRgIHJldHVybmVkIGJ5IGBlbHNlRm5gXG4gICAgICAgICAgICAgICAgaWYgYHJlc3VsdGAgaXMgYW4gYEVyci5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG9yRWxzZTxULCBFLCBGPihcbiAgZWxzZUZuOiAoZXJyOiBFKSA9PiBSZXN1bHQ8VCwgRj4sXG4gIHJlc3VsdDogUmVzdWx0PFQsIEU+XG4pOiBSZXN1bHQ8VCwgRj47XG5leHBvcnQgZnVuY3Rpb24gb3JFbHNlPFQsIEUsIEY+KFxuICBlbHNlRm46IChlcnI6IEUpID0+IFJlc3VsdDxULCBGPlxuKTogKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBSZXN1bHQ8VCwgRj47XG5leHBvcnQgZnVuY3Rpb24gb3JFbHNlPFQsIEUsIEY+KFxuICBlbHNlRm46IChlcnI6IEUpID0+IFJlc3VsdDxULCBGPixcbiAgcmVzdWx0PzogUmVzdWx0PFQsIEU+XG4pOiBSZXN1bHQ8VCwgRj4gfCAoKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBSZXN1bHQ8VCwgRj4pIHtcbiAgY29uc3Qgb3AgPSAocjogUmVzdWx0PFQsIEU+KSA9PiAoaXNPayhyKSA/IChyIGFzIE9rPFQsIGFueT4pIDogZWxzZUZuKHIudW5zYWZlbHlVbndyYXBFcnIoKSkpO1xuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKipcbiAgR2V0IHRoZSB2YWx1ZSBvdXQgb2YgdGhlIGBSZXN1bHRgLlxuXG4gIFJldHVybnMgdGhlIGNvbnRlbnQgb2YgYW4gYE9rYCwgYnV0ICoqdGhyb3dzIGlmIHRoZSBgUmVzdWx0YCBpcyBgRXJyYC4qKlxuICBQcmVmZXIgdG8gdXNlIFtgdW53cmFwT3JgXSgjdW53cmFwb3IpIG9yIFtgdW53cmFwT3JFbHNlYF0oI3Vud3JhcG9yZWxzZSkuXG5cbiAgQHRocm93cyBJZiB0aGUgYFJlc3VsdGAgaW5zdGFuY2UgaXMgYE5vdGhpbmdgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdW5zYWZlbHlVbndyYXA8VCwgRT4ocmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBUIHtcbiAgcmV0dXJuIHJlc3VsdC51bnNhZmVseVVud3JhcCgpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgdW5zYWZlbHlVbndyYXBgXSgjdW5zYWZlbHl1bndyYXApICovXG5leHBvcnQgY29uc3QgdW5zYWZlbHlHZXQgPSB1bnNhZmVseVVud3JhcDtcblxuLyoqIEFsaWFzIGZvciBbYHVuc2FmZWx5VW53cmFwYF0oI3Vuc2FmZWx5dW53cmFwKSAqL1xuZXhwb3J0IGNvbnN0IHVuc2FmZUdldCA9IHVuc2FmZWx5VW53cmFwO1xuXG4vKipcbiAgR2V0IHRoZSBlcnJvciB2YWx1ZSBvdXQgb2YgdGhlIFtgUmVzdWx0YF0oI3Jlc3VsdCkuXG5cbiAgUmV0dXJucyB0aGUgY29udGVudCBvZiBhbiBgRXJyYCwgYnV0ICoqdGhyb3dzIGlmIHRoZSBgUmVzdWx0YCBpcyBgT2tgKiouXG4gIFByZWZlciB0byB1c2UgW2B1bndyYXBPckVsc2VgXSgjdW53cmFwb3JlbHNlKS5cblxuICBAcGFyYW0gcmVzdWx0XG4gIEB0aHJvd3MgRXJyb3IgSWYgdGhlIGBSZXN1bHRgIGluc3RhbmNlIGlzIGBOb3RoaW5nYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHVuc2FmZWx5VW53cmFwRXJyPFQsIEU+KHJlc3VsdDogUmVzdWx0PFQsIEU+KTogRSB7XG4gIHJldHVybiByZXN1bHQudW5zYWZlbHlVbndyYXBFcnIoKTtcbn1cblxuLyoqIEFsaWFzIGZvciBbYHVuc2FmZWx5VW53cmFwRXJyYF0oI3Vuc2FmZWx5dW53cmFwZXJyKSAqL1xuZXhwb3J0IGNvbnN0IHVuc2FmZWx5R2V0RXJyID0gdW5zYWZlbHlVbndyYXBFcnI7XG5cbi8qKlxuICBTYWZlbHkgZ2V0IHRoZSB2YWx1ZSBvdXQgb2YgdGhlIGBPa2AgdmFyaWFudCBvZiBhIFtgUmVzdWx0YF0oI3Jlc3VsdCkuXG5cbiAgVGhpcyBpcyB0aGUgcmVjb21tZW5kZWQgd2F5IHRvIGdldCBhIHZhbHVlIG91dCBvZiBhIGBSZXN1bHRgIG1vc3Qgb2YgdGhlIHRpbWUuXG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsgb2ssIGVyciwgdW53cmFwT3IgfSBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcblxuICBjb25zdCBhbk9rID0gb2s8bnVtYmVyLCBzdHJpbmc+KDEyKTtcbiAgY29uc29sZS5sb2codW53cmFwT3IoMCwgYW5PaykpOyAgLy8gMTJcblxuICBjb25zdCBhbkVyciA9IGVycjxudW1iZXIsIHN0cmluZz4oJ25vb29vbycpO1xuICBjb25zb2xlLmxvZyh1bndyYXBPcigwLCBhbkVycikpOyAgLy8gMFxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgICAgICAgIFRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgT2tgLlxuICBAdHlwZXBhcmFtIEUgICAgICAgIFRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgRXJyYC5cbiAgQHBhcmFtIGRlZmF1bHRWYWx1ZSBUaGUgdmFsdWUgdG8gdXNlIGlmIGByZXN1bHRgIGlzIGFuIGBFcnJgLlxuICBAcGFyYW0gcmVzdWx0ICAgICAgIFRoZSBgUmVzdWx0YCBpbnN0YW5jZSB0byB1bndyYXAgaWYgaXQgaXMgYW4gYE9rYC5cbiAgQHJldHVybnMgICAgICAgICAgICBUaGUgY29udGVudCBvZiBgcmVzdWx0YCBpZiBpdCBpcyBhbiBgT2tgLCBvdGhlcndpc2VcbiAgICAgICAgICAgICAgICAgICAgICBgZGVmYXVsdFZhbHVlYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yPFQsIEU+KGRlZmF1bHRWYWx1ZTogVCwgcmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBUO1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yPFQsIEU+KGRlZmF1bHRWYWx1ZTogVCk6IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gVDtcbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPcjxULCBFPihcbiAgZGVmYXVsdFZhbHVlOiBULFxuICByZXN1bHQ/OiBSZXN1bHQ8VCwgRT5cbik6IFQgfCAoKHJlc3VsdDogUmVzdWx0PFQsIEU+KSA9PiBUKSB7XG4gIGNvbnN0IG9wID0gKHI6IFJlc3VsdDxULCBFPikgPT4gKGlzT2socikgPyByLnZhbHVlIDogZGVmYXVsdFZhbHVlKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgcmVzdWx0KTtcbn1cblxuLyoqIEFsaWFzIGZvciBbYHVud3JhcE9yYF0oI3Vud3JhcG9yKSAqL1xuZXhwb3J0IGNvbnN0IGdldE9yID0gdW53cmFwT3I7XG5cbi8qKlxuICBTYWZlbHkgZ2V0IHRoZSB2YWx1ZSBvdXQgb2YgYSBbYFJlc3VsdGBdKCNyZXN1bHQpIGJ5IHJldHVybmluZyB0aGUgd3JhcHBlZFxuICB2YWx1ZSBpZiBpdCBpcyBgT2tgLCBvciBieSBhcHBseWluZyBgb3JFbHNlRm5gIHRvIHRoZSB2YWx1ZSBpbiB0aGUgYEVycmAuXG5cbiAgVGhpcyBpcyB1c2VmdWwgd2hlbiB5b3UgbmVlZCB0byAqZ2VuZXJhdGUqIGEgdmFsdWUgKGUuZy4gYnkgdXNpbmcgY3VycmVudFxuICB2YWx1ZXMgaW4gdGhlIGVudmlyb25tZW50IOKAkyB3aGV0aGVyIHByZWxvYWRlZCBvciBieSBsb2NhbCBjbG9zdXJlKSBpbnN0ZWFkIG9mXG4gIGhhdmluZyBhIHNpbmdsZSBkZWZhdWx0IHZhbHVlIGF2YWlsYWJsZSAoYXMgaW4gW2B1bndyYXBPcmBdKCN1bndyYXBvcikpLlxuXG4gIGBgYHRzXG4gIGltcG9ydCB7IG9rLCBlcnIsIHVud3JhcE9yRWxzZSB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuXG4gIC8vIFlvdSBjYW4gaW1hZ2luZSB0aGF0IHNvbWVPdGhlclZhbHVlIG1pZ2h0IGJlIGR5bmFtaWMuXG4gIGNvbnN0IHNvbWVPdGhlclZhbHVlID0gMjtcbiAgY29uc3QgaGFuZGxlRXJyID0gKGVyclZhbHVlOiBzdHJpbmcpID0+IGVyclZhbHVlLmxlbmd0aCArIHNvbWVPdGhlclZhbHVlO1xuXG4gIGNvbnN0IGFuT2sgPSBvazxudW1iZXIsIHN0cmluZz4oNDIpO1xuICBjb25zb2xlLmxvZyh1bndyYXBPckVsc2UoaGFuZGxlRXJyLCBhbk9rKSk7ICAvLyA0MlxuXG4gIGNvbnN0IGFuRXJyID0gZXJyPG51bWJlciwgc3RyaW5nPignb2ggdGVoIG5vZXMnKTtcbiAgY29uc29sZS5sb2codW53cmFwT3JFbHNlKGhhbmRsZUVyciwgYW5FcnIpKTsgIC8vIDEzXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICBUaGUgdmFsdWUgd3JhcHBlZCBpbiB0aGUgYE9rYC5cbiAgQHR5cGVwYXJhbSBFICAgIFRoZSB2YWx1ZSB3cmFwcGVkIGluIHRoZSBgRXJyYC5cbiAgQHBhcmFtIG9yRWxzZUZuIEEgZnVuY3Rpb24gYXBwbGllZCB0byB0aGUgdmFsdWUgd3JhcHBlZCBpbiBgcmVzdWx0YCBpZiBpdCBpc1xuICAgICAgICAgICAgICAgICAgYW4gYEVycmAsIHRvIGdlbmVyYXRlIHRoZSBmaW5hbCB2YWx1ZS5cbiAgQHBhcmFtIHJlc3VsdCAgIFRoZSBgcmVzdWx0YCB0byB1bndyYXAgaWYgaXQgaXMgYW4gYE9rYC5cbiAgQHJldHVybnMgICAgICAgIFRoZSB2YWx1ZSB3cmFwcGVkIGluIGByZXN1bHRgIGlmIGl0IGlzIGBPa2Agb3IgdGhlIHZhbHVlXG4gICAgICAgICAgICAgICAgICByZXR1cm5lZCBieSBgb3JFbHNlRm5gIGFwcGxpZWQgdG8gdGhlIHZhbHVlIGluIGBFcnJgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3JFbHNlPFQsIEU+KG9yRWxzZUZuOiAoZXJyb3I6IEUpID0+IFQsIHJlc3VsdDogUmVzdWx0PFQsIEU+KTogVDtcbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPckVsc2U8VCwgRT4ob3JFbHNlRm46IChlcnJvcjogRSkgPT4gVCk6IChyZXN1bHQ6IFJlc3VsdDxULCBFPikgPT4gVDtcbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPckVsc2U8VCwgRT4oXG4gIG9yRWxzZUZuOiAoZXJyb3I6IEUpID0+IFQsXG4gIHJlc3VsdD86IFJlc3VsdDxULCBFPlxuKTogVCB8ICgocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFQpIHtcbiAgY29uc3Qgb3AgPSAocjogUmVzdWx0PFQsIEU+KSA9PiAoaXNPayhyKSA/IHIudmFsdWUgOiBvckVsc2VGbihyLmVycm9yKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIHJlc3VsdCk7XG59XG5cbi8qKiBBbGlhcyBmb3IgW2B1bndyYXBPckVsc2VgXSgjdW53cmFwb3JlbHNlKSAqL1xuZXhwb3J0IGNvbnN0IGdldE9yRWxzZSA9IHVud3JhcE9yRWxzZTtcblxuLyoqXG4gIENvbnZlcnQgYSBbYFJlc3VsdGBdKCNyZXN1bHQpIHRvIGEgW2BNYXliZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21heWJlKS5cblxuICBUaGUgY29udmVydGVkIHR5cGUgd2lsbCBiZSBbYEp1c3RgXSBpZiB0aGUgYFJlc3VsdGAgaXMgW2BPa2BdIG9yIFtgTm90aGluZ2BdXG4gIGlmIHRoZSBgUmVzdWx0YCBpcyBbYEVycmBdOyB0aGUgd3JhcHBlZCBlcnJvciB2YWx1ZSB3aWxsIGJlIGRpc2NhcmRlZC5cblxuICBbYEp1c3RgXTogLi4vY2xhc3Nlcy9fbWF5YmVfLmp1c3QuaHRtbFxuICBbYE5vdGhpbmdgXTogLi4vY2xhc3Nlcy9fbWF5YmVfLm5vdGhpbmcuaHRtbFxuICBbYE9rYF06IC4uL2NsYXNzZXMvX3Jlc3VsdF8ub2suaHRtbFxuICBbYEVycmBdOiAuLi9jbGFzc2VzL19yZXN1bHRfLmVyci5odG1sXG5cbiAgQHBhcmFtIHJlc3VsdCBUaGUgYFJlc3VsdGAgdG8gY29udmVydCB0byBhIGBNYXliZWBcbiAgQHJldHVybnMgICAgICBgSnVzdGAgdGhlIHZhbHVlIGluIGByZXN1bHRgIGlmIGl0IGlzIGBPa2A7IG90aGVyd2lzZSBgTm90aGluZ2BcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHRvTWF5YmU8VD4ocmVzdWx0OiBSZXN1bHQ8VCwgYW55Pik6IE1heWJlPFQ+IHtcbiAgcmV0dXJuIGlzT2socmVzdWx0KSA/IGp1c3QocmVzdWx0LnZhbHVlKSA6IG5vdGhpbmcoKTtcbn1cblxuLyoqXG4gIFRyYW5zZm9ybSBhIFtgTWF5YmVgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXliZSkgaW50byBhIFtgUmVzdWx0YF0oI3Jlc3VsdCkuXG5cbiAgSWYgdGhlIGBNYXliZWAgaXMgYSBbYEp1c3RgXSwgaXRzIHZhbHVlIHdpbGwgYmUgd3JhcHBlZCBpbiB0aGUgW2BPa2BdIHZhcmlhbnQ7XG4gIGlmIGl0IGlzIGEgW2BOb3RoaW5nYF0gdGhlIGBlcnJWYWx1ZWAgd2lsbCBiZSB3cmFwcGVkIGluIHRoZSBbYEVycmBdIHZhcmlhbnQuXG5cbiAgW2BKdXN0YF06IC4uL2NsYXNzZXMvX21heWJlXy5qdXN0Lmh0bWxcbiAgW2BOb3RoaW5nYF06IC4uL2NsYXNzZXMvX21heWJlXy5ub3RoaW5nLmh0bWxcbiAgW2BPa2BdOiAuLi9jbGFzc2VzL19yZXN1bHRfLm9rLmh0bWxcbiAgW2BFcnJgXTogLi4vY2xhc3Nlcy9fcmVzdWx0Xy5lcnIuaHRtbFxuXG4gIEBwYXJhbSBlcnJWYWx1ZSBBIHZhbHVlIHRvIHdyYXAgaW4gYW4gYEVycmAgaWYgYG1heWJlYCBpcyBhIGBOb3RoaW5nYC5cbiAgQHBhcmFtIG1heWJlICAgIFRoZSBgTWF5YmVgIHRvIGNvbnZlcnQgdG8gYSBgUmVzdWx0YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGZyb21NYXliZTxULCBFPihlcnJWYWx1ZTogRSwgbWF5YmU6IE1heWJlPFQ+KTogUmVzdWx0PFQsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIGZyb21NYXliZTxULCBFPihlcnJWYWx1ZTogRSk6IChtYXliZTogTWF5YmU8VD4pID0+IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiBmcm9tTWF5YmU8VCwgRT4oXG4gIGVyclZhbHVlOiBFLFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBSZXN1bHQ8VCwgRT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gUmVzdWx0PFQsIEU+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAoaXNKdXN0KG0pID8gb2s8VCwgRT4oTWF5YmUudW5zYWZlbHlVbndyYXAobSkpIDogZXJyPFQsIEU+KGVyclZhbHVlKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIG1heWJlKTtcbn1cblxuLyoqXG4gIENyZWF0ZSBhIGBTdHJpbmdgIHJlcHJlc2VudGF0aW9uIG9mIGEgYHJlc3VsdGAgaW5zdGFuY2UuXG5cbiAgQW4gYE9rYCBpbnN0YW5jZSB3aWxsIGJlIHByaW50ZWQgYXMgYE9rKDxyZXByZXNlbnRhdGlvbiBvZiB0aGUgdmFsdWU+KWAsIGFuZFxuICBhbiBgRXJyYCBpbnN0YW5jZSB3aWxsIGJlIHByaW50ZWQgYXMgYEVycig8cmVwcmVzZW50YXRpb24gb2YgdGhlIGVycm9yPilgLFxuICB3aGVyZSB0aGUgcmVwcmVzZW50YXRpb24gb2YgdGhlIHZhbHVlIG9yIGVycm9yIGlzIHNpbXBseSB0aGUgdmFsdWUgb3IgZXJyb3Inc1xuICBvd24gYHRvU3RyaW5nYCByZXByZXNlbnRhdGlvbi4gRm9yIGV4YW1wbGU6XG5cbiAgICAgICAgICAgICAgICBjYWxsICAgICAgICAgICAgICAgIHwgICAgICAgICBvdXRwdXRcbiAgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHwgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICBgdG9TdHJpbmcob2soNDIpKWAgICAgICAgICAgICAgICAgfCBgT2soNDIpYFxuICBgdG9TdHJpbmcob2soWzEsIDIsIDNdKSlgICAgICAgICAgfCBgT2soMSwyLDMpYFxuICBgdG9TdHJpbmcob2soeyBhbjogJ29iamVjdCcgfSkpYCAgfCBgT2soW29iamVjdCBPYmplY3RdKWBuXG4gIGB0b1N0cmluZyhlcnIoNDIpKWAgICAgICAgICAgICAgICB8IGBFcnIoNDIpYFxuICBgdG9TdHJpbmcoZXJyKFsxLCAyLCAzXSkpYCAgICAgICAgfCBgRXJyKDEsMiwzKWBcbiAgYHRvU3RyaW5nKGVycih7IGFuOiAnb2JqZWN0JyB9KSlgIHwgYEVycihbb2JqZWN0IE9iamVjdF0pYFxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZTsgaXRzIG93biBgLnRvU3RyaW5nYCB3aWxsIGJlIHVzZWRcbiAgICAgICAgICAgICAgIHRvIHByaW50IHRoZSBpbnRlcmlvciBjb250ZW50cyBvZiB0aGUgYEp1c3RgIHZhcmlhbnQuXG4gIEBwYXJhbSBtYXliZSBUaGUgdmFsdWUgdG8gY29udmVydCB0byBhIHN0cmluZy5cbiAgQHJldHVybnMgICAgIFRoZSBzdHJpbmcgcmVwcmVzZW50YXRpb24gb2YgdGhlIGBNYXliZWAuXG4gKi9cbmV4cG9ydCBjb25zdCB0b1N0cmluZyA9IDxULCBFPihyZXN1bHQ6IFJlc3VsdDxULCBFPik6IHN0cmluZyA9PiB7XG4gIGNvbnN0IGJvZHkgPSAoaXNPayhyZXN1bHQpID8gcmVzdWx0LnZhbHVlIDogcmVzdWx0LmVycm9yKS50b1N0cmluZygpO1xuICByZXR1cm4gYCR7cmVzdWx0LnZhcmlhbnQudG9TdHJpbmcoKX0oJHtib2R5fSlgO1xufTtcblxuLyoqIEEgbGlnaHR3ZWlnaHQgb2JqZWN0IGRlZmluaW5nIGhvdyB0byBoYW5kbGUgZWFjaCB2YXJpYW50IG9mIGEgTWF5YmUuICovXG5leHBvcnQgdHlwZSBNYXRjaGVyPFQsIEUsIEE+ID0ge1xuICBPazogKHZhbHVlOiBUKSA9PiBBO1xuICBFcnI6IChlcnJvcjogRSkgPT4gQTtcbn07XG5cbi8qKlxuICBQZXJmb3JtcyB0aGUgc2FtZSBiYXNpYyBmdW5jdGlvbmFsaXR5IGFzIGBnZXRPckVsc2VgLCBidXQgaW5zdGVhZCBvZiBzaW1wbHlcbiAgdW53cmFwcGluZyB0aGUgdmFsdWUgaWYgaXQgaXMgYE9rYCBhbmQgYXBwbHlpbmcgYSB2YWx1ZSB0byBnZW5lcmF0ZSB0aGUgc2FtZVxuICBkZWZhdWx0IHR5cGUgaWYgaXQgaXMgYE5vdGhpbmdgLCBsZXRzIHlvdSBzdXBwbHkgZnVuY3Rpb25zIHdoaWNoIG1heSB0cmFuc2Zvcm1cbiAgdGhlIHdyYXBwZWQgdHlwZSBpZiBpdCBpcyBgT2tgIG9yIGdldCBhIGRlZmF1bHQgdmFsdWUgZm9yIGBOb3RoaW5nYC5cblxuICBUaGlzIGlzIGtpbmQgb2YgbGlrZSBhIHBvb3IgbWFuJ3MgdmVyc2lvbiBvZiBwYXR0ZXJuIG1hdGNoaW5nLCB3aGljaFxuICBKYXZhU2NyaXB0IGN1cnJlbnRseSBsYWNrcy5cblxuICBJbnN0ZWFkIG9mIGNvZGUgbGlrZSB0aGlzOlxuXG4gIGBgYHRzXG4gIGltcG9ydCB7IFJlc3VsdCwgaXNPaywgbWF0Y2ggfSBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcblxuICBjb25zdCBsb2dWYWx1ZSA9IChtaWdodEJlQU51bWJlcjogUmVzdWx0PG51bWJlciwgc3RyaW5nPikgPT4ge1xuICAgIGNvbnNvbGUubG9nKFxuICAgICAgaXNPayhtaWdodEJlQU51bWJlcilcbiAgICAgICAgPyB1bnNhZmVseVVud3JhcChtaWdodEJlQU51bWJlcikudG9TdHJpbmcoKVxuICAgICAgICA6IGBUaGVyZSB3YXMgYW4gZXJyb3I6ICR7dW5zYWZlbHlHZXRFcnIobWlnaHRCZUFOdW1iZXIpfWBcbiAgICApO1xuICB9O1xuICBgYGBcblxuICAuLi53ZSBjYW4gd3JpdGUgY29kZSBsaWtlIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsgUmVzdWx0LCBtYXRjaCB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuXG4gIGNvbnN0IGxvZ1ZhbHVlID0gKG1pZ2h0QmVBTnVtYmVyOiBSZXN1bHQ8bnVtYmVyLCBzdHJpbmc+KSA9PiB7XG4gICAgY29uc3QgdmFsdWUgPSBtYXRjaChcbiAgICAgIHtcbiAgICAgICAgT2s6IG4gPT4gbi50b1N0cmluZygpLFxuICAgICAgICBFcnI6IGUgPT4gYFRoZXJlIHdhcyBhbiBlcnJvcjogJHtlfWAsXG4gICAgICB9LFxuICAgICAgbWlnaHRCZUFOdW1iZXJcbiAgICApO1xuICAgIGNvbnNvbGUubG9nKHZhbHVlKTtcbiAgfTtcbiAgYGBgXG5cbiAgVGhpcyBpcyBzbGlnaHRseSBsb25nZXIgdG8gd3JpdGUsIGJ1dCBjbGVhcmVyOiB0aGUgbW9yZSBjb21wbGV4IHRoZSByZXN1bHRpbmdcbiAgZXhwcmVzc2lvbiwgdGhlIGhhaXJlciBpdCBpcyB0byB1bmRlcnN0YW5kIHRoZSB0ZXJuYXJ5LiBUaHVzLCB0aGlzIGlzXG4gIGVzcGVjaWFsbHkgY29udmVuaWVudCBmb3IgdGltZXMgd2hlbiB0aGVyZSBpcyBhIGNvbXBsZXggcmVzdWx0LCBlLmcuIHdoZW5cbiAgcmVuZGVyaW5nIHBhcnQgb2YgYSBSZWFjdCBjb21wb25lbnQgaW5saW5lIGluIEpTWC9UU1guXG5cbiAgQHBhcmFtIG1hdGNoZXIgQSBsaWdodHdlaWdodCBvYmplY3QgZGVmaW5pbmcgd2hhdCB0byBkbyBpbiB0aGUgY2FzZSBvZiBlYWNoXG4gICAgICAgICAgICAgICAgIHZhcmlhbnQuXG4gIEBwYXJhbSBtYXliZSAgIFRoZSBgbWF5YmVgIGluc3RhbmNlIHRvIGNoZWNrLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWF0Y2g8VCwgRSwgQT4obWF0Y2hlcjogTWF0Y2hlcjxULCBFLCBBPiwgcmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBBO1xuZXhwb3J0IGZ1bmN0aW9uIG1hdGNoPFQsIEUsIEE+KG1hdGNoZXI6IE1hdGNoZXI8VCwgRSwgQT4pOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IEE7XG5leHBvcnQgZnVuY3Rpb24gbWF0Y2g8VCwgRSwgQT4oXG4gIG1hdGNoZXI6IE1hdGNoZXI8VCwgRSwgQT4sXG4gIHJlc3VsdD86IFJlc3VsdDxULCBFPlxuKTogQSB8ICgocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IEEpIHtcbiAgY29uc3Qgb3AgPSAocjogUmVzdWx0PFQsIEU+KSA9PiBtYXBPckVsc2UobWF0Y2hlci5FcnIsIG1hdGNoZXIuT2ssIHIpO1xuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgbWF0Y2hgXSgjbWF0Y2gpICovXG5leHBvcnQgY29uc3QgY2F0YSA9IG1hdGNoO1xuXG4vKipcbiAgQWxsb3dzIHF1aWNrIHRyaXBsZS1lcXVhbCBlcXVhbGl0eSBjaGVjayBiZXR3ZWVuIHRoZSB2YWx1ZXMgaW5zaWRlIHR3byBgcmVzdWx0YHNcbiAgd2l0aG91dCBoYXZpbmcgdG8gdW53cmFwIHRoZW0gZmlyc3QuXG5cbiAgYGBgdHNcbiAgY29uc3QgYSA9IFJlc3VsdC5vZigzKVxuICBjb25zdCBiID0gUmVzdWx0Lm9mKDMpXG4gIGNvbnN0IGMgPSBSZXN1bHQub2YobnVsbClcbiAgY29uc3QgZCA9IFJlc3VsdC5ub3RoaW5nKClcblxuICBSZXN1bHQuZXF1YWxzKGEsIGIpIC8vIHRydWVcbiAgUmVzdWx0LmVxdWFscyhhLCBjKSAvLyBmYWxzZVxuICBSZXN1bHQuZXF1YWxzKGMsIGQpIC8vIHRydWVcbiAgYGBgXG5cbiAgQHBhcmFtIHJlc3VsdEIgQSBgbWF5YmVgIHRvIGNvbXBhcmUgdG8uXG4gIEBwYXJhbSByZXN1bHRBIEEgYG1heWJlYCBpbnN0YW5jZSB0byBjaGVjay5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGVxdWFsczxULCBFPihyZXN1bHRCOiBSZXN1bHQ8VCwgRT4sIHJlc3VsdEE6IFJlc3VsdDxULCBFPik6IGJvb2xlYW47XG5leHBvcnQgZnVuY3Rpb24gZXF1YWxzPFQsIEU+KHJlc3VsdEI6IFJlc3VsdDxULCBFPik6IChyZXN1bHRBOiBSZXN1bHQ8VCwgRT4pID0+IGJvb2xlYW47XG5leHBvcnQgZnVuY3Rpb24gZXF1YWxzPFQsIEU+KFxuICByZXN1bHRCOiBSZXN1bHQ8VCwgRT4sXG4gIHJlc3VsdEE/OiBSZXN1bHQ8VCwgRT5cbik6IGJvb2xlYW4gfCAoKGE6IFJlc3VsdDxULCBFPikgPT4gYm9vbGVhbikge1xuICByZXR1cm4gcmVzdWx0QSAhPT0gdW5kZWZpbmVkXG4gICAgPyByZXN1bHRBLm1hdGNoKHtcbiAgICAgICAgRXJyOiAoKSA9PiBpc0VycihyZXN1bHRCKSxcbiAgICAgICAgT2s6IGEgPT4gaXNPayhyZXN1bHRCKSAmJiByZXN1bHRCLnVuc2FmZWx5VW53cmFwKCkgPT09IGEsXG4gICAgICB9KVxuICAgIDogKGN1cnJpZWRSZXN1bHRBOiBSZXN1bHQ8VCwgRT4pID0+XG4gICAgICAgIGN1cnJpZWRSZXN1bHRBLm1hdGNoKHtcbiAgICAgICAgICBFcnI6ICgpID0+IGlzRXJyKHJlc3VsdEIpLFxuICAgICAgICAgIE9rOiBhID0+IGlzT2socmVzdWx0QikgJiYgcmVzdWx0Qi51bnNhZmVseVVud3JhcCgpID09PSBhLFxuICAgICAgICB9KTtcbn1cblxuLyoqXG4gIEFsbG93cyB5b3UgdG8gKmFwcGx5KiAodGh1cyBgYXBgKSBhIHZhbHVlIHRvIGEgZnVuY3Rpb24gd2l0aG91dCBoYXZpbmcgdG9cbiAgdGFrZSBlaXRoZXIgb3V0IG9mIHRoZSBjb250ZXh0IG9mIHRoZWlyIGBSZXN1bHRgcy4gVGhpcyBkb2VzIG1lYW4gdGhhdCB0aGVcbiAgdHJhbnNmb3JtaW5nIGZ1bmN0aW9uIGlzIGl0c2VsZiB3aXRoaW4gYSBgUmVzdWx0YCwgd2hpY2ggY2FuIGJlIGhhcmQgdG8gZ3Jva1xuICBhdCBmaXJzdCBidXQgbGV0cyB5b3UgZG8gc29tZSB2ZXJ5IGVsZWdhbnQgdGhpbmdzLiBGb3IgZXhhbXBsZSwgYGFwYCBhbGxvd3NcbiAgeW91IHRvIGRvIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IFJlc3VsdCBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcblxuICBjb25zdCBvbmUgPSBSZXN1bHQub2s8bnVtYmVyLCBzdHJpbmc+KDEpO1xuICBjb25zdCBmaXZlID0gUmVzdWx0Lm9rPG51bWJlciwgc3RyaW5nPig1KTtcbiAgY29uc3Qgd2hvb3BzID0gUmVzdWx0LmVycjxudW1iZXIsIHN0cmluZz4oJ29oIG5vJyk7XG5cbiAgY29uc3QgYWRkID0gKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGI7XG4gIGNvbnN0IHJlc3VsdEFkZCA9IFJlc3VsdC5vazx0eXBlb2YgYWRkLCBzdHJpbmc+KGFkZCk7XG5cbiAgcmVzdWx0QWRkLmFwKG9uZSkuYXAoZml2ZSk7IC8vIE9rKDYpXG4gIHJlc3VsdEFkZC5hcChvbmUpLmFwKHdob29wcyk7IC8vIEVycignb2ggbm8nKVxuICByZXN1bHRBZGQuYXAod2hvb3BzKS5hcChmaXZlKSAvLyBFcnIoJ29oIG5vJylcbiAgYGBgXG5cbiAgV2l0aG91dCBgUmVzdWx0LmFwYCwgeW91J2QgbmVlZCB0byBkbyBzb21ldGhpbmcgbGlrZSBhIG5lc3RlZCBgUmVzdWx0Lm1hdGNoYDpcblxuICBgYGB0c1xuICBpbXBvcnQgeyBvaywgZXJyIH0gZnJvbSAndHJ1ZS1teXRoL3Jlc3VsdCc7XG5cbiAgY29uc3Qgb25lID0gb2s8bnVtYmVyLCBzdHJpbmc+KDEpO1xuICBjb25zdCBmaXZlID0gb2s8bnVtYmVyLCBzdHJpbmc+KDUpO1xuICBjb25zdCB3aG9vcHMgPSBlcnI8bnVtYmVyLCBzdHJpbmc+KCdvaCBubycpO1xuXG4gIG9uZS5tYXRjaCh7XG4gICAgT2s6IG4gPT4gZml2ZS5tYXRjaCh7XG4gICAgICBPazogbyA9PiBvazxudW1iZXIsIHN0cmluZz4obiArIG8pLFxuICAgICAgRXJyOiBlID0+IGVycjxudW1iZXIsIHN0cmluZz4oZSksXG4gICAgfSksXG4gICAgRXJyOiBlICA9PiBlcnI8bnVtYmVyLCBzdHJpbmc+KGUpLFxuICB9KTsgLy8gT2soNilcblxuICBvbmUubWF0Y2goe1xuICAgIE9rOiBuID0+IHdob29wcy5tYXRjaCh7XG4gICAgICBPazogbyA9PiBvazxudW1iZXIsIHN0cmluZz4obiArIG8pLFxuICAgICAgRXJyOiBlID0+IGVycjxudW1iZXIsIHN0cmluZz4oZSksXG4gICAgfSksXG4gICAgRXJyOiBlICA9PiBlcnI8bnVtYmVyLCBzdHJpbmc+KGUpLFxuICB9KTsgLy8gRXJyKCdvaCBubycpXG5cbiAgd2hvb3BzLm1hdGNoKHtcbiAgICBPazogbiA9PiBmaXZlLm1hdGNoKHtcbiAgICAgIE9rOiBvID0+IG9rKG4gKyBvKSxcbiAgICAgIEVycjogZSA9PiBlcnIoZSksXG4gICAgfSksXG4gICAgRXJyOiBlICA9PiBlcnIoZSksXG4gIH0pOyAvLyBFcnIoJ29oIG5vJylcbiAgYGBgXG5cbiAgQW5kIHRoaXMga2luZCBvZiB0aGluZyBjb21lcyB1cCBxdWl0ZSBvZnRlbiBvbmNlIHlvdSdyZSB1c2luZyBgTWF5YmVgIHRvXG4gIGhhbmRsZSBvcHRpb25hbGl0eSB0aHJvdWdob3V0IHlvdXIgYXBwbGljYXRpb24uXG5cbiAgRm9yIGFub3RoZXIgZXhhbXBsZSwgaW1hZ2luZSB5b3UgbmVlZCB0byBjb21wYXJlIHRoZSBlcXVhbGl0eSBvZiB0d29cbiAgSW1tdXRhYmxlSlMgZGF0YSBzdHJ1Y3R1cmVzLCB3aGVyZSBhIGA9PT1gIGNvbXBhcmlzb24gd29uJ3Qgd29yay4gV2l0aCBgYXBgLFxuICB0aGF0J3MgYXMgc2ltcGxlIGFzIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsgb2sgfSBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcbiAgaW1wb3J0IEltbXV0YWJsZSBmcm9tICdpbW11dGFibGUnO1xuICBpbXBvcnQgeyBjdXJyeSB9IGZyb20gJ2xvZGFzaCdcblxuICBjb25zdCBpcyA9IGN1cnJ5KEltbXV0YWJsZS5pcyk7XG5cbiAgY29uc3QgeCA9IG9rKEltbXV0YWJsZS5TZXQub2YoMSwgMiwgMykpO1xuICBjb25zdCB5ID0gb2soSW1tdXRhYmxlLlNldC5vZigyLCAzLCA0KSk7XG5cbiAgb2soaXMpLmFwKHgpLmFwKHkpOyAvLyBPayhmYWxzZSlcbiAgYGBgXG5cbiAgV2l0aG91dCBgYXBgLCB3ZSdyZSBiYWNrIHRvIHRoYXQgZ25hcmx5IG5lc3RlZCBgbWF0Y2hgOlxuXG4gIGBgYHRzXG4gICAqIGltcG9ydCBSZXN1bHQsIHsgb2ssIGVyciB9IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuICBpbXBvcnQgSW1tdXRhYmxlIGZyb20gJ2ltbXV0YWJsZSc7XG4gIGltcG9ydCB7IGN1cnJ5IH0gZnJvbSAnbG9kYXNoJ1xuXG4gIGNvbnN0IGlzID0gY3VycnkoSW1tdXRhYmxlLmlzKTtcblxuICBjb25zdCB4ID0gb2soSW1tdXRhYmxlLlNldC5vZigxLCAyLCAzKSk7XG4gIGNvbnN0IHkgPSBvayhJbW11dGFibGUuU2V0Lm9mKDIsIDMsIDQpKTtcblxuICB4Lm1hdGNoKHtcbiAgICBPazogaVggPT4geS5tYXRjaCh7XG4gICAgICBPazogaVkgPT4gUmVzdWx0Lm9mKEltbXV0YWJsZS5pcyhpWCwgaVkpKSxcbiAgICAgIEVycjogKGUpID0+IG9rKGZhbHNlKSxcbiAgICB9KVxuICAgIEVycjogKGUpID0+IG9rKGZhbHNlKSxcbiAgfSk7IC8vIE9rKGZhbHNlKVxuICBgYGBcblxuICBJbiBzdW1tYXJ5OiBhbnl3aGVyZSB5b3UgaGF2ZSB0d28gYE1heWJlYCBpbnN0YW5jZXMgYW5kIG5lZWQgdG8gcGVyZm9ybSBhblxuICBvcGVyYXRpb24gdGhhdCB1c2VzIGJvdGggb2YgdGhlbSwgYGFwYCBpcyB5b3VyIGZyaWVuZC5cblxuICBUd28gdGhpbmdzIHRvIG5vdGUsIGJvdGggcmVnYXJkaW5nICpjdXJyeWluZyo6XG5cbiAgMS4gIEFsbCBmdW5jdGlvbnMgcGFzc2VkIHRvIGBhcGAgbXVzdCBiZSBjdXJyaWVkLiBUaGF0IGlzLCB0aGV5IG11c3QgYmUgb2YgdGhlXG4gICAgICBmb3JtIChmb3IgYWRkKSBgKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGJgLCAqbm90KiB0aGUgbW9yZSB1c3VhbFxuICAgICAgYChhOiBudW1iZXIsIGI6IG51bWJlcikgPT4gYSArIGJgIHlvdSBzZWUgaW4gSmF2YVNjcmlwdCBtb3JlIGdlbmVyYWxseS5cblxuICAgICAgRm9yIGNvbnZlbmllbmNlLCB5b3UgbWF5IHdhbnQgdG8gbG9vayBhdCBMb2Rhc2gncyBgXy5jdXJyeWAgb3IgUmFtZGEnc1xuICAgICAgYFIuY3VycnlgLCB3aGljaCBhbGxvdyB5b3UgdG8gY3JlYXRlIGN1cnJpZWQgdmVyc2lvbnMgb2YgZnVuY3Rpb25zXG4gICAgICB3aGVuZXZlciB5b3Ugd2FudDpcblxuICAgICAgYGBgXG4gICAgICBpbXBvcnQgUmVzdWx0IGZyb20gJ3RydWUtbXl0aC9yZXN1bHQnO1xuICAgICAgaW1wb3J0IHsgY3VycnkgfSBmcm9tICdsb2Rhc2gnO1xuXG4gICAgICBjb25zdCBub3JtYWxBZGQgPSAoYTogbnVtYmVyLCBiOiBudW1iZXIpID0+IGEgKyBiO1xuICAgICAgY29uc3QgY3VycmllZEFkZCA9IGN1cnJ5KG5vcm1hbEFkZCk7IC8vIChhOiBudW1iZXIpID0+IChiOiBudW1iZXIpID0+IGEgKyBiO1xuXG4gICAgICBSZXN1bHQub2YoY3VycmllZEFkZCkuYXAoUmVzdWx0Lm9mKDEpKS5hcChSZXN1bHQub2YoNSkpOyAvLyBPayg2KVxuICAgICAgYGBgXG5cbiAgMi4gIFlvdSB3aWxsIG5lZWQgdG8gY2FsbCBgYXBgIGFzIG1hbnkgdGltZXMgYXMgdGhlcmUgYXJlIGFyZ3VtZW50cyB0byB0aGVcbiAgICAgIGZ1bmN0aW9uIHlvdSdyZSBkZWFsaW5nIHdpdGguIFNvIGluIHRoZSBjYXNlIG9mIGBhZGRgLCB3aGljaCBoYXMgdGhlXG4gICAgICBcImFyaXR5XCIgKGZ1bmN0aW9uIGFyZ3VtZW50IGNvdW50KSBvZiAyIChgYWAgYW5kIGBiYCksIHlvdSdsbCBuZWVkIHRvIGNhbGxcbiAgICAgIGBhcGAgdHdpY2U6IG9uY2UgZm9yIGBhYCwgYW5kIG9uY2UgZm9yIGBiYC4gVG8gc2VlIHdoeSwgbGV0J3MgbG9vayBhdCB3aGF0XG4gICAgICB0aGUgcmVzdWx0IGluIGVhY2ggcGhhc2UgaXM6XG5cbiAgICAgIGBgYHRzXG4gICAgICBjb25zdCBhZGQgPSAoYTogbnVtYmVyKSA9PiAoYjogbnVtYmVyKSA9PiBhICsgYjtcblxuICAgICAgY29uc3QgbWF5YmVBZGQgPSBSZXN1bHQub2YoYWRkKTsgLy8gT2soKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGIpXG4gICAgICBjb25zdCBtYXliZUFkZDEgPSBtYXliZUFkZC5hcChSZXN1bHQub2YoMSkpOyAvLyBPaygoYjogbnVtYmVyKSA9PiAxICsgYilcbiAgICAgIGNvbnN0IGZpbmFsID0gbWF5YmVBZGQxLmFwKFJlc3VsdC5vZigzKSk7IC8vIE9rKDQpXG4gICAgICBgYGBcblxuICAgICAgU28gZm9yIGB0b1N0cmluZ2AsIHdoaWNoIGp1c3QgdGFrZXMgYSBzaW5nbGUgYXJndW1lbnQsIHlvdSB3b3VsZCBvbmx5IG5lZWRcbiAgICAgIHRvIGNhbGwgYGFwYCBvbmNlLlxuXG4gICAgICBgYGB0c1xuICAgICAgY29uc3QgdG9TdHIgPSAodjogeyB0b1N0cmluZygpOiBzdHJpbmcgfSkgPT4gdi50b1N0cmluZygpO1xuICAgICAgUmVzdWx0Lm9mKHRvU3RyKS5hcCgxMik7IC8vIE9rKFwiMTJcIilcbiAgICAgIGBgYFxuXG4gIE9uZSBvdGhlciBzY2VuYXJpbyB3aGljaCBkb2Vzbid0IGNvbWUgdXAgKnF1aXRlKiBhcyBvZnRlbiBidXQgaXMgY29uY2VpdmFibGVcbiAgaXMgd2hlcmUgeW91IGhhdmUgc29tZXRoaW5nIHRoYXQgbWF5IG9yIG1heSBub3QgYWN0dWFsbHkgY29uc3RydWN0IGEgZnVuY3Rpb25cbiAgZm9yIGhhbmRsaW5nIGEgc3BlY2lmaWMgYFJlc3VsdGAgc2NlbmFyaW8uIEluIHRoYXQgY2FzZSwgeW91IGNhbiB3cmFwIHRoZVxuICBwb3NzaWJseS1wcmVzZW50IGluIGBhcGAgYW5kIHRoZW4gd3JhcCB0aGUgdmFsdWVzIHRvIGFwcGx5IHRvIHRoZSBmdW5jdGlvbiB0b1xuICBpbiBgUmVzdWx0YCB0aGVtc2VsdmVzLlxuXG4gIEJlY2F1c2UgYFJlc3VsdGAgb2Z0ZW4gcmVxdWlyZXMgeW91IHRvIHR5cGUgb3V0IHRoZSBmdWxsIHR5cGUgcGFyYW1ldGVyaXphdGlvblxuICBvbiBhIHJlZ3VsYXIgYmFzaXMsIGl0J3MgY29udmVuaWVudCB0byB1c2UgVHlwZVNjcmlwdCdzIGB0eXBlb2ZgIG9wZXJhdG9yIHRvXG4gIHdyaXRlIG91dCB0aGUgdHlwZSBvZiBhIGN1cnJpZWQgZnVuY3Rpb24uIEZvciBleGFtcGxlLCBpZiB5b3UgaGFkIGEgZnVuY3Rpb25cbiAgdGhhdCBzaW1wbHkgbWVyZ2VkIHRocmVlIHN0cmluZ3MsIHlvdSBtaWdodCB3cml0ZSBpdCBsaWtlIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IFJlc3VsdCBmcm9tICd0cnVlLW15dGgvcmVzdWx0JztcbiAgaW1wb3J0IHsgY3VycnkgfSBmcm9tICdsb2Rhc2gnO1xuXG4gIGNvbnN0IG1lcmdlM1N0cnMgPSAoYTogc3RyaW5nLCBiOiBzdHJpbmcsIGM6IHN0cmluZykgPT4gc3RyaW5nO1xuICBjb25zdCBjdXJyaWVkTWVyZ2UgPSBjdXJyeShtZXJnZTNTdHJzKTtcblxuICBjb25zdCBmbiA9IFJlc3VsdC5vazx0eXBlb2YgY3VycmllZE1lcmdlLCBzdHJpbmc+KGN1cnJpZWRNZXJnZSk7XG4gIGBgYFxuXG4gIFRoZSBhbHRlcm5hdGl2ZSBpcyB3cml0aW5nIG91dCB0aGUgZnVsbCBzaWduYXR1cmUgbG9uZy1mb3JtOlxuXG4gIGBgYHRzXG4gIGNvbnN0IGZuID0gUmVzdWx0Lm9rPChhOiBzdHJpbmcpID0+IChiOiBzdHJpbmcpID0+IChjOiBzdHJpbmcpID0+IHN0cmluZywgc3RyaW5nPihjdXJyaWVkTWVyZ2UpO1xuICBgYGBcblxuICAqKkFzaWRlOioqIGBhcGAgaXMgbm90IG5hbWVkIGBhcHBseWAgYmVjYXVzZSBvZiB0aGUgb3ZlcmxhcCB3aXRoIEphdmFTY3JpcHQnc1xuICBleGlzdGluZyBbYGFwcGx5YF0gZnVuY3Rpb24g4oCTIGFuZCBhbHRob3VnaCBzdHJpY3RseSBzcGVha2luZywgdGhlcmUgaXNuJ3QgYW55XG4gIGRpcmVjdCBvdmVybGFwIChgUmVzdWx0LmFwcGx5YCBhbmQgYEZ1bmN0aW9uLnByb3RvdHlwZS5hcHBseWAgZG9uJ3QgaW50ZXJzZWN0XG4gIGF0IGFsbCkgaXQncyB1c2VmdWwgdG8gaGF2ZSBhIGRpZmZlcmVudCBuYW1lIHRvIGF2b2lkIGltcGx5aW5nIHRoYXQgdGhleSdyZVxuICB0aGUgc2FtZS5cblxuICBbYGFwcGx5YF06IGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0phdmFTY3JpcHQvUmVmZXJlbmNlL0dsb2JhbF9PYmplY3RzL0Z1bmN0aW9uL2FwcGx5XG5cbiAgQHBhcmFtIHJlc3VsdEZuIHJlc3VsdCBvZiBhIGZ1bmN0aW9uIGZyb20gVCB0byBVXG4gIEBwYXJhbSByZXN1bHQgcmVzdWx0IG9mIGEgVCB0byBhcHBseSB0byBgZm5gXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhcDxULCBVLCBFPihyZXN1bHRGbjogUmVzdWx0PCh0OiBUKSA9PiBVLCBFPiwgcmVzdWx0OiBSZXN1bHQ8VCwgRT4pOiBSZXN1bHQ8VSwgRT47XG5leHBvcnQgZnVuY3Rpb24gYXA8VCwgVSwgRT4oXG4gIHJlc3VsdEZuOiBSZXN1bHQ8KHQ6IFQpID0+IFUsIEU+XG4pOiAocmVzdWx0OiBSZXN1bHQ8VCwgRT4pID0+IFJlc3VsdDxVLCBFPjtcbmV4cG9ydCBmdW5jdGlvbiBhcDxULCBVLCBFPihcbiAgcmVzdWx0Rm46IFJlc3VsdDwodmFsOiBUKSA9PiBVLCBFPixcbiAgcmVzdWx0PzogUmVzdWx0PFQsIEU+XG4pOiBSZXN1bHQ8VSwgRT4gfCAoKHZhbDogUmVzdWx0PFQsIEU+KSA9PiBSZXN1bHQ8VSwgRT4pIHtcbiAgY29uc3Qgb3AgPSAocjogUmVzdWx0PFQsIEU+KSA9PlxuICAgIHIubWF0Y2goe1xuICAgICAgT2s6IHZhbCA9PiByZXN1bHRGbi5tYXAoZm4gPT4gZm4odmFsKSksXG4gICAgICBFcnI6IGUgPT4gUmVzdWx0LmVycjxVLCBFPihlKSxcbiAgICB9KTtcblxuICByZXR1cm4gY3VycnkxKG9wLCByZXN1bHQpO1xufVxuXG4vKipcbiAgRGV0ZXJtaW5lIHdoZXRoZXIgYW4gaXRlbSBpcyBhbiBpbnN0YW5jZSBvZiBgSnVzdGAgb3IgYE5vdGhpbmdgLlxuXG4gIEBwYXJhbSBpdGVtIFRoZSBpdGVtIHRvIGNoZWNrLlxuICovXG5leHBvcnQgZnVuY3Rpb24gaXNJbnN0YW5jZTxUID0gYW55LCBFID0gYW55PihpdGVtOiBhbnkpOiBpdGVtIGlzIFJlc3VsdDxULCBFPiB7XG4gIHJldHVybiBpdGVtIGluc3RhbmNlb2YgT2sgfHwgaXRlbSBpbnN0YW5jZW9mIEVycjtcbn1cblxuLyoqXG4gIEEgdmFsdWUgd2hpY2ggbWF5IChgT2tgKSBvciBtYXkgbm90IChgRXJyYCkgYmUgcHJlc2VudC5cblxuICBUaGUgYmVoYXZpb3Igb2YgdGhpcyB0eXBlIGlzIGNoZWNrZWQgYnkgVHlwZVNjcmlwdCBhdCBjb21waWxlIHRpbWUsIGFuZCBiZWFyc1xuICBubyBydW50aW1lIG92ZXJoZWFkIG90aGVyIHRoYW4gdGhlIHZlcnkgc21hbGwgY29zdCBvZiB0aGUgY29udGFpbmVyIG9iamVjdC5cbiAqL1xuZXhwb3J0IHR5cGUgUmVzdWx0PFQsIEU+ID0gT2s8VCwgRT4gfCBFcnI8VCwgRT47XG5leHBvcnQgY29uc3QgUmVzdWx0ID0ge1xuICBWYXJpYW50LFxuICBPayxcbiAgRXJyLFxuICBpc09rLFxuICBpc0VycixcbiAgb2ssXG4gIGVycixcbiAgdHJ5T3IsXG4gIHRyeU9yRWxzZSxcbiAgbWFwLFxuICBtYXBPcixcbiAgbWFwT3JFbHNlLFxuICBtYXBFcnIsXG4gIGFuZCxcbiAgYW5kVGhlbixcbiAgY2hhaW4sXG4gIGZsYXRNYXAsXG4gIG9yLFxuICBvckVsc2UsXG4gIHVuc2FmZWx5VW53cmFwLFxuICB1bnNhZmVseUdldCxcbiAgdW5zYWZlR2V0LFxuICB1bnNhZmVseVVud3JhcEVycixcbiAgdW5zYWZlbHlHZXRFcnIsXG4gIHVud3JhcE9yLFxuICBnZXRPcixcbiAgdW53cmFwT3JFbHNlLFxuICBnZXRPckVsc2UsXG4gIHRvTWF5YmUsXG4gIGZyb21NYXliZSxcbiAgdG9TdHJpbmcsXG4gIG1hdGNoLFxuICBjYXRhLFxuICBlcXVhbHMsXG4gIGFwLFxuICBpc0luc3RhbmNlLFxufTtcblxuZXhwb3J0IGRlZmF1bHQgUmVzdWx0O1xuIl19