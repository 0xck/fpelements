from abc import abstractmethod
from typing import Callable

from fpe.applicative import AbstractApplicative


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

    def bind(self, func: Callable) -> "AbstractMonad":
        """Explicit >>= method."""

        return self.__rshift__(func)
