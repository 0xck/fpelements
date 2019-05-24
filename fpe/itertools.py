from itertools import accumulate, dropwhile, islice, takewhile, zip_longest, filterfalse
from typing import Any, Callable, Iterable, NoReturn, Union, Tuple

from fpe.base import flip
from fpe.builtins import map_, zip_
from fpe.functions import curry


dropWhile = curry(2)(dropwhile)
dropWhile.__doc__ = "The same as itertools.dropwhile but curried."

takeWhile = curry(2)(takewhile)
takeWhile.__doc__ = "The same as itertools.takewhile but curried."


@curry
def take(num: int, iterable: Iterable) -> Union[Iterable, NoReturn]:
    "Return first num items of the iterable."

    return islice(iterable, num)


@curry
def drop(num: int, iterable: Iterable) -> Union[Iterable, NoReturn]:
    "Skipping first num items of the iterable and return rest of them."

    return islice(iterable, num, None)


accumulate_ = curry(2)(flip(accumulate))
accumulate_.__doc__ = """Curried version of itertools.accumulate.

accumulate_ retracts 1st as function that will be applied on items
and waiting for iterable.
Literally accumulate(iterable, func)
"""

zipWith = curry(3)(map)
zipWith.__doc__ = """Curried builtin map for at least 2 iterables.

zipWith retracts 1st as function that will be applied on items,
2nd as first iterable and waiting for other, at least one more, iterables.
Literally map(func, iterable1, iterable2, *iterables)

Borrowed from to zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
But works with any number of iterables, as map does.
"""


@curry(3)
def zipPad(pad: Any, iterable: Iterable, *args: Iterable) -> Union[Iterable, NoReturn]:
    """Curried zip_longest.

    zipPad retracts pad as padding, iterable as first iterable and
    waits for more, at least one more, iterables.
    Literally zip_longest(iterable, *args, fillvalue=pad)
    """

    return zip_longest(iterable, *args, fillvalue=pad)


@curry(4)
def zipWithPad(func: Callable, pad: Any, iterable: Iterable, *args: Iterable) -> Union[Iterable, NoReturn]:
    """Curried zip_longest, where given function is applied on every item.

    zipWithPad retracts func as applying function, pad as padding,
    iterable as first iterable and waits for more, at least one more, iterables.
    Literally (func(*i) for i in zip_longest(iterable, *args, fillvalue=pad))
    """

    return (func(*i) for i in zip_longest(iterable, *args, fillvalue=pad))


@curry
def collect(predicate: Callable[..., bool], func: Callable,
            iterable: Iterable) -> Union[Iterable, NoReturn]:
    """Combined map and filter function.

    It filters given iterable with predicate and applies func
    on filtered items.
    Literally map(func, filter(predicate, iterable))

    Borrowed from Scala collect method.
    """

    return map(func, filter(predicate, iterable))


@curry
def partition(predicate: Callable[..., bool],
              iterable: Iterable) -> Union[Tuple[Iterable, Iterable], NoReturn]:
    """Combined filter and itertools.filterfalse function.

    It returns tuple from filtered and rest items.
    Literally (filter(predicate, iterable), filterfalse(predicate, iterable))

    Borrowed from partition :: (a -> Bool) -> [a] -> ([a], [a])
    """

    return (filter(predicate, iterable), filterfalse(predicate, iterable))
