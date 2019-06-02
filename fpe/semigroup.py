from abc import ABCMeta, abstractmethod


class AbstractSemigroup(metaclass=ABCMeta):
    """An abstract class which represents a Semigroup conception."""

    @abstractmethod
    def __and__(self, other):
        """An associative operation.

        Borrowed from (<>) :: a -> a -> a
        Note.
            `&` must satisfy the associative law:
                (x <> y) <> z == x <> (y <> z)

            This is not possible to satisfy this law in some automatically way,
            implementation should be performed manually.
        """
        pass
