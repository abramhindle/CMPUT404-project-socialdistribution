"use strict";
/** [[include:doc/maybe.md]] */
Object.defineProperty(exports, "__esModule", { value: true });
/** (keep typedoc from getting confused by the imports) */
const result_1 = require("./result");
const utils_1 = require("./utils");
/**
  Discriminant for the `Just` and `Nothing` variants.

  You can use the discriminant via the `variant` property of `Maybe` instances
  if you need to match explicitly on it.
 */
var Variant;
(function (Variant) {
    Variant["Just"] = "Just";
    Variant["Nothing"] = "Nothing";
})(Variant = exports.Variant || (exports.Variant = {}));
/**
  A `Just` instance is the *present* variant instance of the
  [`Maybe`](../modules/_maybe_.html#maybe) type, representing the presence of a
  value which may be absent. For a full discussion, see [the module
  docs](../modules/_maybe_.html).

  @typeparam T The type wrapped in this `Just` variant of `Maybe`.
 */
class Just {
    /**
      Create an instance of `Maybe.Just` with `new`.
  
      @note While you *may* create the `Just` type via normal JavaScript
      class construction, it is not recommended for the functional style for
      which the library is intended. Instead, use [`Maybe.of`] (for the general
      case) or [`Maybe.just`] for this specific case.
  
      [`Maybe.of`]: ../modules/_maybe_.html#of
      [`Maybe.just`]: ../modules/_maybe_.html#just
  
      ```ts
      // Avoid:
      const aString = new Maybe.Just('characters');
  
      // Prefer:
      const aString = Maybe.just('characters);
      ```
  
      @param value
      The value to wrap in a `Maybe.Just`.
  
      `null` and `undefined` are allowed by the type signature so that the
      constructor may `throw` on those rather than constructing a type like
      `Maybe<undefined>`.
  
      @throws      If you pass `null` or `undefined`.
     */
    constructor(value) {
        /** `Just` is always [`Variant.Just`](../enums/_maybe_.variant#just). */
        this.variant = Variant.Just;
        if (utils_1.isVoid(value)) {
            throw new Error('Tried to construct `Just` with `null` or `undefined`');
        }
        this.value = value;
    }
    /**
      Unwrap the contained value. A convenience method for functional idioms.
  
      A common scenario where you might want to use this is in a pipeline of
      functions:
  
      ```ts
      import Maybe, { Just } from 'true-myth/maybe';
  
      function getLengths(maybeStrings: Array<Maybe<string>>): Array<number> {
        return maybeStrings
          .filter(Maybe.isJust)
          .map(Just.unwrap)
          .map(s => s.length);
      }
      ```
     */
    static unwrap(theJust) {
        return theJust.value;
    }
    /** Method variant for [`Maybe.isJust`](../modules/_maybe_.html#isjust) */
    isJust() {
        return true;
    }
    /** Method variant for [`Maybe.isNothing`](../modules/_maybe_.html#isnothing) */
    isNothing() {
        return false;
    }
    /** Method variant for [`Maybe.map`](../modules/_maybe_.html#map) */
    map(mapFn) {
        return map(mapFn, this);
    }
    /** Method variant for [`Maybe.mapOr`](../modules/_maybe_.html#mapor) */
    mapOr(orU, mapFn) {
        return mapOr(orU, mapFn, this);
    }
    /** Method variant for [`Maybe.mapOrElse`](../modules/_maybe_.html#maporelse) */
    mapOrElse(orElseFn, mapFn) {
        return mapOrElse(orElseFn, mapFn, this);
    }
    /** Method variant for [`Maybe.match`](../modules/_maybe_.html#match) */
    match(matcher) {
        return match(matcher, this);
    }
    /** Method variant for [`Maybe.or`](../modules/_maybe_.html#or) */
    or(mOr) {
        return or(mOr, this);
    }
    /** Method variant for [`Maybe.orElse`](../modules/_maybe_.html#orelse) */
    orElse(orElseFn) {
        return orElse(orElseFn, this);
    }
    /** Method variant for [`Maybe.and`](../modules/_maybe_.html#and) */
    and(mAnd) {
        return and(mAnd, this);
    }
    /** Method variant for [`Maybe.andThen`](../modules/_maybe_.html#andthen) */
    andThen(andThenFn) {
        return andThen(andThenFn, this);
    }
    /** Method variant for [`Maybe.chain`](../modules/_maybe_.html#chain) */
    chain(chainFn) {
        return this.andThen(chainFn);
    }
    /** Method variant for [`Maybe.flatMap`](../modules/_maybe_.html#flatmap) */
    flatMap(flatMapFn) {
        return this.andThen(flatMapFn);
    }
    /** Method variant for [`Maybe.unsafelyUnwrap`](../modules/_maybe_.html#unsafelyunwrap) */
    unsafelyUnwrap() {
        return this.value;
    }
    /** Method variant for [`Maybe.unwrapOr`](../modules/_maybe_.html#unwrapor) */
    unwrapOr(defaultValue) {
        return unwrapOr(defaultValue, this);
    }
    /** Method variant for [`Maybe.unwrapOrElse`](../modules/_maybe_.html#unwraporelse) */
    unwrapOrElse(elseFn) {
        return unwrapOrElse(elseFn, this);
    }
    /** Method variant for [`Maybe.toOkOrErr`](../modules/_maybe_.html#tookorerr) */
    toOkOrErr(error) {
        return toOkOrErr(error, this);
    }
    /** Method variant for [`Maybe.toOkOrElseErr`](../modules/_maybe_.html#tookorelseerr) */
    toOkOrElseErr(elseFn) {
        return toOkOrElseErr(elseFn, this);
    }
    /** Method variant for [`Maybe.toString`](../modules/_maybe_.html#tostring) */
    toString() {
        return toString(this);
    }
    /** Method variant for [`Maybe.equals`](../modules/_maybe_.html#equals) */
    equals(comparison) {
        return equals(comparison, this);
    }
    /** Method variant for [`Maybe.ap`](../modules/_maybe_.html#ap) */
    ap(val) {
        return ap(this, val);
    }
    /**
      Method variant for [`Maybe.get`](../modules/_maybe_.html#prop)
  
          If you have a `Maybe` of an object type, you can do `thatMaybe.get('a key')`
      to look up the next layer down in the object.
  
      ```ts
      type DeepOptionalType = {
        something?: {
          with?: {
            deeperKeys?: string;
          }
        }
      };
  
      const fullySet: DeepType = {
        something: {
          with: {
            deeperKeys: 'like this'
          }
        }
      };
  
      const deepJust = Maybe.of(fullySet)
        .get('something')
        .get('with')
        .get('deeperKeys');
  
      console.log(deepJust); // Just('like this');
  
      const partiallyUnset: DeepType = { something: { } };
  
      const deepEmpty = Maybe.of(partiallyUnset)
        .get('something')
        .get('with')
        .get('deeperKeys');
  
      console.log(deepEmpty); // Nothing
      ```
     */
    get(key) {
        return this.andThen(property(key));
    }
}
exports.Just = Just;
/**
  A `Nothing` instance is the *absent* variant instance of the
  [`Maybe`](../modules/_maybe_.html#maybe) type, representing the presence of a
  value which may be absent. For a full discussion, see [the module
  docs](../modules/_maybe_.html).

  @typeparam T The type which would be wrapped in a `Just` variant of `Maybe`.
 */
class Nothing {
    /**
      Create an instance of `Maybe.Nothing` with `new`.
  
      @note While you *may* create the `Nothing` type via normal JavaScript
      class construction, it is not recommended for the functional style for
      which the library is intended. Instead, use [`Maybe.of`] (for the general
      case) or [`Maybe.nothing`] for this specific case.
  
      [`Maybe.of`]: ../modules/_maybe_.html#of
      [`Maybe.nothing`]: ../modules/_maybe_.html#nothing
  
      ```ts
      // Avoid:
      const aNothing = new Maybe.Err();
  
      // Prefer:
      const aNothing = Maybe.nothing();
      ```
  
      `null` and `undefined` are allowed so that you may explicitly construct the
      `Err` type with a known `null` or `undefined` value. (This maybe helpful
      primarily when transitioning a codebase to the use of `Maybe`.)
  
      @throws      If you pass `null` or `undefined`.
     */
    constructor(_) {
        /** `Nothing` is always [`Variant.Nothing`](../enums/_maybe_.variant#nothing). */
        this.variant = Variant.Nothing;
        /* nothing to do */
    }
    /** Method variant for [`Maybe.isJust`](../modules/_maybe_.html#isjust) */
    isJust() {
        return false;
    }
    /** Method variant for [`Maybe.isNothing`](../modules/_maybe_.html#isnothing) */
    isNothing() {
        return true;
    }
    /** Method variant for [`Maybe.map`](../modules/_maybe_.html#map) */
    map(mapFn) {
        return map(mapFn, this);
    }
    /** Method variant for [`Maybe.mapOr`](../modules/_maybe_.html#mapor) */
    mapOr(orU, mapFn) {
        return mapOr(orU, mapFn, this);
    }
    /** Method variant for [`Maybe.mapOrElse`](../modules/_maybe_.html#maporelse) */
    mapOrElse(orElseFn, mapFn) {
        return mapOrElse(orElseFn, mapFn, this);
    }
    /** Method variant for [`Maybe.match`](../modules/_maybe_.html#match) */
    match(matcher) {
        return match(matcher, this);
    }
    /** Method variant for [`Maybe.or`](../modules/_maybe_.html#or) */
    or(mOr) {
        return or(mOr, this);
    }
    /** Method variant for [`Maybe.orElse`](../modules/_maybe_.html#orelse) */
    orElse(orElseFn) {
        return orElse(orElseFn, this);
    }
    /** Method variant for [`Maybe.and`](../modules/_maybe_.html#and) */
    and(mAnd) {
        return and(mAnd, this);
    }
    /** Method variant for [`Maybe.andThen`](../modules/_maybe_.html#andthen) */
    andThen(andThenFn) {
        return andThen(andThenFn, this);
    }
    /** Method variant for [`Maybe.chain`](../modules/_maybe_.html#chain) */
    chain(chainFn) {
        return this.andThen(chainFn);
    }
    /** Method variant for [`Maybe.flatMap`](../modules/_maybe_.html#flatmap) */
    flatMap(flatMapFn) {
        return this.andThen(flatMapFn);
    }
    /** Method variant for [`Maybe.unsafelyUnwrap`](../modules/_maybe_.html#unsafelyunwrap) */
    unsafelyUnwrap() {
        throw new Error('Tried to `unsafelyUnwrap(Nothing)`');
    }
    /** Method variant for [`Maybe.unwrapOr`](../modules/_maybe_.html#unwrapor) */
    unwrapOr(defaultValue) {
        return unwrapOr(defaultValue, this);
    }
    /** Method variant for [`Maybe.unwrapOrElse`](../modules/_maybe_.html#unwraporelse) */
    unwrapOrElse(elseFn) {
        return unwrapOrElse(elseFn, this);
    }
    /** Method variant for [`Maybe.toOkOrErr`](../modules/_maybe_.html#tookorerr) */
    toOkOrErr(error) {
        return toOkOrErr(error, this);
    }
    /** Method variant for [`Maybe.toOkOrElseErr`](../modules/_maybe_.html#tookorelseerr) */
    toOkOrElseErr(elseFn) {
        return toOkOrElseErr(elseFn, this);
    }
    /** Method variant for [`Maybe.toString`](../modules/_maybe_.html#tostring) */
    toString() {
        return toString(this);
    }
    /** Method variant for [`Maybe.equals`](../modules/_maybe_.html#equals) */
    equals(comparison) {
        return equals(comparison, this);
    }
    /** Method variant for [`Maybe.ap`](../modules/_maybe_.html#ap) */
    ap(val) {
        return ap(this, val);
    }
    /**
      Method variant for [`Maybe.get`](../modules/_maybe_.html#prop)
  
          If you have a `Maybe` of an object type, you can do `thatMaybe.get('a key')`
      to look up the next layer down in the object.
  
      ```ts
      type DeepOptionalType = {
        something?: {
          with?: {
            deeperKeys?: string;
          }
        }
      };
  
      const fullySet: DeepType = {
        something: {
          with: {
            deeperKeys: 'like this'
          }
        }
      };
  
      const deepJust = Maybe.of(fullySet)
        .get('something')
        .get('with')
        .get('deeperKeys');
  
      console.log(deepJust); // Just('like this');
  
      const partiallyUnset: DeepType = { something: { } };
  
      const deepEmpty = Maybe.of(partiallyUnset)
        .get('something')
        .get('with')
        .get('deeperKeys');
  
      console.log(deepEmpty); // Nothing
      ```
     */
    get(key) {
        return this.andThen(property(key));
    }
}
exports.Nothing = Nothing;
/**
  Is this result a `Just` instance?

  @typeparam T The type of the wrapped value.
  @param maybe The `Maybe` instance to check.
  @returns     `true` if `maybe` is `Just`, `false` otherwise. In TypeScript,
               also narrows the type from `Maybe<T>` to `Just<T>`.
 */
function isJust(maybe) {
    return maybe.variant === Variant.Just;
}
exports.isJust = isJust;
/**
  Is this result a `Nothing` instance?

  @typeparam T The type of the wrapped value.
  @param maybe The `Maybe` instance to check.
  @returns     `true` if `maybe` is `nothing`, `false` otherwise. In TypeScript,
               also narrows the type from `Maybe<T>` to `Nothing<T>`.
 */
function isNothing(maybe) {
    return maybe.variant === Variant.Nothing;
}
exports.isNothing = isNothing;
/**
  Create an instance of `Maybe.Just`.

  `null` and `undefined` are allowed by the type signature so that the
  function may `throw` on those rather than constructing a type like
  `Maybe<undefined>`.

  @typeparam T The type of the item contained in the `Maybe`.
  @param value The value to wrap in a `Maybe.Just`.
  @returns     An instance of `Maybe.Just<T>`.
  @throws      If you pass `null` or `undefined`.
 */
function just(value) {
    return new Just(value);
}
exports.just = just;
/**
  Create an instance of `Maybe.Nothing`.

  If you want to create an instance with a specific type, e.g. for use in a
  function which expects a `Maybe<T>` where the `<T>` is known but you have no
  value to give it, you can use a type parameter:

  ```ts
  const notString = Maybe.nothing<string>();
  ```

  @typeparam T The type of the item contained in the `Maybe`.
  @returns     An instance of `Maybe.Nothing<T>`.
 */
function nothing(_) {
    return new Nothing(_);
}
exports.nothing = nothing;
/**
  Create a `Maybe` from any value.

  To specify that the result should be interpreted as a specific type, you may
  invoke `Maybe.of` with an explicit type parameter:

  ```ts
  const foo = Maybe.of<string>(null);
  ```

  This is usually only important in two cases:

  1.  If you are intentionally constructing a `Nothing` from a known `null` or
      undefined value *which is untyped*.
  2.  If you are specifying that the type is more general than the value passed
      (since TypeScript can define types as literals).

  @typeparam T The type of the item contained in the `Maybe`.
  @param value The value to wrap in a `Maybe`. If it is `undefined` or `null`,
               the result will be `Nothing`; otherwise it will be the type of
               the value passed.
 */
function of(value) {
    return utils_1.isVoid(value) ? nothing() : just(value);
}
exports.of = of;
/** Alias for [`of`](#of), primarily for compatibility with Folktale. */
exports.fromNullable = of;
function map(mapFn, maybe) {
    const op = (m) => (m.isJust() ? just(mapFn(m.value)) : nothing());
    return utils_1.curry1(op, maybe);
}
exports.map = map;
function mapOr(orU, mapFn, maybe) {
    function fullOp(fn, m) {
        return m.isJust() ? fn(m.value) : orU;
    }
    function partialOp(fn, curriedMaybe) {
        return curriedMaybe !== undefined
            ? fullOp(fn, curriedMaybe)
            : (extraCurriedMaybe) => fullOp(fn, extraCurriedMaybe);
    }
    return mapFn === undefined
        ? partialOp
        : maybe === undefined
            ? partialOp(mapFn)
            : partialOp(mapFn, maybe);
}
exports.mapOr = mapOr;
function mapOrElse(orElseFn, mapFn, maybe) {
    function fullOp(fn, m) {
        return m.isJust() ? fn(m.value) : orElseFn();
    }
    function partialOp(fn, curriedMaybe) {
        return curriedMaybe !== undefined
            ? fullOp(fn, curriedMaybe)
            : (extraCurriedMaybe) => fullOp(fn, extraCurriedMaybe);
    }
    if (mapFn === undefined) {
        return partialOp;
    }
    else if (maybe === undefined) {
        return partialOp(mapFn);
    }
    else {
        return partialOp(mapFn, maybe);
    }
}
exports.mapOrElse = mapOrElse;
function and(andMaybe, maybe) {
    const op = (m) => (m.isJust() ? andMaybe : nothing());
    return utils_1.curry1(op, maybe);
}
exports.and = and;
function andThen(thenFn, maybe) {
    const op = (m) => (m.isJust() ? thenFn(m.value) : nothing());
    return maybe !== undefined ? op(maybe) : op;
}
exports.andThen = andThen;
/** Alias for [`andThen`](#andthen). */
exports.chain = andThen;
/** Alias for [`andThen`](#andthen). */
exports.flatMap = andThen;
function or(defaultMaybe, maybe) {
    const op = (m) => (m.isJust() ? m : defaultMaybe);
    return maybe !== undefined ? op(maybe) : op;
}
exports.or = or;
function orElse(elseFn, maybe) {
    const op = (m) => (m.isJust() ? m : elseFn());
    return utils_1.curry1(op, maybe);
}
exports.orElse = orElse;
/**
  Get the value out of the `Maybe`.

  Returns the content of a `Just`, but **throws if the `Maybe` is `Nothing`**.
  Prefer to use [`unwrapOr`](#unwrapor) or [`unwrapOrElse`](#unwraporelse).

  @typeparam T The type of the wrapped value.
  @param maybe The value to unwrap
  @returns     The unwrapped value if the `Maybe` instance is `Just`.
  @throws      If the `maybe` is `Nothing`.
 */
function unsafelyUnwrap(maybe) {
    return maybe.unsafelyUnwrap();
}
exports.unsafelyUnwrap = unsafelyUnwrap;
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
exports.unsafelyGet = unsafelyUnwrap;
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
exports.unsafeGet = unsafelyUnwrap;
function unwrapOr(defaultValue, maybe) {
    const op = (m) => (m.isJust() ? m.value : defaultValue);
    return utils_1.curry1(op, maybe);
}
exports.unwrapOr = unwrapOr;
/** Alias for [`unwrapOr`](#unwrapor) */
exports.getOr = unwrapOr;
function unwrapOrElse(orElseFn, maybe) {
    const op = (m) => (m.isJust() ? m.value : orElseFn());
    return utils_1.curry1(op, maybe);
}
exports.unwrapOrElse = unwrapOrElse;
/** Alias for [`unwrapOrElse`](#unwraporelse) */
exports.getOrElse = unwrapOrElse;
function toOkOrErr(error, maybe) {
    const op = (m) => (m.isJust() ? result_1.ok(m.value) : result_1.err(error));
    return maybe !== undefined ? op(maybe) : op;
}
exports.toOkOrErr = toOkOrErr;
function toOkOrElseErr(elseFn, maybe) {
    const op = (m) => (m.isJust() ? result_1.ok(m.value) : result_1.err(elseFn()));
    return utils_1.curry1(op, maybe);
}
exports.toOkOrElseErr = toOkOrElseErr;
/**
  Construct a `Maybe<T>` from a `Result<T, E>`.

  If the `Result` is an `Ok`, wrap its value in `Just`. If the `Result` is an
  `Err`, throw away the wrapped `E` and transform to a `Nothing`.

  @typeparam T  The type of the value wrapped in a `Result.Ok` and in the `Just`
                of the resulting `Maybe`.
  @typeparam E  The type of the value wrapped in a `Result.Err`; thrown away in
                the resulting `Maybe`.
  @param result The `Result` to construct a `Maybe` from.
  @returns      `Just` if `result` was `Ok` or `Nothing` if it was `Err`.
 */
function fromResult(result) {
    return result.isOk() ? just(result.value) : nothing();
}
exports.fromResult = fromResult;
/**
  Create a `String` representation of a `Maybe` instance.

  A `Just` instance will be printed as `Just(<representation of the value>)`,
  where the representation of the value is simply the value's own `toString`
  representation. For example:

  | call                                   | output                  |
  |----------------------------------------|-------------------------|
  | `toString(Maybe.of(42))`               | `Just(42)`              |
  | `toString(Maybe.of([1, 2, 3]))`        | `Just(1,2,3)`           |
  | `toString(Maybe.of({ an: 'object' }))` | `Just([object Object])` |
  | `toString(Maybe.nothing())`            | `Nothing`               |

  @typeparam T The type of the wrapped value; its own `.toString` will be used
               to print the interior contents of the `Just` variant.
  @param maybe The value to convert to a string.
  @returns     The string representation of the `Maybe`.
 */
function toString(maybe) {
    const body = maybe.isJust() ? `(${maybe.value.toString()})` : '';
    return `${maybe.variant}${body}`;
}
exports.toString = toString;
function match(matcher, maybe) {
    return maybe !== undefined
        ? mapOrElse(matcher.Nothing, matcher.Just, maybe)
        : (curriedMaybe) => mapOrElse(matcher.Nothing, matcher.Just, curriedMaybe);
}
exports.match = match;
/** Alias for [`match`](#match) */
exports.cata = match;
function equals(mb, ma) {
    return ma !== undefined
        ? ma.match({
            Just: aVal => mb.isJust() && mb.unsafelyUnwrap() === aVal,
            Nothing: () => isNothing(mb),
        })
        : (maybeA) => maybeA.match({
            Nothing: () => isNothing(mb),
            Just: aVal => mb.isJust() && mb.unsafelyUnwrap() === aVal,
        });
}
exports.equals = equals;
function ap(maybeFn, maybe) {
    const op = (m) => m.match({
        Just: val => maybeFn.map(fn => fn(val)),
        Nothing: () => exports.Maybe.nothing(),
    });
    return utils_1.curry1(op, maybe);
}
exports.ap = ap;
/**
  Determine whether an item is an instance of `Just` or `Nothing`.

  @param item The item to check.
 */
function isInstance(item) {
    return item instanceof Just || item instanceof Nothing;
}
exports.isInstance = isInstance;
function find(predicate, array) {
    const op = (a) => exports.Maybe.of(a.find(predicate));
    return utils_1.curry1(op, array);
}
exports.find = find;
/**
  Safely get the first item from a list, returning `Just` the first item if the
  array has at least one item in it, or `Nothing` if it is empty.

  ## Examples

  ```ts
  let empty = [];
  Maybe.head(empty); // => Nothing

  let full = [1, 2, 3];
  Maybe.head(full); // => Just(1)
  ```

  @param array The array to get the first item from.
 */
function head(array) {
    return exports.Maybe.of(array[0]);
}
exports.head = head;
/** A convenience alias for `Maybe.head`. */
exports.first = head;
/**
  Safely get the last item from a list, returning `Just` the last item if the
  array has at least one item in it, or `Nothing` if it is empty.

  ## Examples

  ```ts
  let empty = [];
  Maybe.last(empty); // => Nothing

  let full = [1, 2, 3];
  Maybe.last(full); // => Just(3)
  ```

  @param array The array to get the first item from.
 */
function last(array) {
    return exports.Maybe.of(array[array.length - 1]);
}
exports.last = last;
/**
  Convert the arguments to a single `Maybe`. Useful for dealing with arrays of
  `Maybe`s, via the spread operator.

  ## Examples

  ```ts
  import Maybe from 'true-myth/maybe';

  let valid = [Maybe.just(2), Maybe.just('three')];
  Maybe.all(...valid); // => Just([2, 'three']);

  let invalid = [Maybe.just(2), Maybe.nothing<string>()];
  Maybe.all(...invalid); // => Nothing
  ```

  ## Note on Spread

  This requires the use of the spread operator because (at least as of
  TypeScript 3.0), the type inference falls down when attempting to build this
  same type with an array directly. Moreover, this spread-based approach handles
  heteregenous arrays; TS *also* fails to infer correctly for anything but
  homogeneous arrays when using that approach.

  @param maybes The `Maybe`s to resolve to a single `Maybe`.
 */
function all(...maybes) {
    let result = exports.Maybe.just([]);
    maybes.forEach(maybe => {
        result = result.andThen(accumulatedMaybes => maybe.map(m => {
            accumulatedMaybes.push(m);
            return accumulatedMaybes;
        }));
    });
    return result;
}
exports.all = all;
function tuple(maybes) {
    // @ts-ignore -- this doesn't type-check, but it works correctly.
    return all(...maybes);
}
exports.tuple = tuple;
function property(key, obj) {
    const op = (a) => exports.Maybe.of(a[key]);
    return utils_1.curry1(op, obj);
}
exports.property = property;
function get(key, maybeObj) {
    return utils_1.curry1(exports.Maybe.andThen(property(key)), maybeObj);
}
exports.get = get;
exports.Maybe = {
    Variant,
    Just,
    Nothing,
    all,
    isJust,
    isNothing,
    just,
    nothing,
    of,
    find,
    first: exports.first,
    fromNullable: exports.fromNullable,
    head,
    last,
    map,
    mapOr,
    mapOrElse,
    and,
    andThen,
    chain: exports.chain,
    flatMap: exports.flatMap,
    or,
    orElse,
    unsafelyUnwrap,
    unsafelyGet: exports.unsafelyGet,
    unsafeGet: exports.unsafeGet,
    unwrapOr,
    getOr: exports.getOr,
    unwrapOrElse,
    getOrElse: exports.getOrElse,
    toOkOrErr,
    toOkOrElseErr,
    fromResult,
    toString,
    tuple,
    match,
    cata: exports.cata,
    equals,
    ap,
    isInstance,
    property,
    get,
};
exports.default = exports.Maybe;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWF5YmUuanMiLCJzb3VyY2VSb290IjoiLi8iLCJzb3VyY2VzIjpbIm1heWJlLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFBQSwrQkFBK0I7O0FBRS9CLDBEQUEwRDtBQUMxRCxxQ0FBMkM7QUFDM0MsbUNBQXlDO0FBRXpDOzs7OztHQUtHO0FBQ0gsSUFBWSxPQUdYO0FBSEQsV0FBWSxPQUFPO0lBQ2pCLHdCQUFhLENBQUE7SUFDYiw4QkFBbUIsQ0FBQTtBQUNyQixDQUFDLEVBSFcsT0FBTyxHQUFQLGVBQU8sS0FBUCxlQUFPLFFBR2xCO0FBMkdEOzs7Ozs7O0dBT0c7QUFDSCxNQUFhLElBQUk7SUE0QmY7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztPQTJCRztJQUNILFlBQVksS0FBZ0I7UUFsQzVCLHdFQUF3RTtRQUMvRCxZQUFPLEdBQWlCLE9BQU8sQ0FBQyxJQUFJLENBQUM7UUFrQzVDLElBQUksY0FBTSxDQUFDLEtBQUssQ0FBQyxFQUFFO1lBQ2pCLE1BQU0sSUFBSSxLQUFLLENBQUMsc0RBQXNELENBQUMsQ0FBQztTQUN6RTtRQUVELElBQUksQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDO0lBQ3JCLENBQUM7SUE3REQ7Ozs7Ozs7Ozs7Ozs7Ozs7T0FnQkc7SUFDSCxNQUFNLENBQUMsTUFBTSxDQUFJLE9BQWdCO1FBQy9CLE9BQU8sT0FBTyxDQUFDLEtBQUssQ0FBQztJQUN2QixDQUFDO0lBNENELDBFQUEwRTtJQUMxRSxNQUFNO1FBQ0osT0FBTyxJQUFJLENBQUM7SUFDZCxDQUFDO0lBRUQsZ0ZBQWdGO0lBQ2hGLFNBQVM7UUFDUCxPQUFPLEtBQUssQ0FBQztJQUNmLENBQUM7SUFFRCxvRUFBb0U7SUFDcEUsR0FBRyxDQUFvQixLQUFrQjtRQUN2QyxPQUFPLEdBQUcsQ0FBQyxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDMUIsQ0FBQztJQUVELHdFQUF3RTtJQUN4RSxLQUFLLENBQW9CLEdBQU0sRUFBRSxLQUFrQjtRQUNqRCxPQUFPLEtB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O0lBQ1AsRUFBRTtJQUNGLE1BQU07SUFDTixjQUFjO0lBQ2QsV0FBVyxFQUFYLG1CQUFXO0lBQ1gsU0FBUyxFQUFULGlCQUFTO0lBQ1QsUUFBUTtJQUNSLEtBQUssRUFBTCxhQUFLO0lBQ0wsWUFBWTtJQUNaLFNBQVMsRUFBVCxpQkFBUztJQUNULFNBQVM7SUFDVCxhQUFhO0lBQ2IsVUFBVTtJQUNWLFFBQVE7SUFDUixLQUFLO0lBQ0wsS0FBSztJQUNMLElBQUksRUFBSixZQUFJO0lBQ0osTUFBTTtJQUNOLEVBQUU7SUFDRixVQUFVO0lBQ1YsUUFBUTtJQUNSLEdBQUc7Q0FDSixDQUFDO0FBRUYsa0JBQWUsYUFBSyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqIFtbaW5jbHVkZTpkb2MvbWF5YmUubWRdXSAqL1xuXG4vKiogKGtlZXAgdHlwZWRvYyBmcm9tIGdldHRpbmcgY29uZnVzZWQgYnkgdGhlIGltcG9ydHMpICovXG5pbXBvcnQgUmVzdWx0LCB7IGVyciwgb2sgfSBmcm9tICcuL3Jlc3VsdCc7XG5pbXBvcnQgeyBjdXJyeTEsIGlzVm9pZCB9IGZyb20gJy4vdXRpbHMnO1xuXG4vKipcbiAgRGlzY3JpbWluYW50IGZvciB0aGUgYEp1c3RgIGFuZCBgTm90aGluZ2AgdmFyaWFudHMuXG5cbiAgWW91IGNhbiB1c2UgdGhlIGRpc2NyaW1pbmFudCB2aWEgdGhlIGB2YXJpYW50YCBwcm9wZXJ0eSBvZiBgTWF5YmVgIGluc3RhbmNlc1xuICBpZiB5b3UgbmVlZCB0byBtYXRjaCBleHBsaWNpdGx5IG9uIGl0LlxuICovXG5leHBvcnQgZW51bSBWYXJpYW50IHtcbiAgSnVzdCA9ICdKdXN0JyxcbiAgTm90aGluZyA9ICdOb3RoaW5nJyxcbn1cblxuLyoqIFNpbXBseSBkZWZpbmVzIHRoZSBjb21tb24gc2hhcGUgZm9yIGBKdXN0YCBhbmQgYE5vdGhpbmdgLiAqL1xuZXhwb3J0IGludGVyZmFjZSBNYXliZVNoYXBlPFQ+IHtcbiAgLyoqIERpc3Rpbmd1aXNoIGJldHdlZW4gdGhlIGBKdXN0YCBhbmQgYE5vdGhpbmdgIFt2YXJpYW50c10oLi4vZW51bXMvX21heWJlXy52YXJpYW50KS4gKi9cbiAgcmVhZG9ubHkgdmFyaWFudDogVmFyaWFudDtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuaXNKdXN0YF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjaXNqdXN0KSAqL1xuICBpc0p1c3QodGhpczogTWF5YmU8VD4pOiB0aGlzIGlzIEp1c3Q8VD47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmlzTm90aGluZ2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2lzbm90aGluZykgKi9cbiAgaXNOb3RoaW5nKHRoaXM6IE1heWJlPFQ+KTogdGhpcyBpcyBOb3RoaW5nPFQ+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXApICovXG4gIG1hcDxVPih0aGlzOiBNYXliZTxUPiwgbWFwRm46ICh0OiBUKSA9PiBVKTogTWF5YmU8VT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcE9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWFwb3IpICovXG4gIG1hcE9yPFU+KHRoaXM6IE1heWJlPFQ+LCBvclU6IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFU7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcG9yZWxzZSkgKi9cbiAgbWFwT3JFbHNlPFU+KHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVTtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWF0Y2hgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXRjaCkgKi9cbiAgbWF0Y2g8VT4odGhpczogTWF5YmU8VD4sIG1hdGNoZXI6IE1hdGNoZXI8VCwgVT4pOiBVO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5vcmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI29yKSAqL1xuICBvcih0aGlzOiBNYXliZTxUPiwgbU9yOiBNYXliZTxUPik6IE1heWJlPFQ+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5vckVsc2VgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNvcmVsc2UpICovXG4gIG9yRWxzZSh0aGlzOiBNYXliZTxUPiwgb3JFbHNlRm46ICgpID0+IE1heWJlPFQ+KTogTWF5YmU8VD47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmFuZGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FuZCkgKi9cbiAgYW5kPFU+KHRoaXM6IE1heWJlPFQ+LCBtQW5kOiBNYXliZTxVPik6IE1heWJlPFU+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hbmRUaGVuYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYW5kdGhlbikgKi9cbiAgYW5kVGhlbjxVPih0aGlzOiBNYXliZTxUPiwgYW5kVGhlbkZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiBNYXliZTxVPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuY2hhaW5gXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNjaGFpbikgKi9cbiAgY2hhaW48VT4odGhpczogTWF5YmU8VD4sIGNoYWluRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5mbGF0TWFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjZmxhdG1hcCkgKi9cbiAgZmxhdE1hcDxVPih0aGlzOiBNYXliZTxUPiwgZmxhdE1hcEZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiBNYXliZTxVPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW53cmFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdW53cmFwKSAqL1xuICB1bnNhZmVseVVud3JhcCgpOiBUIHwgbmV2ZXI7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVud3JhcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Vud3JhcG9yZWxzZSkgKi9cbiAgdW53cmFwT3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBlbHNlRm46ICgpID0+IFQpOiBUO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS50b09rT3JFcnJgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN0b29rb3JlcnIpICovXG4gIHRvT2tPckVycjxFPih0aGlzOiBNYXliZTxUPiwgZXJyb3I6IEUpOiBSZXN1bHQ8VCwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvT2tPckVsc2VFcnJgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN0b29rb3JlbHNlZXJyKSAqL1xuICB0b09rT3JFbHNlRXJyPEU+KHRoaXM6IE1heWJlPFQ+LCBlbHNlRm46ICgpID0+IEUpOiBSZXN1bHQ8VCwgRT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvU3RyaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9zdHJpbmcpICovXG4gIHRvU3RyaW5nKHRoaXM6IE1heWJlPFQ+KTogc3RyaW5nO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5lcXVhbHNgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNlcXVhbHMpICovXG4gIGVxdWFscyh0aGlzOiBNYXliZTxUPiwgY29tcGFyaXNvbjogTWF5YmU8VD4pOiBib29sZWFuO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FwKSAqL1xuICBhcDxVPih0aGlzOiBNYXliZTwodmFsOiBUKSA9PiBVPiwgdmFsOiBNYXliZTxUPik6IE1heWJlPFU+O1xuXG4gIC8qKlxuICAgIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmdldGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Byb3ApXG5cbiAgICAgICAgSWYgeW91IGhhdmUgYSBgTWF5YmVgIG9mIGFuIG9iamVjdCB0eXBlLCB5b3UgY2FuIGRvIGB0aGF0TWF5YmUuZ2V0KCdhIGtleScpYFxuICAgIHRvIGxvb2sgdXAgdGhlIG5leHQgbGF5ZXIgZG93biBpbiB0aGUgb2JqZWN0LlxuXG4gICAgYGBgdHNcbiAgICB0eXBlIERlZXBPcHRpb25hbFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc/OiB7XG4gICAgICAgIHdpdGg/OiB7XG4gICAgICAgICAgZGVlcGVyS2V5cz86IHN0cmluZztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH07XG5cbiAgICBjb25zdCBmdWxseVNldDogRGVlcFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc6IHtcbiAgICAgICAgd2l0aDoge1xuICAgICAgICAgIGRlZXBlcktleXM6ICdsaWtlIHRoaXMnXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgZGVlcEp1c3QgPSBNYXliZS5vZihmdWxseVNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBKdXN0KTsgLy8gSnVzdCgnbGlrZSB0aGlzJyk7XG5cbiAgICBjb25zdCBwYXJ0aWFsbHlVbnNldDogRGVlcFR5cGUgPSB7IHNvbWV0aGluZzogeyB9IH07XG5cbiAgICBjb25zdCBkZWVwRW1wdHkgPSBNYXliZS5vZihwYXJ0aWFsbHlVbnNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBFbXB0eSk7IC8vIE5vdGhpbmdcbiAgICBgYGBcbiAgICovXG4gIGdldDxLIGV4dGVuZHMga2V5b2YgVD4odGhpczogTWF5YmU8VD4sIGtleTogSyk6IE1heWJlPFJlcXVpcmVkPFQ+W0tdPjtcbn1cblxuLyoqXG4gIEEgYEp1c3RgIGluc3RhbmNlIGlzIHRoZSAqcHJlc2VudCogdmFyaWFudCBpbnN0YW5jZSBvZiB0aGVcbiAgW2BNYXliZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21heWJlKSB0eXBlLCByZXByZXNlbnRpbmcgdGhlIHByZXNlbmNlIG9mIGFcbiAgdmFsdWUgd2hpY2ggbWF5IGJlIGFic2VudC4gRm9yIGEgZnVsbCBkaXNjdXNzaW9uLCBzZWUgW3RoZSBtb2R1bGVcbiAgZG9jc10oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwpLlxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSB3cmFwcGVkIGluIHRoaXMgYEp1c3RgIHZhcmlhbnQgb2YgYE1heWJlYC5cbiAqL1xuZXhwb3J0IGNsYXNzIEp1c3Q8VD4gaW1wbGVtZW50cyBNYXliZVNoYXBlPFQ+IHtcbiAgLyoqXG4gICAgVW53cmFwIHRoZSBjb250YWluZWQgdmFsdWUuIEEgY29udmVuaWVuY2UgbWV0aG9kIGZvciBmdW5jdGlvbmFsIGlkaW9tcy5cblxuICAgIEEgY29tbW9uIHNjZW5hcmlvIHdoZXJlIHlvdSBtaWdodCB3YW50IHRvIHVzZSB0aGlzIGlzIGluIGEgcGlwZWxpbmUgb2ZcbiAgICBmdW5jdGlvbnM6XG5cbiAgICBgYGB0c1xuICAgIGltcG9ydCBNYXliZSwgeyBKdXN0IH0gZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICAgIGZ1bmN0aW9uIGdldExlbmd0aHMobWF5YmVTdHJpbmdzOiBBcnJheTxNYXliZTxzdHJpbmc+Pik6IEFycmF5PG51bWJlcj4ge1xuICAgICAgcmV0dXJuIG1heWJlU3RyaW5nc1xuICAgICAgICAuZmlsdGVyKE1heWJlLmlzSnVzdClcbiAgICAgICAgLm1hcChKdXN0LnVud3JhcClcbiAgICAgICAgLm1hcChzID0+IHMubGVuZ3RoKTtcbiAgICB9XG4gICAgYGBgXG4gICAqL1xuICBzdGF0aWMgdW53cmFwPEo+KHRoZUp1c3Q6IEp1c3Q8Sj4pOiBKIHtcbiAgICByZXR1cm4gdGhlSnVzdC52YWx1ZTtcbiAgfVxuXG4gIC8qKiBgSnVzdGAgaXMgYWx3YXlzIFtgVmFyaWFudC5KdXN0YF0oLi4vZW51bXMvX21heWJlXy52YXJpYW50I2p1c3QpLiAqL1xuICByZWFkb25seSB2YXJpYW50OiBWYXJpYW50Lkp1c3QgPSBWYXJpYW50Lkp1c3Q7XG5cbiAgLyoqIFRoZSB3cmFwcGVkIHZhbHVlLiAqL1xuICByZWFkb25seSB2YWx1ZTogVDtcblxuICAvKipcbiAgICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYE1heWJlLkp1c3RgIHdpdGggYG5ld2AuXG5cbiAgICBAbm90ZSBXaGlsZSB5b3UgKm1heSogY3JlYXRlIHRoZSBgSnVzdGAgdHlwZSB2aWEgbm9ybWFsIEphdmFTY3JpcHRcbiAgICBjbGFzcyBjb25zdHJ1Y3Rpb24sIGl0IGlzIG5vdCByZWNvbW1lbmRlZCBmb3IgdGhlIGZ1bmN0aW9uYWwgc3R5bGUgZm9yXG4gICAgd2hpY2ggdGhlIGxpYnJhcnkgaXMgaW50ZW5kZWQuIEluc3RlYWQsIHVzZSBbYE1heWJlLm9mYF0gKGZvciB0aGUgZ2VuZXJhbFxuICAgIGNhc2UpIG9yIFtgTWF5YmUuanVzdGBdIGZvciB0aGlzIHNwZWNpZmljIGNhc2UuXG5cbiAgICBbYE1heWJlLm9mYF06IC4uL21vZHVsZXMvX21heWJlXy5odG1sI29mXG4gICAgW2BNYXliZS5qdXN0YF06IC4uL21vZHVsZXMvX21heWJlXy5odG1sI2p1c3RcblxuICAgIGBgYHRzXG4gICAgLy8gQXZvaWQ6XG4gICAgY29uc3QgYVN0cmluZyA9IG5ldyBNYXliZS5KdXN0KCdjaGFyYWN0ZXJzJyk7XG5cbiAgICAvLyBQcmVmZXI6XG4gICAgY29uc3QgYVN0cmluZyA9IE1heWJlLmp1c3QoJ2NoYXJhY3RlcnMpO1xuICAgIGBgYFxuXG4gICAgQHBhcmFtIHZhbHVlXG4gICAgVGhlIHZhbHVlIHRvIHdyYXAgaW4gYSBgTWF5YmUuSnVzdGAuXG5cbiAgICBgbnVsbGAgYW5kIGB1bmRlZmluZWRgIGFyZSBhbGxvd2VkIGJ5IHRoZSB0eXBlIHNpZ25hdHVyZSBzbyB0aGF0IHRoZVxuICAgIGNvbnN0cnVjdG9yIG1heSBgdGhyb3dgIG9uIHRob3NlIHJhdGhlciB0aGFuIGNvbnN0cnVjdGluZyBhIHR5cGUgbGlrZVxuICAgIGBNYXliZTx1bmRlZmluZWQ+YC5cblxuICAgIEB0aHJvd3MgICAgICBJZiB5b3UgcGFzcyBgbnVsbGAgb3IgYHVuZGVmaW5lZGAuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih2YWx1ZT86IFQgfCBudWxsKSB7XG4gICAgaWYgKGlzVm9pZCh2YWx1ZSkpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignVHJpZWQgdG8gY29uc3RydWN0IGBKdXN0YCB3aXRoIGBudWxsYCBvciBgdW5kZWZpbmVkYCcpO1xuICAgIH1cblxuICAgIHRoaXMudmFsdWUgPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5pc0p1c3RgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNpc2p1c3QpICovXG4gIGlzSnVzdCh0aGlzOiBNYXliZTxUPik6IHRoaXMgaXMgSnVzdDxUPiB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuaXNOb3RoaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjaXNub3RoaW5nKSAqL1xuICBpc05vdGhpbmcodGhpczogTWF5YmU8VD4pOiB0aGlzIGlzIE5vdGhpbmc8VD4ge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXApICovXG4gIG1hcDxVPih0aGlzOiBNYXliZTxUPiwgbWFwRm46ICh0OiBUKSA9PiBVKTogTWF5YmU8VT4ge1xuICAgIHJldHVybiBtYXAobWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcE9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWFwb3IpICovXG4gIG1hcE9yPFU+KHRoaXM6IE1heWJlPFQ+LCBvclU6IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFUge1xuICAgIHJldHVybiBtYXBPcihvclUsIG1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXBPckVsc2VgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXBvcmVsc2UpICovXG4gIG1hcE9yRWxzZTxVPih0aGlzOiBNYXliZTxUPiwgb3JFbHNlRm46ICgpID0+IFUsIG1hcEZuOiAodDogVCkgPT4gVSk6IFUge1xuICAgIHJldHVybiBtYXBPckVsc2Uob3JFbHNlRm4sIG1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXRjaGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hdGNoKSAqL1xuICBtYXRjaDxVPih0aGlzOiBNYXliZTxUPiwgbWF0Y2hlcjogTWF0Y2hlcjxULCBVPik6IFUge1xuICAgIHJldHVybiBtYXRjaChtYXRjaGVyLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5vcmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI29yKSAqL1xuICBvcih0aGlzOiBNYXliZTxUPiwgbU9yOiBNYXliZTxUPik6IE1heWJlPFQ+IHtcbiAgICByZXR1cm4gb3IobU9yLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5vckVsc2VgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNvcmVsc2UpICovXG4gIG9yRWxzZSh0aGlzOiBNYXliZTxUPiwgb3JFbHNlRm46ICgpID0+IE1heWJlPFQ+KTogTWF5YmU8VD4ge1xuICAgIHJldHVybiBvckVsc2Uob3JFbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmFuZGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FuZCkgKi9cbiAgYW5kPFU+KHRoaXM6IE1heWJlPFQ+LCBtQW5kOiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gYW5kKG1BbmQsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmFuZFRoZW5gXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNhbmR0aGVuKSAqL1xuICBhbmRUaGVuPFU+KHRoaXM6IE1heWJlPFQ+LCBhbmRUaGVuRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gYW5kVGhlbihhbmRUaGVuRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmNoYWluYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjY2hhaW4pICovXG4gIGNoYWluPFU+KHRoaXM6IE1heWJlPFQ+LCBjaGFpbkZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIHRoaXMuYW5kVGhlbihjaGFpbkZuKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5mbGF0TWFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjZmxhdG1hcCkgKi9cbiAgZmxhdE1hcDxVPih0aGlzOiBNYXliZTxUPiwgZmxhdE1hcEZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIHRoaXMuYW5kVGhlbihmbGF0TWFwRm4pO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVuc2FmZWx5VW53cmFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdW5zYWZlbHl1bndyYXApICovXG4gIHVuc2FmZWx5VW53cmFwKCk6IFQge1xuICAgIHJldHVybiB0aGlzLnZhbHVlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVud3JhcE9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdW53cmFwb3IpICovXG4gIHVud3JhcE9yKHRoaXM6IE1heWJlPFQ+LCBkZWZhdWx0VmFsdWU6IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3IoZGVmYXVsdFZhbHVlLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS51bndyYXBPckVsc2VgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bndyYXBvcmVsc2UpICovXG4gIHVud3JhcE9yRWxzZSh0aGlzOiBNYXliZTxUPiwgZWxzZUZuOiAoKSA9PiBUKTogVCB7XG4gICAgcmV0dXJuIHVud3JhcE9yRWxzZShlbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvT2tPckVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVycikgKi9cbiAgdG9Pa09yRXJyPEU+KHRoaXM6IE1heWJlPFQ+LCBlcnJvcjogRSk6IFJlc3VsdDxULCBFPiB7XG4gICAgcmV0dXJuIHRvT2tPckVycihlcnJvciwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9Pa09yRWxzZUVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVsc2VlcnIpICovXG4gIHRvT2tPckVsc2VFcnI8RT4odGhpczogTWF5YmU8VD4sIGVsc2VGbjogKCkgPT4gRSk6IFJlc3VsdDxULCBFPiB7XG4gICAgcmV0dXJuIHRvT2tPckVsc2VFcnIoZWxzZUZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS50b1N0cmluZ2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvc3RyaW5nKSAqL1xuICB0b1N0cmluZyh0aGlzOiBNYXliZTxUPik6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRvU3RyaW5nKHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmVxdWFsc2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2VxdWFscykgKi9cbiAgZXF1YWxzKHRoaXM6IE1heWJlPFQ+LCBjb21wYXJpc29uOiBNYXliZTxUPik6IGJvb2xlYW4ge1xuICAgIHJldHVybiBlcXVhbHMoY29tcGFyaXNvbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNhcCkgKi9cbiAgYXA8QSwgQj4odGhpczogTWF5YmU8KHZhbDogQSkgPT4gQj4sIHZhbDogTWF5YmU8QT4pOiBNYXliZTxCPiB7XG4gICAgcmV0dXJuIGFwKHRoaXMsIHZhbCk7XG4gIH1cblxuICAvKipcbiAgICBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5nZXRgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNwcm9wKVxuXG4gICAgICAgIElmIHlvdSBoYXZlIGEgYE1heWJlYCBvZiBhbiBvYmplY3QgdHlwZSwgeW91IGNhbiBkbyBgdGhhdE1heWJlLmdldCgnYSBrZXknKWBcbiAgICB0byBsb29rIHVwIHRoZSBuZXh0IGxheWVyIGRvd24gaW4gdGhlIG9iamVjdC5cblxuICAgIGBgYHRzXG4gICAgdHlwZSBEZWVwT3B0aW9uYWxUeXBlID0ge1xuICAgICAgc29tZXRoaW5nPzoge1xuICAgICAgICB3aXRoPzoge1xuICAgICAgICAgIGRlZXBlcktleXM/OiBzdHJpbmc7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgZnVsbHlTZXQ6IERlZXBUeXBlID0ge1xuICAgICAgc29tZXRoaW5nOiB7XG4gICAgICAgIHdpdGg6IHtcbiAgICAgICAgICBkZWVwZXJLZXlzOiAnbGlrZSB0aGlzJ1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfTtcblxuICAgIGNvbnN0IGRlZXBKdXN0ID0gTWF5YmUub2YoZnVsbHlTZXQpXG4gICAgICAuZ2V0KCdzb21ldGhpbmcnKVxuICAgICAgLmdldCgnd2l0aCcpXG4gICAgICAuZ2V0KCdkZWVwZXJLZXlzJyk7XG5cbiAgICBjb25zb2xlLmxvZyhkZWVwSnVzdCk7IC8vIEp1c3QoJ2xpa2UgdGhpcycpO1xuXG4gICAgY29uc3QgcGFydGlhbGx5VW5zZXQ6IERlZXBUeXBlID0geyBzb21ldGhpbmc6IHsgfSB9O1xuXG4gICAgY29uc3QgZGVlcEVtcHR5ID0gTWF5YmUub2YocGFydGlhbGx5VW5zZXQpXG4gICAgICAuZ2V0KCdzb21ldGhpbmcnKVxuICAgICAgLmdldCgnd2l0aCcpXG4gICAgICAuZ2V0KCdkZWVwZXJLZXlzJyk7XG5cbiAgICBjb25zb2xlLmxvZyhkZWVwRW1wdHkpOyAvLyBOb3RoaW5nXG4gICAgYGBgXG4gICAqL1xuICBnZXQ8SyBleHRlbmRzIGtleW9mIFQ+KHRoaXM6IE1heWJlPFQ+LCBrZXk6IEspOiBNYXliZTxOb25OdWxsYWJsZTxUW0tdPj4ge1xuICAgIHJldHVybiB0aGlzLmFuZFRoZW4ocHJvcGVydHkoa2V5KSk7XG4gIH1cbn1cblxuLyoqXG4gIEEgYE5vdGhpbmdgIGluc3RhbmNlIGlzIHRoZSAqYWJzZW50KiB2YXJpYW50IGluc3RhbmNlIG9mIHRoZVxuICBbYE1heWJlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWF5YmUpIHR5cGUsIHJlcHJlc2VudGluZyB0aGUgcHJlc2VuY2Ugb2YgYVxuICB2YWx1ZSB3aGljaCBtYXkgYmUgYWJzZW50LiBGb3IgYSBmdWxsIGRpc2N1c3Npb24sIHNlZSBbdGhlIG1vZHVsZVxuICBkb2NzXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCkuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIHdoaWNoIHdvdWxkIGJlIHdyYXBwZWQgaW4gYSBgSnVzdGAgdmFyaWFudCBvZiBgTWF5YmVgLlxuICovXG5leHBvcnQgY2xhc3MgTm90aGluZzxUPiBpbXBsZW1lbnRzIE1heWJlU2hhcGU8VD4ge1xuICAvKiogYE5vdGhpbmdgIGlzIGFsd2F5cyBbYFZhcmlhbnQuTm90aGluZ2BdKC4uL2VudW1zL19tYXliZV8udmFyaWFudCNub3RoaW5nKS4gKi9cbiAgcmVhZG9ubHkgdmFyaWFudDogVmFyaWFudC5Ob3RoaW5nID0gVmFyaWFudC5Ob3RoaW5nO1xuXG4gIC8qKlxuICAgIENyZWF0ZSBhbiBpbnN0YW5jZSBvZiBgTWF5YmUuTm90aGluZ2Agd2l0aCBgbmV3YC5cblxuICAgIEBub3RlIFdoaWxlIHlvdSAqbWF5KiBjcmVhdGUgdGhlIGBOb3RoaW5nYCB0eXBlIHZpYSBub3JtYWwgSmF2YVNjcmlwdFxuICAgIGNsYXNzIGNvbnN0cnVjdGlvbiwgaXQgaXMgbm90IHJlY29tbWVuZGVkIGZvciB0aGUgZnVuY3Rpb25hbCBzdHlsZSBmb3JcbiAgICB3aGljaCB0aGUgbGlicmFyeSBpcyBpbnRlbmRlZC4gSW5zdGVhZCwgdXNlIFtgTWF5YmUub2ZgXSAoZm9yIHRoZSBnZW5lcmFsXG4gICAgY2FzZSkgb3IgW2BNYXliZS5ub3RoaW5nYF0gZm9yIHRoaXMgc3BlY2lmaWMgY2FzZS5cblxuICAgIFtgTWF5YmUub2ZgXTogLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb2ZcbiAgICBbYE1heWJlLm5vdGhpbmdgXTogLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbm90aGluZ1xuXG4gICAgYGBgdHNcbiAgICAvLyBBdm9pZDpcbiAgICBjb25zdCBhTm90aGluZyA9IG5ldyBNYXliZS5FcnIoKTtcblxuICAgIC8vIFByZWZlcjpcbiAgICBjb25zdCBhTm90aGluZyA9IE1heWJlLm5vdGhpbmcoKTtcbiAgICBgYGBcblxuICAgIGBudWxsYCBhbmQgYHVuZGVmaW5lZGAgYXJlIGFsbG93ZWQgc28gdGhhdCB5b3UgbWF5IGV4cGxpY2l0bHkgY29uc3RydWN0IHRoZVxuICAgIGBFcnJgIHR5cGUgd2l0aCBhIGtub3duIGBudWxsYCBvciBgdW5kZWZpbmVkYCB2YWx1ZS4gKFRoaXMgbWF5YmUgaGVscGZ1bFxuICAgIHByaW1hcmlseSB3aGVuIHRyYW5zaXRpb25pbmcgYSBjb2RlYmFzZSB0byB0aGUgdXNlIG9mIGBNYXliZWAuKVxuXG4gICAgQHRocm93cyAgICAgIElmIHlvdSBwYXNzIGBudWxsYCBvciBgdW5kZWZpbmVkYC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKF8/OiBudWxsKSB7XG4gICAgLyogbm90aGluZyB0byBkbyAqL1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmlzSnVzdGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2lzanVzdCkgKi9cbiAgaXNKdXN0KHRoaXM6IE1heWJlPFQ+KTogdGhpcyBpcyBKdXN0PFQ+IHtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuaXNOb3RoaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjaXNub3RoaW5nKSAqL1xuICBpc05vdGhpbmcodGhpczogTWF5YmU8VD4pOiB0aGlzIGlzIE5vdGhpbmc8VD4ge1xuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcCkgKi9cbiAgbWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBtYXBGbjogKHQ6IFQpID0+IFUpOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIG1hcChtYXBGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwT3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXBvcikgKi9cbiAgbWFwT3I8VT4odGhpczogTWF5YmU8VD4sIG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yKG9yVSwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcG9yZWxzZSkgKi9cbiAgbWFwT3JFbHNlPFU+KHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yRWxzZShvckVsc2VGbiwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hdGNoYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWF0Y2gpICovXG4gIG1hdGNoPFU+KHRoaXM6IE1heWJlPFQ+LCBtYXRjaGVyOiBNYXRjaGVyPFQsIFU+KTogVSB7XG4gICAgcmV0dXJuIG1hdGNoKG1hdGNoZXIsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb3IpICovXG4gIG9yKHRoaXM6IE1heWJlPFQ+LCBtT3I6IE1heWJlPFQ+KTogTWF5YmU8VD4ge1xuICAgIHJldHVybiBvcihtT3IsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI29yZWxzZSkgKi9cbiAgb3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gTWF5YmU8VD4pOiBNYXliZTxUPiB7XG4gICAgcmV0dXJuIG9yRWxzZShvckVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYW5kYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYW5kKSAqL1xuICBhbmQ8VT4odGhpczogTWF5YmU8VD4sIG1BbmQ6IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiBhbmQobUFuZCwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYW5kVGhlbmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FuZHRoZW4pICovXG4gIGFuZFRoZW48VT4odGhpczogTWF5YmU8VD4sIGFuZFRoZW5GbjogKHQ6IFQpID0+IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiBhbmRUaGVuKGFuZFRoZW5GbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuY2hhaW5gXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNjaGFpbikgKi9cbiAgY2hhaW48VT4odGhpczogTWF5YmU8VD4sIGNoYWluRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gdGhpcy5hbmRUaGVuKGNoYWluRm4pO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmZsYXRNYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNmbGF0bWFwKSAqL1xuICBmbGF0TWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBmbGF0TWFwRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gdGhpcy5hbmRUaGVuKGZsYXRNYXBGbik7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW5zYWZlbHlVbndyYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bnNhZmVseXVud3JhcCkgKi9cbiAgdW5zYWZlbHlVbndyYXAoKTogbmV2ZXIge1xuICAgIHRocm93IG5ldyBFcnJvcignVHJpZWQgdG8gYHVuc2FmZWx5VW53cmFwKE5vdGhpbmcpYCcpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVud3JhcE9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdW53cmFwb3IpICovXG4gIHVud3JhcE9yKHRoaXM6IE1heWJlPFQ+LCBkZWZhdWx0VmFsdWU6IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3IoZGVmYXVsdFZhbHVlLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS51bndyYXBPckVsc2VgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bndyYXBvcmVsc2UpICovXG4gIHVud3JhcE9yRWxzZSh0aGlzOiBNYXliZTxUPiwgZWxzZUZuOiAoKSA9PiBUKTogVCB7XG4gICAgcmV0dXJuIHVud3JhcE9yRWxzZShlbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvT2tPckVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVycikgKi9cbiAgdG9Pa09yRXJyPEU+KHRoaXM6IE1heWJlPFQ+LCBlcnJvcjogRSk6IFJlc3VsdDxULCBFPiB7XG4gICAgcmV0dXJuIHRvT2tPckVycihlcnJvciwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9Pa09yRWxzZUVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVsc2VlcnIpICovXG4gIHRvT2tPckVsc2VFcnI8RT4odGhpczogTWF5YmU8VD4sIGVsc2VGbjogKCkgPT4gRSk6IFJlc3VsdDxULCBFPiB7XG4gICAgcmV0dXJuIHRvT2tPckVsc2VFcnIoZWxzZUZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS50b1N0cmluZ2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvc3RyaW5nKSAqL1xuICB0b1N0cmluZyh0aGlzOiBNYXliZTxUPik6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRvU3RyaW5nKHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmVxdWFsc2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2VxdWFscykgKi9cbiAgZXF1YWxzKHRoaXM6IE1heWJlPFQ+LCBjb21wYXJpc29uOiBNYXliZTxUPik6IGJvb2xlYW4ge1xuICAgIHJldHVybiBlcXVhbHMoY29tcGFyaXNvbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNhcCkgKi9cbiAgYXA8QSwgQj4odGhpczogTWF5YmU8KHZhbDogQSkgPT4gQj4sIHZhbDogTWF5YmU8QT4pOiBNYXliZTxCPiB7XG4gICAgcmV0dXJuIGFwKHRoaXMsIHZhbCk7XG4gIH1cblxuICAvKipcbiAgICBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5nZXRgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNwcm9wKVxuXG4gICAgICAgIElmIHlvdSBoYXZlIGEgYE1heWJlYCBvZiBhbiBvYmplY3QgdHlwZSwgeW91IGNhbiBkbyBgdGhhdE1heWJlLmdldCgnYSBrZXknKWBcbiAgICB0byBsb29rIHVwIHRoZSBuZXh0IGxheWVyIGRvd24gaW4gdGhlIG9iamVjdC5cblxuICAgIGBgYHRzXG4gICAgdHlwZSBEZWVwT3B0aW9uYWxUeXBlID0ge1xuICAgICAgc29tZXRoaW5nPzoge1xuICAgICAgICB3aXRoPzoge1xuICAgICAgICAgIGRlZXBlcktleXM/OiBzdHJpbmc7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgZnVsbHlTZXQ6IERlZXBUeXBlID0ge1xuICAgICAgc29tZXRoaW5nOiB7XG4gICAgICAgIHdpdGg6IHtcbiAgICAgICAgICBkZWVwZXJLZXlzOiAnbGlrZSB0aGlzJ1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfTtcblxuICAgIGNvbnN0IGRlZXBKdXN0ID0gTWF5YmUub2YoZnVsbHlTZXQpXG4gICAgICAuZ2V0KCdzb21ldGhpbmcnKVxuICAgICAgLmdldCgnd2l0aCcpXG4gICAgICAuZ2V0KCdkZWVwZXJLZXlzJyk7XG5cbiAgICBjb25zb2xlLmxvZyhkZWVwSnVzdCk7IC8vIEp1c3QoJ2xpa2UgdGhpcycpO1xuXG4gICAgY29uc3QgcGFydGlhbGx5VW5zZXQ6IERlZXBUeXBlID0geyBzb21ldGhpbmc6IHsgfSB9O1xuXG4gICAgY29uc3QgZGVlcEVtcHR5ID0gTWF5YmUub2YocGFydGlhbGx5VW5zZXQpXG4gICAgICAuZ2V0KCdzb21ldGhpbmcnKVxuICAgICAgLmdldCgnd2l0aCcpXG4gICAgICAuZ2V0KCdkZWVwZXJLZXlzJyk7XG5cbiAgICBjb25zb2xlLmxvZyhkZWVwRW1wdHkpOyAvLyBOb3RoaW5nXG4gICAgYGBgXG4gICAqL1xuICBnZXQ8SyBleHRlbmRzIGtleW9mIFQ+KHRoaXM6IE1heWJlPFQ+LCBrZXk6IEspOiBNYXliZTxOb25OdWxsYWJsZTxUW0tdPj4ge1xuICAgIHJldHVybiB0aGlzLmFuZFRoZW4ocHJvcGVydHkoa2V5KSk7XG4gIH1cbn1cblxuLyoqXG4gIElzIHRoaXMgcmVzdWx0IGEgYEp1c3RgIGluc3RhbmNlP1xuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHBhcmFtIG1heWJlIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIGNoZWNrLlxuICBAcmV0dXJucyAgICAgYHRydWVgIGlmIGBtYXliZWAgaXMgYEp1c3RgLCBgZmFsc2VgIG90aGVyd2lzZS4gSW4gVHlwZVNjcmlwdCxcbiAgICAgICAgICAgICAgIGFsc28gbmFycm93cyB0aGUgdHlwZSBmcm9tIGBNYXliZTxUPmAgdG8gYEp1c3Q8VD5gLlxuICovXG5leHBvcnQgZnVuY3Rpb24gaXNKdXN0PFQ+KG1heWJlOiBNYXliZTxUPik6IG1heWJlIGlzIEp1c3Q8VD4ge1xuICByZXR1cm4gbWF5YmUudmFyaWFudCA9PT0gVmFyaWFudC5KdXN0O1xufVxuXG4vKipcbiAgSXMgdGhpcyByZXN1bHQgYSBgTm90aGluZ2AgaW5zdGFuY2U/XG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAcGFyYW0gbWF5YmUgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gY2hlY2suXG4gIEByZXR1cm5zICAgICBgdHJ1ZWAgaWYgYG1heWJlYCBpcyBgbm90aGluZ2AsIGBmYWxzZWAgb3RoZXJ3aXNlLiBJbiBUeXBlU2NyaXB0LFxuICAgICAgICAgICAgICAgYWxzbyBuYXJyb3dzIHRoZSB0eXBlIGZyb20gYE1heWJlPFQ+YCB0byBgTm90aGluZzxUPmAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBpc05vdGhpbmc8VD4obWF5YmU6IE1heWJlPFQ+KTogbWF5YmUgaXMgTm90aGluZzxUPiB7XG4gIHJldHVybiBtYXliZS52YXJpYW50ID09PSBWYXJpYW50Lk5vdGhpbmc7XG59XG5cbi8qKlxuICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYE1heWJlLkp1c3RgLlxuXG4gIGBudWxsYCBhbmQgYHVuZGVmaW5lZGAgYXJlIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgdGhlXG4gIGZ1bmN0aW9uIG1heSBgdGhyb3dgIG9uIHRob3NlIHJhdGhlciB0aGFuIGNvbnN0cnVjdGluZyBhIHR5cGUgbGlrZVxuICBgTWF5YmU8dW5kZWZpbmVkPmAuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSBpdGVtIGNvbnRhaW5lZCBpbiB0aGUgYE1heWJlYC5cbiAgQHBhcmFtIHZhbHVlIFRoZSB2YWx1ZSB0byB3cmFwIGluIGEgYE1heWJlLkp1c3RgLlxuICBAcmV0dXJucyAgICAgQW4gaW5zdGFuY2Ugb2YgYE1heWJlLkp1c3Q8VD5gLlxuICBAdGhyb3dzICAgICAgSWYgeW91IHBhc3MgYG51bGxgIG9yIGB1bmRlZmluZWRgLlxuICovXG5leHBvcnQgZnVuY3Rpb24ganVzdDxUPih2YWx1ZT86IFQgfCBudWxsKTogTWF5YmU8VD4ge1xuICByZXR1cm4gbmV3IEp1c3Q8VD4odmFsdWUpO1xufVxuXG4vKipcbiAgQ3JlYXRlIGFuIGluc3RhbmNlIG9mIGBNYXliZS5Ob3RoaW5nYC5cblxuICBJZiB5b3Ugd2FudCB0byBjcmVhdGUgYW4gaW5zdGFuY2Ugd2l0aCBhIHNwZWNpZmljIHR5cGUsIGUuZy4gZm9yIHVzZSBpbiBhXG4gIGZ1bmN0aW9uIHdoaWNoIGV4cGVjdHMgYSBgTWF5YmU8VD5gIHdoZXJlIHRoZSBgPFQ+YCBpcyBrbm93biBidXQgeW91IGhhdmUgbm9cbiAgdmFsdWUgdG8gZ2l2ZSBpdCwgeW91IGNhbiB1c2UgYSB0eXBlIHBhcmFtZXRlcjpcblxuICBgYGB0c1xuICBjb25zdCBub3RTdHJpbmcgPSBNYXliZS5ub3RoaW5nPHN0cmluZz4oKTtcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSBpdGVtIGNvbnRhaW5lZCBpbiB0aGUgYE1heWJlYC5cbiAgQHJldHVybnMgICAgIEFuIGluc3RhbmNlIG9mIGBNYXliZS5Ob3RoaW5nPFQ+YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG5vdGhpbmc8VD4oXz86IG51bGwpOiBNYXliZTxUPiB7XG4gIHJldHVybiBuZXcgTm90aGluZzxUPihfKTtcbn1cblxuLyoqXG4gIENyZWF0ZSBhIGBNYXliZWAgZnJvbSBhbnkgdmFsdWUuXG5cbiAgVG8gc3BlY2lmeSB0aGF0IHRoZSByZXN1bHQgc2hvdWxkIGJlIGludGVycHJldGVkIGFzIGEgc3BlY2lmaWMgdHlwZSwgeW91IG1heVxuICBpbnZva2UgYE1heWJlLm9mYCB3aXRoIGFuIGV4cGxpY2l0IHR5cGUgcGFyYW1ldGVyOlxuXG4gIGBgYHRzXG4gIGNvbnN0IGZvbyA9IE1heWJlLm9mPHN0cmluZz4obnVsbCk7XG4gIGBgYFxuXG4gIFRoaXMgaXMgdXN1YWxseSBvbmx5IGltcG9ydGFudCBpbiB0d28gY2FzZXM6XG5cbiAgMS4gIElmIHlvdSBhcmUgaW50ZW50aW9uYWxseSBjb25zdHJ1Y3RpbmcgYSBgTm90aGluZ2AgZnJvbSBhIGtub3duIGBudWxsYCBvclxuICAgICAgdW5kZWZpbmVkIHZhbHVlICp3aGljaCBpcyB1bnR5cGVkKi5cbiAgMi4gIElmIHlvdSBhcmUgc3BlY2lmeWluZyB0aGF0IHRoZSB0eXBlIGlzIG1vcmUgZ2VuZXJhbCB0aGFuIHRoZSB2YWx1ZSBwYXNzZWRcbiAgICAgIChzaW5jZSBUeXBlU2NyaXB0IGNhbiBkZWZpbmUgdHlwZXMgYXMgbGl0ZXJhbHMpLlxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgaXRlbSBjb250YWluZWQgaW4gdGhlIGBNYXliZWAuXG4gIEBwYXJhbSB2YWx1ZSBUaGUgdmFsdWUgdG8gd3JhcCBpbiBhIGBNYXliZWAuIElmIGl0IGlzIGB1bmRlZmluZWRgIG9yIGBudWxsYCxcbiAgICAgICAgICAgICAgIHRoZSByZXN1bHQgd2lsbCBiZSBgTm90aGluZ2A7IG90aGVyd2lzZSBpdCB3aWxsIGJlIHRoZSB0eXBlIG9mXG4gICAgICAgICAgICAgICB0aGUgdmFsdWUgcGFzc2VkLlxuICovXG5leHBvcnQgZnVuY3Rpb24gb2Y8VD4odmFsdWU/OiBUIHwgbnVsbCk6IE1heWJlPFQ+IHtcbiAgcmV0dXJuIGlzVm9pZCh2YWx1ZSkgPyBub3RoaW5nPFQ+KCkgOiBqdXN0KHZhbHVlKTtcbn1cblxuLyoqIEFsaWFzIGZvciBbYG9mYF0oI29mKSwgcHJpbWFyaWx5IGZvciBjb21wYXRpYmlsaXR5IHdpdGggRm9sa3RhbGUuICovXG5leHBvcnQgY29uc3QgZnJvbU51bGxhYmxlID0gb2Y7XG5cbi8qKlxuICBNYXAgb3ZlciBhIGBNYXliZWAgaW5zdGFuY2U6IGFwcGx5IHRoZSBmdW5jdGlvbiB0byB0aGUgd3JhcHBlZCB2YWx1ZSBpZiB0aGVcbiAgaW5zdGFuY2UgaXMgYEp1c3RgLCBhbmQgcmV0dXJuIGBOb3RoaW5nYCBpZiB0aGUgaW5zdGFuY2UgaXMgYE5vdGhpbmdgLlxuXG4gIGBNYXliZS5tYXBgIHdvcmtzIGEgbG90IGxpa2UgYEFycmF5LnByb3RvdHlwZS5tYXBgOiBgTWF5YmVgIGFuZCBgQXJyYXlgIGFyZVxuICBib3RoICpjb250YWluZXJzKiBmb3Igb3RoZXIgdGhpbmdzLiBJZiB5b3UgaGF2ZSBubyBpdGVtcyBpbiBhbiBhcnJheSBvZlxuICBudW1iZXJzIG5hbWVkIGBmb29gIGFuZCBjYWxsIGBmb28ubWFwKHggPT4geCArIDEpYCwgeW91J2xsIHN0aWxsIGp1c3QgaGF2ZSBhblxuICBhcnJheSB3aXRoIG5vdGhpbmcgaW4gaXQuIEJ1dCBpZiB5b3UgaGF2ZSBhbnkgaXRlbXMgaW4gdGhlIGFycmF5IChgWzIsIDNdYCksXG4gIGFuZCB5b3UgY2FsbCBgZm9vLm1hcCh4ID0+IHggKyAxKWAgb24gaXQsIHlvdSdsbCBnZXQgYSBuZXcgYXJyYXkgd2l0aCBlYWNoIG9mXG4gIHRob3NlIGl0ZW1zIGluc2lkZSB0aGUgYXJyYXkgXCJjb250YWluZXJcIiB0cmFuc2Zvcm1lZCAoYFszLCA0XWApLlxuXG4gIFRoYXQncyBleGFjdGx5IHdoYXQncyBoYXBwZW5pbmcgd2l0aCBgTWF5YmUubWFwYC4gSWYgdGhlIGNvbnRhaW5lciBpcyAqZW1wdHkqXG4gIOKAk8KgdGhlIGBOb3RoaW5nYCB2YXJpYW50IOKAkyB5b3UganVzdCBnZXQgYmFjayBhbiBlbXB0eSBjb250YWluZXIuIElmIHRoZVxuICBjb250YWluZXIgaGFzIHNvbWV0aGluZyBpbiBpdCDigJPCoHRoZSBgSnVzdGAgdmFyaWFudCDigJPCoHlvdSBnZXQgYmFjayBhIGNvbnRhaW5lclxuICB3aXRoIHRoZSBpdGVtIGluc2lkZSB0cmFuc2Zvcm1lZC5cblxuICAoU28uLi4gd2h5IG5vdCBqdXN0IHVzZSBhbiBhcnJheT8gVGhlIGJpZ2dlc3QgcmVhc29uIGlzIHRoYXQgYW4gYXJyYXkgY2FuIGJlXG4gIGFueSBsZW5ndGguIFdpdGggYSBgTWF5YmVgLCB3ZSdyZSBjYXB0dXJpbmcgdGhlIGlkZWEgb2YgXCJzb21ldGhpbmcgb3JcbiAgbm90aGluZ1wiIHJhdGhlciB0aGFuIFwiMCB0byBuXCIgaXRlbXMuIEFuZCB0aGlzIGxldHMgdXMgaW1wbGVtZW50IGEgd2hvbGUgc2V0XG4gIG9mICpvdGhlciogaW50ZXJmYWNlcywgbGlrZSB0aG9zZSBpbiB0aGlzIG1vZHVsZS4pXG5cbiAgIyMjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGNvbnN0IGxlbmd0aCA9IChzOiBzdHJpbmcpID0+IHMubGVuZ3RoO1xuXG4gIGNvbnN0IGp1c3RBU3RyaW5nID0gTWF5YmUuanVzdCgnc3RyaW5nJyk7XG4gIGNvbnN0IGp1c3RUaGVTdHJpbmdMZW5ndGggPSBtYXAobGVuZ3RoLCBqdXN0QVN0cmluZyk7XG4gIGNvbnNvbGUubG9nKGp1c3RUaGVTdHJpbmdMZW5ndGgudG9TdHJpbmcoKSk7IC8vIEp1c3QoNilcblxuICBjb25zdCBub3RBU3RyaW5nID0gTWF5YmUubm90aGluZzxzdHJpbmc+KCk7XG4gIGNvbnN0IG5vdEFTdHJpbmdMZW5ndGggPSBtYXAobGVuZ3RoLCBub3RBU3RyaW5nKTtcbiAgY29uc29sZS5sb2cobm90QVN0cmluZ0xlbmd0aC50b1N0cmluZygpKTsgLy8gXCJOb3RoaW5nXCJcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIFUgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUgb2YgdGhlIHJldHVybmVkIGBNYXliZWAuXG4gIEBwYXJhbSBtYXBGbiBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdGhlIHZhbHVlIHRvIGlmIGBNYXliZWAgaXMgYEp1c3RgLlxuICBAcGFyYW0gbWF5YmUgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gbWFwIG92ZXIuXG4gIEByZXR1cm5zICAgICBBIG5ldyBgTWF5YmVgIHdpdGggdGhlIHJlc3VsdCBvZiBhcHBseWluZyBgbWFwRm5gIHRvIHRoZSB2YWx1ZVxuICAgICAgICAgICAgICAgaW4gYSBgSnVzdGAsIG9yIGBOb3RoaW5nYCBpZiBgbWF5YmVgIGlzIGBOb3RoaW5nYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hcDxULCBVPihtYXBGbjogKHQ6IFQpID0+IFUpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBtYXA8VCwgVT4obWFwRm46ICh0OiBUKSA9PiBVLCBtYXliZTogTWF5YmU8VD4pOiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBtYXA8VCwgVT4oXG4gIG1hcEZuOiAodDogVCkgPT4gVSxcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogTWF5YmU8VT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VT4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8ganVzdChtYXBGbihtLnZhbHVlKSkgOiBub3RoaW5nPFU+KCkpO1xuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKlxuICBNYXAgb3ZlciBhIGBNYXliZWAgaW5zdGFuY2UgYW5kIGdldCBvdXQgdGhlIHZhbHVlIGlmIGBtYXliZWAgaXMgYSBgSnVzdGAsIG9yXG4gIHJldHVybiBhIGRlZmF1bHQgdmFsdWUgaWYgYG1heWJlYCBpcyBhIGBOb3RoaW5nYC5cblxuICAjIyMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgY29uc3QgbGVuZ3RoID0gKHM6IHN0cmluZykgPT4gcy5sZW5ndGg7XG5cbiAgY29uc3QganVzdEFTdHJpbmcgPSBNYXliZS5qdXN0KCdzdHJpbmcnKTtcbiAgY29uc3QgdGhlU3RyaW5nTGVuZ3RoID0gbWFwT3IoMCwgbGVuZ3RoLCBqdXN0QVN0cmluZyk7XG4gIGNvbnNvbGUubG9nKHRoZVN0cmluZ0xlbmd0aCk7IC8vIDZcblxuICBjb25zdCBub3RBU3RyaW5nID0gTWF5YmUubm90aGluZzxzdHJpbmc+KCk7XG4gIGNvbnN0IG5vdEFTdHJpbmdMZW5ndGggPSBtYXBPcigwLCBsZW5ndGgsIG5vdEFTdHJpbmcpXG4gIGNvbnNvbGUubG9nKG5vdEFTdHJpbmdMZW5ndGgpOyAvLyAwXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHR5cGVwYXJhbSBVIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlIG9mIHRoZSByZXR1cm5lZCBgTWF5YmVgLlxuICBAcGFyYW0gb3JVICAgVGhlIGRlZmF1bHQgdmFsdWUgdG8gdXNlIGlmIGBtYXliZWAgaXMgYE5vdGhpbmdgXG4gIEBwYXJhbSBtYXBGbiBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdGhlIHZhbHVlIHRvIGlmIGBNYXliZWAgaXMgYEp1c3RgXG4gIEBwYXJhbSBtYXliZSBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBtYXAgb3Zlci5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFU+KG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVLCBtYXliZTogTWF5YmU8VD4pOiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFU+KG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogKG1heWJlOiBNYXliZTxUPikgPT4gVTtcbmV4cG9ydCBmdW5jdGlvbiBtYXBPcjxULCBVPihvclU6IFUpOiAobWFwRm46ICh0OiBUKSA9PiBVKSA9PiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFU+KFxuICBvclU6IFUsXG4gIG1hcEZuPzogKHQ6IFQpID0+IFUsXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IFUgfCAoKG1heWJlOiBNYXliZTxUPikgPT4gVSkgfCAoKG1hcEZuOiAodDogVCkgPT4gVSkgPT4gKG1heWJlOiBNYXliZTxUPikgPT4gVSkge1xuICBmdW5jdGlvbiBmdWxsT3AoZm46ICh0OiBUKSA9PiBVLCBtOiBNYXliZTxUPikge1xuICAgIHJldHVybiBtLmlzSnVzdCgpID8gZm4obS52YWx1ZSkgOiBvclU7XG4gIH1cblxuICBmdW5jdGlvbiBwYXJ0aWFsT3AoZm46ICh0OiBUKSA9PiBVKTogKG1heWJlOiBNYXliZTxUPikgPT4gVTtcbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSwgY3VycmllZE1heWJlOiBNYXliZTxUPik6IFU7XG4gIGZ1bmN0aW9uIHBhcnRpYWxPcChmbjogKHQ6IFQpID0+IFUsIGN1cnJpZWRNYXliZT86IE1heWJlPFQ+KTogVSB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB7XG4gICAgcmV0dXJuIGN1cnJpZWRNYXliZSAhPT0gdW5kZWZpbmVkXG4gICAgICA/IGZ1bGxPcChmbiwgY3VycmllZE1heWJlKVxuICAgICAgOiAoZXh0cmFDdXJyaWVkTWF5YmU6IE1heWJlPFQ+KSA9PiBmdWxsT3AoZm4sIGV4dHJhQ3VycmllZE1heWJlKTtcbiAgfVxuXG4gIHJldHVybiBtYXBGbiA9PT0gdW5kZWZpbmVkXG4gICAgPyBwYXJ0aWFsT3BcbiAgICA6IG1heWJlID09PSB1bmRlZmluZWRcbiAgICAgID8gcGFydGlhbE9wKG1hcEZuKVxuICAgICAgOiBwYXJ0aWFsT3AobWFwRm4sIG1heWJlKTtcbn1cblxuLyoqXG4gIE1hcCBvdmVyIGEgYE1heWJlYCBpbnN0YW5jZSBhbmQgZ2V0IG91dCB0aGUgdmFsdWUgaWYgYG1heWJlYCBpcyBhIGBKdXN0YCxcbiAgb3IgdXNlIGEgZnVuY3Rpb24gdG8gY29uc3RydWN0IGEgZGVmYXVsdCB2YWx1ZSBpZiBgbWF5YmVgIGlzIGBOb3RoaW5nYC5cblxuICAjIyMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgY29uc3QgbGVuZ3RoID0gKHM6IHN0cmluZykgPT4gcy5sZW5ndGg7XG4gIGNvbnN0IGdldERlZmF1bHQgPSAoKSA9PiAwO1xuXG4gIGNvbnN0IGp1c3RBU3RyaW5nID0gTWF5YmUuanVzdCgnc3RyaW5nJyk7XG4gIGNvbnN0IHRoZVN0cmluZ0xlbmd0aCA9IG1hcE9yRWxzZShnZXREZWZhdWx0LCBsZW5ndGgsIGp1c3RBU3RyaW5nKTtcbiAgY29uc29sZS5sb2codGhlU3RyaW5nTGVuZ3RoKTsgLy8gNlxuXG4gIGNvbnN0IG5vdEFTdHJpbmcgPSBNYXliZS5ub3RoaW5nPHN0cmluZz4oKTtcbiAgY29uc3Qgbm90QVN0cmluZ0xlbmd0aCA9IG1hcE9yRWxzZShnZXREZWZhdWx0LCBsZW5ndGgsIG5vdEFTdHJpbmcpXG4gIGNvbnNvbGUubG9nKG5vdEFTdHJpbmdMZW5ndGgpOyAvLyAwXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHR5cGVwYXJhbSBVICAgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlIG9mIHRoZSByZXR1cm5lZCBgTWF5YmVgLlxuICBAcGFyYW0gb3JFbHNlRm4gVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IGlmIGBtYXliZWAgaXMgYE5vdGhpbmdgLlxuICBAcGFyYW0gbWFwRm4gICAgVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IHRvIHRoZSB3cmFwcGVkIHZhbHVlIGlmIGBtYXliZWAgaXMgYEp1c3RgXG4gIEBwYXJhbSBtYXliZSAgICBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBtYXAgb3Zlci5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yRWxzZTxULCBVPihvckVsc2VGbjogKCkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVLCBtYXliZTogTWF5YmU8VD4pOiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yRWxzZTxULCBVPihvckVsc2VGbjogKCkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogKG1heWJlOiBNYXliZTxUPikgPT4gVTtcbmV4cG9ydCBmdW5jdGlvbiBtYXBPckVsc2U8VCwgVT4ob3JFbHNlRm46ICgpID0+IFUpOiAobWFwRm46ICh0OiBUKSA9PiBVKSA9PiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yRWxzZTxULCBVPihcbiAgb3JFbHNlRm46ICgpID0+IFUsXG4gIG1hcEZuPzogKHQ6IFQpID0+IFUsXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IFUgfCAoKG1heWJlOiBNYXliZTxUPikgPT4gVSkgfCAoKG1hcEZuOiAodDogVCkgPT4gVSkgPT4gKG1heWJlOiBNYXliZTxUPikgPT4gVSkge1xuICBmdW5jdGlvbiBmdWxsT3AoZm46ICh0OiBUKSA9PiBVLCBtOiBNYXliZTxUPikge1xuICAgIHJldHVybiBtLmlzSnVzdCgpID8gZm4obS52YWx1ZSkgOiBvckVsc2VGbigpO1xuICB9XG5cbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSk6IChtYXliZTogTWF5YmU8VD4pID0+IFU7XG4gIGZ1bmN0aW9uIHBhcnRpYWxPcChmbjogKHQ6IFQpID0+IFUsIGN1cnJpZWRNYXliZTogTWF5YmU8VD4pOiBVO1xuICBmdW5jdGlvbiBwYXJ0aWFsT3AoZm46ICh0OiBUKSA9PiBVLCBjdXJyaWVkTWF5YmU/OiBNYXliZTxUPik6IFUgfCAoKG1heWJlOiBNYXliZTxUPikgPT4gVSkge1xuICAgIHJldHVybiBjdXJyaWVkTWF5YmUgIT09IHVuZGVmaW5lZFxuICAgICAgPyBmdWxsT3AoZm4sIGN1cnJpZWRNYXliZSlcbiAgICAgIDogKGV4dHJhQ3VycmllZE1heWJlOiBNYXliZTxUPikgPT4gZnVsbE9wKGZuLCBleHRyYUN1cnJpZWRNYXliZSk7XG4gIH1cblxuICBpZiAobWFwRm4gPT09IHVuZGVmaW5lZCkge1xuICAgIHJldHVybiBwYXJ0aWFsT3A7XG4gIH0gZWxzZSBpZiAobWF5YmUgPT09IHVuZGVmaW5lZCkge1xuICAgIHJldHVybiBwYXJ0aWFsT3AobWFwRm4pO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBwYXJ0aWFsT3AobWFwRm4sIG1heWJlKTtcbiAgfVxufVxuXG4vKipcbiAgWW91IGNhbiB0aGluayBvZiB0aGlzIGxpa2UgYSBzaG9ydC1jaXJjdWl0aW5nIGxvZ2ljYWwgXCJhbmRcIiBvcGVyYXRpb24gb24gYVxuICBgTWF5YmVgIHR5cGUuIElmIGBtYXliZWAgaXMgYEp1c3RgLCB0aGVuIHRoZSByZXN1bHQgaXMgdGhlIGBhbmRNYXliZWAuIElmXG4gIGBtYXliZWAgaXMgYE5vdGhpbmdgLCB0aGUgcmVzdWx0IGlzIGBOb3RoaW5nYC5cblxuICBUaGlzIGlzIHVzZWZ1bCB3aGVuIHlvdSBoYXZlIGFub3RoZXIgYE1heWJlYCB2YWx1ZSB5b3Ugd2FudCB0byBwcm92aWRlIGlmIGFuZFxuICAqb25seSBpZiogeW91IGhhdmUgYSBgSnVzdGAg4oCTIHRoYXQgaXMsIHdoZW4geW91IG5lZWQgdG8gbWFrZSBzdXJlIHRoYXQgaWYgeW91XG4gIGBOb3RoaW5nYCwgd2hhdGV2ZXIgZWxzZSB5b3UncmUgaGFuZGluZyBhIGBNYXliZWAgdG8gKmFsc28qIGdldHMgYSBgTm90aGluZ2AuXG5cbiAgTm90aWNlIHRoYXQsIHVubGlrZSBpbiBbYG1hcGBdKCNtYXApIG9yIGl0cyB2YXJpYW50cywgdGhlIG9yaWdpbmFsIGBtYXliZWAgaXNcbiAgbm90IGludm9sdmVkIGluIGNvbnN0cnVjdGluZyB0aGUgbmV3IGBNYXliZWAuXG5cbiAgIyMjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGNvbnN0IGp1c3RBID0gTWF5YmUuanVzdCgnQScpO1xuICBjb25zdCBqdXN0QiA9IE1heWJlLmp1c3QoJ0InKTtcbiAgY29uc3Qgbm90aGluZzogTWF5YmU8bnVtYmVyPiA9IG5vdGhpbmcoKTtcblxuICBjb25zb2xlLmxvZyhNYXliZS5hbmQoanVzdEIsIGp1c3RBKS50b1N0cmluZygpKTsgIC8vIEp1c3QoQilcbiAgY29uc29sZS5sb2coTWF5YmUuYW5kKGp1c3RCLCBub3RoaW5nKS50b1N0cmluZygpKTsgIC8vIE5vdGhpbmdcbiAgY29uc29sZS5sb2coTWF5YmUuYW5kKG5vdGhpbmcsIGp1c3RBKS50b1N0cmluZygpKTsgIC8vIE5vdGhpbmdcbiAgY29uc29sZS5sb2coTWF5YmUuYW5kKG5vdGhpbmcsIG5vdGhpbmcpLnRvU3RyaW5nKCkpOyAgLy8gTm90aGluZ1xuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgICAgVGhlIHR5cGUgb2YgdGhlIGluaXRpYWwgd3JhcHBlZCB2YWx1ZS5cbiAgQHR5cGVwYXJhbSBVICAgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlIG9mIHRoZSByZXR1cm5lZCBgTWF5YmVgLlxuICBAcGFyYW0gYW5kTWF5YmUgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gcmV0dXJuIGlmIGBtYXliZWAgaXMgYEp1c3RgXG4gIEBwYXJhbSBtYXliZSAgICBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBjaGVjay5cbiAgQHJldHVybiAgICAgICAgIGBOb3RoaW5nYCBpZiB0aGUgb3JpZ2luYWwgYG1heWJlYCBpcyBgTm90aGluZ2AsIG9yIGBhbmRNYXliZWBcbiAgICAgICAgICAgICAgICAgIGlmIHRoZSBvcmlnaW5hbCBgbWF5YmVgIGlzIGBKdXN0YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFuZDxULCBVPihhbmRNYXliZTogTWF5YmU8VT4sIG1heWJlOiBNYXliZTxUPik6IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFuZDxULCBVPihhbmRNYXliZTogTWF5YmU8VT4pOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBhbmQ8VCwgVT4oXG4gIGFuZE1heWJlOiBNYXliZTxVPixcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogTWF5YmU8VT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VT4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gYW5kTWF5YmUgOiBub3RoaW5nPFU+KCkpO1xuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKlxuICBBcHBseSBhIGZ1bmN0aW9uIHRvIHRoZSB3cmFwcGVkIHZhbHVlIGlmIGBKdXN0YCBhbmQgcmV0dXJuIGEgbmV3IGBKdXN0YFxuICBjb250YWluaW5nIHRoZSByZXN1bHRpbmcgdmFsdWU7IG9yIHJldHVybiBgTm90aGluZ2AgaWYgYE5vdGhpbmdgLlxuXG4gIFRoaXMgZGlmZmVycyBmcm9tIGBtYXBgIGluIHRoYXQgYHRoZW5GbmAgcmV0dXJucyBhbm90aGVyIGBNYXliZWAuIFlvdSBjYW4gdXNlXG4gIGBhbmRUaGVuYCB0byBjb21iaW5lIHR3byBmdW5jdGlvbnMgd2hpY2ggKmJvdGgqIGNyZWF0ZSBhIGBNYXliZWAgZnJvbSBhblxuICB1bndyYXBwZWQgdHlwZS5cblxuICBZb3UgbWF5IGZpbmQgdGhlIGAudGhlbmAgbWV0aG9kIG9uIGFuIEVTNiBgUHJvbWlzZWAgaGVscGZ1bCBmb3IgYjpcbiAgaWYgeW91IGhhdmUgYSBgUHJvbWlzZWAsIHlvdSBjYW4gcGFzcyBpdHMgYHRoZW5gIG1ldGhvZCBhIGNhbGxiYWNrIHdoaWNoXG4gIHJldHVybnMgYW5vdGhlciBgUHJvbWlzZWAsIGFuZCB0aGUgcmVzdWx0IHdpbGwgbm90IGJlIGEgKm5lc3RlZCogcHJvbWlzZSwgYnV0XG4gIGEgc2luZ2xlIGBQcm9taXNlYC4gVGhlIGRpZmZlcmVuY2UgaXMgdGhhdCBgUHJvbWlzZSN0aGVuYCB1bndyYXBzICphbGwqXG4gIGxheWVycyB0byBvbmx5IGV2ZXIgcmV0dXJuIGEgc2luZ2xlIGBQcm9taXNlYCB2YWx1ZSwgd2hlcmVhcyBgTWF5YmUuYW5kVGhlbmBcbiAgd2lsbCBub3QgdW53cmFwIG5lc3RlZCBgTWF5YmVgcy5cblxuICBUaGlzIGlzIGFsc28gY29tbW9ubHkga25vd24gYXMgKGFuZCB0aGVyZWZvcmUgYWxpYXNlZCBhcykgW2BmbGF0TWFwYF0gb3JcbiAgW2BjaGFpbmBdLiBJdCBpcyBzb21ldGltZXMgYWxzbyBrbm93biBhcyBgYmluZGAsIGJ1dCAqbm90KiBhbGlhc2VkIGFzIHN1Y2hcbiAgYmVjYXVzZSBbYGJpbmRgIGFscmVhZHkgbWVhbnMgc29tZXRoaW5nIGluIEphdmFTY3JpcHRdW2JpbmRdLlxuXG4gIFtgZmxhdE1hcGBdOiAjZmxhdG1hcFxuICBbYGNoYWluYF06ICNjaGFpblxuICBbYmluZF06IGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0phdmFTY3JpcHQvUmVmZXJlbmNlL0dsb2JhbF9PYmplY3RzL0Z1bmN0aW9uL2JpbmRcblxuICAjIyMjIEV4YW1wbGVcblxuICAoVGhpcyBpcyBhIHNvbWV3aGF0IGNvbnRyaXZlZCBleGFtcGxlLCBidXQgaXQgc2VydmVzIHRvIHNob3cgdGhlIHdheSB0aGVcbiAgZnVuY3Rpb24gYmVoYXZlcy4pXG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgLy8gc3RyaW5nIC0+IE1heWJlPG51bWJlcj5cbiAgY29uc3QgdG9NYXliZUxlbmd0aCA9IChzOiBzdHJpbmcpOiBNYXliZTxudW1iZXI+ID0+IE1heWJlLm9mKHMubGVuZ3RoKTtcblxuICAvLyBNYXliZTxzdHJpbmc+XG4gIGNvbnN0IGFNYXliZVN0cmluZyA9IE1heWJlLm9mKCdIZWxsbywgdGhlcmUhJyk7XG5cbiAgLy8gTWF5YmU8bnVtYmVyPlxuICBjb25zdCByZXN1bHRpbmdMZW5ndGggPSBNYXliZS5hbmRUaGVuKHRvTWF5YmVMZW5ndGgsIGFNYXliZVN0cmluZyk7XG4gIGNvbnNvbGUubG9nKE1heWJlLnRvU3RyaW5nKHJlc3VsdGluZ0xlbmd0aCkpOyAvLyAxM1xuICBgYGBcblxuICBOb3RlIHRoYXQgdGhlIHJlc3VsdCBpcyBub3QgYChKdXN0KDEzKSlgLCBidXQgYDEzYCFcblxuICBAdHlwZXBhcmFtIFQgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIFQgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlIGluIHRoZSByZXN1bHRpbmcgYE1heWJlYC5cbiAgQHBhcmFtIHRoZW5GbiBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdG8gdGhlIHdyYXBwZWQgYFRgIGlmIGBtYXliZWAgaXMgYEp1c3RgLlxuICBAcGFyYW0gbWF5YmUgIFRoZSBgTWF5YmVgIHRvIGV2YWx1YXRlIGFuZCBwb3NzaWJseSBhcHBseSBhIGZ1bmN0aW9uIHRvIHRoZVxuICAgICAgICAgICAgICAgIGNvbnRlbnRzIG9mLlxuICBAcmV0dXJucyAgICAgIFRoZSByZXN1bHQgb2YgdGhlIGB0aGVuRm5gIChhIG5ldyBgTWF5YmVgKSBpZiBgbWF5YmVgIGlzIGFcbiAgICAgICAgICAgICAgICBgSnVzdGAsIG90aGVyd2lzZSBgTm90aGluZ2AgaWYgYG1heWJlYCBpcyBhIGBOb3RoaW5nYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFuZFRoZW48VCwgVT4odGhlbkZuOiAodDogVCkgPT4gTWF5YmU8VT4sIG1heWJlOiBNYXliZTxUPik6IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFuZFRoZW48VCwgVT4odGhlbkZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBhbmRUaGVuPFQsIFU+KFxuICB0aGVuRm46ICh0OiBUKSA9PiBNYXliZTxVPixcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogTWF5YmU8VT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VT4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gdGhlbkZuKG0udmFsdWUpIDogbm90aGluZzxVPigpKTtcbiAgcmV0dXJuIG1heWJlICE9PSB1bmRlZmluZWQgPyBvcChtYXliZSkgOiBvcDtcbn1cblxuLyoqIEFsaWFzIGZvciBbYGFuZFRoZW5gXSgjYW5kdGhlbikuICovXG5leHBvcnQgY29uc3QgY2hhaW4gPSBhbmRUaGVuO1xuXG4vKiogQWxpYXMgZm9yIFtgYW5kVGhlbmBdKCNhbmR0aGVuKS4gKi9cbmV4cG9ydCBjb25zdCBmbGF0TWFwID0gYW5kVGhlbjtcblxuLyoqXG4gIFByb3ZpZGUgYSBmYWxsYmFjayBmb3IgYSBnaXZlbiBgTWF5YmVgLiBCZWhhdmVzIGxpa2UgYSBsb2dpY2FsIGBvcmA6IGlmIHRoZVxuICBgbWF5YmVgIHZhbHVlIGlzIGEgYEp1c3RgLCByZXR1cm5zIHRoYXQgYG1heWJlYDsgb3RoZXJ3aXNlLCByZXR1cm5zIHRoZVxuICBgZGVmYXVsdE1heWJlYCB2YWx1ZS5cblxuICBUaGlzIGlzIHVzZWZ1bCB3aGVuIHlvdSB3YW50IHRvIG1ha2Ugc3VyZSB0aGF0IHNvbWV0aGluZyB3aGljaCB0YWtlcyBhXG4gIGBNYXliZWAgYWx3YXlzIGVuZHMgdXAgZ2V0dGluZyBhIGBKdXN0YCB2YXJpYW50LCBieSBzdXBwbHlpbmcgYSBkZWZhdWx0IHZhbHVlXG4gIGZvciB0aGUgY2FzZSB0aGF0IHlvdSBjdXJyZW50bHkgaGF2ZSBhIG5vdGhpbmcuXG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtdXRpbHMvbWF5YmUnO1xuXG4gIGNvbnN0IGp1c3RBID0gTWF5YmUuanVzdChcImFcIik7XG4gIGNvbnN0IGp1c3RCID0gTWF5YmUuanVzdChcImJcIik7XG4gIGNvbnN0IGFOb3RoaW5nOiBNYXliZTxzdHJpbmc+ID0gbm90aGluZygpO1xuXG4gIGNvbnNvbGUubG9nKE1heWJlLm9yKGp1c3RCLCBqdXN0QSkudG9TdHJpbmcoKSk7ICAvLyBKdXN0KEEpXG4gIGNvbnNvbGUubG9nKE1heWJlLm9yKGFOb3RoaW5nLCBqdXN0QSkudG9TdHJpbmcoKSk7ICAvLyBKdXN0KEEpXG4gIGNvbnNvbGUubG9nKE1heWJlLm9yKGp1c3RCLCBhTm90aGluZykudG9TdHJpbmcoKSk7ICAvLyBKdXN0KEIpXG4gIGNvbnNvbGUubG9nKE1heWJlLm9yKGFOb3RoaW5nLCBhTm90aGluZykudG9TdHJpbmcoKSk7ICAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICAgICAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBkZWZhdWx0TWF5YmUgVGhlIGBNYXliZWAgdG8gdXNlIGlmIGBtYXliZWAgaXMgYSBgTm90aGluZ2AuXG4gIEBwYXJhbSBtYXliZSAgICAgICAgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gZXZhbHVhdGUuXG4gIEByZXR1cm5zICAgICAgICAgICAgYG1heWJlYCBpZiBpdCBpcyBhIGBKdXN0YCwgb3RoZXJ3aXNlIGBkZWZhdWx0TWF5YmVgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gb3I8VD4oZGVmYXVsdE1heWJlOiBNYXliZTxUPiwgbWF5YmU6IE1heWJlPFQ+KTogTWF5YmU8VD47XG5leHBvcnQgZnVuY3Rpb24gb3I8VD4oZGVmYXVsdE1heWJlOiBNYXliZTxUPik6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFQ+O1xuZXhwb3J0IGZ1bmN0aW9uIG9yPFQ+KFxuICBkZWZhdWx0TWF5YmU6IE1heWJlPFQ+LFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBNYXliZTxUPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxUPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyBtIDogZGVmYXVsdE1heWJlKTtcbiAgcmV0dXJuIG1heWJlICE9PSB1bmRlZmluZWQgPyBvcChtYXliZSkgOiBvcDtcbn1cblxuLyoqXG4gIExpa2UgYG9yYCwgYnV0IHVzaW5nIGEgZnVuY3Rpb24gdG8gY29uc3RydWN0IHRoZSBhbHRlcm5hdGl2ZSBgTWF5YmVgLlxuXG4gIFNvbWV0aW1lcyB5b3UgbmVlZCB0byBwZXJmb3JtIGFuIG9wZXJhdGlvbiB1c2luZyBvdGhlciBkYXRhIGluIHRoZVxuICBlbnZpcm9ubWVudCB0byBjb25zdHJ1Y3QgdGhlIGZhbGxiYWNrIHZhbHVlLiBJbiB0aGVzZSBzaXR1YXRpb25zLCB5b3UgY2FuXG4gIHBhc3MgYSBmdW5jdGlvbiAod2hpY2ggbWF5IGJlIGEgY2xvc3VyZSkgYXMgdGhlIGBlbHNlRm5gIHRvIGdlbmVyYXRlIHRoZVxuICBmYWxsYmFjayBgTWF5YmU8VD5gLlxuXG4gIFVzZWZ1bCBmb3IgdHJhbnNmb3JtaW5nIGVtcHR5IHNjZW5hcmlvcyBiYXNlZCBvbiB2YWx1ZXMgaW4gY29udGV4dC5cblxuICBAdHlwZXBhcmFtIFQgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAcGFyYW0gZWxzZUZuIFRoZSBmdW5jdGlvbiB0byBhcHBseSBpZiBgbWF5YmVgIGlzIGBOb3RoaW5nYFxuICBAcGFyYW0gbWF5YmUgIFRoZSBgbWF5YmVgIHRvIHVzZSBpZiBpdCBpcyBgSnVzdGAuXG4gIEByZXR1cm5zICAgICAgVGhlIGBtYXliZWAgaWYgaXQgaXMgYEp1c3RgLCBvciB0aGUgYE1heWJlYCByZXR1cm5lZCBieVxuICAgICAgICAgICAgICAgIGBlbHNlRm5gIGlmIHRoZSBgbWF5YmVgIGlzIGBOb3RoaW5nYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG9yRWxzZTxUPihlbHNlRm46ICgpID0+IE1heWJlPFQ+LCBtYXliZTogTWF5YmU8VD4pOiBNYXliZTxUPjtcbmV4cG9ydCBmdW5jdGlvbiBvckVsc2U8VD4oZWxzZUZuOiAoKSA9PiBNYXliZTxUPik6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFQ+O1xuZXhwb3J0IGZ1bmN0aW9uIG9yRWxzZTxUPihcbiAgZWxzZUZuOiAoKSA9PiBNYXliZTxUPixcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogTWF5YmU8VD4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VD4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gbSA6IGVsc2VGbigpKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgbWF5YmUpO1xufVxuXG4vKipcbiAgR2V0IHRoZSB2YWx1ZSBvdXQgb2YgdGhlIGBNYXliZWAuXG5cbiAgUmV0dXJucyB0aGUgY29udGVudCBvZiBhIGBKdXN0YCwgYnV0ICoqdGhyb3dzIGlmIHRoZSBgTWF5YmVgIGlzIGBOb3RoaW5nYCoqLlxuICBQcmVmZXIgdG8gdXNlIFtgdW53cmFwT3JgXSgjdW53cmFwb3IpIG9yIFtgdW53cmFwT3JFbHNlYF0oI3Vud3JhcG9yZWxzZSkuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAcGFyYW0gbWF5YmUgVGhlIHZhbHVlIHRvIHVud3JhcFxuICBAcmV0dXJucyAgICAgVGhlIHVud3JhcHBlZCB2YWx1ZSBpZiB0aGUgYE1heWJlYCBpbnN0YW5jZSBpcyBgSnVzdGAuXG4gIEB0aHJvd3MgICAgICBJZiB0aGUgYG1heWJlYCBpcyBgTm90aGluZ2AuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiB1bnNhZmVseVVud3JhcDxUPihtYXliZTogTWF5YmU8VD4pOiBUIHtcbiAgcmV0dXJuIG1heWJlLnVuc2FmZWx5VW53cmFwKCk7XG59XG5cbi8qKiBBbGlhcyBmb3IgW2B1bnNhZmVseVVud3JhcGBdKCN1bnNhZmVseXVud3JhcCkgKi9cbmV4cG9ydCBjb25zdCB1bnNhZmVseUdldCA9IHVuc2FmZWx5VW53cmFwO1xuXG4vKiogQWxpYXMgZm9yIFtgdW5zYWZlbHlVbndyYXBgXSgjdW5zYWZlbHl1bndyYXApICovXG5leHBvcnQgY29uc3QgdW5zYWZlR2V0ID0gdW5zYWZlbHlVbndyYXA7XG5cbi8qKlxuICBTYWZlbHkgZ2V0IHRoZSB2YWx1ZSBvdXQgb2YgYSBgTWF5YmVgLlxuXG4gIFJldHVybnMgdGhlIGNvbnRlbnQgb2YgYSBgSnVzdGAgb3IgYGRlZmF1bHRWYWx1ZWAgaWYgYE5vdGhpbmdgLiBUaGlzIGlzIHRoZVxuICByZWNvbW1lbmRlZCB3YXkgdG8gZ2V0IGEgdmFsdWUgb3V0IG9mIGEgYE1heWJlYCBtb3N0IG9mIHRoZSB0aW1lLlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGNvbnN0IG5vdEFTdHJpbmcgPSBNYXliZS5ub3RoaW5nPHN0cmluZz4oKTtcbiAgY29uc3QgaXNBU3RyaW5nID0gTWF5YmUuanVzdCgnbG9vayBtYSEgc29tZSBjaGFyYWN0ZXJzIScpO1xuXG4gIGNvbnNvbGUubG9nKE1heWJlLnVud3JhcE9yKCc8ZW1wdHk+Jywgbm90QVN0cmluZykpOyAgLy8gXCI8ZW1wdHk+XCJcbiAgY29uc29sZS5sb2coTWF5YmUudW53cmFwT3IoJzxlbXB0eT4nLCBpc0FTdHJpbmcpKTsgIC8vIFwibG9vayBtYSEgc29tZSBjaGFyYWN0ZXJzIVwiXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICAgICAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBkZWZhdWx0VmFsdWUgVGhlIHZhbHVlIHRvIHJldHVybiBpZiBgbWF5YmVgIGlzIGEgYE5vdGhpbmdgLlxuICBAcGFyYW0gbWF5YmUgICAgICAgIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIHVud3JhcCBpZiBpdCBpcyBhIGBKdXN0YC5cbiAgQHJldHVybnMgICAgICAgICAgICBUaGUgY29udGVudCBvZiBgbWF5YmVgIGlmIGl0IGlzIGEgYEp1c3RgLCBvdGhlcndpc2VcbiAgICAgICAgICAgICAgICAgICAgICBgZGVmYXVsdFZhbHVlYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yPFQ+KGRlZmF1bHRWYWx1ZTogVCwgbWF5YmU6IE1heWJlPFQ+KTogVDtcbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPcjxUPihkZWZhdWx0VmFsdWU6IFQpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBUO1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yPFQ+KGRlZmF1bHRWYWx1ZTogVCwgbWF5YmU/OiBNYXliZTxUPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyBtLnZhbHVlIDogZGVmYXVsdFZhbHVlKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgbWF5YmUpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgdW53cmFwT3JgXSgjdW53cmFwb3IpICovXG5leHBvcnQgY29uc3QgZ2V0T3IgPSB1bndyYXBPcjtcblxuLyoqXG4gIFNhZmVseSBnZXQgdGhlIHZhbHVlIG91dCBvZiBhIFtgTWF5YmVgXSgjbWF5YmUpIGJ5IHJldHVybmluZyB0aGUgd3JhcHBlZFxuICB2YWx1ZSBpZiBpdCBpcyBgSnVzdGAsIG9yIGJ5IGFwcGx5aW5nIGBvckVsc2VGbmAgaWYgaXQgaXMgYE5vdGhpbmdgLlxuXG4gIFRoaXMgaXMgdXNlZnVsIHdoZW4geW91IG5lZWQgdG8gKmdlbmVyYXRlKiBhIHZhbHVlIChlLmcuIGJ5IHVzaW5nIGN1cnJlbnRcbiAgdmFsdWVzIGluIHRoZSBlbnZpcm9ubWVudCDigJMgd2hldGhlciBwcmVsb2FkZWQgb3IgYnkgbG9jYWwgY2xvc3VyZSkgaW5zdGVhZCBvZlxuICBoYXZpbmcgYSBzaW5nbGUgZGVmYXVsdCB2YWx1ZSBhdmFpbGFibGUgKGFzIGluIFtgdW53cmFwT3JgXSgjdW53cmFwb3IpKS5cblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICAvLyBZb3UgY2FuIGltYWdpbmUgdGhhdCBzb21lT3RoZXJWYWx1ZSBtaWdodCBiZSBkeW5hbWljLlxuICBjb25zdCBzb21lT3RoZXJWYWx1ZSA9IDk5O1xuICBjb25zdCBoYW5kbGVOb3RoaW5nID0gKCkgPT4gc29tZU90aGVyVmFsdWU7XG5cbiAgY29uc3QgYUp1c3QgPSBNYXliZS5qdXN0KDQyKTtcbiAgY29uc29sZS5sb2coTWF5YmUudW53cmFwT3JFbHNlKGhhbmRsZU5vdGhpbmcsIGFKdXN0KSk7ICAvLyA0MlxuXG4gIGNvbnN0IGFOb3RoaW5nID0gbm90aGluZzxudW1iZXI+KCk7XG4gIGNvbnNvbGUubG9nKE1heWJlLnVud3JhcE9yRWxzZShoYW5kbGVOb3RoaW5nLCBhTm90aGluZykpOyAvLyA5OVxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgIFRoZSB3cmFwcGVkIHZhbHVlLlxuICBAcGFyYW0gb3JFbHNlRm4gQSBmdW5jdGlvbiB1c2VkIHRvIGdlbmVyYXRlIGEgdmFsaWQgdmFsdWUgaWYgYG1heWJlYCBpcyBhXG4gICAgICAgICAgICAgICAgICBgTm90aGluZ2AuXG4gIEBwYXJhbSBtYXliZSAgICBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byB1bndyYXAgaWYgaXQgaXMgYSBgSnVzdGBcbiAgQHJldHVybnMgICAgICAgIEVpdGhlciB0aGUgY29udGVudCBvZiBgbWF5YmVgIG9yIHRoZSB2YWx1ZSByZXR1cm5lZCBmcm9tXG4gICAgICAgICAgICAgICAgICBgb3JFbHNlRm5gLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3JFbHNlPFQ+KG9yRWxzZUZuOiAoKSA9PiBULCBtYXliZTogTWF5YmU8VD4pOiBUO1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yRWxzZTxUPihvckVsc2VGbjogKCkgPT4gVCk6IChtYXliZTogTWF5YmU8VD4pID0+IFQ7XG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3JFbHNlPFQ+KG9yRWxzZUZuOiAoKSA9PiBULCBtYXliZT86IE1heWJlPFQ+KTogVCB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBUKSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAobS5pc0p1c3QoKSA/IG0udmFsdWUgOiBvckVsc2VGbigpKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgbWF5YmUpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgdW53cmFwT3JFbHNlYF0oI3Vud3JhcG9yZWxzZSkgKi9cbmV4cG9ydCBjb25zdCBnZXRPckVsc2UgPSB1bndyYXBPckVsc2U7XG5cbi8qKlxuICBUcmFuc2Zvcm0gdGhlIFtgTWF5YmVgXSgjbWF5YmUpIGludG8gYVxuICBbYFJlc3VsdGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNyZXN1bHQpLCB1c2luZyB0aGUgd3JhcHBlZCB2YWx1ZSBhcyB0aGVcbiAgYE9rYCB2YWx1ZSBpZiBgSnVzdGA7IG90aGVyd2lzZSB1c2luZyB0aGUgc3VwcGxpZWQgYGVycm9yYCB2YWx1ZSBmb3IgYEVycmAuXG5cbiAgQHR5cGVwYXJhbSBUICBUaGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHR5cGVwYXJhbSBFICBUaGUgZXJyb3IgdHlwZSB0byBpbiB0aGUgYFJlc3VsdGAuXG4gIEBwYXJhbSBlcnJvciBUaGUgZXJyb3IgdmFsdWUgdG8gdXNlIGlmIHRoZSBgTWF5YmVgIGlzIGBOb3RoaW5nYC5cbiAgQHBhcmFtIG1heWJlIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIGNvbnZlcnQuXG4gIEByZXR1cm5zICAgICBBIGBSZXN1bHRgIGNvbnRhaW5pbmcgdGhlIHZhbHVlIHdyYXBwZWQgaW4gYG1heWJlYCBpbiBhbiBgT2tgLFxuICAgICAgICAgICAgICAgb3IgYGVycm9yYCBpbiBhbiBgRXJyYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHRvT2tPckVycjxULCBFPihlcnJvcjogRSwgbWF5YmU6IE1heWJlPFQ+KTogUmVzdWx0PFQsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIHRvT2tPckVycjxULCBFPihlcnJvcjogRSk6IChtYXliZTogTWF5YmU8VD4pID0+IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0b09rT3JFcnI8VCwgRT4oXG4gIGVycm9yOiBFLFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBSZXN1bHQ8VCwgRT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gUmVzdWx0PFQsIEU+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAobS5pc0p1c3QoKSA/IG9rPFQsIEU+KG0udmFsdWUpIDogZXJyPFQsIEU+KGVycm9yKSk7XG4gIHJldHVybiBtYXliZSAhPT0gdW5kZWZpbmVkID8gb3AobWF5YmUpIDogb3A7XG59XG5cbi8qKlxuICBUcmFuc2Zvcm0gdGhlIFtgTWF5YmVgXSgjbWF5YmUpIGludG8gYVxuICBbYFJlc3VsdGBdKC4uL21vZHVsZXMvX3Jlc3VsdF8uaHRtbCNyZXN1bHQpLCB1c2luZyB0aGUgd3JhcHBlZCB2YWx1ZSBhcyB0aGVcbiAgYE9rYCB2YWx1ZSBpZiBgSnVzdGA7IG90aGVyd2lzZSB1c2luZyBgZWxzZUZuYCB0byBnZW5lcmF0ZSBgRXJyYC5cblxuICBAdHlwZXBhcmFtIFQgIFRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIEUgIFRoZSBlcnJvciB0eXBlIHRvIGluIHRoZSBgUmVzdWx0YC5cbiAgQHBhcmFtIGVsc2VGbiBUaGUgZnVuY3Rpb24gd2hpY2ggZ2VuZXJhdGVzIGFuIGVycm9yIG9mIHR5cGUgYEVgLlxuICBAcGFyYW0gbWF5YmUgIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIGNvbnZlcnQuXG4gIEByZXR1cm5zICAgICBBIGBSZXN1bHRgIGNvbnRhaW5pbmcgdGhlIHZhbHVlIHdyYXBwZWQgaW4gYG1heWJlYCBpbiBhbiBgT2tgLFxuICAgICAgICAgICAgICAgb3IgdGhlIHZhbHVlIGdlbmVyYXRlZCBieSBgZWxzZUZuYCBpbiBhbiBgRXJyYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHRvT2tPckVsc2VFcnI8VCwgRT4oZWxzZUZuOiAoKSA9PiBFLCBtYXliZTogTWF5YmU8VD4pOiBSZXN1bHQ8VCwgRT47XG5leHBvcnQgZnVuY3Rpb24gdG9Pa09yRWxzZUVycjxULCBFPihlbHNlRm46ICgpID0+IEUpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBSZXN1bHQ8VCwgRT47XG5leHBvcnQgZnVuY3Rpb24gdG9Pa09yRWxzZUVycjxULCBFPihcbiAgZWxzZUZuOiAoKSA9PiBFLFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBSZXN1bHQ8VCwgRT4gfCAoKG1heWJlOiBNYXliZTxUPikgPT4gUmVzdWx0PFQsIEU+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAobS5pc0p1c3QoKSA/IG9rPFQsIEU+KG0udmFsdWUpIDogZXJyPFQsIEU+KGVsc2VGbigpKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIG1heWJlKTtcbn1cblxuLyoqXG4gIENvbnN0cnVjdCBhIGBNYXliZTxUPmAgZnJvbSBhIGBSZXN1bHQ8VCwgRT5gLlxuXG4gIElmIHRoZSBgUmVzdWx0YCBpcyBhbiBgT2tgLCB3cmFwIGl0cyB2YWx1ZSBpbiBgSnVzdGAuIElmIHRoZSBgUmVzdWx0YCBpcyBhblxuICBgRXJyYCwgdGhyb3cgYXdheSB0aGUgd3JhcHBlZCBgRWAgYW5kIHRyYW5zZm9ybSB0byBhIGBOb3RoaW5nYC5cblxuICBAdHlwZXBhcmFtIFQgIFRoZSB0eXBlIG9mIHRoZSB2YWx1ZSB3cmFwcGVkIGluIGEgYFJlc3VsdC5Pa2AgYW5kIGluIHRoZSBgSnVzdGBcbiAgICAgICAgICAgICAgICBvZiB0aGUgcmVzdWx0aW5nIGBNYXliZWAuXG4gIEB0eXBlcGFyYW0gRSAgVGhlIHR5cGUgb2YgdGhlIHZhbHVlIHdyYXBwZWQgaW4gYSBgUmVzdWx0LkVycmA7IHRocm93biBhd2F5IGluXG4gICAgICAgICAgICAgICAgdGhlIHJlc3VsdGluZyBgTWF5YmVgLlxuICBAcGFyYW0gcmVzdWx0IFRoZSBgUmVzdWx0YCB0byBjb25zdHJ1Y3QgYSBgTWF5YmVgIGZyb20uXG4gIEByZXR1cm5zICAgICAgYEp1c3RgIGlmIGByZXN1bHRgIHdhcyBgT2tgIG9yIGBOb3RoaW5nYCBpZiBpdCB3YXMgYEVycmAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBmcm9tUmVzdWx0PFQ+KHJlc3VsdDogUmVzdWx0PFQsIGFueT4pOiBNYXliZTxUPiB7XG4gIHJldHVybiByZXN1bHQuaXNPaygpID8ganVzdChyZXN1bHQudmFsdWUpIDogbm90aGluZzxUPigpO1xufVxuXG4vKipcbiAgQ3JlYXRlIGEgYFN0cmluZ2AgcmVwcmVzZW50YXRpb24gb2YgYSBgTWF5YmVgIGluc3RhbmNlLlxuXG4gIEEgYEp1c3RgIGluc3RhbmNlIHdpbGwgYmUgcHJpbnRlZCBhcyBgSnVzdCg8cmVwcmVzZW50YXRpb24gb2YgdGhlIHZhbHVlPilgLFxuICB3aGVyZSB0aGUgcmVwcmVzZW50YXRpb24gb2YgdGhlIHZhbHVlIGlzIHNpbXBseSB0aGUgdmFsdWUncyBvd24gYHRvU3RyaW5nYFxuICByZXByZXNlbnRhdGlvbi4gRm9yIGV4YW1wbGU6XG5cbiAgfCBjYWxsICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB8IG91dHB1dCAgICAgICAgICAgICAgICAgIHxcbiAgfC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS18LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLXxcbiAgfCBgdG9TdHJpbmcoTWF5YmUub2YoNDIpKWAgICAgICAgICAgICAgICB8IGBKdXN0KDQyKWAgICAgICAgICAgICAgIHxcbiAgfCBgdG9TdHJpbmcoTWF5YmUub2YoWzEsIDIsIDNdKSlgICAgICAgICB8IGBKdXN0KDEsMiwzKWAgICAgICAgICAgIHxcbiAgfCBgdG9TdHJpbmcoTWF5YmUub2YoeyBhbjogJ29iamVjdCcgfSkpYCB8IGBKdXN0KFtvYmplY3QgT2JqZWN0XSlgIHxcbiAgfCBgdG9TdHJpbmcoTWF5YmUubm90aGluZygpKWAgICAgICAgICAgICB8IGBOb3RoaW5nYCAgICAgICAgICAgICAgIHxcblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWU7IGl0cyBvd24gYC50b1N0cmluZ2Agd2lsbCBiZSB1c2VkXG4gICAgICAgICAgICAgICB0byBwcmludCB0aGUgaW50ZXJpb3IgY29udGVudHMgb2YgdGhlIGBKdXN0YCB2YXJpYW50LlxuICBAcGFyYW0gbWF5YmUgVGhlIHZhbHVlIHRvIGNvbnZlcnQgdG8gYSBzdHJpbmcuXG4gIEByZXR1cm5zICAgICBUaGUgc3RyaW5nIHJlcHJlc2VudGF0aW9uIG9mIHRoZSBgTWF5YmVgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdG9TdHJpbmc8VD4obWF5YmU6IE1heWJlPFQ+KTogc3RyaW5nIHtcbiAgY29uc3QgYm9keSA9IG1heWJlLmlzSnVzdCgpID8gYCgke21heWJlLnZhbHVlLnRvU3RyaW5nKCl9KWAgOiAnJztcbiAgcmV0dXJuIGAke21heWJlLnZhcmlhbnR9JHtib2R5fWA7XG59XG5cbi8qKiBBIGxpZ2h0d2VpZ2h0IG9iamVjdCBkZWZpbmluZyBob3cgdG8gaGFuZGxlIGVhY2ggdmFyaWFudCBvZiBhIE1heWJlLiAqL1xuZXhwb3J0IHR5cGUgTWF0Y2hlcjxULCBBPiA9IHtcbiAgSnVzdDogKHZhbHVlOiBUKSA9PiBBO1xuICBOb3RoaW5nOiAoKSA9PiBBO1xufTtcblxuLyoqXG4gIFBlcmZvcm1zIHRoZSBzYW1lIGJhc2ljIGZ1bmN0aW9uYWxpdHkgYXMgYGdldE9yRWxzZWAsIGJ1dCBpbnN0ZWFkIG9mIHNpbXBseVxuICB1bndyYXBwaW5nIHRoZSB2YWx1ZSBpZiBpdCBpcyBgSnVzdGAgYW5kIGFwcGx5aW5nIGEgdmFsdWUgdG8gZ2VuZXJhdGUgdGhlIHNhbWVcbiAgZGVmYXVsdCB0eXBlIGlmIGl0IGlzIGBOb3RoaW5nYCwgbGV0cyB5b3Ugc3VwcGx5IGZ1bmN0aW9ucyB3aGljaCBtYXkgdHJhbnNmb3JtXG4gIHRoZSB3cmFwcGVkIHR5cGUgaWYgaXQgaXMgYEp1c3RgIG9yIGdldCBhIGRlZmF1bHQgdmFsdWUgZm9yIGBOb3RoaW5nYC5cblxuICBUaGlzIGlzIGtpbmQgb2YgbGlrZSBhIHBvb3IgbWFuJ3MgdmVyc2lvbiBvZiBwYXR0ZXJuIG1hdGNoaW5nLCB3aGljaFxuICBKYXZhU2NyaXB0IGN1cnJlbnRseSBsYWNrcy5cblxuICBJbnN0ZWFkIG9mIGNvZGUgbGlrZSB0aGlzOlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGNvbnN0IGxvZ1ZhbHVlID0gKG1pZ2h0QmVBTnVtYmVyOiBNYXliZTxudW1iZXI+KSA9PiB7XG4gICAgY29uc3QgdmFsdWVUb0xvZyA9IE1heWJlLm1pZ2h0QmVBTnVtYmVyLmlzSnVzdCgpXG4gICAgICA/IE1heWJlLnVuc2FmZWx5VW53cmFwKG1pZ2h0QmVBTnVtYmVyKS50b1N0cmluZygpXG4gICAgICA6ICdOb3RoaW5nIHRvIGxvZy4nO1xuXG4gICAgY29uc29sZS5sb2codmFsdWVUb0xvZyk7XG4gIH07XG4gIGBgYFxuXG4gIC4uLndlIGNhbiB3cml0ZSBjb2RlIGxpa2UgdGhpczpcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICBjb25zdCBsb2dWYWx1ZSA9IChtaWdodEJlQU51bWJlcjogTWF5YmU8bnVtYmVyPikgPT4ge1xuICAgIGNvbnN0IHZhbHVlID0gTWF5YmUubWF0Y2goXG4gICAgICB7XG4gICAgICAgIEp1c3Q6IG4gPT4gbi50b1N0cmluZygpLFxuICAgICAgICBOb3RoaW5nOiAoKSA9PiAnTm90aGluZyB0byBsb2cuJyxcbiAgICAgIH0sXG4gICAgICBtaWdodEJlQU51bWJlclxuICAgICk7XG5cbiAgICBjb25zb2xlLmxvZyh2YWx1ZSk7XG4gIH07XG4gIGBgYFxuXG4gIFRoaXMgaXMgc2xpZ2h0bHkgbG9uZ2VyIHRvIHdyaXRlLCBidXQgY2xlYXJlcjogdGhlIG1vcmUgY29tcGxleCB0aGUgcmVzdWx0aW5nXG4gIGV4cHJlc3Npb24sIHRoZSBoYWlyZXIgaXQgaXMgdG8gdW5kZXJzdGFuZCB0aGUgdGVybmFyeS4gVGh1cywgdGhpcyBpc1xuICBlc3BlY2lhbGx5IGNvbnZlbmllbnQgZm9yIHRpbWVzIHdoZW4gdGhlcmUgaXMgYSBjb21wbGV4IHJlc3VsdCwgZS5nLiB3aGVuXG4gIHJlbmRlcmluZyBwYXJ0IG9mIGEgUmVhY3QgY29tcG9uZW50IGlubGluZSBpbiBKU1gvVFNYLlxuXG4gIEBwYXJhbSBtYXRjaGVyIEEgbGlnaHR3ZWlnaHQgb2JqZWN0IGRlZmluaW5nIHdoYXQgdG8gZG8gaW4gdGhlIGNhc2Ugb2YgZWFjaFxuICAgICAgICAgICAgICAgICB2YXJpYW50LlxuICBAcGFyYW0gbWF5YmUgICBUaGUgYG1heWJlYCBpbnN0YW5jZSB0byBjaGVjay5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIG1hdGNoPFQsIEE+KG1hdGNoZXI6IE1hdGNoZXI8VCwgQT4sIG1heWJlOiBNYXliZTxUPik6IEE7XG5leHBvcnQgZnVuY3Rpb24gbWF0Y2g8VCwgQT4obWF0Y2hlcjogTWF0Y2hlcjxULCBBPik6IChtOiBNYXliZTxUPikgPT4gQTtcbmV4cG9ydCBmdW5jdGlvbiBtYXRjaDxULCBBPihtYXRjaGVyOiBNYXRjaGVyPFQsIEE+LCBtYXliZT86IE1heWJlPFQ+KTogQSB8ICgobTogTWF5YmU8VD4pID0+IEEpIHtcbiAgcmV0dXJuIG1heWJlICE9PSB1bmRlZmluZWRcbiAgICA/IG1hcE9yRWxzZShtYXRjaGVyLk5vdGhpbmcsIG1hdGNoZXIuSnVzdCwgbWF5YmUpXG4gICAgOiAoY3VycmllZE1heWJlOiBNYXliZTxUPikgPT4gbWFwT3JFbHNlKG1hdGNoZXIuTm90aGluZywgbWF0Y2hlci5KdXN0LCBjdXJyaWVkTWF5YmUpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgbWF0Y2hgXSgjbWF0Y2gpICovXG5leHBvcnQgY29uc3QgY2F0YSA9IG1hdGNoO1xuXG4vKipcbiAgQWxsb3dzIHF1aWNrIHRyaXBsZS1lcXVhbCBlcXVhbGl0eSBjaGVjayBiZXR3ZWVuIHRoZSB2YWx1ZXMgaW5zaWRlIHR3byBgbWF5YmVgc1xuICB3aXRob3V0IGhhdmluZyB0byB1bndyYXAgdGhlbSBmaXJzdC5cblxuICBgYGB0c1xuICBjb25zdCBhID0gTWF5YmUub2YoMyk7XG4gIGNvbnN0IGIgPSBNYXliZS5vZigzKTtcbiAgY29uc3QgYyA9IE1heWJlLm9mKG51bGwpO1xuICBjb25zdCBkID0gTWF5YmUubm90aGluZygpO1xuXG4gIE1heWJlLmVxdWFscyhhLCBiKTsgLy8gdHJ1ZVxuICBNYXliZS5lcXVhbHMoYSwgYyk7IC8vIGZhbHNlXG4gIE1heWJlLmVxdWFscyhjLCBkKTsgLy8gdHJ1ZVxuICBgYGBcblxuICBAcGFyYW0gbWIgQSBgbWF5YmVgIHRvIGNvbXBhcmUgdG8uXG4gIEBwYXJhbSBtYSBBIGBtYXliZWAgaW5zdGFuY2UgdG8gY2hlY2suXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBlcXVhbHM8VD4obWI6IE1heWJlPFQ+LCBtYTogTWF5YmU8VD4pOiBib29sZWFuO1xuZXhwb3J0IGZ1bmN0aW9uIGVxdWFsczxUPihtYjogTWF5YmU8VD4pOiAobWE6IE1heWJlPFQ+KSA9PiBib29sZWFuO1xuZXhwb3J0IGZ1bmN0aW9uIGVxdWFsczxUPihtYjogTWF5YmU8VD4sIG1hPzogTWF5YmU8VD4pOiBib29sZWFuIHwgKChhOiBNYXliZTxUPikgPT4gYm9vbGVhbikge1xuICByZXR1cm4gbWEgIT09IHVuZGVmaW5lZFxuICAgID8gbWEubWF0Y2goe1xuICAgICAgICBKdXN0OiBhVmFsID0+IG1iLmlzSnVzdCgpICYmIG1iLnVuc2FmZWx5VW53cmFwKCkgPT09IGFWYWwsXG4gICAgICAgIE5vdGhpbmc6ICgpID0+IGlzTm90aGluZyhtYiksXG4gICAgICB9KVxuICAgIDogKG1heWJlQTogTWF5YmU8VD4pID0+XG4gICAgICAgIG1heWJlQS5tYXRjaCh7XG4gICAgICAgICAgTm90aGluZzogKCkgPT4gaXNOb3RoaW5nKG1iKSxcbiAgICAgICAgICBKdXN0OiBhVmFsID0+IG1iLmlzSnVzdCgpICYmIG1iLnVuc2FmZWx5VW53cmFwKCkgPT09IGFWYWwsXG4gICAgICAgIH0pO1xufVxuXG4vKipcbiAgQWxsb3dzIHlvdSB0byAqYXBwbHkqICh0aHVzIGBhcGApIGEgdmFsdWUgdG8gYSBmdW5jdGlvbiB3aXRob3V0IGhhdmluZyB0b1xuICB0YWtlIGVpdGhlciBvdXQgb2YgdGhlIGNvbnRleHQgb2YgdGhlaXIgYE1heWJlYHMuIFRoaXMgZG9lcyBtZWFuIHRoYXQgdGhlXG4gIHRyYW5zZm9ybWluZyBmdW5jdGlvbiBpcyBpdHNlbGYgd2l0aGluIGEgYE1heWJlYCwgd2hpY2ggY2FuIGJlIGhhcmQgdG8gZ3Jva1xuICBhdCBmaXJzdCBidXQgbGV0cyB5b3UgZG8gc29tZSB2ZXJ5IGVsZWdhbnQgdGhpbmdzLiBGb3IgZXhhbXBsZSwgYGFwYCBhbGxvd3NcbiAgeW91IHRvIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsganVzdCwgbm90aGluZyB9IGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgY29uc3Qgb25lID0ganVzdCgxKTtcbiAgY29uc3QgZml2ZSA9IGp1c3QoNSk7XG4gIGNvbnN0IG5vbmUgPSBub3RoaW5nKCk7XG5cbiAgY29uc3QgYWRkID0gKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGI7XG4gIGNvbnN0IG1heWJlQWRkID0ganVzdChhZGQpO1xuXG4gIG1heWJlQWRkLmFwKG9uZSkuYXAoZml2ZSk7IC8vIEp1c3QoNilcbiAgbWF5YmVBZGQuYXAob25lKS5hcChub25lKTsgLy8gTm90aGluZ1xuICBtYXliZUFkZC5hcChub25lKS5hcChmaXZlKSAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIFdpdGhvdXQgYE1heWJlLmFwYCwgeW91J2QgbmVlZCB0byBkbyBzb21ldGhpbmcgbGlrZSBhIG5lc3RlZCBgTWF5YmUubWF0Y2hgOlxuXG4gIGBgYHRzXG4gIGltcG9ydCB7IGp1c3QsIG5vdGhpbmcgfSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGNvbnN0IG9uZSA9IGp1c3QoMSk7XG4gIGNvbnN0IGZpdmUgPSBqdXN0KDUpO1xuICBjb25zdCBub25lID0gbm90aGluZygpO1xuXG4gIG9uZS5tYXRjaCh7XG4gICAgSnVzdDogbiA9PiBmaXZlLm1hdGNoKHtcbiAgICAgIEp1c3Q6IG8gPT4ganVzdChuICsgbyksXG4gICAgICBOb3RoaW5nOiAoKSA9PiBub3RoaW5nKCksXG4gICAgfSksXG4gICAgTm90aGluZzogKCkgID0+IG5vdGhpbmcoKSxcbiAgfSk7IC8vIEp1c3QoNilcblxuICBvbmUubWF0Y2goe1xuICAgIEp1c3Q6IG4gPT4gbm9uZS5tYXRjaCh7XG4gICAgICBKdXN0OiBvID0+IGp1c3QobiArIG8pLFxuICAgICAgTm90aGluZzogKCkgPT4gbm90aGluZygpLFxuICAgIH0pLFxuICAgIE5vdGhpbmc6ICgpICA9PiBub3RoaW5nKCksXG4gIH0pOyAvLyBOb3RoaW5nXG5cbiAgbm9uZS5tYXRjaCh7XG4gICAgSnVzdDogbiA9PiBmaXZlLm1hdGNoKHtcbiAgICAgIEp1c3Q6IG8gPT4ganVzdChuICsgbyksXG4gICAgICBOb3RoaW5nOiAoKSA9PiBub3RoaW5nKCksXG4gICAgfSksXG4gICAgTm90aGluZzogKCkgID0+IG5vdGhpbmcoKSxcbiAgfSk7IC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgQW5kIHRoaXMga2luZCBvZiB0aGluZyBjb21lcyB1cCBxdWl0ZSBvZnRlbiBvbmNlIHlvdSdyZSB1c2luZyBgTWF5YmVgIHRvXG4gIGhhbmRsZSBvcHRpb25hbGl0eSB0aHJvdWdob3V0IHlvdXIgYXBwbGljYXRpb24uXG5cbiAgRm9yIGFub3RoZXIgZXhhbXBsZSwgaW1hZ2luZSB5b3UgbmVlZCB0byBjb21wYXJlIHRoZSBlcXVhbGl0eSBvZiB0d29cbiAgSW1tdXRhYmxlSlMgZGF0YSBzdHJ1Y3R1cmVzLCB3aGVyZSBhIGA9PT1gIGNvbXBhcmlzb24gd29uJ3Qgd29yay4gV2l0aCBgYXBgLFxuICB0aGF0J3MgYXMgc2ltcGxlIGFzIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG4gIGltcG9ydCBJbW11dGFibGUgZnJvbSAnaW1tdXRhYmxlJztcbiAgaW1wb3J0IHsgY3VycnkgfSBmcm9tICdsb2Rhc2gnXG5cbiAgY29uc3QgaXMgPSBjdXJyeShJbW11dGFibGUuaXMpO1xuXG4gIGNvbnN0IHggPSBNYXliZS5vZihJbW11dGFibGUuU2V0Lm9mKDEsIDIsIDMpKTtcbiAgY29uc3QgeSA9IE1heWJlLm9mKEltbXV0YWJsZS5TZXQub2YoMiwgMywgNCkpO1xuXG4gIE1heWJlLm9mKGlzKS5hcCh4KS5hcCh5KTsgLy8gSnVzdChmYWxzZSlcbiAgYGBgXG5cbiAgV2l0aG91dCBgYXBgLCB3ZSdyZSBiYWNrIHRvIHRoYXQgZ25hcmx5IG5lc3RlZCBgbWF0Y2hgOlxuXG4gIGBgYHRzXG4gICAqIGltcG9ydCBNYXliZSwgeyBqdXN0LCBub3RoaW5nIH0gZnJvbSAndHJ1ZS1teXRoL21heWJlJztcbiAgaW1wb3J0IEltbXV0YWJsZSBmcm9tICdpbW11dGFibGUnO1xuICBpbXBvcnQgeyBjdXJyeSB9IGZyb20gJ2xvZGFzaCdcblxuICBjb25zdCBpcyA9IGN1cnJ5KEltbXV0YWJsZS5pcyk7XG5cbiAgY29uc3QgeCA9IE1heWJlLm9mKEltbXV0YWJsZS5TZXQub2YoMSwgMiwgMykpO1xuICBjb25zdCB5ID0gTWF5YmUub2YoSW1tdXRhYmxlLlNldC5vZigyLCAzLCA0KSk7XG5cbiAgeC5tYXRjaCh7XG4gICAgSnVzdDogaVggPT4geS5tYXRjaCh7XG4gICAgICBKdXN0OiBpWSA9PiBNYXliZS5qdXN0KEltbXV0YWJsZS5pcyhpWCwgaVkpKSxcbiAgICAgIE5vdGhpbmc6ICgpID0+IE1heWJlLm5vdGhpbmcoKSxcbiAgICB9KVxuICAgIE5vdGhpbmc6ICgpID0+IE1heWJlLm5vdGhpbmcoKSxcbiAgfSk7IC8vIEp1c3QoZmFsc2UpXG4gIGBgYFxuXG4gIEluIHN1bW1hcnk6IGFueXdoZXJlIHlvdSBoYXZlIHR3byBgTWF5YmVgIGluc3RhbmNlcyBhbmQgbmVlZCB0byBwZXJmb3JtIGFuXG4gIG9wZXJhdGlvbiB0aGF0IHVzZXMgYm90aCBvZiB0aGVtLCBgYXBgIGlzIHlvdXIgZnJpZW5kLlxuXG4gIFR3byB0aGluZ3MgdG8gbm90ZSwgYm90aCByZWdhcmRpbmcgKmN1cnJ5aW5nKjpcblxuICAxLiAgQWxsIGZ1bmN0aW9ucyBwYXNzZWQgdG8gYGFwYCBtdXN0IGJlIGN1cnJpZWQuIFRoYXQgaXMsIHRoZXkgbXVzdCBiZSBvZiB0aGVcbiAgICAgIGZvcm0gKGZvciBhZGQpIGAoYTogbnVtYmVyKSA9PiAoYjogbnVtYmVyKSA9PiBhICsgYmAsICpub3QqIHRoZSBtb3JlIHVzdWFsXG4gICAgICBgKGE6IG51bWJlciwgYjogbnVtYmVyKSA9PiBhICsgYmAgeW91IHNlZSBpbiBKYXZhU2NyaXB0IG1vcmUgZ2VuZXJhbGx5LlxuXG4gICAgICBGb3IgY29udmVuaWVuY2UsIHlvdSBtYXkgd2FudCB0byBsb29rIGF0IExvZGFzaCdzIGBfLmN1cnJ5YCBvciBSYW1kYSdzXG4gICAgICBgUi5jdXJyeWAsIHdoaWNoIGFsbG93IHlvdSB0byBjcmVhdGUgY3VycmllZCB2ZXJzaW9ucyBvZiBmdW5jdGlvbnNcbiAgICAgIHdoZW5ldmVyIHlvdSB3YW50OlxuXG4gICAgICBgYGBcbiAgICAgIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuICAgICAgaW1wb3J0IHsgY3VycnkgfSBmcm9tICdsb2Rhc2gnO1xuXG4gICAgICBjb25zdCBub3JtYWxBZGQgPSAoYTogbnVtYmVyLCBiOiBudW1iZXIpID0+IGEgKyBiO1xuICAgICAgY29uc3QgY3VycmllZEFkZCA9IGN1cnJ5KG5vcm1hbEFkZCk7IC8vIChhOiBudW1iZXIpID0+IChiOiBudW1iZXIpID0+IGEgKyBiO1xuXG4gICAgICBNYXliZS5vZihjdXJyaWVkQWRkKS5hcChNYXliZS5vZigxKSkuYXAoTWF5YmUub2YoNSkpOyAvLyBKdXN0KDYpXG4gICAgICBgYGBcblxuICAyLiAgWW91IHdpbGwgbmVlZCB0byBjYWxsIGBhcGAgYXMgbWFueSB0aW1lcyBhcyB0aGVyZSBhcmUgYXJndW1lbnRzIHRvIHRoZVxuICAgICAgZnVuY3Rpb24geW91J3JlIGRlYWxpbmcgd2l0aC4gU28gaW4gdGhlIGNhc2Ugb2YgYGFkZGAsIHdoaWNoIGhhcyB0aGVcbiAgICAgIFwiYXJpdHlcIiAoZnVuY3Rpb24gYXJndW1lbnQgY291bnQpIG9mIDIgKGBhYCBhbmQgYGJgKSwgeW91J2xsIG5lZWQgdG8gY2FsbFxuICAgICAgYGFwYCB0d2ljZTogb25jZSBmb3IgYGFgLCBhbmQgb25jZSBmb3IgYGJgLiBUbyBzZWUgd2h5LCBsZXQncyBsb29rIGF0IHdoYXRcbiAgICAgIHRoZSByZXN1bHQgaW4gZWFjaCBwaGFzZSBpczpcblxuICAgICAgYGBgdHNcbiAgICAgIGNvbnN0IGFkZCA9IChhOiBudW1iZXIpID0+IChiOiBudW1iZXIpID0+IGEgKyBiO1xuXG4gICAgICBjb25zdCBtYXliZUFkZCA9IE1heWJlLm9mKGFkZCk7IC8vIEp1c3QoKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGIpXG4gICAgICBjb25zdCBtYXliZUFkZDEgPSBtYXliZUFkZC5hcChNYXliZS5vZigxKSk7IC8vIEp1c3QoKGI6IG51bWJlcikgPT4gMSArIGIpXG4gICAgICBjb25zdCBmaW5hbCA9IG1heWJlQWRkMS5hcChNYXliZS5vZigzKSk7IC8vIEp1c3QoNClcbiAgICAgIGBgYFxuXG4gICAgICBTbyBmb3IgYHRvU3RyaW5nYCwgd2hpY2gganVzdCB0YWtlcyBhIHNpbmdsZSBhcmd1bWVudCwgeW91IHdvdWxkIG9ubHkgbmVlZFxuICAgICAgdG8gY2FsbCBgYXBgIG9uY2UuXG5cbiAgICAgIGBgYHRzXG4gICAgICBjb25zdCB0b1N0ciA9ICh2OiB7IHRvU3RyaW5nKCk6IHN0cmluZyB9KSA9PiB2LnRvU3RyaW5nKCk7XG4gICAgICBNYXliZS5vZih0b1N0cikuYXAoMTIpOyAvLyBKdXN0KFwiMTJcIilcbiAgICAgIGBgYFxuXG4gIE9uZSBvdGhlciBzY2VuYXJpbyB3aGljaCBkb2Vzbid0IGNvbWUgdXAgKnF1aXRlKiBhcyBvZnRlbiBidXQgaXMgY29uY2VpdmFibGVcbiAgaXMgd2hlcmUgeW91IGhhdmUgc29tZXRoaW5nIHRoYXQgbWF5IG9yIG1heSBub3QgYWN0dWFsbHkgY29uc3RydWN0IGEgZnVuY3Rpb25cbiAgZm9yIGhhbmRsaW5nIGEgc3BlY2lmaWMgYE1heWJlYCBzY2VuYXJpby4gSW4gdGhhdCBjYXNlLCB5b3UgY2FuIHdyYXAgdGhlXG4gIHBvc3NpYmx5LXByZXNlbnQgaW4gYGFwYCBhbmQgdGhlbiB3cmFwIHRoZSB2YWx1ZXMgdG8gYXBwbHkgdG8gdGhlIGZ1bmN0aW9uIHRvXG4gIGluIGBNYXliZWAgdGhlbXNlbHZlcy5cblxuICAqKkFzaWRlOioqIGBhcGAgaXMgbm90IG5hbWVkIGBhcHBseWAgYmVjYXVzZSBvZiB0aGUgb3ZlcmxhcCB3aXRoIEphdmFTY3JpcHQnc1xuICBleGlzdGluZyBbYGFwcGx5YF0gZnVuY3Rpb24g4oCTIGFuZCBhbHRob3VnaCBzdHJpY3RseSBzcGVha2luZywgdGhlcmUgaXNuJ3QgYW55XG4gIGRpcmVjdCBvdmVybGFwIChgTWF5YmUuYXBwbHlgIGFuZCBgRnVuY3Rpb24ucHJvdG90eXBlLmFwcGx5YCBkb24ndCBpbnRlcnNlY3RcbiAgYXQgYWxsKSBpdCdzIHVzZWZ1bCB0byBoYXZlIGEgZGlmZmVyZW50IG5hbWUgdG8gYXZvaWQgaW1wbHlpbmcgdGhhdCB0aGV5J3JlXG4gIHRoZSBzYW1lLlxuXG4gIFtgYXBwbHlgXTogaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvSmF2YVNjcmlwdC9SZWZlcmVuY2UvR2xvYmFsX09iamVjdHMvRnVuY3Rpb24vYXBwbHlcblxuICBAcGFyYW0gbWF5YmVGbiBtYXliZSBhIGZ1bmN0aW9uIGZyb20gVCB0byBVXG4gIEBwYXJhbSBtYXliZSBtYXliZSBhIFQgdG8gYXBwbHkgdG8gYGZuYFxuICovXG5leHBvcnQgZnVuY3Rpb24gYXA8VCwgVT4obWF5YmVGbjogTWF5YmU8KHQ6IFQpID0+IFU+LCBtYXliZTogTWF5YmU8VD4pOiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBhcDxULCBVPihtYXliZUZuOiBNYXliZTwodDogVCkgPT4gVT4pOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPjtcbmV4cG9ydCBmdW5jdGlvbiBhcDxULCBVPihcbiAgbWF5YmVGbjogTWF5YmU8KHZhbDogVCkgPT4gVT4sXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IE1heWJlPFU+IHwgKCh2YWw6IE1heWJlPFQ+KSA9PiBNYXliZTxVPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT5cbiAgICBtLm1hdGNoKHtcbiAgICAgIEp1c3Q6IHZhbCA9PiBtYXliZUZuLm1hcChmbiA9PiBmbih2YWwpKSxcbiAgICAgIE5vdGhpbmc6ICgpID0+IE1heWJlLm5vdGhpbmc8VT4oKSxcbiAgICB9KTtcblxuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKlxuICBEZXRlcm1pbmUgd2hldGhlciBhbiBpdGVtIGlzIGFuIGluc3RhbmNlIG9mIGBKdXN0YCBvciBgTm90aGluZ2AuXG5cbiAgQHBhcmFtIGl0ZW0gVGhlIGl0ZW0gdG8gY2hlY2suXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBpc0luc3RhbmNlPFQgPSBhbnk+KGl0ZW06IGFueSk6IGl0ZW0gaXMgTWF5YmU8VD4ge1xuICByZXR1cm4gaXRlbSBpbnN0YW5jZW9mIEp1c3QgfHwgaXRlbSBpbnN0YW5jZW9mIE5vdGhpbmc7XG59XG5cbnR5cGUgUHJlZGljYXRlPFQ+ID0gKGVsZW1lbnQ6IFQsIGluZGV4OiBudW1iZXIsIGFycmF5OiBUW10pID0+IGJvb2xlYW47XG5cbi8vIE5PVEU6IGRvY3VtZW50YXRpb24gaXMgbGlnaHRseSBhZGFwdGVkIGZyb20gdGhlIE1ETiBhbmQgVHlwZVNjcmlwdCBkb2NzIGZvclxuLy8gYEFycmF5LnByb3RvdHlwZS5maW5kYC5cbi8qKlxuICBTYWZlbHkgc2VhcmNoIGZvciBhbiBlbGVtZW50IGluIGFuIGFycmF5LlxuICBcbiAgVGhpcyBmdW5jdGlvbiBiZWhhdmVzIGxpa2UgYEFycmF5LnByb3RvdHlwZS5maW5kYCwgYnV0IHJldHVybnMgYE1heWJlPFQ+YFxuICBpbnN0ZWFkIG9mIGBUIHwgdW5kZWZpbmVkYC5cbiAgXG4gICMjIEV4YW1wbGVzXG5cbiAgVGhlIGJhc2ljIGZvcm0gaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgbGV0IGFycmF5ID0gWzEsIDIsIDNdO1xuICBNYXliZS5maW5kKHYgPT4gdiA+IDEsIGFycmF5KTsgLy8gSnVzdCgyKVxuICBNYXliZS5maW5kKHYgPT4gdiA8IDEsIGFycmF5KTsgLy8gTm90aGluZ1xuICBgYGBcblxuICBUaGUgZnVuY3Rpb24gaXMgY3VycmllZCBzbyB5b3UgY2FuIHVzZSBpdCBpbiBhIGZ1bmN0aW9uYWwgY2hhaW4uIEZvciBleGFtcGxlXG4gIChsZWF2aW5nIGFzaWRlIGVycm9yIGhhbmRsaW5nIG9uIGEgYmFkIHJlc3BvbnNlIGZvciBzaW1wbGljaXR5KSwgc3VwcG9zZSB0aGVcbiAgdXJsIGBodHRwczovL2FycmF5cy5leGFtcGxlLmNvbWAgcmV0dXJuZWQgYSBKU09OIHBheWxvYWQgd2l0aCB0aGUgdHlwZVxuICBgQXJyYXk8eyBjb3VudDogbnVtYmVyLCBuYW1lOiBzdHJpbmcgfT5gLCBhbmQgd2Ugd2FudGVkIHRvIGdldCB0aGUgZmlyc3RcbiAgb2YgdGhlc2Ugd2hlcmUgYGNvdW50YCB3YXMgYXQgbGVhc3QgMTAwLiBXZSBjb3VsZCB3cml0ZSB0aGlzOlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIHR5cGUgSXRlbSA9IHsgY291bnQ6IG51bWJlcjsgbmFtZTogc3RyaW5nIH07XG4gIHR5cGUgUmVzcG9uc2UgPSBBcnJheTxJdGVtPjtcblxuICAvLyBjdXJyaWVkIHZhcmlhbnQhXG4gIGNvbnN0IGZpbmRBdExlYXN0MTAwID0gTWF5YmUuZmluZCgoeyBjb3VudCB9OiBJdGVtKSA9PiBjb3VudCA+IDEwMCk7XG5cbiAgZmV0Y2goJ2h0dHBzOi8vYXJyYXlzLmV4YW1wbGUuY29tJylcbiAgICAudGhlbihyZXNwb25zZSA9PiByZXNwb25zZS5qc29uKCkgYXMgUmVzcG9uc2UpXG4gICAgLnRoZW4oZmluZEF0TGVhc3QxMDApXG4gICAgLnRoZW4oZm91bmQgPT4ge1xuICAgICAgaWYgKGZvdW5kLmlzSnVzdCgpKSB7XG4gICAgICAgIGNvbnNvbGUubG9nKGBUaGUgbWF0Y2hpbmcgdmFsdWUgaXMgJHtmb3VuZC52YWx1ZS5uYW1lfSFgKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgYGBgXG4gIFxuICBAcGFyYW0gcHJlZGljYXRlICBBIGZ1bmN0aW9uIHRvIGV4ZWN1dGUgb24gZWFjaCB2YWx1ZSBpbiB0aGUgYXJyYXksIHJldHVybmluZ1xuICAgICAgICAgICAgICAgICAgICBgdHJ1ZWAgd2hlbiB0aGUgaXRlbSBpbiB0aGUgYXJyYXkgbWF0Y2hlcyB0aGUgY29uZGl0aW9uLiBUaGVcbiAgICAgICAgICAgICAgICAgICAgc2lnbmF0dXJlIGZvciBgcHJlZGljYXRlYCBpcyBpZGVudGljYWwgdG8gdGhlIHNpZ25hdHVyZSBmb3JcbiAgICAgICAgICAgICAgICAgICAgdGhlIGZpcnN0IGFyZ3VtZW50IHRvIGBBcnJheS5wcm90b3R5cGUuZmluZGAuIFRoZSBmdW5jdGlvblxuICAgICAgICAgICAgICAgICAgICBpcyBjYWxsZWQgb25jZSBmb3IgZWFjaCBlbGVtZW50IG9mIHRoZSBhcnJheSwgaW4gYXNjZW5kaW5nXG4gICAgICAgICAgICAgICAgICAgIG9yZGVyLCB1bnRpbCBpdCBmaW5kcyBvbmUgd2hlcmUgcHJlZGljYXRlIHJldHVybnMgdHJ1ZS4gSWZcbiAgICAgICAgICAgICAgICAgICAgc3VjaCBhbiBlbGVtZW50IGlzIGZvdW5kLCBmaW5kIGltbWVkaWF0ZWx5IHJldHVybnMgdGhhdFxuICAgICAgICAgICAgICAgICAgICBlbGVtZW50IHZhbHVlIHdyYXBwZWQgaW4gYEp1c3RgLiBPdGhlcndpc2UsIGBNYXliZS5maW5kYFxuICAgICAgICAgICAgICAgICAgICByZXR1cm5zIGBOb3RoaW5nYC5cbiAqIEBwYXJhbSBhcnJheSAgICAgVGhlIGFycmF5IHRvIHNlYXJjaCB1c2luZyB0aGUgcHJlZGljYXRlLlxuICovXG5leHBvcnQgZnVuY3Rpb24gZmluZDxUPihwcmVkaWNhdGU6IFByZWRpY2F0ZTxUPiwgYXJyYXk6IFRbXSk6IE1heWJlPFQ+O1xuZXhwb3J0IGZ1bmN0aW9uIGZpbmQ8VD4ocHJlZGljYXRlOiBQcmVkaWNhdGU8VD4pOiAoYXJyYXk6IFRbXSkgPT4gTWF5YmU8VD47XG5leHBvcnQgZnVuY3Rpb24gZmluZDxUPihcbiAgcHJlZGljYXRlOiBQcmVkaWNhdGU8VD4sXG4gIGFycmF5PzogVFtdXG4pOiBNYXliZTxUPiB8ICgoYXJyYXk6IFRbXSkgPT4gTWF5YmU8VD4pIHtcbiAgY29uc3Qgb3AgPSAoYTogVFtdKSA9PiBNYXliZS5vZihhLmZpbmQocHJlZGljYXRlKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIGFycmF5KTtcbn1cblxuLyoqXG4gIFNhZmVseSBnZXQgdGhlIGZpcnN0IGl0ZW0gZnJvbSBhIGxpc3QsIHJldHVybmluZyBgSnVzdGAgdGhlIGZpcnN0IGl0ZW0gaWYgdGhlXG4gIGFycmF5IGhhcyBhdCBsZWFzdCBvbmUgaXRlbSBpbiBpdCwgb3IgYE5vdGhpbmdgIGlmIGl0IGlzIGVtcHR5LlxuXG4gICMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgbGV0IGVtcHR5ID0gW107XG4gIE1heWJlLmhlYWQoZW1wdHkpOyAvLyA9PiBOb3RoaW5nXG5cbiAgbGV0IGZ1bGwgPSBbMSwgMiwgM107XG4gIE1heWJlLmhlYWQoZnVsbCk7IC8vID0+IEp1c3QoMSlcbiAgYGBgXG5cbiAgQHBhcmFtIGFycmF5IFRoZSBhcnJheSB0byBnZXQgdGhlIGZpcnN0IGl0ZW0gZnJvbS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGhlYWQ8VD4oYXJyYXk6IEFycmF5PFQgfCBudWxsIHwgdW5kZWZpbmVkPik6IE1heWJlPFQ+IHtcbiAgcmV0dXJuIE1heWJlLm9mKGFycmF5WzBdKTtcbn1cblxuLyoqIEEgY29udmVuaWVuY2UgYWxpYXMgZm9yIGBNYXliZS5oZWFkYC4gKi9cbmV4cG9ydCBjb25zdCBmaXJzdCA9IGhlYWQ7XG5cbi8qKlxuICBTYWZlbHkgZ2V0IHRoZSBsYXN0IGl0ZW0gZnJvbSBhIGxpc3QsIHJldHVybmluZyBgSnVzdGAgdGhlIGxhc3QgaXRlbSBpZiB0aGVcbiAgYXJyYXkgaGFzIGF0IGxlYXN0IG9uZSBpdGVtIGluIGl0LCBvciBgTm90aGluZ2AgaWYgaXQgaXMgZW1wdHkuXG5cbiAgIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBsZXQgZW1wdHkgPSBbXTtcbiAgTWF5YmUubGFzdChlbXB0eSk7IC8vID0+IE5vdGhpbmdcblxuICBsZXQgZnVsbCA9IFsxLCAyLCAzXTtcbiAgTWF5YmUubGFzdChmdWxsKTsgLy8gPT4gSnVzdCgzKVxuICBgYGBcblxuICBAcGFyYW0gYXJyYXkgVGhlIGFycmF5IHRvIGdldCB0aGUgZmlyc3QgaXRlbSBmcm9tLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbGFzdDxUPihhcnJheTogQXJyYXk8VCB8IG51bGwgfCB1bmRlZmluZWQ+KTogTWF5YmU8VD4ge1xuICByZXR1cm4gTWF5YmUub2YoYXJyYXlbYXJyYXkubGVuZ3RoIC0gMV0pO1xufVxuXG4vKipcbiAgQ29udmVydCB0aGUgYXJndW1lbnRzIHRvIGEgc2luZ2xlIGBNYXliZWAuIFVzZWZ1bCBmb3IgZGVhbGluZyB3aXRoIGFycmF5cyBvZlxuICBgTWF5YmVgcywgdmlhIHRoZSBzcHJlYWQgb3BlcmF0b3IuXG5cbiAgIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICBsZXQgdmFsaWQgPSBbTWF5YmUuanVzdCgyKSwgTWF5YmUuanVzdCgndGhyZWUnKV07XG4gIE1heWJlLmFsbCguLi52YWxpZCk7IC8vID0+IEp1c3QoWzIsICd0aHJlZSddKTtcblxuICBsZXQgaW52YWxpZCA9IFtNYXliZS5qdXN0KDIpLCBNYXliZS5ub3RoaW5nPHN0cmluZz4oKV07XG4gIE1heWJlLmFsbCguLi5pbnZhbGlkKTsgLy8gPT4gTm90aGluZ1xuICBgYGBcblxuICAjIyBOb3RlIG9uIFNwcmVhZFxuXG4gIFRoaXMgcmVxdWlyZXMgdGhlIHVzZSBvZiB0aGUgc3ByZWFkIG9wZXJhdG9yIGJlY2F1c2UgKGF0IGxlYXN0IGFzIG9mXG4gIFR5cGVTY3JpcHQgMy4wKSwgdGhlIHR5cGUgaW5mZXJlbmNlIGZhbGxzIGRvd24gd2hlbiBhdHRlbXB0aW5nIHRvIGJ1aWxkIHRoaXNcbiAgc2FtZSB0eXBlIHdpdGggYW4gYXJyYXkgZGlyZWN0bHkuIE1vcmVvdmVyLCB0aGlzIHNwcmVhZC1iYXNlZCBhcHByb2FjaCBoYW5kbGVzXG4gIGhldGVyZWdlbm91cyBhcnJheXM7IFRTICphbHNvKiBmYWlscyB0byBpbmZlciBjb3JyZWN0bHkgZm9yIGFueXRoaW5nIGJ1dFxuICBob21vZ2VuZW91cyBhcnJheXMgd2hlbiB1c2luZyB0aGF0IGFwcHJvYWNoLlxuXG4gIEBwYXJhbSBtYXliZXMgVGhlIGBNYXliZWBzIHRvIHJlc29sdmUgdG8gYSBzaW5nbGUgYE1heWJlYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFsbDxUIGV4dGVuZHMgQXJyYXk8TWF5YmU8dW5rbm93bj4+PiguLi5tYXliZXM6IFQpOiBBbGw8VD4ge1xuICBsZXQgcmVzdWx0OiBBbGw8VD4gPSBNYXliZS5qdXN0KFtdIGFzIE1heWJlPHVua25vd24+W10pIGFzIEFsbDxUPjtcbiAgbWF5YmVzLmZvckVhY2gobWF5YmUgPT4ge1xuICAgIHJlc3VsdCA9IHJlc3VsdC5hbmRUaGVuKGFjY3VtdWxhdGVkTWF5YmVzID0+XG4gICAgICBtYXliZS5tYXAobSA9PiB7XG4gICAgICAgIGFjY3VtdWxhdGVkTWF5YmVzLnB1c2gobSk7XG4gICAgICAgIHJldHVybiBhY2N1bXVsYXRlZE1heWJlcztcbiAgICAgIH0pXG4gICAgKSBhcyBBbGw8VD47XG4gIH0pO1xuXG4gIHJldHVybiByZXN1bHQ7XG59XG5cbnR5cGUgQWxsPFQgZXh0ZW5kcyBBcnJheTxNYXliZTxhbnk+Pj4gPSBUIGV4dGVuZHMgQXJyYXk8TWF5YmU8aW5mZXIgVT4+ID8gTWF5YmU8QXJyYXk8VT4+IDogbmV2ZXI7XG5cbi8qKlxuICBHaXZlbiBhIHR1cGxlIG9mIGBNYXliZWBzLCByZXR1cm4gYSBgTWF5YmVgIG9mIHRoZSB0dXBsZSB2YWx1ZXMuXG5cbiAgR2l2ZW4gYSB0dXBsZSBvZiB0eXBlIGBbTWF5YmU8QT4sIE1heWJlPEI+XWAsIHRoZSByZXN1bHRpbmcgdHlwZSBpc1xuICBgTWF5YmU8W0EsIEJdPmAuIFdvcmtzIHdpdGggdXAgdG8gYSA1LXR1cGxlLiAoSWYgeW91J3JlIGRvaW5nIG1vcmUgdGhhbiBhXG4gIDUtdHVwbGUsIHdoYXQgYXJlIHlvdSBkb2luZz8/PylcblxuICAjIyBFeGFtcGxlc1xuXG4gIElmIGFueSBvZiB0aGUgaXRlbXMgaW4gdGhlIHR1cGxlIGFyZSBgTm90aGluZ2AsIHRoZSB3aG9sZSByZXN1bHQgaXMgYE5vdGhpbmdgLlxuICBIZXJlLCBmb3IgZXhhbXBsZSwgYHJlc3VsdGAgaGFzIHRoZSB0eXBlIGBNYXliZTxbc3RyaW5nLCBudW1iZXJdPmAgYW5kIHdpbGwgYmVcbiAgYE5vdGhpbmdgOlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIHR5cGUgVHVwbGUgPSBbTWF5YmU8c3RyaW5nPiwgTWF5YmU8bnVtYmVyPl07XG5cbiAgbGV0IGludmFsaWQ6IFR1cGxlID0gW01heWJlLmp1c3QoJ3dhdCcpLCBNYXliZS5ub3RoaW5nKCldO1xuICBsZXQgcmVzdWx0ID0gTWF5YmUudHVwbGUoaW52YWxpZCk7ICAvLyA9PiBOb3RoaW5nXG4gIGBgYFxuXG4gIElmIGFsbCBvZiB0aGUgaXRlbXMgaW4gdGhlIHR1cGxlIGFyZSBgSnVzdGAsIHRoZSByZXN1bHQgaXMgYEp1c3RgIHdyYXBwaW5nIHRoZVxuICB0dXBsZSBvZiB0aGUgdmFsdWVzIG9mIHRoZSBpdGVtcy4gSGVyZSwgZm9yIGV4YW1wbGUsIGByZXN1bHRgIGFnYWluIGhhcyB0aGVcbiAgdHlwZSBgTWF5YmU8W3N0cmluZywgbnVtYmVyXT5gIGFuZCB3aWxsIGJlIGBKdXN0KFsnaGV5JywgMTJdYDpcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICB0eXBlIFR1cGxlID0gW01heWJlPHN0cmluZz4sIE1heWJlPG51bWJlcj5dO1xuXG4gIGxldCB2YWxpZDogVHVwbGUgPSBbTWF5YmUuanVzdCgnaGV5JyksIE1heWJlLmp1c3QoMTIpXTtcbiAgbGV0IHJlc3VsdCA9IE1heWJlLnR1cGxlKHZhbGlkKTsgIC8vID0+IEp1c3QoWydoZXknLCAxMl0pXG4gIGBgYFxuXG4gIEBwYXJhbSBtYXliZXM6IHRoZSB0dXBsZSBvZiBgTWF5YmVgcyB0byBjb252ZXJ0IHRvIGEgYE1heWJlYCBvZiB0dXBsZSB2YWx1ZXMuXG4gKi9cbi8vIEB0cy1pZ25vcmUgLS0gdGhpcyBkb2Vzbid0IHR5cGUtY2hlY2ssIGJ1dCBpdCBpcyBjb3JyZWN0IVxuZXhwb3J0IGZ1bmN0aW9uIHR1cGxlPFQ+KG1heWJlczogW01heWJlPFQ+XSk6IE1heWJlPFtUXT47XG5leHBvcnQgZnVuY3Rpb24gdHVwbGU8VCwgVT4obWF5YmVzOiBbTWF5YmU8VD4sIE1heWJlPFU+XSk6IE1heWJlPFtULCBVXT47XG5leHBvcnQgZnVuY3Rpb24gdHVwbGU8VCwgVSwgVj4obWF5YmVzOiBbTWF5YmU8VD4sIE1heWJlPFU+LCBNYXliZTxWPl0pOiBNYXliZTxbVCwgVSwgVl0+O1xuZXhwb3J0IGZ1bmN0aW9uIHR1cGxlPFQsIFUsIFYsIFc+KFxuICBtYXliZXM6IFtNYXliZTxUPiwgTWF5YmU8VT4sIE1heWJlPFY+LCBNYXliZTxXPl1cbik6IE1heWJlPFtULCBVLCBWLCBXXT47XG5leHBvcnQgZnVuY3Rpb24gdHVwbGU8VCwgVSwgViwgVywgWD4oXG4gIG1heWJlczogW01heWJlPFQ+LCBNYXliZTxVPiwgTWF5YmU8Vj4sIE1heWJlPFc+LCBNYXliZTxYPl1cbik6IE1heWJlPFtULCBVLCBWLCBXLCBYXT4ge1xuICAvLyBAdHMtaWdub3JlIC0tIHRoaXMgZG9lc24ndCB0eXBlLWNoZWNrLCBidXQgaXQgd29ya3MgY29ycmVjdGx5LlxuICByZXR1cm4gYWxsKC4uLm1heWJlcyk7XG59XG5cbi8qKlxuICBTYWZlbHkgZXh0cmFjdCBhIGtleSBmcm9tIGFuIG9iamVjdCwgcmV0dXJuaW5nIGBKdXN0YCBpZiB0aGUga2V5IGhhcyBhIHZhbHVlXG4gIG9uIHRoZSBvYmplY3QgYW5kIGBOb3RoaW5nYCBpZiBpdCBkb2VzIG5vdC5cblxuICBUaGUgY2hlY2sgaXMgdHlwZS1zYWZlOiB5b3Ugd29uJ3QgZXZlbiBiZSBhYmxlIHRvIGNvbXBpbGUgaWYgeW91IHRyeSB0byBsb29rXG4gIHVwIGEgcHJvcGVydHkgdGhhdCBUeXBlU2NyaXB0ICprbm93cyogZG9lc24ndCBleGlzdCBvbiB0aGUgb2JqZWN0LlxuXG4gIGBgYHRzXG4gIHR5cGUgUGVyc29uID0geyBuYW1lPzogc3RyaW5nIH07XG5cbiAgY29uc3QgbWU6IFBlcnNvbiA9IHsgbmFtZTogJ0NocmlzJyB9O1xuICBjb25zb2xlLmxvZyhNYXliZS5wcm9wZXJ0eSgnbmFtZScsIG1lKSk7IC8vIEp1c3QoJ0NocmlzJylcblxuICBjb25zdCBub2JvZHk6IFBlcnNvbiA9IHt9O1xuICBjb25zb2xlLmxvZyhNYXliZS5wcm9wZXJ0eSgnbmFtZScsIG5vYm9keSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIEhvd2V2ZXIsIGl0IGFsc28gd29ya3MgY29ycmVjdGx5IHdpdGggZGljdGlvbmFyeSB0eXBlczpcblxuICBgYGB0c1xuICB0eXBlIERpY3Q8VD4gPSB7IFtrZXk6IHN0cmluZ106IFQgfTtcblxuICBjb25zdCBzY29yZTogRGljdDxudW1iZXI+ID0ge1xuICAgIHBsYXllcjE6IDAsXG4gICAgcGxheWVyMjogMVxuICB9O1xuXG4gIGNvbnNvbGUubG9nKE1heWJlLnByb3BlcnR5KCdwbGF5ZXIxJywgc2NvcmUpKTsgLy8gSnVzdCgwKVxuICBjb25zb2xlLmxvZyhNYXliZS5wcm9wZXJ0eSgncGxheWVyMicsIHNjb3JlKSk7IC8vIEp1c3QoMSlcbiAgY29uc29sZS5sb2coTWF5YmUucHJvcGVydHkoJ3BsYXllcjMnLCBzY29yZSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIFRoZSBvcmRlciBvZiBrZXlzIGlzIHNvIHRoYXQgaXQgY2FuIGJlIHBhcnRpYWxseSBhcHBsaWVkOlxuXG4gIGBgYHRzXG4gIHR5cGUgUGVyc29uID0geyBuYW1lPzogc3RyaW5nIH07XG4gIFxuICBjb25zdCBsb29rdXBOYW1lID0gTWF5YmUucHJvcGVydHkoJ25hbWUnKTtcbiAgXG4gIGNvbnN0IG1lOiBQZXJzb24gPSB7IG5hbWU6ICdDaHJpcycgfTtcbiAgY29uc29sZS5sb2cobG9va3VwTmFtZShtZSkpOyAvLyBKdXN0KCdDaHJpcycpXG5cbiAgY29uc3Qgbm9ib2R5OiBQZXJzb24gPSB7fTtcbiAgY29uc29sZS5sb2cobG9va3VwTmFtZShub2JvZHkpKTsgLy8gTm90aGluZ1xuICBgYGBcbiAgXG4gIEBwYXJhbSBrZXkgVGhlIGtleSB0byBwdWxsIG91dCBvZiB0aGUgb2JqZWN0LlxuICBAcGFyYW0gb2JqIFRoZSBvYmplY3QgdG8gbG9vayB1cCB0aGUga2V5IGZyb20uXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBwcm9wZXJ0eTxULCBLIGV4dGVuZHMga2V5b2YgVD4oa2V5OiBLLCBvYmo6IFQpOiBNYXliZTxOb25OdWxsYWJsZTxUW0tdPj47XG5leHBvcnQgZnVuY3Rpb24gcHJvcGVydHk8VCwgSyBleHRlbmRzIGtleW9mIFQ+KGtleTogSyk6IChvYmo6IFQpID0+IE1heWJlPE5vbk51bGxhYmxlPFRbS10+PjtcbmV4cG9ydCBmdW5jdGlvbiBwcm9wZXJ0eTxULCBLIGV4dGVuZHMga2V5b2YgVD4oXG4gIGtleTogSyxcbiAgb2JqPzogVFxuKTogTWF5YmU8Tm9uTnVsbGFibGU8VFtLXT4+IHwgKChvYmo6IFQpID0+IE1heWJlPE5vbk51bGxhYmxlPFRbS10+Pikge1xuICBjb25zdCBvcCA9IChhOiBUKSA9PiBNYXliZS5vZihhW2tleV0pIGFzIE1heWJlPE5vbk51bGxhYmxlPFRbS10+PjtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgb2JqKTtcbn1cblxuLyoqXG4gIFNhZmVseSBleHRyYWN0IGEga2V5IGZyb20gYSBNYXliZSBvZiBhbiBvYmplY3QsIHJldHVybmluZyBgSnVzdGAgaWYgdGhlIGtleVxuICBoYXMgYSB2YWx1ZSBvbiB0aGUgb2JqZWN0IGFuZCBgTm90aGluZ2AgaWYgaXQgZG9lcyBub3QuIChMaWtlIGBNYXliZS5wcm9wZXJ0eWBcbiAgYnV0IG9wZXJhdGluZyBvbiBhIGBNYXliZTxUPmAgcmF0aGVyIHRoYW4gZGlyZWN0bHkgb24gYSBgVGAuKVxuXG4gIFRoZSBjaGVjayBpcyB0eXBlLXNhZmU6IHlvdSB3b24ndCBldmVuIGJlIGFibGUgdG8gY29tcGlsZSBpZiB5b3UgdHJ5IHRvIGxvb2tcbiAgdXAgYSBwcm9wZXJ0eSB0aGF0IFR5cGVTY3JpcHQgKmtub3dzKiBkb2Vzbid0IGV4aXN0IG9uIHRoZSBvYmplY3QuXG5cbiAgYGBgdHNcbiAgdHlwZSBQZXJzb24gPSB7IG5hbWU/OiBzdHJpbmcgfTtcblxuICBjb25zdCBtZTogTWF5YmU8UGVyc29uPiA9IE1heWJlLmp1c3QoeyBuYW1lOiAnQ2hyaXMnIH0pO1xuICBjb25zb2xlLmxvZyhNYXliZS5nZXQoJ25hbWUnLCBtZSkpOyAvLyBKdXN0KCdDaHJpcycpXG5cbiAgY29uc3Qgbm9ib2R5ID0gTWF5YmUubm90aGluZzxQZXJzb24+KCk7XG4gIGNvbnNvbGUubG9nKE1heWJlLmdldCgnbmFtZScsIG5vYm9keSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIEhvd2V2ZXIsIGl0IGFsc28gd29ya3MgY29ycmVjdGx5IHdpdGggZGljdGlvbmFyeSB0eXBlczpcblxuICBgYGB0c1xuICB0eXBlIERpY3Q8VD4gPSB7IFtrZXk6IHN0cmluZ106IFQgfTtcblxuICBjb25zdCBzY29yZTogTWF5YmU8RGljdDxudW1iZXI+PiA9IE1heWJlLmp1c3Qoe1xuICAgIHBsYXllcjE6IDAsXG4gICAgcGxheWVyMjogMVxuICB9KTtcblxuICBjb25zb2xlLmxvZyhNYXliZS5nZXQoJ3BsYXllcjEnLCBzY29yZSkpOyAvLyBKdXN0KDApXG4gIGNvbnNvbGUubG9nKE1heWJlLmdldCgncGxheWVyMicsIHNjb3JlKSk7IC8vIEp1c3QoMSlcbiAgY29uc29sZS5sb2coTWF5YmUuZ2V0KCdwbGF5ZXIzJywgc2NvcmUpKTsgLy8gTm90aGluZ1xuICBgYGBcblxuICBUaGUgb3JkZXIgb2Yga2V5cyBpcyBzbyB0aGF0IGl0IGNhbiBiZSBwYXJ0aWFsbHkgYXBwbGllZDpcblxuICBgYGB0c1xuICB0eXBlIFBlcnNvbiA9IHsgbmFtZT86IHN0cmluZyB9O1xuICBcbiAgY29uc3QgbG9va3VwTmFtZSA9IE1heWJlLmdldCgnbmFtZScpO1xuICBcbiAgY29uc3QgbWU6IFBlcnNvbiA9IHsgbmFtZTogJ0NocmlzJyB9O1xuICBjb25zb2xlLmxvZyhsb29rdXBOYW1lKG1lKSk7IC8vIEp1c3QoJ0NocmlzJylcblxuICBjb25zdCBub2JvZHk6IFBlcnNvbiA9IHt9O1xuICBjb25zb2xlLmxvZyhsb29rdXBOYW1lKG5vYm9keSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuICBcbiAgQHBhcmFtIGtleSBUaGUga2V5IHRvIHB1bGwgb3V0IG9mIHRoZSBvYmplY3QuXG4gIEBwYXJhbSBvYmogVGhlIG9iamVjdCB0byBsb29rIHVwIHRoZSBrZXkgZnJvbS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGdldDxULCBLIGV4dGVuZHMga2V5b2YgVD4oa2V5OiBLLCBtYXliZU9iajogTWF5YmU8VD4pOiBNYXliZTxSZXF1aXJlZDxUPltLXT47XG5leHBvcnQgZnVuY3Rpb24gZ2V0PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPihrZXk6IEspOiAobWF5YmVPYmo6IE1heWJlPFQ+KSA9PiBNYXliZTxSZXF1aXJlZDxUPltLXT47XG5leHBvcnQgZnVuY3Rpb24gZ2V0PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPihcbiAga2V5OiBLLFxuICBtYXliZU9iaj86IE1heWJlPFQ+XG4pOiBNYXliZTxSZXF1aXJlZDxUPltLXT4gfCAoKG1heWJlT2JqOiBNYXliZTxUPikgPT4gTWF5YmU8UmVxdWlyZWQ8VD5bS10+KSB7XG4gIHJldHVybiBjdXJyeTEoTWF5YmUuYW5kVGhlbihwcm9wZXJ0eTxULCBLPihrZXkpKSwgbWF5YmVPYmopO1xufVxuXG4vKiogQSB2YWx1ZSB3aGljaCBtYXkgKGBKdXN0PFQ+YCkgb3IgbWF5IG5vdCAoYE5vdGhpbmdgKSBiZSBwcmVzZW50LiAqL1xuZXhwb3J0IHR5cGUgTWF5YmU8VD4gPSBKdXN0PFQ+IHwgTm90aGluZzxUPjtcbmV4cG9ydCBjb25zdCBNYXliZSA9IHtcbiAgVmFyaWFudCxcbiAgSnVzdCxcbiAgTm90aGluZyxcbiAgYWxsLFxuICBpc0p1c3QsXG4gIGlzTm90aGluZyxcbiAganVzdCxcbiAgbm90aGluZyxcbiAgb2YsXG4gIGZpbmQsXG4gIGZpcnN0LFxuICBmcm9tTnVsbGFibGUsXG4gIGhlYWQsXG4gIGxhc3QsXG4gIG1hcCxcbiAgbWFwT3IsXG4gIG1hcE9yRWxzZSxcbiAgYW5kLFxuICBhbmRUaGVuLFxuICBjaGFpbixcbiAgZmxhdE1hcCxcbiAgb3IsXG4gIG9yRWxzZSxcbiAgdW5zYWZlbHlVbndyYXAsXG4gIHVuc2FmZWx5R2V0LFxuICB1bnNhZmVHZXQsXG4gIHVud3JhcE9yLFxuICBnZXRPcixcbiAgdW53cmFwT3JFbHNlLFxuICBnZXRPckVsc2UsXG4gIHRvT2tPckVycixcbiAgdG9Pa09yRWxzZUVycixcbiAgZnJvbVJlc3VsdCxcbiAgdG9TdHJpbmcsXG4gIHR1cGxlLFxuICBtYXRjaCxcbiAgY2F0YSxcbiAgZXF1YWxzLFxuICBhcCxcbiAgaXNJbnN0YW5jZSxcbiAgcHJvcGVydHksXG4gIGdldCxcbn07XG5cbmV4cG9ydCBkZWZhdWx0IE1heWJlO1xuIl19