from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from fpe.asserts import AssertNonCallable, AssertWrongArgumentType
from fpe.functions import curry


class AbstractFunctor(metaclass=ABCMeta):
    """An abstract class which represents a Functor conception.
    """

    @abstractmethod
    def __or__(self, func: Callable) -> "AbstractFunctor":
        """fmap function for mapping values with functions

        Borrowed from fmap :: (a -> b) -> f a -> f b
        Very similar to builtin map on sequences.

        Note.
            fmap must satisfy the following laws:
                fmap id  ==  id
                fmap (f . g)  ==  fmap f . fmap g

            This is not possible to satisfy these laws in some automatically way,
            implementation should be performed manually.
        """
        pass

    def fmap(self, func: Callable) -> "AbstractFunctor":
        """Explicit fmap method."""

        return self.__or__(func)


@curry
def fmap(func: Callable, instance) -> Any:
    """Common fmap function"""

    # only callable
    assert callable(func), AssertNonCallable()
    # only Functor
    assert isinstance(instance, AbstractFunctor), AssertWrongArgumentType(
        "AbstractFunctor")

    return instance.fmap(func)
