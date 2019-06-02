from collections.abc import Iterable
from typing import Any, Callable, Collection, Generator, NoReturn, Tuple, Union

from fpe.asserts import AssertNonCallable, AssertWrongArgumentType
from fpe.functions import curry, enrichFunction
from fpe.monad import AbstractMonad
from fpe.semigroup import AbstractSemigroup


Eithers = Union["Left", "Right"]
EitherCollection = Collection[Eithers]
LeftCollection = Collection["Left"]
RightCollection = Collection["Right"]
EitherGenerator = Generator[Eithers, None, None]


class Either(AbstractMonad, AbstractSemigroup):
    """An abstract class for representation Either from Haskell.

    In whole, class represents conception of handling computation
    that can not performed due some reason, e.g. domain of function
    might not be compatible its range, e.g. 1/0 can not be finished.
    In this case result can not be retrieved, but can be represented
    in some way. Here Right class contains finished computation, and
    Left class contains something that represents computation failure.
    E.g.
        def div(a, b):
            if b == 0:
                return Left("ZeroDivision")
            else:
                return Right(a//b)

        div(42, 2) == Right(21)
        div(42, 0) == Left("ZeroDivision")

    Borrowed from data Either a b = Left a | Right b
    """

    @staticmethod
    @enrichFunction
    def pure(value: Any) -> Eithers:
        """Implementation of pure from ApplicativeFunctor.

        Return value embraced by Right class.
        E.g.
            pure(42) == Right(42)
            pure(isinstance) = Right(isinstance)
        """

        if isinstance(value, Either):
            return value

        return Right(value)

    @staticmethod
    @curry
    def liftA2(func: Callable, either1: Eithers, either2: Eithers) -> Eithers:
        """Implementation of lift2 from ApplicativeFunctor.

        It applies binary function to two Either embraced values.
        E.g.
            lift2(max, Right(1), Right(42)) == Right(42)
            lift2(max, Right(1), Left("ZeroDivision")) == Left("ZeroDivision")
            lift2(max, Left("ZeroDivision"), Right(42)) == Left("ZeroDivision")
        """

        # only callabe
        assert callable(func), AssertNonCallable()
        # only Either
        assert isinstance(either1, Either) and isinstance(either2, Either), AssertWrongArgumentType("Either")

        return (either1 | func) % either2

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
        return "{}: {}".format(self.__class__.__name__, self._value)


class Left(Either):
    """Left class for representation failed computation.

    Borrowed from Left :: a -> Either a b
    """

    def __init__(self, value: Any):
        self._value = value

    def __or__(self, _: Callable) -> "Left":
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
    """Right class for representation completed computation.

    Borrowed from Right :: b -> Either a b
    """

    def __init__(self, value: Any):
        self._value = value

    def __or__(self, func: Callable) -> "Right":

        # only callable
        assert callable(func), AssertNonCallable()

        return Right(func(self._value))

    def __mod__(self, either: Eithers) -> Eithers:

        # only callable
        assert callable(self._value), AssertNonCallable()
        # only Either
        assert isinstance(either, Either), AssertWrongArgumentType("Either")

        return either | self._value

    def __rshift__(self, func: Callable[..., Eithers]) -> Eithers:

        # only callable
        assert callable(func), AssertNonCallable()

        return func(self._value)

    def __and__(self, either: Eithers) -> Eithers:

        # only Either
        assert isinstance(either, Either), AssertWrongArgumentType("Either")

        return self


@enrichFunction
def lefts(seq: Union[EitherCollection, EitherGenerator]) -> Tuple[Left, ...]:

    # seq has to be iterable
    assert isinstance(seq, Iterable), AssertWrongArgumentType("Iterable")

    return tuple(i._value for i in seq if isinstance(i, Left))


@enrichFunction
def rights(seq: Union[EitherCollection, EitherGenerator]) -> Tuple[Right, ...]:

    # seq has to be iterable
    assert isinstance(seq, Iterable), AssertWrongArgumentType("Iterable")

    return tuple(i._value for i in seq if isinstance(i, Right))


@curry
def either(func_left: Callable, func_right: Callable, left_right: Eithers) -> Any:

    # only callable
    assert callable(func_left) and callable(func_right), AssertNonCallable()
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


@enrichFunction
def isLeft(either: Eithers) -> bool:

    # only Either
    assert isinstance(either, Either), AssertWrongArgumentType(
        "Either")

    return isinstance(either, Left)


@enrichFunction
def isRight(either: Eithers) -> bool:

    # only Either
    assert isinstance(either, Either), AssertWrongArgumentType(
        "Either")

    return isinstance(either, Right)
