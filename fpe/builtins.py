from typing import Any, NoReturn, Optional, Union

from fpe.base import flip
from fpe.functions import curry


isinstance_ =  curry(2)(flip(isinstance))
isinstance_.__doc__ = """Curried version of builtin isinstance.

1st argument is type or tuple of types of possible classes,
2nd is target obj.
E.g. isinstance_((int, str), obj)
"""

issubclass_ = curry(2)(flip(issubclass))
issubclass_.__doc__ = """Curried version of builtin issubclass.

1st argument is type or tuple of types of possible superclasses,
2nd is target type.
E.g. isinstance_((int, str), obj)
"""

hasattr_ = curry(2)(flip(hasattr))
hasattr_.__doc__ = """Curried version of builtin hasattr.

1st argument is name, 2nd is obj.
E.g. hasattr_("attr", obj)
"""

getattrRaise = curry(2)(flip(getattr))
getattrRaise.__doc__ = """Curried version of builtin getattr without default.

This version rises exception if there is not attribute, as original getattr.
1st argument is name, 2nd is obj.
E.g. getattrRaise("attr", obj)
"""


@curry
def getattr_(name: str, default: Any, obj: Any) -> Union[Any, NoReturn]:
    """Curried version of builtin getattr with default.

    This version demands default value and always returns value of
    obj attribute or default, it depends on obj.
    E.g. getattr_("attr", None, obj)
    """

    return getattr(obj, name, default)


@curry
def setattr_(name: str, value: Any, obj: Any) -> Optional[NoReturn]:
    """Curried version of builtin setattr.

    1st argument is name, 2nd is value and 3rd is object.
    E.g. setattr_("attr", 42, obj)
    """

    return setattr(obj, name, value)


zip_ = curry(2)(zip)
zip_.__doc__ = """Curried builtin zip.

It retracts 1st iterable and waiting for other,
at least one more, iterables.
Literally zip(iterable1, iterable2, *iterables)
"""

map_ = curry(2)(map)
map_.__doc__ = """Curried builtin map.

It retracts 1st as function that will be applied on items
and waiting for other, at least one more, iterables.
Literally map(func, iterable, *iterables)
"""

next_ = curry(2)(flip(next))
next_.__doc__ = """Curried version of builtin next with default.

This version demands default value and always returns item of
iterable or default, it depends on iterable.
1st argument is default, 2nd is iterator.
E.g. next_(None, iterator)
"""

iter_ = curry(2)(flip(iter))
iter_.__doc__ = """Curried version of builtin iter

1st argument is sentinel, 2nd is callable.
E.g. iter_('', func)
"""
