from abc import abstractmethod
from typing import Any, Callable

from fpe.asserts import AssertNonCallable, AssertWrongArgumentType

from fpe.functions import enrichFunction, curry

from fpe.functor import AbstractFunctor


class AbstractApplicative(AbstractFunctor):
    """An abstract class which represents na Applicative Functor conception.
    """

    @staticmethod
    @abstractmethod
    def pure(value: Any):
        """Lift a value function.

        Borrowed from pure :: a -> f a
        """
        pass

    @abstractmethod
    def __mod__(self, instance: "AbstractApplicative") -> "AbstractApplicative":
        """Sequential application function.

        Borrower from (<*>) :: f (a -> b) -> f a -> f b
        May be defined as liftA2 id

        Note.
            Further, any definition must satisfy the following laws:
                identity: pure id <*> v = v
                composition: pure (.) <*> u <*> v <*> w = u <*> (v <*> w)
                homomorphism: pure f <*> pure x = pure (f x)
                interchange: u <*> pure y = pure ($ y) <*> u

            This is not possible to satisfy these laws in some automatically way,
            implementation should be performed manually.
        """
        pass

    @enrichFunction
    def apply(self, instance: "AbstractApplicative") -> "AbstractApplicative":
        """Explicit <*> method."""

        return self.__mod__(instance)

    @staticmethod
    @abstractmethod
    def liftA2(func: Callable, fa, fb):
        """Lift a binary function to actions.

        Borrowed from liftA2 :: (a -> b -> c) -> f a -> f b -> f c
        May be defined as liftA2 f x y = f <$> x <*> y
        """
        pass


@curry
def apply(pured_func: AbstractApplicative, instance: AbstractApplicative) -> AbstractApplicative:
    """Common sequential application function (<*>)."""

    # only Applicative
    assert isinstance(pured_func, AbstractApplicative), AssertWrongArgumentType("AbstractApplicative")
    # only callable
    assert callable(pured_func._value), AssertNonCallable()
    # only Applicative
    assert isinstance(instance, AbstractApplicative), AssertWrongArgumentType("AbstractApplicative")

    return pured_func % instance
