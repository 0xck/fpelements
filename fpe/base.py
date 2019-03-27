from typing import Any, Callable

from fpe.asserts import AssertNotCallable


def flip(func: Callable) -> Callable:
    """
    Decorator swaps arguments provided to decorated function.

    Thus flip(f)(x, y) == f(y, x)

    Borrowed from flip :: (a -> b -> c) -> b -> a -> c
    """

    # only callable
    assert callable(func), AssertNotCallable()

    def flipped(first: Any, second: Any) -> Any:
        """
        Swapping provided arguments to given function.

        Thus f(x, y) -> f(y, x)
        """

        return func(second, first)

    flipped.__name__ = "flipped <{}>".format(getattr(func, "__name__", "Unknown"))

    return flipped
