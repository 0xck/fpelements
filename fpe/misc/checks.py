from collections import Sequence
from typing import Any, Set, Type

from fpe.asserts import (AssertEmptyValue, AssertWrongArgumentType,
                         AssertWrongValue)


def get_parent_by_attr(mro: Sequence, attr: str, default=None):
    """
    Searching for right parent by class which is attribue base endpoint.

    E.g.
        An attribute `attr` is defined in class X and X is parent for A and B,
        A redefined `attr`, B did not, A is parent for C and B is parent for D.
        MRO looks like object -> Z -> X.attr -> ((A.attr -> C), (B -> D)).
        Let c, d = C(), D(), then:
            c `attr` base endpoint is A, because it redefined `attr`
            d `attr` base endpoint is X, because it defined `attr` first

    Algorithm is simple, it checks every class in given sequence where success is:
        if current item has attribute in its __dict__
        if attribute is defined attribute magic methods, then
        current item has the attribute and:
            there is not parent for current item (last item) or
            parent for current item does not have this attribue
    """
    # mro is sequence
    assert isinstance(mro, Sequence), AssertWrongArgumentType("Sequence")
    # attr is str
    assert isinstance(attr, str), AssertWrongArgumentType("str")
    # attr is alphanum and _
    assert attr.replace('_', '').isalnum(
    ), AssertWrongValue(attr, "alphanum and _")

    if not len(mro):
        return default

    parent = default
    # cut mro, throw out `object` and rest
    parents = mro if object not in mro else mro[:mro.index(object)]

    # searching for right parent
    for i in range(len(parents)):

        # checking if attr is exist in current
        if hasattr(parents[i], attr):
            current = True
        else:
            current = False

        # parent provides the attribute
        # but is the attribute based on parent as its endpoint,
        # for knowing that, parent has to be checked, so skip futher checking for current
        if (current and (i + 1) < len(parents)) and getattr(parents[i], attr) is getattr(parents[i + 1], attr):
            continue

        # checking if current is right parent
        if current and any(
                ((parents[i].__dict__.get(attr, False if default is not False else None)),
                 ((i + 1) >= len(parents)),
                 ((i + 1) < len(parents) and (not hasattr(parents[i + 1], attr))))):

            parent = parents[i]
            break

    return parent


def items_has_same_parent_by_method(mtd: str, seq: Sequence) -> bool:

    # seq is sequence
    assert isinstance(seq, Sequence), AssertWrongArgumentType("Sequence")
    # non empty sequence
    assert len(seq), AssertEmptyValue()
    # mtd is str
    assert isinstance(mtd, str), AssertWrongArgumentType("String")
    # mtd is alphanum and _
    assert mtd.replace('_', '').isalnum(
    ), AssertWrongValue(mtd, "alphanum and _")

    if len(seq) == 1:
        return hasattr(seq[0], mtd)

    parent = get_parent_by_attr(type(seq[0]).mro()[-1:], mtd)

    if parent is None:
        return False

    for i in seq[1:]:
        if not isinstance(i, parent):
            return False

    return True


def get_common_parents(x: Any, y: Any) -> Set[Type]:
    return set(type(x).mro()[:-1]).intersection(type(y).mro()[:-1])


def is_common_parents(x: Any, y: Any) -> bool:
    return bool(get_common_parents(x, y))
