from typing import Any, Collection, NoReturn, Union

from fpe.functions import curry


@curry
def elem(item: Any, sequence: Collection) -> Union[bool, NoReturn]:
    """Return True if item is in given sequence.

    Literally item in sequence.
    """

    return item in sequence
