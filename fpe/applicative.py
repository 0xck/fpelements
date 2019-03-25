from abc import abstractmethod, abstractstaticmethod
from typing import Any, Callable

from fpe.functor import AbstractFunctor


class AbstractApplicative(AbstractFunctor):

    @staticmethod
    @abstractstaticmethod
    def pure(value: Any):
        """
        Lift a value function.

        Borrorwed from pure :: a -> f a
        """
        pass

    @abstractmethod
    def __mod__(self, func: Callable):
        """
        Sequential application function.

        Borrower from (<*>) :: f (a -> b) -> f a -> f b
        May be defined as liftA2 id

        Note.
            Further, any definition must satisfy the following laws:
                identity: pure id <*> v = v
                composition: pure (.) <*> u <*> v <*> w = u <*> (v <*> w)
                homomorphism: pure f <*> pure x = pure (f x)
                interchange: u <*> pure y = pure ($ y) <*> u

            This is not possible to satisfy these laws in some automatical way,
            implementation should be performed manually.
        """
        pass

    @staticmethod
    @abstractstaticmethod
    def liftA2(func: Callable, fa, fb):
        """
        Lift a binary function to actions.

        Borrowed from liftA2 :: (a -> b -> c) -> f a -> f b -> f c
        May be defined as liftA2 f x y = f <$> x <*> y
        """
        pass
