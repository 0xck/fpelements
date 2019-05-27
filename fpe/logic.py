from typing import Any, Callable

from fpe.asserts import AssertNonCallable
from fpe.functions import curry


@curry
def ite(predicate: Callable, alternative: Any, value: Any) -> Any:
    """Ternary predicate function: if then else

    Same as value if predicate(value) else alternative
    """

    # only callable
    assert callable(predicate), AssertNonCallable()

    return value if predicate(value) else alternative
