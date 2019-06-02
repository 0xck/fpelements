from abc import abstractmethod
from typing import Callable, Any

from fpe.asserts import AssertWrongArgumentType, AssertNonCallable

from fpe.applicative import AbstractApplicative
from fpe.functions import enrichFunction, curry


class AbstractMonad(AbstractApplicative):

    @abstractmethod
    def __rshift__(self, func: Callable) -> "AbstractMonad":
        """
        Sequentially compose two actions, passing any value produced by the first as an argument to the second.

        Borrowed from (>>=) :: forall a b. m a -> (a -> m b) -> m b
        Note.
            Further, any definition must satisfy the following laws:
                pure a >>= k = k a
                m >>= pure = m
                m >>= (\\x -> k x >>= h) = (m >>= k) >>= h

            This is not possible to satisfy these laws in some automatic way,
            implementation should be performed manually.
        """
        pass

    @enrichFunction
    def bind(self, func: Callable) -> "AbstractMonad":
        """Explicit >>= method."""

        return self.__rshift__(func)


@curry
def bind(func: Callable, instance: AbstractMonad) -> AbstractMonad:
    """Common sequentially compose two actions function (>>=)."""

    # only callable
    assert callable(func), AssertNonCallable()
    # only Monad
    assert isinstance(instance, AbstractMonad), AssertWrongArgumentType("AbstractMonad")

    return instance >> func
