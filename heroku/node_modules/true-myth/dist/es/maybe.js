/** [[include:doc/maybe.md]] */
/** (keep typedoc from getting confused by the imports) */
import { err, ok } from './result';
import { curry1, isVoid } from './utils';
/**
  Discriminant for the `Just` and `Nothing` variants.

  You can use the discriminant via the `variant` property of `Maybe` instances
  if you need to match explicitly on it.
 */
export var Variant;
(function (Variant) {
    Variant["Just"] = "Just";
    Variant["Nothing"] = "Nothing";
})(Variant || (Variant = {}));
/**
  A `Just` instance is the *present* variant instance of the
  [`Maybe`](../modules/_maybe_.html#maybe) type, representing the presence of a
  value which may be absent. For a full discussion, see [the module
  docs](../modules/_maybe_.html).

  @typeparam T The type wrapped in this `Just` variant of `Maybe`.
 */
export class Just {
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
        if (isVoid(value)) {
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
/**
  A `Nothing` instance is the *absent* variant instance of the
  [`Maybe`](../modules/_maybe_.html#maybe) type, representing the presence of a
  value which may be absent. For a full discussion, see [the module
  docs](../modules/_maybe_.html).

  @typeparam T The type which would be wrapped in a `Just` variant of `Maybe`.
 */
export class Nothing {
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
/**
  Is this result a `Just` instance?

  @typeparam T The type of the wrapped value.
  @param maybe The `Maybe` instance to check.
  @returns     `true` if `maybe` is `Just`, `false` otherwise. In TypeScript,
               also narrows the type from `Maybe<T>` to `Just<T>`.
 */
export function isJust(maybe) {
    return maybe.variant === Variant.Just;
}
/**
  Is this result a `Nothing` instance?

  @typeparam T The type of the wrapped value.
  @param maybe The `Maybe` instance to check.
  @returns     `true` if `maybe` is `nothing`, `false` otherwise. In TypeScript,
               also narrows the type from `Maybe<T>` to `Nothing<T>`.
 */
export function isNothing(maybe) {
    return maybe.variant === Variant.Nothing;
}
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
export function just(value) {
    return new Just(value);
}
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
export function nothing(_) {
    return new Nothing(_);
}
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
export function of(value) {
    return isVoid(value) ? nothing() : just(value);
}
/** Alias for [`of`](#of), primarily for compatibility with Folktale. */
export const fromNullable = of;
export function map(mapFn, maybe) {
    const op = (m) => (m.isJust() ? just(mapFn(m.value)) : nothing());
    return curry1(op, maybe);
}
export function mapOr(orU, mapFn, maybe) {
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
export function mapOrElse(orElseFn, mapFn, maybe) {
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
export function and(andMaybe, maybe) {
    const op = (m) => (m.isJust() ? andMaybe : nothing());
    return curry1(op, maybe);
}
export function andThen(thenFn, maybe) {
    const op = (m) => (m.isJust() ? thenFn(m.value) : nothing());
    return maybe !== undefined ? op(maybe) : op;
}
/** Alias for [`andThen`](#andthen). */
export const chain = andThen;
/** Alias for [`andThen`](#andthen). */
export const flatMap = andThen;
export function or(defaultMaybe, maybe) {
    const op = (m) => (m.isJust() ? m : defaultMaybe);
    return maybe !== undefined ? op(maybe) : op;
}
export function orElse(elseFn, maybe) {
    const op = (m) => (m.isJust() ? m : elseFn());
    return curry1(op, maybe);
}
/**
  Get the value out of the `Maybe`.

  Returns the content of a `Just`, but **throws if the `Maybe` is `Nothing`**.
  Prefer to use [`unwrapOr`](#unwrapor) or [`unwrapOrElse`](#unwraporelse).

  @typeparam T The type of the wrapped value.
  @param maybe The value to unwrap
  @returns     The unwrapped value if the `Maybe` instance is `Just`.
  @throws      If the `maybe` is `Nothing`.
 */
export function unsafelyUnwrap(maybe) {
    return maybe.unsafelyUnwrap();
}
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
export const unsafelyGet = unsafelyUnwrap;
/** Alias for [`unsafelyUnwrap`](#unsafelyunwrap) */
export const unsafeGet = unsafelyUnwrap;
export function unwrapOr(defaultValue, maybe) {
    const op = (m) => (m.isJust() ? m.value : defaultValue);
    return curry1(op, maybe);
}
/** Alias for [`unwrapOr`](#unwrapor) */
export const getOr = unwrapOr;
export function unwrapOrElse(orElseFn, maybe) {
    const op = (m) => (m.isJust() ? m.value : orElseFn());
    return curry1(op, maybe);
}
/** Alias for [`unwrapOrElse`](#unwraporelse) */
export const getOrElse = unwrapOrElse;
export function toOkOrErr(error, maybe) {
    const op = (m) => (m.isJust() ? ok(m.value) : err(error));
    return maybe !== undefined ? op(maybe) : op;
}
export function toOkOrElseErr(elseFn, maybe) {
    const op = (m) => (m.isJust() ? ok(m.value) : err(elseFn()));
    return curry1(op, maybe);
}
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
export function fromResult(result) {
    return result.isOk() ? just(result.value) : nothing();
}
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
export function toString(maybe) {
    const body = maybe.isJust() ? `(${maybe.value.toString()})` : '';
    return `${maybe.variant}${body}`;
}
export function match(matcher, maybe) {
    return maybe !== undefined
        ? mapOrElse(matcher.Nothing, matcher.Just, maybe)
        : (curriedMaybe) => mapOrElse(matcher.Nothing, matcher.Just, curriedMaybe);
}
/** Alias for [`match`](#match) */
export const cata = match;
export function equals(mb, ma) {
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
export function ap(maybeFn, maybe) {
    const op = (m) => m.match({
        Just: val => maybeFn.map(fn => fn(val)),
        Nothing: () => Maybe.nothing(),
    });
    return curry1(op, maybe);
}
/**
  Determine whether an item is an instance of `Just` or `Nothing`.

  @param item The item to check.
 */
export function isInstance(item) {
    return item instanceof Just || item instanceof Nothing;
}
export function find(predicate, array) {
    const op = (a) => Maybe.of(a.find(predicate));
    return curry1(op, array);
}
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
export function head(array) {
    return Maybe.of(array[0]);
}
/** A convenience alias for `Maybe.head`. */
export const first = head;
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
export function last(array) {
    return Maybe.of(array[array.length - 1]);
}
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
export function all(...maybes) {
    let result = Maybe.just([]);
    maybes.forEach(maybe => {
        result = result.andThen(accumulatedMaybes => maybe.map(m => {
            accumulatedMaybes.push(m);
            return accumulatedMaybes;
        }));
    });
    return result;
}
export function tuple(maybes) {
    // @ts-ignore -- this doesn't type-check, but it works correctly.
    return all(...maybes);
}
export function property(key, obj) {
    const op = (a) => Maybe.of(a[key]);
    return curry1(op, obj);
}
export function get(key, maybeObj) {
    return curry1(Maybe.andThen(property(key)), maybeObj);
}
export const Maybe = {
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
    first,
    fromNullable,
    head,
    last,
    map,
    mapOr,
    mapOrElse,
    and,
    andThen,
    chain,
    flatMap,
    or,
    orElse,
    unsafelyUnwrap,
    unsafelyGet,
    unsafeGet,
    unwrapOr,
    getOr,
    unwrapOrElse,
    getOrElse,
    toOkOrErr,
    toOkOrElseErr,
    fromResult,
    toString,
    tuple,
    match,
    cata,
    equals,
    ap,
    isInstance,
    property,
    get,
};
export default Maybe;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWF5YmUuanMiLCJzb3VyY2VSb290IjoiLi8iLCJzb3VyY2VzIjpbIm1heWJlLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBLCtCQUErQjtBQUUvQiwwREFBMEQ7QUFDMUQsT0FBZSxFQUFFLEdBQUcsRUFBRSxFQUFFLEVBQUUsTUFBTSxVQUFVLENBQUM7QUFDM0MsT0FBTyxFQUFFLE1BQU0sRUFBRSxNQUFNLEVBQUUsTUFBTSxTQUFTLENBQUM7QUFFekM7Ozs7O0dBS0c7QUFDSCxNQUFNLENBQU4sSUFBWSxPQUdYO0FBSEQsV0FBWSxPQUFPO0lBQ2pCLHdCQUFhLENBQUE7SUFDYiw4QkFBbUIsQ0FBQTtBQUNyQixDQUFDLEVBSFcsT0FBTyxLQUFQLE9BQU8sUUFHbEI7QUEyR0Q7Ozs7Ozs7R0FPRztBQUNILE1BQU0sT0FBTyxJQUFJO0lBNEJmOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7T0EyQkc7SUFDSCxZQUFZLEtBQWdCO1FBbEM1Qix3RUFBd0U7UUFDL0QsWUFBTyxHQUFpQixPQUFPLENBQUMsSUFBSSxDQUFDO1FBa0M1QyxJQUFJLE1BQU0sQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUNqQixNQUFNLElBQUksS0FBSyxDQUFDLHNEQUFzRCxDQUFDLENBQUM7U0FDekU7UUFFRCxJQUFJLENBQUMsS0FBSyxHQUFHLEtBQUssQ0FBQztJQUNyQixDQUFDO0lBN0REOzs7Ozs7Ozs7Ozs7Ozs7O09BZ0JHO0lBQ0gsTUFBTSxDQUFDLE1BQU0sQ0FBSSxPQUFnQjtRQUMvQixPQUFPLE9BQU8sQ0FBQyxLQUFLLENBQUM7SUFDdkIsQ0FBQztJQTRDRCwwRUFBMEU7SUFDMUUsTUFBTTtRQUNKLE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztJQUVELGdGQUFnRjtJQUNoRixTQUFTO1FBQ1AsT0FBTyxLQUFLLENBQUM7SUFDZixDQUFDO0lBRUQsb0VBQW9FO0lBQ3BFLEdBQUcsQ0FBb0IsS0FBa0I7UUFDdkMsT0FBTyxHQUFHLENBQUMsS0FBSyxFQUFFLElBQUks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QUFTO0lBQ1QsYUFBYTtJQUNiLFVBQVU7SUFDVixRQUFRO0lBQ1IsS0FBSztJQUNMLEtBQUs7SUFDTCxJQUFJO0lBQ0osTUFBTTtJQUNOLEVBQUU7SUFDRixVQUFVO0lBQ1YsUUFBUTtJQUNSLEdBQUc7Q0FDSixDQUFDO0FBRUYsZUFBZSxLQUFLLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyIvKiogW1tpbmNsdWRlOmRvYy9tYXliZS5tZF1dICovXG5cbi8qKiAoa2VlcCB0eXBlZG9jIGZyb20gZ2V0dGluZyBjb25mdXNlZCBieSB0aGUgaW1wb3J0cykgKi9cbmltcG9ydCBSZXN1bHQsIHsgZXJyLCBvayB9IGZyb20gJy4vcmVzdWx0JztcbmltcG9ydCB7IGN1cnJ5MSwgaXNWb2lkIH0gZnJvbSAnLi91dGlscyc7XG5cbi8qKlxuICBEaXNjcmltaW5hbnQgZm9yIHRoZSBgSnVzdGAgYW5kIGBOb3RoaW5nYCB2YXJpYW50cy5cblxuICBZb3UgY2FuIHVzZSB0aGUgZGlzY3JpbWluYW50IHZpYSB0aGUgYHZhcmlhbnRgIHByb3BlcnR5IG9mIGBNYXliZWAgaW5zdGFuY2VzXG4gIGlmIHlvdSBuZWVkIHRvIG1hdGNoIGV4cGxpY2l0bHkgb24gaXQuXG4gKi9cbmV4cG9ydCBlbnVtIFZhcmlhbnQge1xuICBKdXN0ID0gJ0p1c3QnLFxuICBOb3RoaW5nID0gJ05vdGhpbmcnLFxufVxuXG4vKiogU2ltcGx5IGRlZmluZXMgdGhlIGNvbW1vbiBzaGFwZSBmb3IgYEp1c3RgIGFuZCBgTm90aGluZ2AuICovXG5leHBvcnQgaW50ZXJmYWNlIE1heWJlU2hhcGU8VD4ge1xuICAvKiogRGlzdGluZ3Vpc2ggYmV0d2VlbiB0aGUgYEp1c3RgIGFuZCBgTm90aGluZ2AgW3ZhcmlhbnRzXSguLi9lbnVtcy9fbWF5YmVfLnZhcmlhbnQpLiAqL1xuICByZWFkb25seSB2YXJpYW50OiBWYXJpYW50O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5pc0p1c3RgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNpc2p1c3QpICovXG4gIGlzSnVzdCh0aGlzOiBNYXliZTxUPik6IHRoaXMgaXMgSnVzdDxUPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuaXNOb3RoaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjaXNub3RoaW5nKSAqL1xuICBpc05vdGhpbmcodGhpczogTWF5YmU8VD4pOiB0aGlzIGlzIE5vdGhpbmc8VD47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcCkgKi9cbiAgbWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBtYXBGbjogKHQ6IFQpID0+IFUpOiBNYXliZTxVPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwT3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXBvcikgKi9cbiAgbWFwT3I8VT4odGhpczogTWF5YmU8VD4sIG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVTtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwT3JFbHNlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWFwb3JlbHNlKSAqL1xuICBtYXBPckVsc2U8VT4odGhpczogTWF5YmU8VD4sIG9yRWxzZUZuOiAoKSA9PiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiBVO1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXRjaGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hdGNoKSAqL1xuICBtYXRjaDxVPih0aGlzOiBNYXliZTxUPiwgbWF0Y2hlcjogTWF0Y2hlcjxULCBVPik6IFU7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb3IpICovXG4gIG9yKHRoaXM6IE1heWJlPFQ+LCBtT3I6IE1heWJlPFQ+KTogTWF5YmU8VD47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI29yZWxzZSkgKi9cbiAgb3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gTWF5YmU8VD4pOiBNYXliZTxUPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYW5kYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYW5kKSAqL1xuICBhbmQ8VT4odGhpczogTWF5YmU8VD4sIG1BbmQ6IE1heWJlPFU+KTogTWF5YmU8VT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmFuZFRoZW5gXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNhbmR0aGVuKSAqL1xuICBhbmRUaGVuPFU+KHRoaXM6IE1heWJlPFQ+LCBhbmRUaGVuRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5jaGFpbmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2NoYWluKSAqL1xuICBjaGFpbjxVPih0aGlzOiBNYXliZTxUPiwgY2hhaW5GbjogKHQ6IFQpID0+IE1heWJlPFU+KTogTWF5YmU8VT47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmZsYXRNYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNmbGF0bWFwKSAqL1xuICBmbGF0TWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBmbGF0TWFwRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+O1xuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS51bndyYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bndyYXApICovXG4gIHVuc2FmZWx5VW53cmFwKCk6IFQgfCBuZXZlcjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW53cmFwT3JFbHNlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdW53cmFwb3JlbHNlKSAqL1xuICB1bndyYXBPckVsc2UodGhpczogTWF5YmU8VD4sIGVsc2VGbjogKCkgPT4gVCk6IFQ7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvT2tPckVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVycikgKi9cbiAgdG9Pa09yRXJyPEU+KHRoaXM6IE1heWJlPFQ+LCBlcnJvcjogRSk6IFJlc3VsdDxULCBFPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9Pa09yRWxzZUVycmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Rvb2tvcmVsc2VlcnIpICovXG4gIHRvT2tPckVsc2VFcnI8RT4odGhpczogTWF5YmU8VD4sIGVsc2VGbjogKCkgPT4gRSk6IFJlc3VsdDxULCBFPjtcblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9TdHJpbmdgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN0b3N0cmluZykgKi9cbiAgdG9TdHJpbmcodGhpczogTWF5YmU8VD4pOiBzdHJpbmc7XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmVxdWFsc2BdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2VxdWFscykgKi9cbiAgZXF1YWxzKHRoaXM6IE1heWJlPFQ+LCBjb21wYXJpc29uOiBNYXliZTxUPik6IGJvb2xlYW47XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYXApICovXG4gIGFwPFU+KHRoaXM6IE1heWJlPCh2YWw6IFQpID0+IFU+LCB2YWw6IE1heWJlPFQ+KTogTWF5YmU8VT47XG5cbiAgLyoqXG4gICAgTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuZ2V0YF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjcHJvcClcblxuICAgICAgICBJZiB5b3UgaGF2ZSBhIGBNYXliZWAgb2YgYW4gb2JqZWN0IHR5cGUsIHlvdSBjYW4gZG8gYHRoYXRNYXliZS5nZXQoJ2Ega2V5JylgXG4gICAgdG8gbG9vayB1cCB0aGUgbmV4dCBsYXllciBkb3duIGluIHRoZSBvYmplY3QuXG5cbiAgICBgYGB0c1xuICAgIHR5cGUgRGVlcE9wdGlvbmFsVHlwZSA9IHtcbiAgICAgIHNvbWV0aGluZz86IHtcbiAgICAgICAgd2l0aD86IHtcbiAgICAgICAgICBkZWVwZXJLZXlzPzogc3RyaW5nO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfTtcblxuICAgIGNvbnN0IGZ1bGx5U2V0OiBEZWVwVHlwZSA9IHtcbiAgICAgIHNvbWV0aGluZzoge1xuICAgICAgICB3aXRoOiB7XG4gICAgICAgICAgZGVlcGVyS2V5czogJ2xpa2UgdGhpcydcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH07XG5cbiAgICBjb25zdCBkZWVwSnVzdCA9IE1heWJlLm9mKGZ1bGx5U2V0KVxuICAgICAgLmdldCgnc29tZXRoaW5nJylcbiAgICAgIC5nZXQoJ3dpdGgnKVxuICAgICAgLmdldCgnZGVlcGVyS2V5cycpO1xuXG4gICAgY29uc29sZS5sb2coZGVlcEp1c3QpOyAvLyBKdXN0KCdsaWtlIHRoaXMnKTtcblxuICAgIGNvbnN0IHBhcnRpYWxseVVuc2V0OiBEZWVwVHlwZSA9IHsgc29tZXRoaW5nOiB7IH0gfTtcblxuICAgIGNvbnN0IGRlZXBFbXB0eSA9IE1heWJlLm9mKHBhcnRpYWxseVVuc2V0KVxuICAgICAgLmdldCgnc29tZXRoaW5nJylcbiAgICAgIC5nZXQoJ3dpdGgnKVxuICAgICAgLmdldCgnZGVlcGVyS2V5cycpO1xuXG4gICAgY29uc29sZS5sb2coZGVlcEVtcHR5KTsgLy8gTm90aGluZ1xuICAgIGBgYFxuICAgKi9cbiAgZ2V0PEsgZXh0ZW5kcyBrZXlvZiBUPih0aGlzOiBNYXliZTxUPiwga2V5OiBLKTogTWF5YmU8UmVxdWlyZWQ8VD5bS10+O1xufVxuXG4vKipcbiAgQSBgSnVzdGAgaW5zdGFuY2UgaXMgdGhlICpwcmVzZW50KiB2YXJpYW50IGluc3RhbmNlIG9mIHRoZVxuICBbYE1heWJlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWF5YmUpIHR5cGUsIHJlcHJlc2VudGluZyB0aGUgcHJlc2VuY2Ugb2YgYVxuICB2YWx1ZSB3aGljaCBtYXkgYmUgYWJzZW50LiBGb3IgYSBmdWxsIGRpc2N1c3Npb24sIHNlZSBbdGhlIG1vZHVsZVxuICBkb2NzXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCkuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIHdyYXBwZWQgaW4gdGhpcyBgSnVzdGAgdmFyaWFudCBvZiBgTWF5YmVgLlxuICovXG5leHBvcnQgY2xhc3MgSnVzdDxUPiBpbXBsZW1lbnRzIE1heWJlU2hhcGU8VD4ge1xuICAvKipcbiAgICBVbndyYXAgdGhlIGNvbnRhaW5lZCB2YWx1ZS4gQSBjb252ZW5pZW5jZSBtZXRob2QgZm9yIGZ1bmN0aW9uYWwgaWRpb21zLlxuXG4gICAgQSBjb21tb24gc2NlbmFyaW8gd2hlcmUgeW91IG1pZ2h0IHdhbnQgdG8gdXNlIHRoaXMgaXMgaW4gYSBwaXBlbGluZSBvZlxuICAgIGZ1bmN0aW9uczpcblxuICAgIGBgYHRzXG4gICAgaW1wb3J0IE1heWJlLCB7IEp1c3QgfSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gICAgZnVuY3Rpb24gZ2V0TGVuZ3RocyhtYXliZVN0cmluZ3M6IEFycmF5PE1heWJlPHN0cmluZz4+KTogQXJyYXk8bnVtYmVyPiB7XG4gICAgICByZXR1cm4gbWF5YmVTdHJpbmdzXG4gICAgICAgIC5maWx0ZXIoTWF5YmUuaXNKdXN0KVxuICAgICAgICAubWFwKEp1c3QudW53cmFwKVxuICAgICAgICAubWFwKHMgPT4gcy5sZW5ndGgpO1xuICAgIH1cbiAgICBgYGBcbiAgICovXG4gIHN0YXRpYyB1bndyYXA8Sj4odGhlSnVzdDogSnVzdDxKPik6IEoge1xuICAgIHJldHVybiB0aGVKdXN0LnZhbHVlO1xuICB9XG5cbiAgLyoqIGBKdXN0YCBpcyBhbHdheXMgW2BWYXJpYW50Lkp1c3RgXSguLi9lbnVtcy9fbWF5YmVfLnZhcmlhbnQjanVzdCkuICovXG4gIHJlYWRvbmx5IHZhcmlhbnQ6IFZhcmlhbnQuSnVzdCA9IFZhcmlhbnQuSnVzdDtcblxuICAvKiogVGhlIHdyYXBwZWQgdmFsdWUuICovXG4gIHJlYWRvbmx5IHZhbHVlOiBUO1xuXG4gIC8qKlxuICAgIENyZWF0ZSBhbiBpbnN0YW5jZSBvZiBgTWF5YmUuSnVzdGAgd2l0aCBgbmV3YC5cblxuICAgIEBub3RlIFdoaWxlIHlvdSAqbWF5KiBjcmVhdGUgdGhlIGBKdXN0YCB0eXBlIHZpYSBub3JtYWwgSmF2YVNjcmlwdFxuICAgIGNsYXNzIGNvbnN0cnVjdGlvbiwgaXQgaXMgbm90IHJlY29tbWVuZGVkIGZvciB0aGUgZnVuY3Rpb25hbCBzdHlsZSBmb3JcbiAgICB3aGljaCB0aGUgbGlicmFyeSBpcyBpbnRlbmRlZC4gSW5zdGVhZCwgdXNlIFtgTWF5YmUub2ZgXSAoZm9yIHRoZSBnZW5lcmFsXG4gICAgY2FzZSkgb3IgW2BNYXliZS5qdXN0YF0gZm9yIHRoaXMgc3BlY2lmaWMgY2FzZS5cblxuICAgIFtgTWF5YmUub2ZgXTogLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb2ZcbiAgICBbYE1heWJlLmp1c3RgXTogLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjanVzdFxuXG4gICAgYGBgdHNcbiAgICAvLyBBdm9pZDpcbiAgICBjb25zdCBhU3RyaW5nID0gbmV3IE1heWJlLkp1c3QoJ2NoYXJhY3RlcnMnKTtcblxuICAgIC8vIFByZWZlcjpcbiAgICBjb25zdCBhU3RyaW5nID0gTWF5YmUuanVzdCgnY2hhcmFjdGVycyk7XG4gICAgYGBgXG5cbiAgICBAcGFyYW0gdmFsdWVcbiAgICBUaGUgdmFsdWUgdG8gd3JhcCBpbiBhIGBNYXliZS5KdXN0YC5cblxuICAgIGBudWxsYCBhbmQgYHVuZGVmaW5lZGAgYXJlIGFsbG93ZWQgYnkgdGhlIHR5cGUgc2lnbmF0dXJlIHNvIHRoYXQgdGhlXG4gICAgY29uc3RydWN0b3IgbWF5IGB0aHJvd2Agb24gdGhvc2UgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gICAgYE1heWJlPHVuZGVmaW5lZD5gLlxuXG4gICAgQHRocm93cyAgICAgIElmIHlvdSBwYXNzIGBudWxsYCBvciBgdW5kZWZpbmVkYC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKHZhbHVlPzogVCB8IG51bGwpIHtcbiAgICBpZiAoaXNWb2lkKHZhbHVlKSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdUcmllZCB0byBjb25zdHJ1Y3QgYEp1c3RgIHdpdGggYG51bGxgIG9yIGB1bmRlZmluZWRgJyk7XG4gICAgfVxuXG4gICAgdGhpcy52YWx1ZSA9IHZhbHVlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmlzSnVzdGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2lzanVzdCkgKi9cbiAgaXNKdXN0KHRoaXM6IE1heWJlPFQ+KTogdGhpcyBpcyBKdXN0PFQ+IHtcbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5pc05vdGhpbmdgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNpc25vdGhpbmcpICovXG4gIGlzTm90aGluZyh0aGlzOiBNYXliZTxUPik6IHRoaXMgaXMgTm90aGluZzxUPiB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcCkgKi9cbiAgbWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBtYXBGbjogKHQ6IFQpID0+IFUpOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIG1hcChtYXBGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwT3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXBvcikgKi9cbiAgbWFwT3I8VT4odGhpczogTWF5YmU8VD4sIG9yVTogVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yKG9yVSwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcG9yZWxzZSkgKi9cbiAgbWFwT3JFbHNlPFU+KHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gVSwgbWFwRm46ICh0OiBUKSA9PiBVKTogVSB7XG4gICAgcmV0dXJuIG1hcE9yRWxzZShvckVsc2VGbiwgbWFwRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm1hdGNoYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWF0Y2gpICovXG4gIG1hdGNoPFU+KHRoaXM6IE1heWJlPFQ+LCBtYXRjaGVyOiBNYXRjaGVyPFQsIFU+KTogVSB7XG4gICAgcmV0dXJuIG1hdGNoKG1hdGNoZXIsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb3IpICovXG4gIG9yKHRoaXM6IE1heWJlPFQ+LCBtT3I6IE1heWJlPFQ+KTogTWF5YmU8VD4ge1xuICAgIHJldHVybiBvcihtT3IsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLm9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI29yZWxzZSkgKi9cbiAgb3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBvckVsc2VGbjogKCkgPT4gTWF5YmU8VD4pOiBNYXliZTxUPiB7XG4gICAgcmV0dXJuIG9yRWxzZShvckVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYW5kYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYW5kKSAqL1xuICBhbmQ8VT4odGhpczogTWF5YmU8VD4sIG1BbmQ6IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiBhbmQobUFuZCwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuYW5kVGhlbmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FuZHRoZW4pICovXG4gIGFuZFRoZW48VT4odGhpczogTWF5YmU8VD4sIGFuZFRoZW5GbjogKHQ6IFQpID0+IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiBhbmRUaGVuKGFuZFRoZW5GbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuY2hhaW5gXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNjaGFpbikgKi9cbiAgY2hhaW48VT4odGhpczogTWF5YmU8VD4sIGNoYWluRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gdGhpcy5hbmRUaGVuKGNoYWluRm4pO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmZsYXRNYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNmbGF0bWFwKSAqL1xuICBmbGF0TWFwPFU+KHRoaXM6IE1heWJlPFQ+LCBmbGF0TWFwRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gdGhpcy5hbmRUaGVuKGZsYXRNYXBGbik7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW5zYWZlbHlVbndyYXBgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bnNhZmVseXVud3JhcCkgKi9cbiAgdW5zYWZlbHlVbndyYXAoKTogVCB7XG4gICAgcmV0dXJuIHRoaXMudmFsdWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW53cmFwT3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bndyYXBvcikgKi9cbiAgdW53cmFwT3IodGhpczogTWF5YmU8VD4sIGRlZmF1bHRWYWx1ZTogVCk6IFQge1xuICAgIHJldHVybiB1bndyYXBPcihkZWZhdWx0VmFsdWUsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVud3JhcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Vud3JhcG9yZWxzZSkgKi9cbiAgdW53cmFwT3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBlbHNlRm46ICgpID0+IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3JFbHNlKGVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9Pa09yRXJyYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9va29yZXJyKSAqL1xuICB0b09rT3JFcnI8RT4odGhpczogTWF5YmU8VD4sIGVycm9yOiBFKTogUmVzdWx0PFQsIEU+IHtcbiAgICByZXR1cm4gdG9Pa09yRXJyKGVycm9yLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS50b09rT3JFbHNlRXJyYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9va29yZWxzZWVycikgKi9cbiAgdG9Pa09yRWxzZUVycjxFPih0aGlzOiBNYXliZTxUPiwgZWxzZUZuOiAoKSA9PiBFKTogUmVzdWx0PFQsIEU+IHtcbiAgICByZXR1cm4gdG9Pa09yRWxzZUVycihlbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvU3RyaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9zdHJpbmcpICovXG4gIHRvU3RyaW5nKHRoaXM6IE1heWJlPFQ+KTogc3RyaW5nIHtcbiAgICByZXR1cm4gdG9TdHJpbmcodGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuZXF1YWxzYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjZXF1YWxzKSAqL1xuICBlcXVhbHModGhpczogTWF5YmU8VD4sIGNvbXBhcmlzb246IE1heWJlPFQ+KTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGVxdWFscyhjb21wYXJpc29uLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FwKSAqL1xuICBhcDxBLCBCPih0aGlzOiBNYXliZTwodmFsOiBBKSA9PiBCPiwgdmFsOiBNYXliZTxBPik6IE1heWJlPEI+IHtcbiAgICByZXR1cm4gYXAodGhpcywgdmFsKTtcbiAgfVxuXG4gIC8qKlxuICAgIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmdldGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Byb3ApXG5cbiAgICAgICAgSWYgeW91IGhhdmUgYSBgTWF5YmVgIG9mIGFuIG9iamVjdCB0eXBlLCB5b3UgY2FuIGRvIGB0aGF0TWF5YmUuZ2V0KCdhIGtleScpYFxuICAgIHRvIGxvb2sgdXAgdGhlIG5leHQgbGF5ZXIgZG93biBpbiB0aGUgb2JqZWN0LlxuXG4gICAgYGBgdHNcbiAgICB0eXBlIERlZXBPcHRpb25hbFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc/OiB7XG4gICAgICAgIHdpdGg/OiB7XG4gICAgICAgICAgZGVlcGVyS2V5cz86IHN0cmluZztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH07XG5cbiAgICBjb25zdCBmdWxseVNldDogRGVlcFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc6IHtcbiAgICAgICAgd2l0aDoge1xuICAgICAgICAgIGRlZXBlcktleXM6ICdsaWtlIHRoaXMnXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgZGVlcEp1c3QgPSBNYXliZS5vZihmdWxseVNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBKdXN0KTsgLy8gSnVzdCgnbGlrZSB0aGlzJyk7XG5cbiAgICBjb25zdCBwYXJ0aWFsbHlVbnNldDogRGVlcFR5cGUgPSB7IHNvbWV0aGluZzogeyB9IH07XG5cbiAgICBjb25zdCBkZWVwRW1wdHkgPSBNYXliZS5vZihwYXJ0aWFsbHlVbnNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBFbXB0eSk7IC8vIE5vdGhpbmdcbiAgICBgYGBcbiAgICovXG4gIGdldDxLIGV4dGVuZHMga2V5b2YgVD4odGhpczogTWF5YmU8VD4sIGtleTogSyk6IE1heWJlPE5vbk51bGxhYmxlPFRbS10+PiB7XG4gICAgcmV0dXJuIHRoaXMuYW5kVGhlbihwcm9wZXJ0eShrZXkpKTtcbiAgfVxufVxuXG4vKipcbiAgQSBgTm90aGluZ2AgaW5zdGFuY2UgaXMgdGhlICphYnNlbnQqIHZhcmlhbnQgaW5zdGFuY2Ugb2YgdGhlXG4gIFtgTWF5YmVgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXliZSkgdHlwZSwgcmVwcmVzZW50aW5nIHRoZSBwcmVzZW5jZSBvZiBhXG4gIHZhbHVlIHdoaWNoIG1heSBiZSBhYnNlbnQuIEZvciBhIGZ1bGwgZGlzY3Vzc2lvbiwgc2VlIFt0aGUgbW9kdWxlXG4gIGRvY3NdKC4uL21vZHVsZXMvX21heWJlXy5odG1sKS5cblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgd2hpY2ggd291bGQgYmUgd3JhcHBlZCBpbiBhIGBKdXN0YCB2YXJpYW50IG9mIGBNYXliZWAuXG4gKi9cbmV4cG9ydCBjbGFzcyBOb3RoaW5nPFQ+IGltcGxlbWVudHMgTWF5YmVTaGFwZTxUPiB7XG4gIC8qKiBgTm90aGluZ2AgaXMgYWx3YXlzIFtgVmFyaWFudC5Ob3RoaW5nYF0oLi4vZW51bXMvX21heWJlXy52YXJpYW50I25vdGhpbmcpLiAqL1xuICByZWFkb25seSB2YXJpYW50OiBWYXJpYW50Lk5vdGhpbmcgPSBWYXJpYW50Lk5vdGhpbmc7XG5cbiAgLyoqXG4gICAgQ3JlYXRlIGFuIGluc3RhbmNlIG9mIGBNYXliZS5Ob3RoaW5nYCB3aXRoIGBuZXdgLlxuXG4gICAgQG5vdGUgV2hpbGUgeW91ICptYXkqIGNyZWF0ZSB0aGUgYE5vdGhpbmdgIHR5cGUgdmlhIG5vcm1hbCBKYXZhU2NyaXB0XG4gICAgY2xhc3MgY29uc3RydWN0aW9uLCBpdCBpcyBub3QgcmVjb21tZW5kZWQgZm9yIHRoZSBmdW5jdGlvbmFsIHN0eWxlIGZvclxuICAgIHdoaWNoIHRoZSBsaWJyYXJ5IGlzIGludGVuZGVkLiBJbnN0ZWFkLCB1c2UgW2BNYXliZS5vZmBdIChmb3IgdGhlIGdlbmVyYWxcbiAgICBjYXNlKSBvciBbYE1heWJlLm5vdGhpbmdgXSBmb3IgdGhpcyBzcGVjaWZpYyBjYXNlLlxuXG4gICAgW2BNYXliZS5vZmBdOiAuLi9tb2R1bGVzL19tYXliZV8uaHRtbCNvZlxuICAgIFtgTWF5YmUubm90aGluZ2BdOiAuLi9tb2R1bGVzL19tYXliZV8uaHRtbCNub3RoaW5nXG5cbiAgICBgYGB0c1xuICAgIC8vIEF2b2lkOlxuICAgIGNvbnN0IGFOb3RoaW5nID0gbmV3IE1heWJlLkVycigpO1xuXG4gICAgLy8gUHJlZmVyOlxuICAgIGNvbnN0IGFOb3RoaW5nID0gTWF5YmUubm90aGluZygpO1xuICAgIGBgYFxuXG4gICAgYG51bGxgIGFuZCBgdW5kZWZpbmVkYCBhcmUgYWxsb3dlZCBzbyB0aGF0IHlvdSBtYXkgZXhwbGljaXRseSBjb25zdHJ1Y3QgdGhlXG4gICAgYEVycmAgdHlwZSB3aXRoIGEga25vd24gYG51bGxgIG9yIGB1bmRlZmluZWRgIHZhbHVlLiAoVGhpcyBtYXliZSBoZWxwZnVsXG4gICAgcHJpbWFyaWx5IHdoZW4gdHJhbnNpdGlvbmluZyBhIGNvZGViYXNlIHRvIHRoZSB1c2Ugb2YgYE1heWJlYC4pXG5cbiAgICBAdGhyb3dzICAgICAgSWYgeW91IHBhc3MgYG51bGxgIG9yIGB1bmRlZmluZWRgLlxuICAgKi9cbiAgY29uc3RydWN0b3IoXz86IG51bGwpIHtcbiAgICAvKiBub3RoaW5nIHRvIGRvICovXG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuaXNKdXN0YF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjaXNqdXN0KSAqL1xuICBpc0p1c3QodGhpczogTWF5YmU8VD4pOiB0aGlzIGlzIEp1c3Q8VD4ge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5pc05vdGhpbmdgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNpc25vdGhpbmcpICovXG4gIGlzTm90aGluZyh0aGlzOiBNYXliZTxUPik6IHRoaXMgaXMgTm90aGluZzxUPiB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWFwKSAqL1xuICBtYXA8VT4odGhpczogTWF5YmU8VD4sIG1hcEZuOiAodDogVCkgPT4gVSk6IE1heWJlPFU+IHtcbiAgICByZXR1cm4gbWFwKG1hcEZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5tYXBPcmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI21hcG9yKSAqL1xuICBtYXBPcjxVPih0aGlzOiBNYXliZTxUPiwgb3JVOiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiBVIHtcbiAgICByZXR1cm4gbWFwT3Iob3JVLCBtYXBGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWFwT3JFbHNlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjbWFwb3JlbHNlKSAqL1xuICBtYXBPckVsc2U8VT4odGhpczogTWF5YmU8VD4sIG9yRWxzZUZuOiAoKSA9PiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiBVIHtcbiAgICByZXR1cm4gbWFwT3JFbHNlKG9yRWxzZUZuLCBtYXBGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUubWF0Y2hgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNtYXRjaCkgKi9cbiAgbWF0Y2g8VT4odGhpczogTWF5YmU8VD4sIG1hdGNoZXI6IE1hdGNoZXI8VCwgVT4pOiBVIHtcbiAgICByZXR1cm4gbWF0Y2gobWF0Y2hlciwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUub3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNvcikgKi9cbiAgb3IodGhpczogTWF5YmU8VD4sIG1PcjogTWF5YmU8VD4pOiBNYXliZTxUPiB7XG4gICAgcmV0dXJuIG9yKG1PciwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUub3JFbHNlYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjb3JlbHNlKSAqL1xuICBvckVsc2UodGhpczogTWF5YmU8VD4sIG9yRWxzZUZuOiAoKSA9PiBNYXliZTxUPik6IE1heWJlPFQ+IHtcbiAgICByZXR1cm4gb3JFbHNlKG9yRWxzZUZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hbmRgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCNhbmQpICovXG4gIGFuZDxVPih0aGlzOiBNYXliZTxUPiwgbUFuZDogTWF5YmU8VT4pOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIGFuZChtQW5kLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hbmRUaGVuYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjYW5kdGhlbikgKi9cbiAgYW5kVGhlbjxVPih0aGlzOiBNYXliZTxUPiwgYW5kVGhlbkZuOiAodDogVCkgPT4gTWF5YmU8VT4pOiBNYXliZTxVPiB7XG4gICAgcmV0dXJuIGFuZFRoZW4oYW5kVGhlbkZuLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5jaGFpbmBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2NoYWluKSAqL1xuICBjaGFpbjxVPih0aGlzOiBNYXliZTxUPiwgY2hhaW5GbjogKHQ6IFQpID0+IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiB0aGlzLmFuZFRoZW4oY2hhaW5Gbik7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuZmxhdE1hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2ZsYXRtYXApICovXG4gIGZsYXRNYXA8VT4odGhpczogTWF5YmU8VD4sIGZsYXRNYXBGbjogKHQ6IFQpID0+IE1heWJlPFU+KTogTWF5YmU8VT4ge1xuICAgIHJldHVybiB0aGlzLmFuZFRoZW4oZmxhdE1hcEZuKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS51bnNhZmVseVVud3JhcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Vuc2FmZWx5dW53cmFwKSAqL1xuICB1bnNhZmVseVVud3JhcCgpOiBuZXZlciB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCdUcmllZCB0byBgdW5zYWZlbHlVbndyYXAoTm90aGluZylgJyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudW53cmFwT3JgXSguLi9tb2R1bGVzL19tYXliZV8uaHRtbCN1bndyYXBvcikgKi9cbiAgdW53cmFwT3IodGhpczogTWF5YmU8VD4sIGRlZmF1bHRWYWx1ZTogVCk6IFQge1xuICAgIHJldHVybiB1bndyYXBPcihkZWZhdWx0VmFsdWUsIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnVud3JhcE9yRWxzZWBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Vud3JhcG9yZWxzZSkgKi9cbiAgdW53cmFwT3JFbHNlKHRoaXM6IE1heWJlPFQ+LCBlbHNlRm46ICgpID0+IFQpOiBUIHtcbiAgICByZXR1cm4gdW53cmFwT3JFbHNlKGVsc2VGbiwgdGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUudG9Pa09yRXJyYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9va29yZXJyKSAqL1xuICB0b09rT3JFcnI8RT4odGhpczogTWF5YmU8VD4sIGVycm9yOiBFKTogUmVzdWx0PFQsIEU+IHtcbiAgICByZXR1cm4gdG9Pa09yRXJyKGVycm9yLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS50b09rT3JFbHNlRXJyYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9va29yZWxzZWVycikgKi9cbiAgdG9Pa09yRWxzZUVycjxFPih0aGlzOiBNYXliZTxUPiwgZWxzZUZuOiAoKSA9PiBFKTogUmVzdWx0PFQsIEU+IHtcbiAgICByZXR1cm4gdG9Pa09yRWxzZUVycihlbHNlRm4sIHRoaXMpO1xuICB9XG5cbiAgLyoqIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLnRvU3RyaW5nYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjdG9zdHJpbmcpICovXG4gIHRvU3RyaW5nKHRoaXM6IE1heWJlPFQ+KTogc3RyaW5nIHtcbiAgICByZXR1cm4gdG9TdHJpbmcodGhpcyk7XG4gIH1cblxuICAvKiogTWV0aG9kIHZhcmlhbnQgZm9yIFtgTWF5YmUuZXF1YWxzYF0oLi4vbW9kdWxlcy9fbWF5YmVfLmh0bWwjZXF1YWxzKSAqL1xuICBlcXVhbHModGhpczogTWF5YmU8VD4sIGNvbXBhcmlzb246IE1heWJlPFQ+KTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGVxdWFscyhjb21wYXJpc29uLCB0aGlzKTtcbiAgfVxuXG4gIC8qKiBNZXRob2QgdmFyaWFudCBmb3IgW2BNYXliZS5hcGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI2FwKSAqL1xuICBhcDxBLCBCPih0aGlzOiBNYXliZTwodmFsOiBBKSA9PiBCPiwgdmFsOiBNYXliZTxBPik6IE1heWJlPEI+IHtcbiAgICByZXR1cm4gYXAodGhpcywgdmFsKTtcbiAgfVxuXG4gIC8qKlxuICAgIE1ldGhvZCB2YXJpYW50IGZvciBbYE1heWJlLmdldGBdKC4uL21vZHVsZXMvX21heWJlXy5odG1sI3Byb3ApXG5cbiAgICAgICAgSWYgeW91IGhhdmUgYSBgTWF5YmVgIG9mIGFuIG9iamVjdCB0eXBlLCB5b3UgY2FuIGRvIGB0aGF0TWF5YmUuZ2V0KCdhIGtleScpYFxuICAgIHRvIGxvb2sgdXAgdGhlIG5leHQgbGF5ZXIgZG93biBpbiB0aGUgb2JqZWN0LlxuXG4gICAgYGBgdHNcbiAgICB0eXBlIERlZXBPcHRpb25hbFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc/OiB7XG4gICAgICAgIHdpdGg/OiB7XG4gICAgICAgICAgZGVlcGVyS2V5cz86IHN0cmluZztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH07XG5cbiAgICBjb25zdCBmdWxseVNldDogRGVlcFR5cGUgPSB7XG4gICAgICBzb21ldGhpbmc6IHtcbiAgICAgICAgd2l0aDoge1xuICAgICAgICAgIGRlZXBlcktleXM6ICdsaWtlIHRoaXMnXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgZGVlcEp1c3QgPSBNYXliZS5vZihmdWxseVNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBKdXN0KTsgLy8gSnVzdCgnbGlrZSB0aGlzJyk7XG5cbiAgICBjb25zdCBwYXJ0aWFsbHlVbnNldDogRGVlcFR5cGUgPSB7IHNvbWV0aGluZzogeyB9IH07XG5cbiAgICBjb25zdCBkZWVwRW1wdHkgPSBNYXliZS5vZihwYXJ0aWFsbHlVbnNldClcbiAgICAgIC5nZXQoJ3NvbWV0aGluZycpXG4gICAgICAuZ2V0KCd3aXRoJylcbiAgICAgIC5nZXQoJ2RlZXBlcktleXMnKTtcblxuICAgIGNvbnNvbGUubG9nKGRlZXBFbXB0eSk7IC8vIE5vdGhpbmdcbiAgICBgYGBcbiAgICovXG4gIGdldDxLIGV4dGVuZHMga2V5b2YgVD4odGhpczogTWF5YmU8VD4sIGtleTogSyk6IE1heWJlPE5vbk51bGxhYmxlPFRbS10+PiB7XG4gICAgcmV0dXJuIHRoaXMuYW5kVGhlbihwcm9wZXJ0eShrZXkpKTtcbiAgfVxufVxuXG4vKipcbiAgSXMgdGhpcyByZXN1bHQgYSBgSnVzdGAgaW5zdGFuY2U/XG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAcGFyYW0gbWF5YmUgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gY2hlY2suXG4gIEByZXR1cm5zICAgICBgdHJ1ZWAgaWYgYG1heWJlYCBpcyBgSnVzdGAsIGBmYWxzZWAgb3RoZXJ3aXNlLiBJbiBUeXBlU2NyaXB0LFxuICAgICAgICAgICAgICAgYWxzbyBuYXJyb3dzIHRoZSB0eXBlIGZyb20gYE1heWJlPFQ+YCB0byBgSnVzdDxUPmAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBpc0p1c3Q8VD4obWF5YmU6IE1heWJlPFQ+KTogbWF5YmUgaXMgSnVzdDxUPiB7XG4gIHJldHVybiBtYXliZS52YXJpYW50ID09PSBWYXJpYW50Lkp1c3Q7XG59XG5cbi8qKlxuICBJcyB0aGlzIHJlc3VsdCBhIGBOb3RoaW5nYCBpbnN0YW5jZT9cblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBtYXliZSBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBjaGVjay5cbiAgQHJldHVybnMgICAgIGB0cnVlYCBpZiBgbWF5YmVgIGlzIGBub3RoaW5nYCwgYGZhbHNlYCBvdGhlcndpc2UuIEluIFR5cGVTY3JpcHQsXG4gICAgICAgICAgICAgICBhbHNvIG5hcnJvd3MgdGhlIHR5cGUgZnJvbSBgTWF5YmU8VD5gIHRvIGBOb3RoaW5nPFQ+YC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzTm90aGluZzxUPihtYXliZTogTWF5YmU8VD4pOiBtYXliZSBpcyBOb3RoaW5nPFQ+IHtcbiAgcmV0dXJuIG1heWJlLnZhcmlhbnQgPT09IFZhcmlhbnQuTm90aGluZztcbn1cblxuLyoqXG4gIENyZWF0ZSBhbiBpbnN0YW5jZSBvZiBgTWF5YmUuSnVzdGAuXG5cbiAgYG51bGxgIGFuZCBgdW5kZWZpbmVkYCBhcmUgYWxsb3dlZCBieSB0aGUgdHlwZSBzaWduYXR1cmUgc28gdGhhdCB0aGVcbiAgZnVuY3Rpb24gbWF5IGB0aHJvd2Agb24gdGhvc2UgcmF0aGVyIHRoYW4gY29uc3RydWN0aW5nIGEgdHlwZSBsaWtlXG4gIGBNYXliZTx1bmRlZmluZWQ+YC5cblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIGl0ZW0gY29udGFpbmVkIGluIHRoZSBgTWF5YmVgLlxuICBAcGFyYW0gdmFsdWUgVGhlIHZhbHVlIHRvIHdyYXAgaW4gYSBgTWF5YmUuSnVzdGAuXG4gIEByZXR1cm5zICAgICBBbiBpbnN0YW5jZSBvZiBgTWF5YmUuSnVzdDxUPmAuXG4gIEB0aHJvd3MgICAgICBJZiB5b3UgcGFzcyBgbnVsbGAgb3IgYHVuZGVmaW5lZGAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBqdXN0PFQ+KHZhbHVlPzogVCB8IG51bGwpOiBNYXliZTxUPiB7XG4gIHJldHVybiBuZXcgSnVzdDxUPih2YWx1ZSk7XG59XG5cbi8qKlxuICBDcmVhdGUgYW4gaW5zdGFuY2Ugb2YgYE1heWJlLk5vdGhpbmdgLlxuXG4gIElmIHlvdSB3YW50IHRvIGNyZWF0ZSBhbiBpbnN0YW5jZSB3aXRoIGEgc3BlY2lmaWMgdHlwZSwgZS5nLiBmb3IgdXNlIGluIGFcbiAgZnVuY3Rpb24gd2hpY2ggZXhwZWN0cyBhIGBNYXliZTxUPmAgd2hlcmUgdGhlIGA8VD5gIGlzIGtub3duIGJ1dCB5b3UgaGF2ZSBub1xuICB2YWx1ZSB0byBnaXZlIGl0LCB5b3UgY2FuIHVzZSBhIHR5cGUgcGFyYW1ldGVyOlxuXG4gIGBgYHRzXG4gIGNvbnN0IG5vdFN0cmluZyA9IE1heWJlLm5vdGhpbmc8c3RyaW5nPigpO1xuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIGl0ZW0gY29udGFpbmVkIGluIHRoZSBgTWF5YmVgLlxuICBAcmV0dXJucyAgICAgQW4gaW5zdGFuY2Ugb2YgYE1heWJlLk5vdGhpbmc8VD5gLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbm90aGluZzxUPihfPzogbnVsbCk6IE1heWJlPFQ+IHtcbiAgcmV0dXJuIG5ldyBOb3RoaW5nPFQ+KF8pO1xufVxuXG4vKipcbiAgQ3JlYXRlIGEgYE1heWJlYCBmcm9tIGFueSB2YWx1ZS5cblxuICBUbyBzcGVjaWZ5IHRoYXQgdGhlIHJlc3VsdCBzaG91bGQgYmUgaW50ZXJwcmV0ZWQgYXMgYSBzcGVjaWZpYyB0eXBlLCB5b3UgbWF5XG4gIGludm9rZSBgTWF5YmUub2ZgIHdpdGggYW4gZXhwbGljaXQgdHlwZSBwYXJhbWV0ZXI6XG5cbiAgYGBgdHNcbiAgY29uc3QgZm9vID0gTWF5YmUub2Y8c3RyaW5nPihudWxsKTtcbiAgYGBgXG5cbiAgVGhpcyBpcyB1c3VhbGx5IG9ubHkgaW1wb3J0YW50IGluIHR3byBjYXNlczpcblxuICAxLiAgSWYgeW91IGFyZSBpbnRlbnRpb25hbGx5IGNvbnN0cnVjdGluZyBhIGBOb3RoaW5nYCBmcm9tIGEga25vd24gYG51bGxgIG9yXG4gICAgICB1bmRlZmluZWQgdmFsdWUgKndoaWNoIGlzIHVudHlwZWQqLlxuICAyLiAgSWYgeW91IGFyZSBzcGVjaWZ5aW5nIHRoYXQgdGhlIHR5cGUgaXMgbW9yZSBnZW5lcmFsIHRoYW4gdGhlIHZhbHVlIHBhc3NlZFxuICAgICAgKHNpbmNlIFR5cGVTY3JpcHQgY2FuIGRlZmluZSB0eXBlcyBhcyBsaXRlcmFscykuXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSBpdGVtIGNvbnRhaW5lZCBpbiB0aGUgYE1heWJlYC5cbiAgQHBhcmFtIHZhbHVlIFRoZSB2YWx1ZSB0byB3cmFwIGluIGEgYE1heWJlYC4gSWYgaXQgaXMgYHVuZGVmaW5lZGAgb3IgYG51bGxgLFxuICAgICAgICAgICAgICAgdGhlIHJlc3VsdCB3aWxsIGJlIGBOb3RoaW5nYDsgb3RoZXJ3aXNlIGl0IHdpbGwgYmUgdGhlIHR5cGUgb2ZcbiAgICAgICAgICAgICAgIHRoZSB2YWx1ZSBwYXNzZWQuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBvZjxUPih2YWx1ZT86IFQgfCBudWxsKTogTWF5YmU8VD4ge1xuICByZXR1cm4gaXNWb2lkKHZhbHVlKSA/IG5vdGhpbmc8VD4oKSA6IGp1c3QodmFsdWUpO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgb2ZgXSgjb2YpLCBwcmltYXJpbHkgZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBGb2xrdGFsZS4gKi9cbmV4cG9ydCBjb25zdCBmcm9tTnVsbGFibGUgPSBvZjtcblxuLyoqXG4gIE1hcCBvdmVyIGEgYE1heWJlYCBpbnN0YW5jZTogYXBwbHkgdGhlIGZ1bmN0aW9uIHRvIHRoZSB3cmFwcGVkIHZhbHVlIGlmIHRoZVxuICBpbnN0YW5jZSBpcyBgSnVzdGAsIGFuZCByZXR1cm4gYE5vdGhpbmdgIGlmIHRoZSBpbnN0YW5jZSBpcyBgTm90aGluZ2AuXG5cbiAgYE1heWJlLm1hcGAgd29ya3MgYSBsb3QgbGlrZSBgQXJyYXkucHJvdG90eXBlLm1hcGA6IGBNYXliZWAgYW5kIGBBcnJheWAgYXJlXG4gIGJvdGggKmNvbnRhaW5lcnMqIGZvciBvdGhlciB0aGluZ3MuIElmIHlvdSBoYXZlIG5vIGl0ZW1zIGluIGFuIGFycmF5IG9mXG4gIG51bWJlcnMgbmFtZWQgYGZvb2AgYW5kIGNhbGwgYGZvby5tYXAoeCA9PiB4ICsgMSlgLCB5b3UnbGwgc3RpbGwganVzdCBoYXZlIGFuXG4gIGFycmF5IHdpdGggbm90aGluZyBpbiBpdC4gQnV0IGlmIHlvdSBoYXZlIGFueSBpdGVtcyBpbiB0aGUgYXJyYXkgKGBbMiwgM11gKSxcbiAgYW5kIHlvdSBjYWxsIGBmb28ubWFwKHggPT4geCArIDEpYCBvbiBpdCwgeW91J2xsIGdldCBhIG5ldyBhcnJheSB3aXRoIGVhY2ggb2ZcbiAgdGhvc2UgaXRlbXMgaW5zaWRlIHRoZSBhcnJheSBcImNvbnRhaW5lclwiIHRyYW5zZm9ybWVkIChgWzMsIDRdYCkuXG5cbiAgVGhhdCdzIGV4YWN0bHkgd2hhdCdzIGhhcHBlbmluZyB3aXRoIGBNYXliZS5tYXBgLiBJZiB0aGUgY29udGFpbmVyIGlzICplbXB0eSpcbiAg4oCTwqB0aGUgYE5vdGhpbmdgIHZhcmlhbnQg4oCTIHlvdSBqdXN0IGdldCBiYWNrIGFuIGVtcHR5IGNvbnRhaW5lci4gSWYgdGhlXG4gIGNvbnRhaW5lciBoYXMgc29tZXRoaW5nIGluIGl0IOKAk8KgdGhlIGBKdXN0YCB2YXJpYW50IOKAk8KgeW91IGdldCBiYWNrIGEgY29udGFpbmVyXG4gIHdpdGggdGhlIGl0ZW0gaW5zaWRlIHRyYW5zZm9ybWVkLlxuXG4gIChTby4uLiB3aHkgbm90IGp1c3QgdXNlIGFuIGFycmF5PyBUaGUgYmlnZ2VzdCByZWFzb24gaXMgdGhhdCBhbiBhcnJheSBjYW4gYmVcbiAgYW55IGxlbmd0aC4gV2l0aCBhIGBNYXliZWAsIHdlJ3JlIGNhcHR1cmluZyB0aGUgaWRlYSBvZiBcInNvbWV0aGluZyBvclxuICBub3RoaW5nXCIgcmF0aGVyIHRoYW4gXCIwIHRvIG5cIiBpdGVtcy4gQW5kIHRoaXMgbGV0cyB1cyBpbXBsZW1lbnQgYSB3aG9sZSBzZXRcbiAgb2YgKm90aGVyKiBpbnRlcmZhY2VzLCBsaWtlIHRob3NlIGluIHRoaXMgbW9kdWxlLilcblxuICAjIyMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgY29uc3QgbGVuZ3RoID0gKHM6IHN0cmluZykgPT4gcy5sZW5ndGg7XG5cbiAgY29uc3QganVzdEFTdHJpbmcgPSBNYXliZS5qdXN0KCdzdHJpbmcnKTtcbiAgY29uc3QganVzdFRoZVN0cmluZ0xlbmd0aCA9IG1hcChsZW5ndGgsIGp1c3RBU3RyaW5nKTtcbiAgY29uc29sZS5sb2coanVzdFRoZVN0cmluZ0xlbmd0aC50b1N0cmluZygpKTsgLy8gSnVzdCg2KVxuXG4gIGNvbnN0IG5vdEFTdHJpbmcgPSBNYXliZS5ub3RoaW5nPHN0cmluZz4oKTtcbiAgY29uc3Qgbm90QVN0cmluZ0xlbmd0aCA9IG1hcChsZW5ndGgsIG5vdEFTdHJpbmcpO1xuICBjb25zb2xlLmxvZyhub3RBU3RyaW5nTGVuZ3RoLnRvU3RyaW5nKCkpOyAvLyBcIk5vdGhpbmdcIlxuICBgYGBcblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEB0eXBlcGFyYW0gVSBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZSBvZiB0aGUgcmV0dXJuZWQgYE1heWJlYC5cbiAgQHBhcmFtIG1hcEZuIFRoZSBmdW5jdGlvbiB0byBhcHBseSB0aGUgdmFsdWUgdG8gaWYgYE1heWJlYCBpcyBgSnVzdGAuXG4gIEBwYXJhbSBtYXliZSBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBtYXAgb3Zlci5cbiAgQHJldHVybnMgICAgIEEgbmV3IGBNYXliZWAgd2l0aCB0aGUgcmVzdWx0IG9mIGFwcGx5aW5nIGBtYXBGbmAgdG8gdGhlIHZhbHVlXG4gICAgICAgICAgICAgICBpbiBhIGBKdXN0YCwgb3IgYE5vdGhpbmdgIGlmIGBtYXliZWAgaXMgYE5vdGhpbmdgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWFwPFQsIFU+KG1hcEZuOiAodDogVCkgPT4gVSk6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIG1hcDxULCBVPihtYXBGbjogKHQ6IFQpID0+IFUsIG1heWJlOiBNYXliZTxUPik6IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIG1hcDxULCBVPihcbiAgbWFwRm46ICh0OiBUKSA9PiBVLFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBNYXliZTxVPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyBqdXN0KG1hcEZuKG0udmFsdWUpKSA6IG5vdGhpbmc8VT4oKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIG1heWJlKTtcbn1cblxuLyoqXG4gIE1hcCBvdmVyIGEgYE1heWJlYCBpbnN0YW5jZSBhbmQgZ2V0IG91dCB0aGUgdmFsdWUgaWYgYG1heWJlYCBpcyBhIGBKdXN0YCwgb3JcbiAgcmV0dXJuIGEgZGVmYXVsdCB2YWx1ZSBpZiBgbWF5YmVgIGlzIGEgYE5vdGhpbmdgLlxuXG4gICMjIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBjb25zdCBsZW5ndGggPSAoczogc3RyaW5nKSA9PiBzLmxlbmd0aDtcblxuICBjb25zdCBqdXN0QVN0cmluZyA9IE1heWJlLmp1c3QoJ3N0cmluZycpO1xuICBjb25zdCB0aGVTdHJpbmdMZW5ndGggPSBtYXBPcigwLCBsZW5ndGgsIGp1c3RBU3RyaW5nKTtcbiAgY29uc29sZS5sb2codGhlU3RyaW5nTGVuZ3RoKTsgLy8gNlxuXG4gIGNvbnN0IG5vdEFTdHJpbmcgPSBNYXliZS5ub3RoaW5nPHN0cmluZz4oKTtcbiAgY29uc3Qgbm90QVN0cmluZ0xlbmd0aCA9IG1hcE9yKDAsIGxlbmd0aCwgbm90QVN0cmluZylcbiAgY29uc29sZS5sb2cobm90QVN0cmluZ0xlbmd0aCk7IC8vIDBcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIFUgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUgb2YgdGhlIHJldHVybmVkIGBNYXliZWAuXG4gIEBwYXJhbSBvclUgICBUaGUgZGVmYXVsdCB2YWx1ZSB0byB1c2UgaWYgYG1heWJlYCBpcyBgTm90aGluZ2BcbiAgQHBhcmFtIG1hcEZuIFRoZSBmdW5jdGlvbiB0byBhcHBseSB0aGUgdmFsdWUgdG8gaWYgYE1heWJlYCBpcyBgSnVzdGBcbiAgQHBhcmFtIG1heWJlIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIG1hcCBvdmVyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWFwT3I8VCwgVT4ob3JVOiBVLCBtYXBGbjogKHQ6IFQpID0+IFUsIG1heWJlOiBNYXliZTxUPik6IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3I8VCwgVT4ob3JVOiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yPFQsIFU+KG9yVTogVSk6IChtYXBGbjogKHQ6IFQpID0+IFUpID0+IChtYXliZTogTWF5YmU8VD4pID0+IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3I8VCwgVT4oXG4gIG9yVTogVSxcbiAgbWFwRm4/OiAodDogVCkgPT4gVSxcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogVSB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB8ICgobWFwRm46ICh0OiBUKSA9PiBVKSA9PiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB7XG4gIGZ1bmN0aW9uIGZ1bGxPcChmbjogKHQ6IFQpID0+IFUsIG06IE1heWJlPFQ+KSB7XG4gICAgcmV0dXJuIG0uaXNKdXN0KCkgPyBmbihtLnZhbHVlKSA6IG9yVTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHBhcnRpYWxPcChmbjogKHQ6IFQpID0+IFUpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVO1xuICBmdW5jdGlvbiBwYXJ0aWFsT3AoZm46ICh0OiBUKSA9PiBVLCBjdXJyaWVkTWF5YmU6IE1heWJlPFQ+KTogVTtcbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSwgY3VycmllZE1heWJlPzogTWF5YmU8VD4pOiBVIHwgKChtYXliZTogTWF5YmU8VD4pID0+IFUpIHtcbiAgICByZXR1cm4gY3VycmllZE1heWJlICE9PSB1bmRlZmluZWRcbiAgICAgID8gZnVsbE9wKGZuLCBjdXJyaWVkTWF5YmUpXG4gICAgICA6IChleHRyYUN1cnJpZWRNYXliZTogTWF5YmU8VD4pID0+IGZ1bGxPcChmbiwgZXh0cmFDdXJyaWVkTWF5YmUpO1xuICB9XG5cbiAgcmV0dXJuIG1hcEZuID09PSB1bmRlZmluZWRcbiAgICA/IHBhcnRpYWxPcFxuICAgIDogbWF5YmUgPT09IHVuZGVmaW5lZFxuICAgICAgPyBwYXJ0aWFsT3AobWFwRm4pXG4gICAgICA6IHBhcnRpYWxPcChtYXBGbiwgbWF5YmUpO1xufVxuXG4vKipcbiAgTWFwIG92ZXIgYSBgTWF5YmVgIGluc3RhbmNlIGFuZCBnZXQgb3V0IHRoZSB2YWx1ZSBpZiBgbWF5YmVgIGlzIGEgYEp1c3RgLFxuICBvciB1c2UgYSBmdW5jdGlvbiB0byBjb25zdHJ1Y3QgYSBkZWZhdWx0IHZhbHVlIGlmIGBtYXliZWAgaXMgYE5vdGhpbmdgLlxuXG4gICMjIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBjb25zdCBsZW5ndGggPSAoczogc3RyaW5nKSA9PiBzLmxlbmd0aDtcbiAgY29uc3QgZ2V0RGVmYXVsdCA9ICgpID0+IDA7XG5cbiAgY29uc3QganVzdEFTdHJpbmcgPSBNYXliZS5qdXN0KCdzdHJpbmcnKTtcbiAgY29uc3QgdGhlU3RyaW5nTGVuZ3RoID0gbWFwT3JFbHNlKGdldERlZmF1bHQsIGxlbmd0aCwganVzdEFTdHJpbmcpO1xuICBjb25zb2xlLmxvZyh0aGVTdHJpbmdMZW5ndGgpOyAvLyA2XG5cbiAgY29uc3Qgbm90QVN0cmluZyA9IE1heWJlLm5vdGhpbmc8c3RyaW5nPigpO1xuICBjb25zdCBub3RBU3RyaW5nTGVuZ3RoID0gbWFwT3JFbHNlKGdldERlZmF1bHQsIGxlbmd0aCwgbm90QVN0cmluZylcbiAgY29uc29sZS5sb2cobm90QVN0cmluZ0xlbmd0aCk7IC8vIDBcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUICAgIFRoZSB0eXBlIG9mIHRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIFUgICAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUgb2YgdGhlIHJldHVybmVkIGBNYXliZWAuXG4gIEBwYXJhbSBvckVsc2VGbiBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgaWYgYG1heWJlYCBpcyBgTm90aGluZ2AuXG4gIEBwYXJhbSBtYXBGbiAgICBUaGUgZnVuY3Rpb24gdG8gYXBwbHkgdG8gdGhlIHdyYXBwZWQgdmFsdWUgaWYgYG1heWJlYCBpcyBgSnVzdGBcbiAgQHBhcmFtIG1heWJlICAgIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIG1hcCBvdmVyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWFwT3JFbHNlPFQsIFU+KG9yRWxzZUZuOiAoKSA9PiBVLCBtYXBGbjogKHQ6IFQpID0+IFUsIG1heWJlOiBNYXliZTxUPik6IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3JFbHNlPFQsIFU+KG9yRWxzZUZuOiAoKSA9PiBVLCBtYXBGbjogKHQ6IFQpID0+IFUpOiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVO1xuZXhwb3J0IGZ1bmN0aW9uIG1hcE9yRWxzZTxULCBVPihvckVsc2VGbjogKCkgPT4gVSk6IChtYXBGbjogKHQ6IFQpID0+IFUpID0+IChtYXliZTogTWF5YmU8VD4pID0+IFU7XG5leHBvcnQgZnVuY3Rpb24gbWFwT3JFbHNlPFQsIFU+KFxuICBvckVsc2VGbjogKCkgPT4gVSxcbiAgbWFwRm4/OiAodDogVCkgPT4gVSxcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogVSB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB8ICgobWFwRm46ICh0OiBUKSA9PiBVKSA9PiAobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB7XG4gIGZ1bmN0aW9uIGZ1bGxPcChmbjogKHQ6IFQpID0+IFUsIG06IE1heWJlPFQ+KSB7XG4gICAgcmV0dXJuIG0uaXNKdXN0KCkgPyBmbihtLnZhbHVlKSA6IG9yRWxzZUZuKCk7XG4gIH1cblxuICBmdW5jdGlvbiBwYXJ0aWFsT3AoZm46ICh0OiBUKSA9PiBVKTogKG1heWJlOiBNYXliZTxUPikgPT4gVTtcbiAgZnVuY3Rpb24gcGFydGlhbE9wKGZuOiAodDogVCkgPT4gVSwgY3VycmllZE1heWJlOiBNYXliZTxUPik6IFU7XG4gIGZ1bmN0aW9uIHBhcnRpYWxPcChmbjogKHQ6IFQpID0+IFUsIGN1cnJpZWRNYXliZT86IE1heWJlPFQ+KTogVSB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBVKSB7XG4gICAgcmV0dXJuIGN1cnJpZWRNYXliZSAhPT0gdW5kZWZpbmVkXG4gICAgICA/IGZ1bGxPcChmbiwgY3VycmllZE1heWJlKVxuICAgICAgOiAoZXh0cmFDdXJyaWVkTWF5YmU6IE1heWJlPFQ+KSA9PiBmdWxsT3AoZm4sIGV4dHJhQ3VycmllZE1heWJlKTtcbiAgfVxuXG4gIGlmIChtYXBGbiA9PT0gdW5kZWZpbmVkKSB7XG4gICAgcmV0dXJuIHBhcnRpYWxPcDtcbiAgfSBlbHNlIGlmIChtYXliZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgcmV0dXJuIHBhcnRpYWxPcChtYXBGbik7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHBhcnRpYWxPcChtYXBGbiwgbWF5YmUpO1xuICB9XG59XG5cbi8qKlxuICBZb3UgY2FuIHRoaW5rIG9mIHRoaXMgbGlrZSBhIHNob3J0LWNpcmN1aXRpbmcgbG9naWNhbCBcImFuZFwiIG9wZXJhdGlvbiBvbiBhXG4gIGBNYXliZWAgdHlwZS4gSWYgYG1heWJlYCBpcyBgSnVzdGAsIHRoZW4gdGhlIHJlc3VsdCBpcyB0aGUgYGFuZE1heWJlYC4gSWZcbiAgYG1heWJlYCBpcyBgTm90aGluZ2AsIHRoZSByZXN1bHQgaXMgYE5vdGhpbmdgLlxuXG4gIFRoaXMgaXMgdXNlZnVsIHdoZW4geW91IGhhdmUgYW5vdGhlciBgTWF5YmVgIHZhbHVlIHlvdSB3YW50IHRvIHByb3ZpZGUgaWYgYW5kXG4gICpvbmx5IGlmKiB5b3UgaGF2ZSBhIGBKdXN0YCDigJMgdGhhdCBpcywgd2hlbiB5b3UgbmVlZCB0byBtYWtlIHN1cmUgdGhhdCBpZiB5b3VcbiAgYE5vdGhpbmdgLCB3aGF0ZXZlciBlbHNlIHlvdSdyZSBoYW5kaW5nIGEgYE1heWJlYCB0byAqYWxzbyogZ2V0cyBhIGBOb3RoaW5nYC5cblxuICBOb3RpY2UgdGhhdCwgdW5saWtlIGluIFtgbWFwYF0oI21hcCkgb3IgaXRzIHZhcmlhbnRzLCB0aGUgb3JpZ2luYWwgYG1heWJlYCBpc1xuICBub3QgaW52b2x2ZWQgaW4gY29uc3RydWN0aW5nIHRoZSBuZXcgYE1heWJlYC5cblxuICAjIyMjIEV4YW1wbGVzXG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgY29uc3QganVzdEEgPSBNYXliZS5qdXN0KCdBJyk7XG4gIGNvbnN0IGp1c3RCID0gTWF5YmUuanVzdCgnQicpO1xuICBjb25zdCBub3RoaW5nOiBNYXliZTxudW1iZXI+ID0gbm90aGluZygpO1xuXG4gIGNvbnNvbGUubG9nKE1heWJlLmFuZChqdXN0QiwganVzdEEpLnRvU3RyaW5nKCkpOyAgLy8gSnVzdChCKVxuICBjb25zb2xlLmxvZyhNYXliZS5hbmQoanVzdEIsIG5vdGhpbmcpLnRvU3RyaW5nKCkpOyAgLy8gTm90aGluZ1xuICBjb25zb2xlLmxvZyhNYXliZS5hbmQobm90aGluZywganVzdEEpLnRvU3RyaW5nKCkpOyAgLy8gTm90aGluZ1xuICBjb25zb2xlLmxvZyhNYXliZS5hbmQobm90aGluZywgbm90aGluZykudG9TdHJpbmcoKSk7ICAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgICBUaGUgdHlwZSBvZiB0aGUgaW5pdGlhbCB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIFUgICAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUgb2YgdGhlIHJldHVybmVkIGBNYXliZWAuXG4gIEBwYXJhbSBhbmRNYXliZSBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byByZXR1cm4gaWYgYG1heWJlYCBpcyBgSnVzdGBcbiAgQHBhcmFtIG1heWJlICAgIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIGNoZWNrLlxuICBAcmV0dXJuICAgICAgICAgYE5vdGhpbmdgIGlmIHRoZSBvcmlnaW5hbCBgbWF5YmVgIGlzIGBOb3RoaW5nYCwgb3IgYGFuZE1heWJlYFxuICAgICAgICAgICAgICAgICAgaWYgdGhlIG9yaWdpbmFsIGBtYXliZWAgaXMgYEp1c3RgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYW5kPFQsIFU+KGFuZE1heWJlOiBNYXliZTxVPiwgbWF5YmU6IE1heWJlPFQ+KTogTWF5YmU8VT47XG5leHBvcnQgZnVuY3Rpb24gYW5kPFQsIFU+KGFuZE1heWJlOiBNYXliZTxVPik6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFuZDxULCBVPihcbiAgYW5kTWF5YmU6IE1heWJlPFU+LFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBNYXliZTxVPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyBhbmRNYXliZSA6IG5vdGhpbmc8VT4oKSk7XG4gIHJldHVybiBjdXJyeTEob3AsIG1heWJlKTtcbn1cblxuLyoqXG4gIEFwcGx5IGEgZnVuY3Rpb24gdG8gdGhlIHdyYXBwZWQgdmFsdWUgaWYgYEp1c3RgIGFuZCByZXR1cm4gYSBuZXcgYEp1c3RgXG4gIGNvbnRhaW5pbmcgdGhlIHJlc3VsdGluZyB2YWx1ZTsgb3IgcmV0dXJuIGBOb3RoaW5nYCBpZiBgTm90aGluZ2AuXG5cbiAgVGhpcyBkaWZmZXJzIGZyb20gYG1hcGAgaW4gdGhhdCBgdGhlbkZuYCByZXR1cm5zIGFub3RoZXIgYE1heWJlYC4gWW91IGNhbiB1c2VcbiAgYGFuZFRoZW5gIHRvIGNvbWJpbmUgdHdvIGZ1bmN0aW9ucyB3aGljaCAqYm90aCogY3JlYXRlIGEgYE1heWJlYCBmcm9tIGFuXG4gIHVud3JhcHBlZCB0eXBlLlxuXG4gIFlvdSBtYXkgZmluZCB0aGUgYC50aGVuYCBtZXRob2Qgb24gYW4gRVM2IGBQcm9taXNlYCBoZWxwZnVsIGZvciBiOlxuICBpZiB5b3UgaGF2ZSBhIGBQcm9taXNlYCwgeW91IGNhbiBwYXNzIGl0cyBgdGhlbmAgbWV0aG9kIGEgY2FsbGJhY2sgd2hpY2hcbiAgcmV0dXJucyBhbm90aGVyIGBQcm9taXNlYCwgYW5kIHRoZSByZXN1bHQgd2lsbCBub3QgYmUgYSAqbmVzdGVkKiBwcm9taXNlLCBidXRcbiAgYSBzaW5nbGUgYFByb21pc2VgLiBUaGUgZGlmZmVyZW5jZSBpcyB0aGF0IGBQcm9taXNlI3RoZW5gIHVud3JhcHMgKmFsbCpcbiAgbGF5ZXJzIHRvIG9ubHkgZXZlciByZXR1cm4gYSBzaW5nbGUgYFByb21pc2VgIHZhbHVlLCB3aGVyZWFzIGBNYXliZS5hbmRUaGVuYFxuICB3aWxsIG5vdCB1bndyYXAgbmVzdGVkIGBNYXliZWBzLlxuXG4gIFRoaXMgaXMgYWxzbyBjb21tb25seSBrbm93biBhcyAoYW5kIHRoZXJlZm9yZSBhbGlhc2VkIGFzKSBbYGZsYXRNYXBgXSBvclxuICBbYGNoYWluYF0uIEl0IGlzIHNvbWV0aW1lcyBhbHNvIGtub3duIGFzIGBiaW5kYCwgYnV0ICpub3QqIGFsaWFzZWQgYXMgc3VjaFxuICBiZWNhdXNlIFtgYmluZGAgYWxyZWFkeSBtZWFucyBzb21ldGhpbmcgaW4gSmF2YVNjcmlwdF1bYmluZF0uXG5cbiAgW2BmbGF0TWFwYF06ICNmbGF0bWFwXG4gIFtgY2hhaW5gXTogI2NoYWluXG4gIFtiaW5kXTogaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvSmF2YVNjcmlwdC9SZWZlcmVuY2UvR2xvYmFsX09iamVjdHMvRnVuY3Rpb24vYmluZFxuXG4gICMjIyMgRXhhbXBsZVxuXG4gIChUaGlzIGlzIGEgc29tZXdoYXQgY29udHJpdmVkIGV4YW1wbGUsIGJ1dCBpdCBzZXJ2ZXMgdG8gc2hvdyB0aGUgd2F5IHRoZVxuICBmdW5jdGlvbiBiZWhhdmVzLilcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICAvLyBzdHJpbmcgLT4gTWF5YmU8bnVtYmVyPlxuICBjb25zdCB0b01heWJlTGVuZ3RoID0gKHM6IHN0cmluZyk6IE1heWJlPG51bWJlcj4gPT4gTWF5YmUub2Yocy5sZW5ndGgpO1xuXG4gIC8vIE1heWJlPHN0cmluZz5cbiAgY29uc3QgYU1heWJlU3RyaW5nID0gTWF5YmUub2YoJ0hlbGxvLCB0aGVyZSEnKTtcblxuICAvLyBNYXliZTxudW1iZXI+XG4gIGNvbnN0IHJlc3VsdGluZ0xlbmd0aCA9IE1heWJlLmFuZFRoZW4odG9NYXliZUxlbmd0aCwgYU1heWJlU3RyaW5nKTtcbiAgY29uc29sZS5sb2coTWF5YmUudG9TdHJpbmcocmVzdWx0aW5nTGVuZ3RoKSk7IC8vIDEzXG4gIGBgYFxuXG4gIE5vdGUgdGhhdCB0aGUgcmVzdWx0IGlzIG5vdCBgKEp1c3QoMTMpKWAsIGJ1dCBgMTNgIVxuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUgaW4gdGhlIHJlc3VsdGluZyBgTWF5YmVgLlxuICBAcGFyYW0gdGhlbkZuIFRoZSBmdW5jdGlvbiB0byBhcHBseSB0byB0aGUgd3JhcHBlZCBgVGAgaWYgYG1heWJlYCBpcyBgSnVzdGAuXG4gIEBwYXJhbSBtYXliZSAgVGhlIGBNYXliZWAgdG8gZXZhbHVhdGUgYW5kIHBvc3NpYmx5IGFwcGx5IGEgZnVuY3Rpb24gdG8gdGhlXG4gICAgICAgICAgICAgICAgY29udGVudHMgb2YuXG4gIEByZXR1cm5zICAgICAgVGhlIHJlc3VsdCBvZiB0aGUgYHRoZW5GbmAgKGEgbmV3IGBNYXliZWApIGlmIGBtYXliZWAgaXMgYVxuICAgICAgICAgICAgICAgIGBKdXN0YCwgb3RoZXJ3aXNlIGBOb3RoaW5nYCBpZiBgbWF5YmVgIGlzIGEgYE5vdGhpbmdgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYW5kVGhlbjxULCBVPih0aGVuRm46ICh0OiBUKSA9PiBNYXliZTxVPiwgbWF5YmU6IE1heWJlPFQ+KTogTWF5YmU8VT47XG5leHBvcnQgZnVuY3Rpb24gYW5kVGhlbjxULCBVPih0aGVuRm46ICh0OiBUKSA9PiBNYXliZTxVPik6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFuZFRoZW48VCwgVT4oXG4gIHRoZW5GbjogKHQ6IFQpID0+IE1heWJlPFU+LFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBNYXliZTxVPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxVPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyB0aGVuRm4obS52YWx1ZSkgOiBub3RoaW5nPFU+KCkpO1xuICByZXR1cm4gbWF5YmUgIT09IHVuZGVmaW5lZCA/IG9wKG1heWJlKSA6IG9wO1xufVxuXG4vKiogQWxpYXMgZm9yIFtgYW5kVGhlbmBdKCNhbmR0aGVuKS4gKi9cbmV4cG9ydCBjb25zdCBjaGFpbiA9IGFuZFRoZW47XG5cbi8qKiBBbGlhcyBmb3IgW2BhbmRUaGVuYF0oI2FuZHRoZW4pLiAqL1xuZXhwb3J0IGNvbnN0IGZsYXRNYXAgPSBhbmRUaGVuO1xuXG4vKipcbiAgUHJvdmlkZSBhIGZhbGxiYWNrIGZvciBhIGdpdmVuIGBNYXliZWAuIEJlaGF2ZXMgbGlrZSBhIGxvZ2ljYWwgYG9yYDogaWYgdGhlXG4gIGBtYXliZWAgdmFsdWUgaXMgYSBgSnVzdGAsIHJldHVybnMgdGhhdCBgbWF5YmVgOyBvdGhlcndpc2UsIHJldHVybnMgdGhlXG4gIGBkZWZhdWx0TWF5YmVgIHZhbHVlLlxuXG4gIFRoaXMgaXMgdXNlZnVsIHdoZW4geW91IHdhbnQgdG8gbWFrZSBzdXJlIHRoYXQgc29tZXRoaW5nIHdoaWNoIHRha2VzIGFcbiAgYE1heWJlYCBhbHdheXMgZW5kcyB1cCBnZXR0aW5nIGEgYEp1c3RgIHZhcmlhbnQsIGJ5IHN1cHBseWluZyBhIGRlZmF1bHQgdmFsdWVcbiAgZm9yIHRoZSBjYXNlIHRoYXQgeW91IGN1cnJlbnRseSBoYXZlIGEgbm90aGluZy5cblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS11dGlscy9tYXliZSc7XG5cbiAgY29uc3QganVzdEEgPSBNYXliZS5qdXN0KFwiYVwiKTtcbiAgY29uc3QganVzdEIgPSBNYXliZS5qdXN0KFwiYlwiKTtcbiAgY29uc3QgYU5vdGhpbmc6IE1heWJlPHN0cmluZz4gPSBub3RoaW5nKCk7XG5cbiAgY29uc29sZS5sb2coTWF5YmUub3IoanVzdEIsIGp1c3RBKS50b1N0cmluZygpKTsgIC8vIEp1c3QoQSlcbiAgY29uc29sZS5sb2coTWF5YmUub3IoYU5vdGhpbmcsIGp1c3RBKS50b1N0cmluZygpKTsgIC8vIEp1c3QoQSlcbiAgY29uc29sZS5sb2coTWF5YmUub3IoanVzdEIsIGFOb3RoaW5nKS50b1N0cmluZygpKTsgIC8vIEp1c3QoQilcbiAgY29uc29sZS5sb2coTWF5YmUub3IoYU5vdGhpbmcsIGFOb3RoaW5nKS50b1N0cmluZygpKTsgIC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUICAgICAgICBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHBhcmFtIGRlZmF1bHRNYXliZSBUaGUgYE1heWJlYCB0byB1c2UgaWYgYG1heWJlYCBpcyBhIGBOb3RoaW5nYC5cbiAgQHBhcmFtIG1heWJlICAgICAgICBUaGUgYE1heWJlYCBpbnN0YW5jZSB0byBldmFsdWF0ZS5cbiAgQHJldHVybnMgICAgICAgICAgICBgbWF5YmVgIGlmIGl0IGlzIGEgYEp1c3RgLCBvdGhlcndpc2UgYGRlZmF1bHRNYXliZWAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBvcjxUPihkZWZhdWx0TWF5YmU6IE1heWJlPFQ+LCBtYXliZTogTWF5YmU8VD4pOiBNYXliZTxUPjtcbmV4cG9ydCBmdW5jdGlvbiBvcjxUPihkZWZhdWx0TWF5YmU6IE1heWJlPFQ+KTogKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VD47XG5leHBvcnQgZnVuY3Rpb24gb3I8VD4oXG4gIGRlZmF1bHRNYXliZTogTWF5YmU8VD4sXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IE1heWJlPFQ+IHwgKChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFQ+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAobS5pc0p1c3QoKSA/IG0gOiBkZWZhdWx0TWF5YmUpO1xuICByZXR1cm4gbWF5YmUgIT09IHVuZGVmaW5lZCA/IG9wKG1heWJlKSA6IG9wO1xufVxuXG4vKipcbiAgTGlrZSBgb3JgLCBidXQgdXNpbmcgYSBmdW5jdGlvbiB0byBjb25zdHJ1Y3QgdGhlIGFsdGVybmF0aXZlIGBNYXliZWAuXG5cbiAgU29tZXRpbWVzIHlvdSBuZWVkIHRvIHBlcmZvcm0gYW4gb3BlcmF0aW9uIHVzaW5nIG90aGVyIGRhdGEgaW4gdGhlXG4gIGVudmlyb25tZW50IHRvIGNvbnN0cnVjdCB0aGUgZmFsbGJhY2sgdmFsdWUuIEluIHRoZXNlIHNpdHVhdGlvbnMsIHlvdSBjYW5cbiAgcGFzcyBhIGZ1bmN0aW9uICh3aGljaCBtYXkgYmUgYSBjbG9zdXJlKSBhcyB0aGUgYGVsc2VGbmAgdG8gZ2VuZXJhdGUgdGhlXG4gIGZhbGxiYWNrIGBNYXliZTxUPmAuXG5cbiAgVXNlZnVsIGZvciB0cmFuc2Zvcm1pbmcgZW1wdHkgc2NlbmFyaW9zIGJhc2VkIG9uIHZhbHVlcyBpbiBjb250ZXh0LlxuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBlbHNlRm4gVGhlIGZ1bmN0aW9uIHRvIGFwcGx5IGlmIGBtYXliZWAgaXMgYE5vdGhpbmdgXG4gIEBwYXJhbSBtYXliZSAgVGhlIGBtYXliZWAgdG8gdXNlIGlmIGl0IGlzIGBKdXN0YC5cbiAgQHJldHVybnMgICAgICBUaGUgYG1heWJlYCBpZiBpdCBpcyBgSnVzdGAsIG9yIHRoZSBgTWF5YmVgIHJldHVybmVkIGJ5XG4gICAgICAgICAgICAgICAgYGVsc2VGbmAgaWYgdGhlIGBtYXliZWAgaXMgYE5vdGhpbmdgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gb3JFbHNlPFQ+KGVsc2VGbjogKCkgPT4gTWF5YmU8VD4sIG1heWJlOiBNYXliZTxUPik6IE1heWJlPFQ+O1xuZXhwb3J0IGZ1bmN0aW9uIG9yRWxzZTxUPihlbHNlRm46ICgpID0+IE1heWJlPFQ+KTogKG1heWJlOiBNYXliZTxUPikgPT4gTWF5YmU8VD47XG5leHBvcnQgZnVuY3Rpb24gb3JFbHNlPFQ+KFxuICBlbHNlRm46ICgpID0+IE1heWJlPFQ+LFxuICBtYXliZT86IE1heWJlPFQ+XG4pOiBNYXliZTxUPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBNYXliZTxUPikge1xuICBjb25zdCBvcCA9IChtOiBNYXliZTxUPikgPT4gKG0uaXNKdXN0KCkgPyBtIDogZWxzZUZuKCkpO1xuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKlxuICBHZXQgdGhlIHZhbHVlIG91dCBvZiB0aGUgYE1heWJlYC5cblxuICBSZXR1cm5zIHRoZSBjb250ZW50IG9mIGEgYEp1c3RgLCBidXQgKip0aHJvd3MgaWYgdGhlIGBNYXliZWAgaXMgYE5vdGhpbmdgKiouXG4gIFByZWZlciB0byB1c2UgW2B1bndyYXBPcmBdKCN1bndyYXBvcikgb3IgW2B1bndyYXBPckVsc2VgXSgjdW53cmFwb3JlbHNlKS5cblxuICBAdHlwZXBhcmFtIFQgVGhlIHR5cGUgb2YgdGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBtYXliZSBUaGUgdmFsdWUgdG8gdW53cmFwXG4gIEByZXR1cm5zICAgICBUaGUgdW53cmFwcGVkIHZhbHVlIGlmIHRoZSBgTWF5YmVgIGluc3RhbmNlIGlzIGBKdXN0YC5cbiAgQHRocm93cyAgICAgIElmIHRoZSBgbWF5YmVgIGlzIGBOb3RoaW5nYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHVuc2FmZWx5VW53cmFwPFQ+KG1heWJlOiBNYXliZTxUPik6IFQge1xuICByZXR1cm4gbWF5YmUudW5zYWZlbHlVbndyYXAoKTtcbn1cblxuLyoqIEFsaWFzIGZvciBbYHVuc2FmZWx5VW53cmFwYF0oI3Vuc2FmZWx5dW53cmFwKSAqL1xuZXhwb3J0IGNvbnN0IHVuc2FmZWx5R2V0ID0gdW5zYWZlbHlVbndyYXA7XG5cbi8qKiBBbGlhcyBmb3IgW2B1bnNhZmVseVVud3JhcGBdKCN1bnNhZmVseXVud3JhcCkgKi9cbmV4cG9ydCBjb25zdCB1bnNhZmVHZXQgPSB1bnNhZmVseVVud3JhcDtcblxuLyoqXG4gIFNhZmVseSBnZXQgdGhlIHZhbHVlIG91dCBvZiBhIGBNYXliZWAuXG5cbiAgUmV0dXJucyB0aGUgY29udGVudCBvZiBhIGBKdXN0YCBvciBgZGVmYXVsdFZhbHVlYCBpZiBgTm90aGluZ2AuIFRoaXMgaXMgdGhlXG4gIHJlY29tbWVuZGVkIHdheSB0byBnZXQgYSB2YWx1ZSBvdXQgb2YgYSBgTWF5YmVgIG1vc3Qgb2YgdGhlIHRpbWUuXG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgY29uc3Qgbm90QVN0cmluZyA9IE1heWJlLm5vdGhpbmc8c3RyaW5nPigpO1xuICBjb25zdCBpc0FTdHJpbmcgPSBNYXliZS5qdXN0KCdsb29rIG1hISBzb21lIGNoYXJhY3RlcnMhJyk7XG5cbiAgY29uc29sZS5sb2coTWF5YmUudW53cmFwT3IoJzxlbXB0eT4nLCBub3RBU3RyaW5nKSk7ICAvLyBcIjxlbXB0eT5cIlxuICBjb25zb2xlLmxvZyhNYXliZS51bndyYXBPcignPGVtcHR5PicsIGlzQVN0cmluZykpOyAgLy8gXCJsb29rIG1hISBzb21lIGNoYXJhY3RlcnMhXCJcbiAgYGBgXG5cbiAgQHR5cGVwYXJhbSBUICAgICAgICBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZS5cbiAgQHBhcmFtIGRlZmF1bHRWYWx1ZSBUaGUgdmFsdWUgdG8gcmV0dXJuIGlmIGBtYXliZWAgaXMgYSBgTm90aGluZ2AuXG4gIEBwYXJhbSBtYXliZSAgICAgICAgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gdW53cmFwIGlmIGl0IGlzIGEgYEp1c3RgLlxuICBAcmV0dXJucyAgICAgICAgICAgIFRoZSBjb250ZW50IG9mIGBtYXliZWAgaWYgaXQgaXMgYSBgSnVzdGAsIG90aGVyd2lzZVxuICAgICAgICAgICAgICAgICAgICAgIGBkZWZhdWx0VmFsdWVgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3I8VD4oZGVmYXVsdFZhbHVlOiBULCBtYXliZTogTWF5YmU8VD4pOiBUO1xuZXhwb3J0IGZ1bmN0aW9uIHVud3JhcE9yPFQ+KGRlZmF1bHRWYWx1ZTogVCk6IChtYXliZTogTWF5YmU8VD4pID0+IFQ7XG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3I8VD4oZGVmYXVsdFZhbHVlOiBULCBtYXliZT86IE1heWJlPFQ+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PiAobS5pc0p1c3QoKSA/IG0udmFsdWUgOiBkZWZhdWx0VmFsdWUpO1xuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKiBBbGlhcyBmb3IgW2B1bndyYXBPcmBdKCN1bndyYXBvcikgKi9cbmV4cG9ydCBjb25zdCBnZXRPciA9IHVud3JhcE9yO1xuXG4vKipcbiAgU2FmZWx5IGdldCB0aGUgdmFsdWUgb3V0IG9mIGEgW2BNYXliZWBdKCNtYXliZSkgYnkgcmV0dXJuaW5nIHRoZSB3cmFwcGVkXG4gIHZhbHVlIGlmIGl0IGlzIGBKdXN0YCwgb3IgYnkgYXBwbHlpbmcgYG9yRWxzZUZuYCBpZiBpdCBpcyBgTm90aGluZ2AuXG5cbiAgVGhpcyBpcyB1c2VmdWwgd2hlbiB5b3UgbmVlZCB0byAqZ2VuZXJhdGUqIGEgdmFsdWUgKGUuZy4gYnkgdXNpbmcgY3VycmVudFxuICB2YWx1ZXMgaW4gdGhlIGVudmlyb25tZW50IOKAkyB3aGV0aGVyIHByZWxvYWRlZCBvciBieSBsb2NhbCBjbG9zdXJlKSBpbnN0ZWFkIG9mXG4gIGhhdmluZyBhIHNpbmdsZSBkZWZhdWx0IHZhbHVlIGF2YWlsYWJsZSAoYXMgaW4gW2B1bndyYXBPcmBdKCN1bndyYXBvcikpLlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIC8vIFlvdSBjYW4gaW1hZ2luZSB0aGF0IHNvbWVPdGhlclZhbHVlIG1pZ2h0IGJlIGR5bmFtaWMuXG4gIGNvbnN0IHNvbWVPdGhlclZhbHVlID0gOTk7XG4gIGNvbnN0IGhhbmRsZU5vdGhpbmcgPSAoKSA9PiBzb21lT3RoZXJWYWx1ZTtcblxuICBjb25zdCBhSnVzdCA9IE1heWJlLmp1c3QoNDIpO1xuICBjb25zb2xlLmxvZyhNYXliZS51bndyYXBPckVsc2UoaGFuZGxlTm90aGluZywgYUp1c3QpKTsgIC8vIDQyXG5cbiAgY29uc3QgYU5vdGhpbmcgPSBub3RoaW5nPG51bWJlcj4oKTtcbiAgY29uc29sZS5sb2coTWF5YmUudW53cmFwT3JFbHNlKGhhbmRsZU5vdGhpbmcsIGFOb3RoaW5nKSk7IC8vIDk5XG4gIGBgYFxuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHdyYXBwZWQgdmFsdWUuXG4gIEBwYXJhbSBvckVsc2VGbiBBIGZ1bmN0aW9uIHVzZWQgdG8gZ2VuZXJhdGUgYSB2YWxpZCB2YWx1ZSBpZiBgbWF5YmVgIGlzIGFcbiAgICAgICAgICAgICAgICAgIGBOb3RoaW5nYC5cbiAgQHBhcmFtIG1heWJlICAgIFRoZSBgTWF5YmVgIGluc3RhbmNlIHRvIHVud3JhcCBpZiBpdCBpcyBhIGBKdXN0YFxuICBAcmV0dXJucyAgICAgICAgRWl0aGVyIHRoZSBjb250ZW50IG9mIGBtYXliZWAgb3IgdGhlIHZhbHVlIHJldHVybmVkIGZyb21cbiAgICAgICAgICAgICAgICAgIGBvckVsc2VGbmAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPckVsc2U8VD4ob3JFbHNlRm46ICgpID0+IFQsIG1heWJlOiBNYXliZTxUPik6IFQ7XG5leHBvcnQgZnVuY3Rpb24gdW53cmFwT3JFbHNlPFQ+KG9yRWxzZUZuOiAoKSA9PiBUKTogKG1heWJlOiBNYXliZTxUPikgPT4gVDtcbmV4cG9ydCBmdW5jdGlvbiB1bndyYXBPckVsc2U8VD4ob3JFbHNlRm46ICgpID0+IFQsIG1heWJlPzogTWF5YmU8VD4pOiBUIHwgKChtYXliZTogTWF5YmU8VD4pID0+IFQpIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gbS52YWx1ZSA6IG9yRWxzZUZuKCkpO1xuICByZXR1cm4gY3VycnkxKG9wLCBtYXliZSk7XG59XG5cbi8qKiBBbGlhcyBmb3IgW2B1bndyYXBPckVsc2VgXSgjdW53cmFwb3JlbHNlKSAqL1xuZXhwb3J0IGNvbnN0IGdldE9yRWxzZSA9IHVud3JhcE9yRWxzZTtcblxuLyoqXG4gIFRyYW5zZm9ybSB0aGUgW2BNYXliZWBdKCNtYXliZSkgaW50byBhXG4gIFtgUmVzdWx0YF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Jlc3VsdCksIHVzaW5nIHRoZSB3cmFwcGVkIHZhbHVlIGFzIHRoZVxuICBgT2tgIHZhbHVlIGlmIGBKdXN0YDsgb3RoZXJ3aXNlIHVzaW5nIHRoZSBzdXBwbGllZCBgZXJyb3JgIHZhbHVlIGZvciBgRXJyYC5cblxuICBAdHlwZXBhcmFtIFQgIFRoZSB3cmFwcGVkIHZhbHVlLlxuICBAdHlwZXBhcmFtIEUgIFRoZSBlcnJvciB0eXBlIHRvIGluIHRoZSBgUmVzdWx0YC5cbiAgQHBhcmFtIGVycm9yIFRoZSBlcnJvciB2YWx1ZSB0byB1c2UgaWYgdGhlIGBNYXliZWAgaXMgYE5vdGhpbmdgLlxuICBAcGFyYW0gbWF5YmUgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gY29udmVydC5cbiAgQHJldHVybnMgICAgIEEgYFJlc3VsdGAgY29udGFpbmluZyB0aGUgdmFsdWUgd3JhcHBlZCBpbiBgbWF5YmVgIGluIGFuIGBPa2AsXG4gICAgICAgICAgICAgICBvciBgZXJyb3JgIGluIGFuIGBFcnJgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdG9Pa09yRXJyPFQsIEU+KGVycm9yOiBFLCBtYXliZTogTWF5YmU8VD4pOiBSZXN1bHQ8VCwgRT47XG5leHBvcnQgZnVuY3Rpb24gdG9Pa09yRXJyPFQsIEU+KGVycm9yOiBFKTogKG1heWJlOiBNYXliZTxUPikgPT4gUmVzdWx0PFQsIEU+O1xuZXhwb3J0IGZ1bmN0aW9uIHRvT2tPckVycjxULCBFPihcbiAgZXJyb3I6IEUsXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IFJlc3VsdDxULCBFPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBSZXN1bHQ8VCwgRT4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gb2s8VCwgRT4obS52YWx1ZSkgOiBlcnI8VCwgRT4oZXJyb3IpKTtcbiAgcmV0dXJuIG1heWJlICE9PSB1bmRlZmluZWQgPyBvcChtYXliZSkgOiBvcDtcbn1cblxuLyoqXG4gIFRyYW5zZm9ybSB0aGUgW2BNYXliZWBdKCNtYXliZSkgaW50byBhXG4gIFtgUmVzdWx0YF0oLi4vbW9kdWxlcy9fcmVzdWx0Xy5odG1sI3Jlc3VsdCksIHVzaW5nIHRoZSB3cmFwcGVkIHZhbHVlIGFzIHRoZVxuICBgT2tgIHZhbHVlIGlmIGBKdXN0YDsgb3RoZXJ3aXNlIHVzaW5nIGBlbHNlRm5gIHRvIGdlbmVyYXRlIGBFcnJgLlxuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHdyYXBwZWQgdmFsdWUuXG4gIEB0eXBlcGFyYW0gRSAgVGhlIGVycm9yIHR5cGUgdG8gaW4gdGhlIGBSZXN1bHRgLlxuICBAcGFyYW0gZWxzZUZuIFRoZSBmdW5jdGlvbiB3aGljaCBnZW5lcmF0ZXMgYW4gZXJyb3Igb2YgdHlwZSBgRWAuXG4gIEBwYXJhbSBtYXliZSAgVGhlIGBNYXliZWAgaW5zdGFuY2UgdG8gY29udmVydC5cbiAgQHJldHVybnMgICAgIEEgYFJlc3VsdGAgY29udGFpbmluZyB0aGUgdmFsdWUgd3JhcHBlZCBpbiBgbWF5YmVgIGluIGFuIGBPa2AsXG4gICAgICAgICAgICAgICBvciB0aGUgdmFsdWUgZ2VuZXJhdGVkIGJ5IGBlbHNlRm5gIGluIGFuIGBFcnJgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdG9Pa09yRWxzZUVycjxULCBFPihlbHNlRm46ICgpID0+IEUsIG1heWJlOiBNYXliZTxUPik6IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0b09rT3JFbHNlRXJyPFQsIEU+KGVsc2VGbjogKCkgPT4gRSk6IChtYXliZTogTWF5YmU8VD4pID0+IFJlc3VsdDxULCBFPjtcbmV4cG9ydCBmdW5jdGlvbiB0b09rT3JFbHNlRXJyPFQsIEU+KFxuICBlbHNlRm46ICgpID0+IEUsXG4gIG1heWJlPzogTWF5YmU8VD5cbik6IFJlc3VsdDxULCBFPiB8ICgobWF5YmU6IE1heWJlPFQ+KSA9PiBSZXN1bHQ8VCwgRT4pIHtcbiAgY29uc3Qgb3AgPSAobTogTWF5YmU8VD4pID0+IChtLmlzSnVzdCgpID8gb2s8VCwgRT4obS52YWx1ZSkgOiBlcnI8VCwgRT4oZWxzZUZuKCkpKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgbWF5YmUpO1xufVxuXG4vKipcbiAgQ29uc3RydWN0IGEgYE1heWJlPFQ+YCBmcm9tIGEgYFJlc3VsdDxULCBFPmAuXG5cbiAgSWYgdGhlIGBSZXN1bHRgIGlzIGFuIGBPa2AsIHdyYXAgaXRzIHZhbHVlIGluIGBKdXN0YC4gSWYgdGhlIGBSZXN1bHRgIGlzIGFuXG4gIGBFcnJgLCB0aHJvdyBhd2F5IHRoZSB3cmFwcGVkIGBFYCBhbmQgdHJhbnNmb3JtIHRvIGEgYE5vdGhpbmdgLlxuXG4gIEB0eXBlcGFyYW0gVCAgVGhlIHR5cGUgb2YgdGhlIHZhbHVlIHdyYXBwZWQgaW4gYSBgUmVzdWx0Lk9rYCBhbmQgaW4gdGhlIGBKdXN0YFxuICAgICAgICAgICAgICAgIG9mIHRoZSByZXN1bHRpbmcgYE1heWJlYC5cbiAgQHR5cGVwYXJhbSBFICBUaGUgdHlwZSBvZiB0aGUgdmFsdWUgd3JhcHBlZCBpbiBhIGBSZXN1bHQuRXJyYDsgdGhyb3duIGF3YXkgaW5cbiAgICAgICAgICAgICAgICB0aGUgcmVzdWx0aW5nIGBNYXliZWAuXG4gIEBwYXJhbSByZXN1bHQgVGhlIGBSZXN1bHRgIHRvIGNvbnN0cnVjdCBhIGBNYXliZWAgZnJvbS5cbiAgQHJldHVybnMgICAgICBgSnVzdGAgaWYgYHJlc3VsdGAgd2FzIGBPa2Agb3IgYE5vdGhpbmdgIGlmIGl0IHdhcyBgRXJyYC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGZyb21SZXN1bHQ8VD4ocmVzdWx0OiBSZXN1bHQ8VCwgYW55Pik6IE1heWJlPFQ+IHtcbiAgcmV0dXJuIHJlc3VsdC5pc09rKCkgPyBqdXN0KHJlc3VsdC52YWx1ZSkgOiBub3RoaW5nPFQ+KCk7XG59XG5cbi8qKlxuICBDcmVhdGUgYSBgU3RyaW5nYCByZXByZXNlbnRhdGlvbiBvZiBhIGBNYXliZWAgaW5zdGFuY2UuXG5cbiAgQSBgSnVzdGAgaW5zdGFuY2Ugd2lsbCBiZSBwcmludGVkIGFzIGBKdXN0KDxyZXByZXNlbnRhdGlvbiBvZiB0aGUgdmFsdWU+KWAsXG4gIHdoZXJlIHRoZSByZXByZXNlbnRhdGlvbiBvZiB0aGUgdmFsdWUgaXMgc2ltcGx5IHRoZSB2YWx1ZSdzIG93biBgdG9TdHJpbmdgXG4gIHJlcHJlc2VudGF0aW9uLiBGb3IgZXhhbXBsZTpcblxuICB8IGNhbGwgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHwgb3V0cHV0ICAgICAgICAgICAgICAgICAgfFxuICB8LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLXwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tfFxuICB8IGB0b1N0cmluZyhNYXliZS5vZig0MikpYCAgICAgICAgICAgICAgIHwgYEp1c3QoNDIpYCAgICAgICAgICAgICAgfFxuICB8IGB0b1N0cmluZyhNYXliZS5vZihbMSwgMiwgM10pKWAgICAgICAgIHwgYEp1c3QoMSwyLDMpYCAgICAgICAgICAgfFxuICB8IGB0b1N0cmluZyhNYXliZS5vZih7IGFuOiAnb2JqZWN0JyB9KSlgIHwgYEp1c3QoW29iamVjdCBPYmplY3RdKWAgfFxuICB8IGB0b1N0cmluZyhNYXliZS5ub3RoaW5nKCkpYCAgICAgICAgICAgIHwgYE5vdGhpbmdgICAgICAgICAgICAgICAgfFxuXG4gIEB0eXBlcGFyYW0gVCBUaGUgdHlwZSBvZiB0aGUgd3JhcHBlZCB2YWx1ZTsgaXRzIG93biBgLnRvU3RyaW5nYCB3aWxsIGJlIHVzZWRcbiAgICAgICAgICAgICAgIHRvIHByaW50IHRoZSBpbnRlcmlvciBjb250ZW50cyBvZiB0aGUgYEp1c3RgIHZhcmlhbnQuXG4gIEBwYXJhbSBtYXliZSBUaGUgdmFsdWUgdG8gY29udmVydCB0byBhIHN0cmluZy5cbiAgQHJldHVybnMgICAgIFRoZSBzdHJpbmcgcmVwcmVzZW50YXRpb24gb2YgdGhlIGBNYXliZWAuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiB0b1N0cmluZzxUPihtYXliZTogTWF5YmU8VD4pOiBzdHJpbmcge1xuICBjb25zdCBib2R5ID0gbWF5YmUuaXNKdXN0KCkgPyBgKCR7bWF5YmUudmFsdWUudG9TdHJpbmcoKX0pYCA6ICcnO1xuICByZXR1cm4gYCR7bWF5YmUudmFyaWFudH0ke2JvZHl9YDtcbn1cblxuLyoqIEEgbGlnaHR3ZWlnaHQgb2JqZWN0IGRlZmluaW5nIGhvdyB0byBoYW5kbGUgZWFjaCB2YXJpYW50IG9mIGEgTWF5YmUuICovXG5leHBvcnQgdHlwZSBNYXRjaGVyPFQsIEE+ID0ge1xuICBKdXN0OiAodmFsdWU6IFQpID0+IEE7XG4gIE5vdGhpbmc6ICgpID0+IEE7XG59O1xuXG4vKipcbiAgUGVyZm9ybXMgdGhlIHNhbWUgYmFzaWMgZnVuY3Rpb25hbGl0eSBhcyBgZ2V0T3JFbHNlYCwgYnV0IGluc3RlYWQgb2Ygc2ltcGx5XG4gIHVud3JhcHBpbmcgdGhlIHZhbHVlIGlmIGl0IGlzIGBKdXN0YCBhbmQgYXBwbHlpbmcgYSB2YWx1ZSB0byBnZW5lcmF0ZSB0aGUgc2FtZVxuICBkZWZhdWx0IHR5cGUgaWYgaXQgaXMgYE5vdGhpbmdgLCBsZXRzIHlvdSBzdXBwbHkgZnVuY3Rpb25zIHdoaWNoIG1heSB0cmFuc2Zvcm1cbiAgdGhlIHdyYXBwZWQgdHlwZSBpZiBpdCBpcyBgSnVzdGAgb3IgZ2V0IGEgZGVmYXVsdCB2YWx1ZSBmb3IgYE5vdGhpbmdgLlxuXG4gIFRoaXMgaXMga2luZCBvZiBsaWtlIGEgcG9vciBtYW4ncyB2ZXJzaW9uIG9mIHBhdHRlcm4gbWF0Y2hpbmcsIHdoaWNoXG4gIEphdmFTY3JpcHQgY3VycmVudGx5IGxhY2tzLlxuXG4gIEluc3RlYWQgb2YgY29kZSBsaWtlIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgY29uc3QgbG9nVmFsdWUgPSAobWlnaHRCZUFOdW1iZXI6IE1heWJlPG51bWJlcj4pID0+IHtcbiAgICBjb25zdCB2YWx1ZVRvTG9nID0gTWF5YmUubWlnaHRCZUFOdW1iZXIuaXNKdXN0KClcbiAgICAgID8gTWF5YmUudW5zYWZlbHlVbndyYXAobWlnaHRCZUFOdW1iZXIpLnRvU3RyaW5nKClcbiAgICAgIDogJ05vdGhpbmcgdG8gbG9nLic7XG5cbiAgICBjb25zb2xlLmxvZyh2YWx1ZVRvTG9nKTtcbiAgfTtcbiAgYGBgXG5cbiAgLi4ud2UgY2FuIHdyaXRlIGNvZGUgbGlrZSB0aGlzOlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGNvbnN0IGxvZ1ZhbHVlID0gKG1pZ2h0QmVBTnVtYmVyOiBNYXliZTxudW1iZXI+KSA9PiB7XG4gICAgY29uc3QgdmFsdWUgPSBNYXliZS5tYXRjaChcbiAgICAgIHtcbiAgICAgICAgSnVzdDogbiA9PiBuLnRvU3RyaW5nKCksXG4gICAgICAgIE5vdGhpbmc6ICgpID0+ICdOb3RoaW5nIHRvIGxvZy4nLFxuICAgICAgfSxcbiAgICAgIG1pZ2h0QmVBTnVtYmVyXG4gICAgKTtcblxuICAgIGNvbnNvbGUubG9nKHZhbHVlKTtcbiAgfTtcbiAgYGBgXG5cbiAgVGhpcyBpcyBzbGlnaHRseSBsb25nZXIgdG8gd3JpdGUsIGJ1dCBjbGVhcmVyOiB0aGUgbW9yZSBjb21wbGV4IHRoZSByZXN1bHRpbmdcbiAgZXhwcmVzc2lvbiwgdGhlIGhhaXJlciBpdCBpcyB0byB1bmRlcnN0YW5kIHRoZSB0ZXJuYXJ5LiBUaHVzLCB0aGlzIGlzXG4gIGVzcGVjaWFsbHkgY29udmVuaWVudCBmb3IgdGltZXMgd2hlbiB0aGVyZSBpcyBhIGNvbXBsZXggcmVzdWx0LCBlLmcuIHdoZW5cbiAgcmVuZGVyaW5nIHBhcnQgb2YgYSBSZWFjdCBjb21wb25lbnQgaW5saW5lIGluIEpTWC9UU1guXG5cbiAgQHBhcmFtIG1hdGNoZXIgQSBsaWdodHdlaWdodCBvYmplY3QgZGVmaW5pbmcgd2hhdCB0byBkbyBpbiB0aGUgY2FzZSBvZiBlYWNoXG4gICAgICAgICAgICAgICAgIHZhcmlhbnQuXG4gIEBwYXJhbSBtYXliZSAgIFRoZSBgbWF5YmVgIGluc3RhbmNlIHRvIGNoZWNrLlxuICovXG5leHBvcnQgZnVuY3Rpb24gbWF0Y2g8VCwgQT4obWF0Y2hlcjogTWF0Y2hlcjxULCBBPiwgbWF5YmU6IE1heWJlPFQ+KTogQTtcbmV4cG9ydCBmdW5jdGlvbiBtYXRjaDxULCBBPihtYXRjaGVyOiBNYXRjaGVyPFQsIEE+KTogKG06IE1heWJlPFQ+KSA9PiBBO1xuZXhwb3J0IGZ1bmN0aW9uIG1hdGNoPFQsIEE+KG1hdGNoZXI6IE1hdGNoZXI8VCwgQT4sIG1heWJlPzogTWF5YmU8VD4pOiBBIHwgKChtOiBNYXliZTxUPikgPT4gQSkge1xuICByZXR1cm4gbWF5YmUgIT09IHVuZGVmaW5lZFxuICAgID8gbWFwT3JFbHNlKG1hdGNoZXIuTm90aGluZywgbWF0Y2hlci5KdXN0LCBtYXliZSlcbiAgICA6IChjdXJyaWVkTWF5YmU6IE1heWJlPFQ+KSA9PiBtYXBPckVsc2UobWF0Y2hlci5Ob3RoaW5nLCBtYXRjaGVyLkp1c3QsIGN1cnJpZWRNYXliZSk7XG59XG5cbi8qKiBBbGlhcyBmb3IgW2BtYXRjaGBdKCNtYXRjaCkgKi9cbmV4cG9ydCBjb25zdCBjYXRhID0gbWF0Y2g7XG5cbi8qKlxuICBBbGxvd3MgcXVpY2sgdHJpcGxlLWVxdWFsIGVxdWFsaXR5IGNoZWNrIGJldHdlZW4gdGhlIHZhbHVlcyBpbnNpZGUgdHdvIGBtYXliZWBzXG4gIHdpdGhvdXQgaGF2aW5nIHRvIHVud3JhcCB0aGVtIGZpcnN0LlxuXG4gIGBgYHRzXG4gIGNvbnN0IGEgPSBNYXliZS5vZigzKTtcbiAgY29uc3QgYiA9IE1heWJlLm9mKDMpO1xuICBjb25zdCBjID0gTWF5YmUub2YobnVsbCk7XG4gIGNvbnN0IGQgPSBNYXliZS5ub3RoaW5nKCk7XG5cbiAgTWF5YmUuZXF1YWxzKGEsIGIpOyAvLyB0cnVlXG4gIE1heWJlLmVxdWFscyhhLCBjKTsgLy8gZmFsc2VcbiAgTWF5YmUuZXF1YWxzKGMsIGQpOyAvLyB0cnVlXG4gIGBgYFxuXG4gIEBwYXJhbSBtYiBBIGBtYXliZWAgdG8gY29tcGFyZSB0by5cbiAgQHBhcmFtIG1hIEEgYG1heWJlYCBpbnN0YW5jZSB0byBjaGVjay5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGVxdWFsczxUPihtYjogTWF5YmU8VD4sIG1hOiBNYXliZTxUPik6IGJvb2xlYW47XG5leHBvcnQgZnVuY3Rpb24gZXF1YWxzPFQ+KG1iOiBNYXliZTxUPik6IChtYTogTWF5YmU8VD4pID0+IGJvb2xlYW47XG5leHBvcnQgZnVuY3Rpb24gZXF1YWxzPFQ+KG1iOiBNYXliZTxUPiwgbWE/OiBNYXliZTxUPik6IGJvb2xlYW4gfCAoKGE6IE1heWJlPFQ+KSA9PiBib29sZWFuKSB7XG4gIHJldHVybiBtYSAhPT0gdW5kZWZpbmVkXG4gICAgPyBtYS5tYXRjaCh7XG4gICAgICAgIEp1c3Q6IGFWYWwgPT4gbWIuaXNKdXN0KCkgJiYgbWIudW5zYWZlbHlVbndyYXAoKSA9PT0gYVZhbCxcbiAgICAgICAgTm90aGluZzogKCkgPT4gaXNOb3RoaW5nKG1iKSxcbiAgICAgIH0pXG4gICAgOiAobWF5YmVBOiBNYXliZTxUPikgPT5cbiAgICAgICAgbWF5YmVBLm1hdGNoKHtcbiAgICAgICAgICBOb3RoaW5nOiAoKSA9PiBpc05vdGhpbmcobWIpLFxuICAgICAgICAgIEp1c3Q6IGFWYWwgPT4gbWIuaXNKdXN0KCkgJiYgbWIudW5zYWZlbHlVbndyYXAoKSA9PT0gYVZhbCxcbiAgICAgICAgfSk7XG59XG5cbi8qKlxuICBBbGxvd3MgeW91IHRvICphcHBseSogKHRodXMgYGFwYCkgYSB2YWx1ZSB0byBhIGZ1bmN0aW9uIHdpdGhvdXQgaGF2aW5nIHRvXG4gIHRha2UgZWl0aGVyIG91dCBvZiB0aGUgY29udGV4dCBvZiB0aGVpciBgTWF5YmVgcy4gVGhpcyBkb2VzIG1lYW4gdGhhdCB0aGVcbiAgdHJhbnNmb3JtaW5nIGZ1bmN0aW9uIGlzIGl0c2VsZiB3aXRoaW4gYSBgTWF5YmVgLCB3aGljaCBjYW4gYmUgaGFyZCB0byBncm9rXG4gIGF0IGZpcnN0IGJ1dCBsZXRzIHlvdSBkbyBzb21lIHZlcnkgZWxlZ2FudCB0aGluZ3MuIEZvciBleGFtcGxlLCBgYXBgIGFsbG93c1xuICB5b3UgdG8gdGhpczpcblxuICBgYGB0c1xuICBpbXBvcnQgeyBqdXN0LCBub3RoaW5nIH0gZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICBjb25zdCBvbmUgPSBqdXN0KDEpO1xuICBjb25zdCBmaXZlID0ganVzdCg1KTtcbiAgY29uc3Qgbm9uZSA9IG5vdGhpbmcoKTtcblxuICBjb25zdCBhZGQgPSAoYTogbnVtYmVyKSA9PiAoYjogbnVtYmVyKSA9PiBhICsgYjtcbiAgY29uc3QgbWF5YmVBZGQgPSBqdXN0KGFkZCk7XG5cbiAgbWF5YmVBZGQuYXAob25lKS5hcChmaXZlKTsgLy8gSnVzdCg2KVxuICBtYXliZUFkZC5hcChvbmUpLmFwKG5vbmUpOyAvLyBOb3RoaW5nXG4gIG1heWJlQWRkLmFwKG5vbmUpLmFwKGZpdmUpIC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgV2l0aG91dCBgTWF5YmUuYXBgLCB5b3UnZCBuZWVkIHRvIGRvIHNvbWV0aGluZyBsaWtlIGEgbmVzdGVkIGBNYXliZS5tYXRjaGA6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IHsganVzdCwgbm90aGluZyB9IGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgY29uc3Qgb25lID0ganVzdCgxKTtcbiAgY29uc3QgZml2ZSA9IGp1c3QoNSk7XG4gIGNvbnN0IG5vbmUgPSBub3RoaW5nKCk7XG5cbiAgb25lLm1hdGNoKHtcbiAgICBKdXN0OiBuID0+IGZpdmUubWF0Y2goe1xuICAgICAgSnVzdDogbyA9PiBqdXN0KG4gKyBvKSxcbiAgICAgIE5vdGhpbmc6ICgpID0+IG5vdGhpbmcoKSxcbiAgICB9KSxcbiAgICBOb3RoaW5nOiAoKSAgPT4gbm90aGluZygpLFxuICB9KTsgLy8gSnVzdCg2KVxuXG4gIG9uZS5tYXRjaCh7XG4gICAgSnVzdDogbiA9PiBub25lLm1hdGNoKHtcbiAgICAgIEp1c3Q6IG8gPT4ganVzdChuICsgbyksXG4gICAgICBOb3RoaW5nOiAoKSA9PiBub3RoaW5nKCksXG4gICAgfSksXG4gICAgTm90aGluZzogKCkgID0+IG5vdGhpbmcoKSxcbiAgfSk7IC8vIE5vdGhpbmdcblxuICBub25lLm1hdGNoKHtcbiAgICBKdXN0OiBuID0+IGZpdmUubWF0Y2goe1xuICAgICAgSnVzdDogbyA9PiBqdXN0KG4gKyBvKSxcbiAgICAgIE5vdGhpbmc6ICgpID0+IG5vdGhpbmcoKSxcbiAgICB9KSxcbiAgICBOb3RoaW5nOiAoKSAgPT4gbm90aGluZygpLFxuICB9KTsgLy8gTm90aGluZ1xuICBgYGBcblxuICBBbmQgdGhpcyBraW5kIG9mIHRoaW5nIGNvbWVzIHVwIHF1aXRlIG9mdGVuIG9uY2UgeW91J3JlIHVzaW5nIGBNYXliZWAgdG9cbiAgaGFuZGxlIG9wdGlvbmFsaXR5IHRocm91Z2hvdXQgeW91ciBhcHBsaWNhdGlvbi5cblxuICBGb3IgYW5vdGhlciBleGFtcGxlLCBpbWFnaW5lIHlvdSBuZWVkIHRvIGNvbXBhcmUgdGhlIGVxdWFsaXR5IG9mIHR3b1xuICBJbW11dGFibGVKUyBkYXRhIHN0cnVjdHVyZXMsIHdoZXJlIGEgYD09PWAgY29tcGFyaXNvbiB3b24ndCB3b3JrLiBXaXRoIGBhcGAsXG4gIHRoYXQncyBhcyBzaW1wbGUgYXMgdGhpczpcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcbiAgaW1wb3J0IEltbXV0YWJsZSBmcm9tICdpbW11dGFibGUnO1xuICBpbXBvcnQgeyBjdXJyeSB9IGZyb20gJ2xvZGFzaCdcblxuICBjb25zdCBpcyA9IGN1cnJ5KEltbXV0YWJsZS5pcyk7XG5cbiAgY29uc3QgeCA9IE1heWJlLm9mKEltbXV0YWJsZS5TZXQub2YoMSwgMiwgMykpO1xuICBjb25zdCB5ID0gTWF5YmUub2YoSW1tdXRhYmxlLlNldC5vZigyLCAzLCA0KSk7XG5cbiAgTWF5YmUub2YoaXMpLmFwKHgpLmFwKHkpOyAvLyBKdXN0KGZhbHNlKVxuICBgYGBcblxuICBXaXRob3V0IGBhcGAsIHdlJ3JlIGJhY2sgdG8gdGhhdCBnbmFybHkgbmVzdGVkIGBtYXRjaGA6XG5cbiAgYGBgdHNcbiAgICogaW1wb3J0IE1heWJlLCB7IGp1c3QsIG5vdGhpbmcgfSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuICBpbXBvcnQgSW1tdXRhYmxlIGZyb20gJ2ltbXV0YWJsZSc7XG4gIGltcG9ydCB7IGN1cnJ5IH0gZnJvbSAnbG9kYXNoJ1xuXG4gIGNvbnN0IGlzID0gY3VycnkoSW1tdXRhYmxlLmlzKTtcblxuICBjb25zdCB4ID0gTWF5YmUub2YoSW1tdXRhYmxlLlNldC5vZigxLCAyLCAzKSk7XG4gIGNvbnN0IHkgPSBNYXliZS5vZihJbW11dGFibGUuU2V0Lm9mKDIsIDMsIDQpKTtcblxuICB4Lm1hdGNoKHtcbiAgICBKdXN0OiBpWCA9PiB5Lm1hdGNoKHtcbiAgICAgIEp1c3Q6IGlZID0+IE1heWJlLmp1c3QoSW1tdXRhYmxlLmlzKGlYLCBpWSkpLFxuICAgICAgTm90aGluZzogKCkgPT4gTWF5YmUubm90aGluZygpLFxuICAgIH0pXG4gICAgTm90aGluZzogKCkgPT4gTWF5YmUubm90aGluZygpLFxuICB9KTsgLy8gSnVzdChmYWxzZSlcbiAgYGBgXG5cbiAgSW4gc3VtbWFyeTogYW55d2hlcmUgeW91IGhhdmUgdHdvIGBNYXliZWAgaW5zdGFuY2VzIGFuZCBuZWVkIHRvIHBlcmZvcm0gYW5cbiAgb3BlcmF0aW9uIHRoYXQgdXNlcyBib3RoIG9mIHRoZW0sIGBhcGAgaXMgeW91ciBmcmllbmQuXG5cbiAgVHdvIHRoaW5ncyB0byBub3RlLCBib3RoIHJlZ2FyZGluZyAqY3VycnlpbmcqOlxuXG4gIDEuICBBbGwgZnVuY3Rpb25zIHBhc3NlZCB0byBgYXBgIG11c3QgYmUgY3VycmllZC4gVGhhdCBpcywgdGhleSBtdXN0IGJlIG9mIHRoZVxuICAgICAgZm9ybSAoZm9yIGFkZCkgYChhOiBudW1iZXIpID0+IChiOiBudW1iZXIpID0+IGEgKyBiYCwgKm5vdCogdGhlIG1vcmUgdXN1YWxcbiAgICAgIGAoYTogbnVtYmVyLCBiOiBudW1iZXIpID0+IGEgKyBiYCB5b3Ugc2VlIGluIEphdmFTY3JpcHQgbW9yZSBnZW5lcmFsbHkuXG5cbiAgICAgIEZvciBjb252ZW5pZW5jZSwgeW91IG1heSB3YW50IHRvIGxvb2sgYXQgTG9kYXNoJ3MgYF8uY3VycnlgIG9yIFJhbWRhJ3NcbiAgICAgIGBSLmN1cnJ5YCwgd2hpY2ggYWxsb3cgeW91IHRvIGNyZWF0ZSBjdXJyaWVkIHZlcnNpb25zIG9mIGZ1bmN0aW9uc1xuICAgICAgd2hlbmV2ZXIgeW91IHdhbnQ6XG5cbiAgICAgIGBgYFxuICAgICAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG4gICAgICBpbXBvcnQgeyBjdXJyeSB9IGZyb20gJ2xvZGFzaCc7XG5cbiAgICAgIGNvbnN0IG5vcm1hbEFkZCA9IChhOiBudW1iZXIsIGI6IG51bWJlcikgPT4gYSArIGI7XG4gICAgICBjb25zdCBjdXJyaWVkQWRkID0gY3Vycnkobm9ybWFsQWRkKTsgLy8gKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGI7XG5cbiAgICAgIE1heWJlLm9mKGN1cnJpZWRBZGQpLmFwKE1heWJlLm9mKDEpKS5hcChNYXliZS5vZig1KSk7IC8vIEp1c3QoNilcbiAgICAgIGBgYFxuXG4gIDIuICBZb3Ugd2lsbCBuZWVkIHRvIGNhbGwgYGFwYCBhcyBtYW55IHRpbWVzIGFzIHRoZXJlIGFyZSBhcmd1bWVudHMgdG8gdGhlXG4gICAgICBmdW5jdGlvbiB5b3UncmUgZGVhbGluZyB3aXRoLiBTbyBpbiB0aGUgY2FzZSBvZiBgYWRkYCwgd2hpY2ggaGFzIHRoZVxuICAgICAgXCJhcml0eVwiIChmdW5jdGlvbiBhcmd1bWVudCBjb3VudCkgb2YgMiAoYGFgIGFuZCBgYmApLCB5b3UnbGwgbmVlZCB0byBjYWxsXG4gICAgICBgYXBgIHR3aWNlOiBvbmNlIGZvciBgYWAsIGFuZCBvbmNlIGZvciBgYmAuIFRvIHNlZSB3aHksIGxldCdzIGxvb2sgYXQgd2hhdFxuICAgICAgdGhlIHJlc3VsdCBpbiBlYWNoIHBoYXNlIGlzOlxuXG4gICAgICBgYGB0c1xuICAgICAgY29uc3QgYWRkID0gKGE6IG51bWJlcikgPT4gKGI6IG51bWJlcikgPT4gYSArIGI7XG5cbiAgICAgIGNvbnN0IG1heWJlQWRkID0gTWF5YmUub2YoYWRkKTsgLy8gSnVzdCgoYTogbnVtYmVyKSA9PiAoYjogbnVtYmVyKSA9PiBhICsgYilcbiAgICAgIGNvbnN0IG1heWJlQWRkMSA9IG1heWJlQWRkLmFwKE1heWJlLm9mKDEpKTsgLy8gSnVzdCgoYjogbnVtYmVyKSA9PiAxICsgYilcbiAgICAgIGNvbnN0IGZpbmFsID0gbWF5YmVBZGQxLmFwKE1heWJlLm9mKDMpKTsgLy8gSnVzdCg0KVxuICAgICAgYGBgXG5cbiAgICAgIFNvIGZvciBgdG9TdHJpbmdgLCB3aGljaCBqdXN0IHRha2VzIGEgc2luZ2xlIGFyZ3VtZW50LCB5b3Ugd291bGQgb25seSBuZWVkXG4gICAgICB0byBjYWxsIGBhcGAgb25jZS5cblxuICAgICAgYGBgdHNcbiAgICAgIGNvbnN0IHRvU3RyID0gKHY6IHsgdG9TdHJpbmcoKTogc3RyaW5nIH0pID0+IHYudG9TdHJpbmcoKTtcbiAgICAgIE1heWJlLm9mKHRvU3RyKS5hcCgxMik7IC8vIEp1c3QoXCIxMlwiKVxuICAgICAgYGBgXG5cbiAgT25lIG90aGVyIHNjZW5hcmlvIHdoaWNoIGRvZXNuJ3QgY29tZSB1cCAqcXVpdGUqIGFzIG9mdGVuIGJ1dCBpcyBjb25jZWl2YWJsZVxuICBpcyB3aGVyZSB5b3UgaGF2ZSBzb21ldGhpbmcgdGhhdCBtYXkgb3IgbWF5IG5vdCBhY3R1YWxseSBjb25zdHJ1Y3QgYSBmdW5jdGlvblxuICBmb3IgaGFuZGxpbmcgYSBzcGVjaWZpYyBgTWF5YmVgIHNjZW5hcmlvLiBJbiB0aGF0IGNhc2UsIHlvdSBjYW4gd3JhcCB0aGVcbiAgcG9zc2libHktcHJlc2VudCBpbiBgYXBgIGFuZCB0aGVuIHdyYXAgdGhlIHZhbHVlcyB0byBhcHBseSB0byB0aGUgZnVuY3Rpb24gdG9cbiAgaW4gYE1heWJlYCB0aGVtc2VsdmVzLlxuXG4gICoqQXNpZGU6KiogYGFwYCBpcyBub3QgbmFtZWQgYGFwcGx5YCBiZWNhdXNlIG9mIHRoZSBvdmVybGFwIHdpdGggSmF2YVNjcmlwdCdzXG4gIGV4aXN0aW5nIFtgYXBwbHlgXSBmdW5jdGlvbiDigJMgYW5kIGFsdGhvdWdoIHN0cmljdGx5IHNwZWFraW5nLCB0aGVyZSBpc24ndCBhbnlcbiAgZGlyZWN0IG92ZXJsYXAgKGBNYXliZS5hcHBseWAgYW5kIGBGdW5jdGlvbi5wcm90b3R5cGUuYXBwbHlgIGRvbid0IGludGVyc2VjdFxuICBhdCBhbGwpIGl0J3MgdXNlZnVsIHRvIGhhdmUgYSBkaWZmZXJlbnQgbmFtZSB0byBhdm9pZCBpbXBseWluZyB0aGF0IHRoZXkncmVcbiAgdGhlIHNhbWUuXG5cbiAgW2BhcHBseWBdOiBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9KYXZhU2NyaXB0L1JlZmVyZW5jZS9HbG9iYWxfT2JqZWN0cy9GdW5jdGlvbi9hcHBseVxuXG4gIEBwYXJhbSBtYXliZUZuIG1heWJlIGEgZnVuY3Rpb24gZnJvbSBUIHRvIFVcbiAgQHBhcmFtIG1heWJlIG1heWJlIGEgVCB0byBhcHBseSB0byBgZm5gXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhcDxULCBVPihtYXliZUZuOiBNYXliZTwodDogVCkgPT4gVT4sIG1heWJlOiBNYXliZTxUPik6IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFwPFQsIFU+KG1heWJlRm46IE1heWJlPCh0OiBUKSA9PiBVPik6IChtYXliZTogTWF5YmU8VD4pID0+IE1heWJlPFU+O1xuZXhwb3J0IGZ1bmN0aW9uIGFwPFQsIFU+KFxuICBtYXliZUZuOiBNYXliZTwodmFsOiBUKSA9PiBVPixcbiAgbWF5YmU/OiBNYXliZTxUPlxuKTogTWF5YmU8VT4gfCAoKHZhbDogTWF5YmU8VD4pID0+IE1heWJlPFU+KSB7XG4gIGNvbnN0IG9wID0gKG06IE1heWJlPFQ+KSA9PlxuICAgIG0ubWF0Y2goe1xuICAgICAgSnVzdDogdmFsID0+IG1heWJlRm4ubWFwKGZuID0+IGZuKHZhbCkpLFxuICAgICAgTm90aGluZzogKCkgPT4gTWF5YmUubm90aGluZzxVPigpLFxuICAgIH0pO1xuXG4gIHJldHVybiBjdXJyeTEob3AsIG1heWJlKTtcbn1cblxuLyoqXG4gIERldGVybWluZSB3aGV0aGVyIGFuIGl0ZW0gaXMgYW4gaW5zdGFuY2Ugb2YgYEp1c3RgIG9yIGBOb3RoaW5nYC5cblxuICBAcGFyYW0gaXRlbSBUaGUgaXRlbSB0byBjaGVjay5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzSW5zdGFuY2U8VCA9IGFueT4oaXRlbTogYW55KTogaXRlbSBpcyBNYXliZTxUPiB7XG4gIHJldHVybiBpdGVtIGluc3RhbmNlb2YgSnVzdCB8fCBpdGVtIGluc3RhbmNlb2YgTm90aGluZztcbn1cblxudHlwZSBQcmVkaWNhdGU8VD4gPSAoZWxlbWVudDogVCwgaW5kZXg6IG51bWJlciwgYXJyYXk6IFRbXSkgPT4gYm9vbGVhbjtcblxuLy8gTk9URTogZG9jdW1lbnRhdGlvbiBpcyBsaWdodGx5IGFkYXB0ZWQgZnJvbSB0aGUgTUROIGFuZCBUeXBlU2NyaXB0IGRvY3MgZm9yXG4vLyBgQXJyYXkucHJvdG90eXBlLmZpbmRgLlxuLyoqXG4gIFNhZmVseSBzZWFyY2ggZm9yIGFuIGVsZW1lbnQgaW4gYW4gYXJyYXkuXG4gIFxuICBUaGlzIGZ1bmN0aW9uIGJlaGF2ZXMgbGlrZSBgQXJyYXkucHJvdG90eXBlLmZpbmRgLCBidXQgcmV0dXJucyBgTWF5YmU8VD5gXG4gIGluc3RlYWQgb2YgYFQgfCB1bmRlZmluZWRgLlxuICBcbiAgIyMgRXhhbXBsZXNcblxuICBUaGUgYmFzaWMgZm9ybSBpczpcblxuICBgYGB0c1xuICBpbXBvcnQgTWF5YmUgZnJvbSAndHJ1ZS1teXRoL21heWJlJztcblxuICBsZXQgYXJyYXkgPSBbMSwgMiwgM107XG4gIE1heWJlLmZpbmQodiA9PiB2ID4gMSwgYXJyYXkpOyAvLyBKdXN0KDIpXG4gIE1heWJlLmZpbmQodiA9PiB2IDwgMSwgYXJyYXkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIFRoZSBmdW5jdGlvbiBpcyBjdXJyaWVkIHNvIHlvdSBjYW4gdXNlIGl0IGluIGEgZnVuY3Rpb25hbCBjaGFpbi4gRm9yIGV4YW1wbGVcbiAgKGxlYXZpbmcgYXNpZGUgZXJyb3IgaGFuZGxpbmcgb24gYSBiYWQgcmVzcG9uc2UgZm9yIHNpbXBsaWNpdHkpLCBzdXBwb3NlIHRoZVxuICB1cmwgYGh0dHBzOi8vYXJyYXlzLmV4YW1wbGUuY29tYCByZXR1cm5lZCBhIEpTT04gcGF5bG9hZCB3aXRoIHRoZSB0eXBlXG4gIGBBcnJheTx7IGNvdW50OiBudW1iZXIsIG5hbWU6IHN0cmluZyB9PmAsIGFuZCB3ZSB3YW50ZWQgdG8gZ2V0IHRoZSBmaXJzdFxuICBvZiB0aGVzZSB3aGVyZSBgY291bnRgIHdhcyBhdCBsZWFzdCAxMDAuIFdlIGNvdWxkIHdyaXRlIHRoaXM6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgdHlwZSBJdGVtID0geyBjb3VudDogbnVtYmVyOyBuYW1lOiBzdHJpbmcgfTtcbiAgdHlwZSBSZXNwb25zZSA9IEFycmF5PEl0ZW0+O1xuXG4gIC8vIGN1cnJpZWQgdmFyaWFudCFcbiAgY29uc3QgZmluZEF0TGVhc3QxMDAgPSBNYXliZS5maW5kKCh7IGNvdW50IH06IEl0ZW0pID0+IGNvdW50ID4gMTAwKTtcblxuICBmZXRjaCgnaHR0cHM6Ly9hcnJheXMuZXhhbXBsZS5jb20nKVxuICAgIC50aGVuKHJlc3BvbnNlID0+IHJlc3BvbnNlLmpzb24oKSBhcyBSZXNwb25zZSlcbiAgICAudGhlbihmaW5kQXRMZWFzdDEwMClcbiAgICAudGhlbihmb3VuZCA9PiB7XG4gICAgICBpZiAoZm91bmQuaXNKdXN0KCkpIHtcbiAgICAgICAgY29uc29sZS5sb2coYFRoZSBtYXRjaGluZyB2YWx1ZSBpcyAke2ZvdW5kLnZhbHVlLm5hbWV9IWApO1xuICAgICAgfVxuICAgIH0pO1xuICBgYGBcbiAgXG4gIEBwYXJhbSBwcmVkaWNhdGUgIEEgZnVuY3Rpb24gdG8gZXhlY3V0ZSBvbiBlYWNoIHZhbHVlIGluIHRoZSBhcnJheSwgcmV0dXJuaW5nXG4gICAgICAgICAgICAgICAgICAgIGB0cnVlYCB3aGVuIHRoZSBpdGVtIGluIHRoZSBhcnJheSBtYXRjaGVzIHRoZSBjb25kaXRpb24uIFRoZVxuICAgICAgICAgICAgICAgICAgICBzaWduYXR1cmUgZm9yIGBwcmVkaWNhdGVgIGlzIGlkZW50aWNhbCB0byB0aGUgc2lnbmF0dXJlIGZvclxuICAgICAgICAgICAgICAgICAgICB0aGUgZmlyc3QgYXJndW1lbnQgdG8gYEFycmF5LnByb3RvdHlwZS5maW5kYC4gVGhlIGZ1bmN0aW9uXG4gICAgICAgICAgICAgICAgICAgIGlzIGNhbGxlZCBvbmNlIGZvciBlYWNoIGVsZW1lbnQgb2YgdGhlIGFycmF5LCBpbiBhc2NlbmRpbmdcbiAgICAgICAgICAgICAgICAgICAgb3JkZXIsIHVudGlsIGl0IGZpbmRzIG9uZSB3aGVyZSBwcmVkaWNhdGUgcmV0dXJucyB0cnVlLiBJZlxuICAgICAgICAgICAgICAgICAgICBzdWNoIGFuIGVsZW1lbnQgaXMgZm91bmQsIGZpbmQgaW1tZWRpYXRlbHkgcmV0dXJucyB0aGF0XG4gICAgICAgICAgICAgICAgICAgIGVsZW1lbnQgdmFsdWUgd3JhcHBlZCBpbiBgSnVzdGAuIE90aGVyd2lzZSwgYE1heWJlLmZpbmRgXG4gICAgICAgICAgICAgICAgICAgIHJldHVybnMgYE5vdGhpbmdgLlxuICogQHBhcmFtIGFycmF5ICAgICBUaGUgYXJyYXkgdG8gc2VhcmNoIHVzaW5nIHRoZSBwcmVkaWNhdGUuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBmaW5kPFQ+KHByZWRpY2F0ZTogUHJlZGljYXRlPFQ+LCBhcnJheTogVFtdKTogTWF5YmU8VD47XG5leHBvcnQgZnVuY3Rpb24gZmluZDxUPihwcmVkaWNhdGU6IFByZWRpY2F0ZTxUPik6IChhcnJheTogVFtdKSA9PiBNYXliZTxUPjtcbmV4cG9ydCBmdW5jdGlvbiBmaW5kPFQ+KFxuICBwcmVkaWNhdGU6IFByZWRpY2F0ZTxUPixcbiAgYXJyYXk/OiBUW11cbik6IE1heWJlPFQ+IHwgKChhcnJheTogVFtdKSA9PiBNYXliZTxUPikge1xuICBjb25zdCBvcCA9IChhOiBUW10pID0+IE1heWJlLm9mKGEuZmluZChwcmVkaWNhdGUpKTtcbiAgcmV0dXJuIGN1cnJ5MShvcCwgYXJyYXkpO1xufVxuXG4vKipcbiAgU2FmZWx5IGdldCB0aGUgZmlyc3QgaXRlbSBmcm9tIGEgbGlzdCwgcmV0dXJuaW5nIGBKdXN0YCB0aGUgZmlyc3QgaXRlbSBpZiB0aGVcbiAgYXJyYXkgaGFzIGF0IGxlYXN0IG9uZSBpdGVtIGluIGl0LCBvciBgTm90aGluZ2AgaWYgaXQgaXMgZW1wdHkuXG5cbiAgIyMgRXhhbXBsZXNcblxuICBgYGB0c1xuICBsZXQgZW1wdHkgPSBbXTtcbiAgTWF5YmUuaGVhZChlbXB0eSk7IC8vID0+IE5vdGhpbmdcblxuICBsZXQgZnVsbCA9IFsxLCAyLCAzXTtcbiAgTWF5YmUuaGVhZChmdWxsKTsgLy8gPT4gSnVzdCgxKVxuICBgYGBcblxuICBAcGFyYW0gYXJyYXkgVGhlIGFycmF5IHRvIGdldCB0aGUgZmlyc3QgaXRlbSBmcm9tLlxuICovXG5leHBvcnQgZnVuY3Rpb24gaGVhZDxUPihhcnJheTogQXJyYXk8VCB8IG51bGwgfCB1bmRlZmluZWQ+KTogTWF5YmU8VD4ge1xuICByZXR1cm4gTWF5YmUub2YoYXJyYXlbMF0pO1xufVxuXG4vKiogQSBjb252ZW5pZW5jZSBhbGlhcyBmb3IgYE1heWJlLmhlYWRgLiAqL1xuZXhwb3J0IGNvbnN0IGZpcnN0ID0gaGVhZDtcblxuLyoqXG4gIFNhZmVseSBnZXQgdGhlIGxhc3QgaXRlbSBmcm9tIGEgbGlzdCwgcmV0dXJuaW5nIGBKdXN0YCB0aGUgbGFzdCBpdGVtIGlmIHRoZVxuICBhcnJheSBoYXMgYXQgbGVhc3Qgb25lIGl0ZW0gaW4gaXQsIG9yIGBOb3RoaW5nYCBpZiBpdCBpcyBlbXB0eS5cblxuICAjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGxldCBlbXB0eSA9IFtdO1xuICBNYXliZS5sYXN0KGVtcHR5KTsgLy8gPT4gTm90aGluZ1xuXG4gIGxldCBmdWxsID0gWzEsIDIsIDNdO1xuICBNYXliZS5sYXN0KGZ1bGwpOyAvLyA9PiBKdXN0KDMpXG4gIGBgYFxuXG4gIEBwYXJhbSBhcnJheSBUaGUgYXJyYXkgdG8gZ2V0IHRoZSBmaXJzdCBpdGVtIGZyb20uXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBsYXN0PFQ+KGFycmF5OiBBcnJheTxUIHwgbnVsbCB8IHVuZGVmaW5lZD4pOiBNYXliZTxUPiB7XG4gIHJldHVybiBNYXliZS5vZihhcnJheVthcnJheS5sZW5ndGggLSAxXSk7XG59XG5cbi8qKlxuICBDb252ZXJ0IHRoZSBhcmd1bWVudHMgdG8gYSBzaW5nbGUgYE1heWJlYC4gVXNlZnVsIGZvciBkZWFsaW5nIHdpdGggYXJyYXlzIG9mXG4gIGBNYXliZWBzLCB2aWEgdGhlIHNwcmVhZCBvcGVyYXRvci5cblxuICAjIyBFeGFtcGxlc1xuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIGxldCB2YWxpZCA9IFtNYXliZS5qdXN0KDIpLCBNYXliZS5qdXN0KCd0aHJlZScpXTtcbiAgTWF5YmUuYWxsKC4uLnZhbGlkKTsgLy8gPT4gSnVzdChbMiwgJ3RocmVlJ10pO1xuXG4gIGxldCBpbnZhbGlkID0gW01heWJlLmp1c3QoMiksIE1heWJlLm5vdGhpbmc8c3RyaW5nPigpXTtcbiAgTWF5YmUuYWxsKC4uLmludmFsaWQpOyAvLyA9PiBOb3RoaW5nXG4gIGBgYFxuXG4gICMjIE5vdGUgb24gU3ByZWFkXG5cbiAgVGhpcyByZXF1aXJlcyB0aGUgdXNlIG9mIHRoZSBzcHJlYWQgb3BlcmF0b3IgYmVjYXVzZSAoYXQgbGVhc3QgYXMgb2ZcbiAgVHlwZVNjcmlwdCAzLjApLCB0aGUgdHlwZSBpbmZlcmVuY2UgZmFsbHMgZG93biB3aGVuIGF0dGVtcHRpbmcgdG8gYnVpbGQgdGhpc1xuICBzYW1lIHR5cGUgd2l0aCBhbiBhcnJheSBkaXJlY3RseS4gTW9yZW92ZXIsIHRoaXMgc3ByZWFkLWJhc2VkIGFwcHJvYWNoIGhhbmRsZXNcbiAgaGV0ZXJlZ2Vub3VzIGFycmF5czsgVFMgKmFsc28qIGZhaWxzIHRvIGluZmVyIGNvcnJlY3RseSBmb3IgYW55dGhpbmcgYnV0XG4gIGhvbW9nZW5lb3VzIGFycmF5cyB3aGVuIHVzaW5nIHRoYXQgYXBwcm9hY2guXG5cbiAgQHBhcmFtIG1heWJlcyBUaGUgYE1heWJlYHMgdG8gcmVzb2x2ZSB0byBhIHNpbmdsZSBgTWF5YmVgLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYWxsPFQgZXh0ZW5kcyBBcnJheTxNYXliZTx1bmtub3duPj4+KC4uLm1heWJlczogVCk6IEFsbDxUPiB7XG4gIGxldCByZXN1bHQ6IEFsbDxUPiA9IE1heWJlLmp1c3QoW10gYXMgTWF5YmU8dW5rbm93bj5bXSkgYXMgQWxsPFQ+O1xuICBtYXliZXMuZm9yRWFjaChtYXliZSA9PiB7XG4gICAgcmVzdWx0ID0gcmVzdWx0LmFuZFRoZW4oYWNjdW11bGF0ZWRNYXliZXMgPT5cbiAgICAgIG1heWJlLm1hcChtID0+IHtcbiAgICAgICAgYWNjdW11bGF0ZWRNYXliZXMucHVzaChtKTtcbiAgICAgICAgcmV0dXJuIGFjY3VtdWxhdGVkTWF5YmVzO1xuICAgICAgfSlcbiAgICApIGFzIEFsbDxUPjtcbiAgfSk7XG5cbiAgcmV0dXJuIHJlc3VsdDtcbn1cblxudHlwZSBBbGw8VCBleHRlbmRzIEFycmF5PE1heWJlPGFueT4+PiA9IFQgZXh0ZW5kcyBBcnJheTxNYXliZTxpbmZlciBVPj4gPyBNYXliZTxBcnJheTxVPj4gOiBuZXZlcjtcblxuLyoqXG4gIEdpdmVuIGEgdHVwbGUgb2YgYE1heWJlYHMsIHJldHVybiBhIGBNYXliZWAgb2YgdGhlIHR1cGxlIHZhbHVlcy5cblxuICBHaXZlbiBhIHR1cGxlIG9mIHR5cGUgYFtNYXliZTxBPiwgTWF5YmU8Qj5dYCwgdGhlIHJlc3VsdGluZyB0eXBlIGlzXG4gIGBNYXliZTxbQSwgQl0+YC4gV29ya3Mgd2l0aCB1cCB0byBhIDUtdHVwbGUuIChJZiB5b3UncmUgZG9pbmcgbW9yZSB0aGFuIGFcbiAgNS10dXBsZSwgd2hhdCBhcmUgeW91IGRvaW5nPz8/KVxuXG4gICMjIEV4YW1wbGVzXG5cbiAgSWYgYW55IG9mIHRoZSBpdGVtcyBpbiB0aGUgdHVwbGUgYXJlIGBOb3RoaW5nYCwgdGhlIHdob2xlIHJlc3VsdCBpcyBgTm90aGluZ2AuXG4gIEhlcmUsIGZvciBleGFtcGxlLCBgcmVzdWx0YCBoYXMgdGhlIHR5cGUgYE1heWJlPFtzdHJpbmcsIG51bWJlcl0+YCBhbmQgd2lsbCBiZVxuICBgTm90aGluZ2A6XG5cbiAgYGBgdHNcbiAgaW1wb3J0IE1heWJlIGZyb20gJ3RydWUtbXl0aC9tYXliZSc7XG5cbiAgdHlwZSBUdXBsZSA9IFtNYXliZTxzdHJpbmc+LCBNYXliZTxudW1iZXI+XTtcblxuICBsZXQgaW52YWxpZDogVHVwbGUgPSBbTWF5YmUuanVzdCgnd2F0JyksIE1heWJlLm5vdGhpbmcoKV07XG4gIGxldCByZXN1bHQgPSBNYXliZS50dXBsZShpbnZhbGlkKTsgIC8vID0+IE5vdGhpbmdcbiAgYGBgXG5cbiAgSWYgYWxsIG9mIHRoZSBpdGVtcyBpbiB0aGUgdHVwbGUgYXJlIGBKdXN0YCwgdGhlIHJlc3VsdCBpcyBgSnVzdGAgd3JhcHBpbmcgdGhlXG4gIHR1cGxlIG9mIHRoZSB2YWx1ZXMgb2YgdGhlIGl0ZW1zLiBIZXJlLCBmb3IgZXhhbXBsZSwgYHJlc3VsdGAgYWdhaW4gaGFzIHRoZVxuICB0eXBlIGBNYXliZTxbc3RyaW5nLCBudW1iZXJdPmAgYW5kIHdpbGwgYmUgYEp1c3QoWydoZXknLCAxMl1gOlxuXG4gIGBgYHRzXG4gIGltcG9ydCBNYXliZSBmcm9tICd0cnVlLW15dGgvbWF5YmUnO1xuXG4gIHR5cGUgVHVwbGUgPSBbTWF5YmU8c3RyaW5nPiwgTWF5YmU8bnVtYmVyPl07XG5cbiAgbGV0IHZhbGlkOiBUdXBsZSA9IFtNYXliZS5qdXN0KCdoZXknKSwgTWF5YmUuanVzdCgxMildO1xuICBsZXQgcmVzdWx0ID0gTWF5YmUudHVwbGUodmFsaWQpOyAgLy8gPT4gSnVzdChbJ2hleScsIDEyXSlcbiAgYGBgXG5cbiAgQHBhcmFtIG1heWJlczogdGhlIHR1cGxlIG9mIGBNYXliZWBzIHRvIGNvbnZlcnQgdG8gYSBgTWF5YmVgIG9mIHR1cGxlIHZhbHVlcy5cbiAqL1xuLy8gQHRzLWlnbm9yZSAtLSB0aGlzIGRvZXNuJ3QgdHlwZS1jaGVjaywgYnV0IGl0IGlzIGNvcnJlY3QhXG5leHBvcnQgZnVuY3Rpb24gdHVwbGU8VD4obWF5YmVzOiBbTWF5YmU8VD5dKTogTWF5YmU8W1RdPjtcbmV4cG9ydCBmdW5jdGlvbiB0dXBsZTxULCBVPihtYXliZXM6IFtNYXliZTxUPiwgTWF5YmU8VT5dKTogTWF5YmU8W1QsIFVdPjtcbmV4cG9ydCBmdW5jdGlvbiB0dXBsZTxULCBVLCBWPihtYXliZXM6IFtNYXliZTxUPiwgTWF5YmU8VT4sIE1heWJlPFY+XSk6IE1heWJlPFtULCBVLCBWXT47XG5leHBvcnQgZnVuY3Rpb24gdHVwbGU8VCwgVSwgViwgVz4oXG4gIG1heWJlczogW01heWJlPFQ+LCBNYXliZTxVPiwgTWF5YmU8Vj4sIE1heWJlPFc+XVxuKTogTWF5YmU8W1QsIFUsIFYsIFddPjtcbmV4cG9ydCBmdW5jdGlvbiB0dXBsZTxULCBVLCBWLCBXLCBYPihcbiAgbWF5YmVzOiBbTWF5YmU8VD4sIE1heWJlPFU+LCBNYXliZTxWPiwgTWF5YmU8Vz4sIE1heWJlPFg+XVxuKTogTWF5YmU8W1QsIFUsIFYsIFcsIFhdPiB7XG4gIC8vIEB0cy1pZ25vcmUgLS0gdGhpcyBkb2Vzbid0IHR5cGUtY2hlY2ssIGJ1dCBpdCB3b3JrcyBjb3JyZWN0bHkuXG4gIHJldHVybiBhbGwoLi4ubWF5YmVzKTtcbn1cblxuLyoqXG4gIFNhZmVseSBleHRyYWN0IGEga2V5IGZyb20gYW4gb2JqZWN0LCByZXR1cm5pbmcgYEp1c3RgIGlmIHRoZSBrZXkgaGFzIGEgdmFsdWVcbiAgb24gdGhlIG9iamVjdCBhbmQgYE5vdGhpbmdgIGlmIGl0IGRvZXMgbm90LlxuXG4gIFRoZSBjaGVjayBpcyB0eXBlLXNhZmU6IHlvdSB3b24ndCBldmVuIGJlIGFibGUgdG8gY29tcGlsZSBpZiB5b3UgdHJ5IHRvIGxvb2tcbiAgdXAgYSBwcm9wZXJ0eSB0aGF0IFR5cGVTY3JpcHQgKmtub3dzKiBkb2Vzbid0IGV4aXN0IG9uIHRoZSBvYmplY3QuXG5cbiAgYGBgdHNcbiAgdHlwZSBQZXJzb24gPSB7IG5hbWU/OiBzdHJpbmcgfTtcblxuICBjb25zdCBtZTogUGVyc29uID0geyBuYW1lOiAnQ2hyaXMnIH07XG4gIGNvbnNvbGUubG9nKE1heWJlLnByb3BlcnR5KCduYW1lJywgbWUpKTsgLy8gSnVzdCgnQ2hyaXMnKVxuXG4gIGNvbnN0IG5vYm9keTogUGVyc29uID0ge307XG4gIGNvbnNvbGUubG9nKE1heWJlLnByb3BlcnR5KCduYW1lJywgbm9ib2R5KSk7IC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgSG93ZXZlciwgaXQgYWxzbyB3b3JrcyBjb3JyZWN0bHkgd2l0aCBkaWN0aW9uYXJ5IHR5cGVzOlxuXG4gIGBgYHRzXG4gIHR5cGUgRGljdDxUPiA9IHsgW2tleTogc3RyaW5nXTogVCB9O1xuXG4gIGNvbnN0IHNjb3JlOiBEaWN0PG51bWJlcj4gPSB7XG4gICAgcGxheWVyMTogMCxcbiAgICBwbGF5ZXIyOiAxXG4gIH07XG5cbiAgY29uc29sZS5sb2coTWF5YmUucHJvcGVydHkoJ3BsYXllcjEnLCBzY29yZSkpOyAvLyBKdXN0KDApXG4gIGNvbnNvbGUubG9nKE1heWJlLnByb3BlcnR5KCdwbGF5ZXIyJywgc2NvcmUpKTsgLy8gSnVzdCgxKVxuICBjb25zb2xlLmxvZyhNYXliZS5wcm9wZXJ0eSgncGxheWVyMycsIHNjb3JlKSk7IC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgVGhlIG9yZGVyIG9mIGtleXMgaXMgc28gdGhhdCBpdCBjYW4gYmUgcGFydGlhbGx5IGFwcGxpZWQ6XG5cbiAgYGBgdHNcbiAgdHlwZSBQZXJzb24gPSB7IG5hbWU/OiBzdHJpbmcgfTtcbiAgXG4gIGNvbnN0IGxvb2t1cE5hbWUgPSBNYXliZS5wcm9wZXJ0eSgnbmFtZScpO1xuICBcbiAgY29uc3QgbWU6IFBlcnNvbiA9IHsgbmFtZTogJ0NocmlzJyB9O1xuICBjb25zb2xlLmxvZyhsb29rdXBOYW1lKG1lKSk7IC8vIEp1c3QoJ0NocmlzJylcblxuICBjb25zdCBub2JvZHk6IFBlcnNvbiA9IHt9O1xuICBjb25zb2xlLmxvZyhsb29rdXBOYW1lKG5vYm9keSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuICBcbiAgQHBhcmFtIGtleSBUaGUga2V5IHRvIHB1bGwgb3V0IG9mIHRoZSBvYmplY3QuXG4gIEBwYXJhbSBvYmogVGhlIG9iamVjdCB0byBsb29rIHVwIHRoZSBrZXkgZnJvbS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHByb3BlcnR5PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPihrZXk6IEssIG9iajogVCk6IE1heWJlPE5vbk51bGxhYmxlPFRbS10+PjtcbmV4cG9ydCBmdW5jdGlvbiBwcm9wZXJ0eTxULCBLIGV4dGVuZHMga2V5b2YgVD4oa2V5OiBLKTogKG9iajogVCkgPT4gTWF5YmU8Tm9uTnVsbGFibGU8VFtLXT4+O1xuZXhwb3J0IGZ1bmN0aW9uIHByb3BlcnR5PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPihcbiAga2V5OiBLLFxuICBvYmo/OiBUXG4pOiBNYXliZTxOb25OdWxsYWJsZTxUW0tdPj4gfCAoKG9iajogVCkgPT4gTWF5YmU8Tm9uTnVsbGFibGU8VFtLXT4+KSB7XG4gIGNvbnN0IG9wID0gKGE6IFQpID0+IE1heWJlLm9mKGFba2V5XSkgYXMgTWF5YmU8Tm9uTnVsbGFibGU8VFtLXT4+O1xuICByZXR1cm4gY3VycnkxKG9wLCBvYmopO1xufVxuXG4vKipcbiAgU2FmZWx5IGV4dHJhY3QgYSBrZXkgZnJvbSBhIE1heWJlIG9mIGFuIG9iamVjdCwgcmV0dXJuaW5nIGBKdXN0YCBpZiB0aGUga2V5XG4gIGhhcyBhIHZhbHVlIG9uIHRoZSBvYmplY3QgYW5kIGBOb3RoaW5nYCBpZiBpdCBkb2VzIG5vdC4gKExpa2UgYE1heWJlLnByb3BlcnR5YFxuICBidXQgb3BlcmF0aW5nIG9uIGEgYE1heWJlPFQ+YCByYXRoZXIgdGhhbiBkaXJlY3RseSBvbiBhIGBUYC4pXG5cbiAgVGhlIGNoZWNrIGlzIHR5cGUtc2FmZTogeW91IHdvbid0IGV2ZW4gYmUgYWJsZSB0byBjb21waWxlIGlmIHlvdSB0cnkgdG8gbG9va1xuICB1cCBhIHByb3BlcnR5IHRoYXQgVHlwZVNjcmlwdCAqa25vd3MqIGRvZXNuJ3QgZXhpc3Qgb24gdGhlIG9iamVjdC5cblxuICBgYGB0c1xuICB0eXBlIFBlcnNvbiA9IHsgbmFtZT86IHN0cmluZyB9O1xuXG4gIGNvbnN0IG1lOiBNYXliZTxQZXJzb24+ID0gTWF5YmUuanVzdCh7IG5hbWU6ICdDaHJpcycgfSk7XG4gIGNvbnNvbGUubG9nKE1heWJlLmdldCgnbmFtZScsIG1lKSk7IC8vIEp1c3QoJ0NocmlzJylcblxuICBjb25zdCBub2JvZHkgPSBNYXliZS5ub3RoaW5nPFBlcnNvbj4oKTtcbiAgY29uc29sZS5sb2coTWF5YmUuZ2V0KCduYW1lJywgbm9ib2R5KSk7IC8vIE5vdGhpbmdcbiAgYGBgXG5cbiAgSG93ZXZlciwgaXQgYWxzbyB3b3JrcyBjb3JyZWN0bHkgd2l0aCBkaWN0aW9uYXJ5IHR5cGVzOlxuXG4gIGBgYHRzXG4gIHR5cGUgRGljdDxUPiA9IHsgW2tleTogc3RyaW5nXTogVCB9O1xuXG4gIGNvbnN0IHNjb3JlOiBNYXliZTxEaWN0PG51bWJlcj4+ID0gTWF5YmUuanVzdCh7XG4gICAgcGxheWVyMTogMCxcbiAgICBwbGF5ZXIyOiAxXG4gIH0pO1xuXG4gIGNvbnNvbGUubG9nKE1heWJlLmdldCgncGxheWVyMScsIHNjb3JlKSk7IC8vIEp1c3QoMClcbiAgY29uc29sZS5sb2coTWF5YmUuZ2V0KCdwbGF5ZXIyJywgc2NvcmUpKTsgLy8gSnVzdCgxKVxuICBjb25zb2xlLmxvZyhNYXliZS5nZXQoJ3BsYXllcjMnLCBzY29yZSkpOyAvLyBOb3RoaW5nXG4gIGBgYFxuXG4gIFRoZSBvcmRlciBvZiBrZXlzIGlzIHNvIHRoYXQgaXQgY2FuIGJlIHBhcnRpYWxseSBhcHBsaWVkOlxuXG4gIGBgYHRzXG4gIHR5cGUgUGVyc29uID0geyBuYW1lPzogc3RyaW5nIH07XG4gIFxuICBjb25zdCBsb29rdXBOYW1lID0gTWF5YmUuZ2V0KCduYW1lJyk7XG4gIFxuICBjb25zdCBtZTogUGVyc29uID0geyBuYW1lOiAnQ2hyaXMnIH07XG4gIGNvbnNvbGUubG9nKGxvb2t1cE5hbWUobWUpKTsgLy8gSnVzdCgnQ2hyaXMnKVxuXG4gIGNvbnN0IG5vYm9keTogUGVyc29uID0ge307XG4gIGNvbnNvbGUubG9nKGxvb2t1cE5hbWUobm9ib2R5KSk7IC8vIE5vdGhpbmdcbiAgYGBgXG4gIFxuICBAcGFyYW0ga2V5IFRoZSBrZXkgdG8gcHVsbCBvdXQgb2YgdGhlIG9iamVjdC5cbiAgQHBhcmFtIG9iaiBUaGUgb2JqZWN0IHRvIGxvb2sgdXAgdGhlIGtleSBmcm9tLlxuICovXG5leHBvcnQgZnVuY3Rpb24gZ2V0PFQsIEsgZXh0ZW5kcyBrZXlvZiBUPihrZXk6IEssIG1heWJlT2JqOiBNYXliZTxUPik6IE1heWJlPFJlcXVpcmVkPFQ+W0tdPjtcbmV4cG9ydCBmdW5jdGlvbiBnZXQ8VCwgSyBleHRlbmRzIGtleW9mIFQ+KGtleTogSyk6IChtYXliZU9iajogTWF5YmU8VD4pID0+IE1heWJlPFJlcXVpcmVkPFQ+W0tdPjtcbmV4cG9ydCBmdW5jdGlvbiBnZXQ8VCwgSyBleHRlbmRzIGtleW9mIFQ+KFxuICBrZXk6IEssXG4gIG1heWJlT2JqPzogTWF5YmU8VD5cbik6IE1heWJlPFJlcXVpcmVkPFQ+W0tdPiB8ICgobWF5YmVPYmo6IE1heWJlPFQ+KSA9PiBNYXliZTxSZXF1aXJlZDxUPltLXT4pIHtcbiAgcmV0dXJuIGN1cnJ5MShNYXliZS5hbmRUaGVuKHByb3BlcnR5PFQsIEs+KGtleSkpLCBtYXliZU9iaik7XG59XG5cbi8qKiBBIHZhbHVlIHdoaWNoIG1heSAoYEp1c3Q8VD5gKSBvciBtYXkgbm90IChgTm90aGluZ2ApIGJlIHByZXNlbnQuICovXG5leHBvcnQgdHlwZSBNYXliZTxUPiA9IEp1c3Q8VD4gfCBOb3RoaW5nPFQ+O1xuZXhwb3J0IGNvbnN0IE1heWJlID0ge1xuICBWYXJpYW50LFxuICBKdXN0LFxuICBOb3RoaW5nLFxuICBhbGwsXG4gIGlzSnVzdCxcbiAgaXNOb3RoaW5nLFxuICBqdXN0LFxuICBub3RoaW5nLFxuICBvZixcbiAgZmluZCxcbiAgZmlyc3QsXG4gIGZyb21OdWxsYWJsZSxcbiAgaGVhZCxcbiAgbGFzdCxcbiAgbWFwLFxuICBtYXBPcixcbiAgbWFwT3JFbHNlLFxuICBhbmQsXG4gIGFuZFRoZW4sXG4gIGNoYWluLFxuICBmbGF0TWFwLFxuICBvcixcbiAgb3JFbHNlLFxuICB1bnNhZmVseVVud3JhcCxcbiAgdW5zYWZlbHlHZXQsXG4gIHVuc2FmZUdldCxcbiAgdW53cmFwT3IsXG4gIGdldE9yLFxuICB1bndyYXBPckVsc2UsXG4gIGdldE9yRWxzZSxcbiAgdG9Pa09yRXJyLFxuICB0b09rT3JFbHNlRXJyLFxuICBmcm9tUmVzdWx0LFxuICB0b1N0cmluZyxcbiAgdHVwbGUsXG4gIG1hdGNoLFxuICBjYXRhLFxuICBlcXVhbHMsXG4gIGFwLFxuICBpc0luc3RhbmNlLFxuICBwcm9wZXJ0eSxcbiAgZ2V0LFxufTtcblxuZXhwb3J0IGRlZmF1bHQgTWF5YmU7XG4iXX0=