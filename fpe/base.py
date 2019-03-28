from typing import Any, Callable

from fpe.asserts import AssertNotCallable, AssertWrongArgumentType


def flip(func: Callable[[Any, Any], Any]) -> Callable:
    """Decorator swaps arguments provided to decorated function.

    Thus flip(f)(x, y) == f(y, x)

    Borrowed from flip :: (a -> b -> c) -> b -> a -> c
    """

    # only callable
    assert callable(func), AssertNotCallable()

    def flipped(first: Any, second: Any) -> Any:
        """Swapping provided arguments to given function.

        Thus f(x, y) -> f(y, x)
        """

        return func(second, first)

    flipped.__name__ = getattr(func, "__name__", "Unknown")

    if hasattr(func, "__doc__"):
        flipped.__doc__ = getattr(func, "__doc__")

    return flipped


def even(num: int) -> bool:
    "Return True if given num is even, otherwise False"

    # only int
    assert isinstance(num, int), AssertWrongArgumentType("int")

    return not (num % 2)


def odd(num: int) -> bool:
    "Return True if given num is odd, otherwise False"

    # only int
    assert isinstance(num, int), AssertWrongArgumentType("int")

    return bool(num % 2)
