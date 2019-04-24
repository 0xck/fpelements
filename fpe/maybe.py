from typing import Any, Callable, Collection, Generator, NoReturn, Union

from fpe.asserts import AssertNotCallable, AssertWrongArgumentType
from fpe.functions import curry, enrichFunction
from fpe.monad import AbstractMonad
from fpe.semigroup import AbstractSemigroup


Maybies = Union["Nothing_", "Just"]
MaybeCollection = Collection[Maybies]
NothingCollection = Collection["Nothing_"]
JustCollection = Collection["Just"]
MaybeGenerator = Generator[Maybies, None, None]


class Maybe(AbstractMonad, AbstractSemigroup):
    """An abstract class for representation Maybe from Haskell.

    In whole, class represents conception of handling computation
    that can not performed due some reason, e.g. domain of function
    might not be compatible its range, e.g. 1/0 can not be finished.
    In this case result can not be retrived, but can be represented
    in some way. Here Just class contains finished computation, and
    Nothing class represents computation failure.
    E.g.
        def div(a, b):
            if b == 0:
                return Nothing
            else:
                return Just(a//b)

        div(42, 2) == Just(21)
        div(42, 0) == Nothing

    Borrowed from data Maybe a = Nothing | Just a
    """

    @staticmethod
    @enrichFunction
    def pure(value: Any) -> Maybies:
        """Implementation of pure from ApplicativeFunctor.

        Return value contexted by Just class.
        E.g.
            pure(42) == Just(42)
            pure(isinstance) = Just(isinstance)
        """

        if isinstance(value, Maybe):
            return value

        return Just(value)

    @staticmethod
    @curry
    def liftA2(func: Callable, maybe1: Maybies, maybe2: Maybies) -> Maybies:
        """Implementation of lift2 from ApplicativeFunctor.

        It applies binary function to two Maybe contexted values.
        E.g.
            lift2(max, Just(1), Just(42)) == Just(42)
            lift2(max, Just(1), Nothing) == Nothing
            lift2(max, Nothing, Just(42)) == Nothing
        """

        # only callabe
        assert callable(func), AssertNotCallable()
        # only Maybe
        assert isinstance(maybe1, Maybe) and isinstance(maybe2, Maybe), AssertWrongArgumentType("Maybe")

        return maybe1.fmap(func) % maybe2

    @property
    def value(self) -> NoReturn:
        raise AttributeError("Value of Maybe can not be used directly")

    def __eq__(self, other) -> bool:

        if type(self) is not type(other):
            return False

        if isinstance(self, Nothing_) and isinstance(other, Nothing_):
            return True

        return self._value == other._value

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __bool__(self):
        return True

    def __repr__(self):

        if isinstance(self, Nothing_):
            return "Maybe Nothing"

        return "Maybe Just: <{}>".format(self._value)


class Nothing_(Maybe):
    """Nothing_ class for representation failed computation.

    Name of this class is ending with undercore, because
    there is the class' object with name Nothing, which have to
    used in code as representation computation failure.
    E. g. 1/0 = Nothing, not 1/0 = Nothing_(). For class checking
    also use Nothing_, e.g. isinstance(Nothing, Nothing_)
    Note.
        Nothing is object of Nothing_, but is not really singleton,
        anyway you do not need to create more Nothing_ objects.

    Borrowed from Nothing :: Maybe a
    """

    def fmap(self, _: Callable) -> "Nothing_":
        return self

    def __mod__(self, _: Callable) -> "Nothing_":
        return self

    def __rshift__(self, _: Callable) -> "Nothing_":
        return self

    def __and__(self, maybe: Maybies) -> Maybies:

        # only Maybe
        assert isinstance(maybe, Maybe), AssertWrongArgumentType("Maybe")

        return maybe


class Just(Maybe):
    """Just class for representation completed computation.

    Borrowed from Just :: a -> Maybe a
    """

    def __init__(self, value: Any):
        self._value = value

    def fmap(self, func: Callable) -> "Just":

        # only callable
        assert callable(func), AssertNotCallable()

        return Just(func(self._value))

    def __mod__(self, maybe: Maybies) -> Maybies:

        # only callable
        assert callable(self._value), AssertNotCallable()
        # only Maybe
        assert isinstance(maybe, Maybe), AssertWrongArgumentType("Maybe")

        return maybe.fmap(self._value)

    def __rshift__(self, func: Callable[..., Maybies]) -> Maybies:

        # only callable
        assert callable(func), AssertNotCallable()

        return func(self._value)

    def __and__(self, maybe: Maybies) -> Maybies:

        # only Maybe
        assert isinstance(maybe, Maybe), AssertWrongArgumentType("Maybe")
        assert isinstance(self._value, AbstractSemigroup) and isinstance(getattr(
            maybe, "_value", None), AbstractSemigroup), AssertWrongArgumentType("AbstractSemigroup")

        return Just(self._value & maybe._value)


# defined Nonthing
Nothing = Nothing_()
