from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from fpe.asserts import AssertNotCallable, AssertWrongArgumentType
from fpe.functions import curry


class AbstractFunctor(metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, func: Callable) -> Any:
        """
        fmap function for mapping values with functions

        Borrowed from fmap :: (a -> b) -> f a -> f b

        Note.
            fmap must satisfy the following laws:
                fmap id  ==  id
                fmap (f . g)  ==  fmap f . fmap g

            This is not possible to satisfy these laws in some automatically way,
            implementation should be performed manually.
        """
        pass


@curry
def fmap(func: Callable, instance) -> Any:

    # only callable
    assert callable(func), AssertNotCallable()
    # only Functor
    assert isinstance(instance, AbstractFunctor), AssertWrongArgumentType(
        "AbstractFunctor")

    return instance.fmap(func)
