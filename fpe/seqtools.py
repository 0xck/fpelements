from typing import Any, NoReturn, Union, Callable, Iterable, Container, Collection
from collections.abc import Sequence, Mapping
from functools import reduce

from fpe.functions import curry
from fpe.maybe import Just, Nothing, Maybe


@curry
def elem(item: Any, sequence: Container) -> Union[bool, NoReturn]:
    """Return True if item is in given sequence.

    Literally item in sequence.
    """

    return item in sequence


@curry
def first(predicate: Callable[..., bool], iterable: Iterable) -> Union[Maybe, NoReturn]:
    """Getting first element of iterable.

    Functions returns Just with first found item, otherwise Nothing.

    Note.
        Be careful in case of using this function with iterators,
        function exhausts them.
    """

    try:
        return Just(next(filter(predicate, iterable)))

    except StopIteration:
        pass

    return Nothing


@curry
def count(item: Any, sequence: Collection) -> Union[int, NoReturn]:
    """Getting number of given element in sequence.

    Note.
        Function works with Mapping by counting its values, not keys,
        due counting keys does not have any sense, result is always 0 or 1,
        and the better is using `in` for this purpose. See example below:
            mapping = {'a': 1, 'b': 1, c: 2}
            count(1, mapping)  # 2, not 0
            # the same as
            count(1, mapping.values())  # 2
    """

    if isinstance(sequence, Mapping):
        sequence = sequence.values()

    if isinstance(sequence, Sequence):
        return sequence.count(item)

    count = 0
    for i in sequence:
        if i == item:
            count += 1

    return count


@curry
def foldl(func: Callable, init: Any, iterable: Iterable) -> Union[Any, NoReturn]:
    """Curried version of functools.reduce with defined initial.

    Apply a function of two arguments cumulatively to the items of a sequence,
    from left to right, so as to reduce the sequence to a single value.
    E.g.
        reduce(lambda acc, x: acc + x, [3, 4, 14, 21], 0) == ((((0+3)+4)+14)+21) == 42
        reduce(lambda acc, x: acc + x, [], 0) == 0

    Literally reduce(func, iterable, init)
    """

    return reduce(func, iterable, init)


@curry
def foldl_(func: Callable, iterable: Iterable) -> Union[Any, NoReturn]:
    """Curried version of functools.reduce with 1st element as initial.

    Apply a function of two arguments cumulatively to the items of a sequence,
    from left to right, so as to reduce the sequence to a single value.
    E.g.
        reduce(lambda acc, x: acc + x, [3, 4, 14, 21]) == (((3+4)+14)+21) == 42
        reduce(lambda acc, x: acc + x, [])  # raise TypeError

    Literally reduce(func, iterable)
    """

    return reduce(func, iterable)


@curry
def foldr(func: Callable, init: Any, iterable: Iterable) -> Union[Any, NoReturn]:
    """Curried version of functools.reduce with defined initial and reversed sequence.

    Apply a function of two arguments cumulatively to the items of a sequence,
    from right to left, so as to reduce the sequence to a single value.
    E.g.
        reduce(lambda acc, x: acc + x, [3, 4, 14, 21], 0) == ((((0+21)+14)+4)+3) == 42
        reduce(lambda acc, x: acc + x, [], 0) == 0

    Literally reduce(func, reversed(iterable), init)
    """

    return reduce(func, reversed(iterable), init)


@curry
def foldr_(func: Callable, iterable: Iterable) -> Union[Any, NoReturn]:
    """Curried version of functools.reduce with 1st element as initial and reversed sequence.

    Apply a function of two arguments cumulatively to the items of a sequence,
    from right to left, so as to reduce the sequence to a single value.
    E.g.
        reduce(lambda acc, x: acc + x, [3, 4, 14, 21]) == (((21+14)+4)+3) == 42
        reduce(lambda acc, x: acc + x, [])  # raise TypeError

    Literally reduce(func, reversed(iterable))
    """

    return reduce(func, reversed(iterable))
