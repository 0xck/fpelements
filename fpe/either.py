from collections import Iterable
from typing import Any, Callable, Collection, Generator, NoReturn, Tuple, Union

from fpe.asserts import AssertNotCallable, AssertWrongArgumentType
from fpe.functions import curry
from fpe.monad import AbstractMonad
from fpe.semigroup import AbstractSemigroup


Eithers = Union["Left", "Right"]
EitherCollection = Collection[Eithers]
LeftCollection = Collection["Left"]
RightCollection = Collection["Right"]
EitherGenerator = Generator[Eithers, None, None]


class Either(AbstractMonad, AbstractSemigroup):

    @staticmethod
    def pure(value: Any):

        if isinstance(value, Either):
            return value

        return Right(value)

    @staticmethod
    @curry
    def liftA2(func: Callable, either1: Eithers, either2: Eithers) -> Eithers:

        # only callabe
        assert callable(func), AssertNotCallable()
        # only Either
        assert isinstance(either1, Either) and isinstance(either2, Either), AssertWrongArgumentType("Either")

        return either1.fmap(func) % either2

    @property
    def value(self) -> NoReturn:
        raise AttributeError("Value of Either can not be used directly")

    def __eq__(self, other) -> bool:

        if type(self) is not type(other):
            return False

        return self._value == other._value

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __bool__(self):
        return True

    def __repr__(self):
        return "Either {}: <{}>".format(self.__class__.__name__, self._value)


class Left(Either):

    def __init__(self, value: Any):
        self._value = value

    def fmap(self, _: Callable) -> "Left":
        return self

    def __mod__(self, _: Callable) -> "Left":
        return self

    def __rshift__(self, _: Callable) -> "Left":
        return self

    def __and__(self, either: Eithers) -> Eithers:

        # only Either
        assert isinstance(either, Either), AssertWrongArgumentType("Either")

        return either


class Right(Either):

    def __init__(self, value: Any):
        self._value = value

    def fmap(self, func: Callable) -> "Right":

        # only callable
        assert callable(func), AssertNotCallable()

        return Right(func(self._value))

    def __mod__(self, either: Eithers) -> Eithers:

        # only callable
        assert callable(self._value), AssertNotCallable()
        # only Either
        assert isinstance(either, Either), AssertWrongArgumentType("Either")

        return either.fmap(self._value)

    def __rshift__(self, func: Callable[..., Eithers]) -> Eithers:

        # only callable
        assert callable(func), AssertNotCallable()

        return func(self._value)

    def __and__(self, either: Eithers) -> Eithers:

        # only Either
        assert isinstance(either, Either), AssertWrongArgumentType("Either")

        return self


def lefts(seq: Union[EitherCollection, EitherGenerator]) -> Tuple[Left, ...]:

    # seq has to be iterable
    assert isinstance(seq, Iterable), AssertWrongArgumentType("Iterable")

    return tuple(i._value for i in seq if isinstance(i, Left))


def rights(seq: Union[EitherCollection, EitherGenerator]) -> Tuple[Right, ...]:

    # seq has to be iterable
    assert isinstance(seq, Iterable), AssertWrongArgumentType("Iterable")

    return tuple(i._value for i in seq if isinstance(i, Right))


@curry
def either(func_left: Callable, func_right: Callable, left_right: Eithers) -> Any:

    # only callable
    assert callable(func_left) and callable(func_right), AssertNotCallable()
    # only Either
    assert isinstance(left_right, Either), AssertWrongArgumentType(
        "Either")

    if isinstance(left_right, Left):
        return func_left(left_right._value)

    return func_right(left_right._value)


@curry
def fromLeft(alternative: Any, either: Eithers) -> Any:

    # only Either
    assert isinstance(either, Either), AssertWrongArgumentType(
        "Either")
    # alternative type has to be the same as either embracing value
    assert isinstance(alternative, type(either._value)), AssertWrongArgumentType(
        str(type(either._value)))

    return either._value if isinstance(either, Left) else alternative


@curry
def fromRight(alternative: Any, either: Eithers) -> Any:

    # only Either
    assert isinstance(either, Either), AssertWrongArgumentType(
        "Either")
    # alternative type has to be the same as either embracing value
    assert isinstance(alternative, type(either._value)), AssertWrongArgumentType(
        str(type(either._value)))

    return either._value if isinstance(either, Right) else alternative
