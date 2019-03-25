from typing import Any, Callable

from fpe.applicative import AbstractApplicative
from fpe.asserts import (AssertCheckingFailed, AssertNotCallable,
                         AssertWrongArgumentType)
from fpe.functions import compose, id_
from fpe.functor import AbstractFunctor, fmap
from fpe.misc.checks import get_common_parents
from fpe.monad import AbstractMonad
from fpe.semigroup import AbstractSemigroup


def associative_operation_simple_satisfy_check(x: AbstractSemigroup,
                                               y: AbstractSemigroup,
                                               z: AbstractSemigroup) -> bool:
    """
    Very simple `&` (associative operation) satisfy checker

    Function provides very generic checking for law:
        (x <> y) <> z == x <> (y <> z)

    Satisfying is checked by simple equals, e.g. (x & y) & z == x & (y & z).
    It raises assert AssertCheckingFailed in case test failure.
    """

    # every item has to have same class or common parent that is an AbstractSemigroup
    assert all(any(issubclass(j, AbstractSemigroup) for j in get_common_parents(x, i)) for i in (y, z)), AssertWrongArgumentType(
        "{} for every argument and has common parent with other".format(AbstractSemigroup))

    # 1st law checking
    assert ((x & y) & z == x & (y & z)), AssertCheckingFailed(
        "law (x & y) & z == x & (y & z) failed")

    return True


def fmap_simple_satisfy_check(instance: AbstractFunctor, func1: Callable, func2: Callable) -> bool:
    """
    Very simple fmap satisfy checker

    Function provides very generic checking for both laws:
        fmap id  ==  id
        fmap (f . g)  ==  fmap f . fmap g

    In the composition of func1 and func2, func2 executes before func1.
    Satisfying is checked by simple equals, e.g. fmap(id_, obj) == id_(obj).
    It raises assert AssertCheckingFailed in case test failure.
    """

    # only callable
    assert callable(func1) and callable(func2), AssertNotCallable()
    # only Functor
    assert isinstance(instance, AbstractFunctor), AssertWrongArgumentType(
        "AbstractFunctor")

    # 1st law checking
    assert fmap(id_, instance) == id_(instance), AssertCheckingFailed("law <fmap id  ==  id> failed")

    # 2nd law checking
    compose_func = compose(func1, func2)
    compose_fmap = fmap(func1) * fmap(func2)

    assert instance.fmap(compose_func) == compose_fmap(instance), AssertCheckingFailed(
        "law <fmap (f . g)  ==  fmap f . fmap g> failed")

    return True


def applicative_simple_satisfy_check(instance_value: AbstractApplicative,
                                    instance_func1: AbstractApplicative,
                                    instance_func2: AbstractApplicative,
                                    func: Callable, value: Any) -> bool:
    """
    Very simple `%` (applicatinve operation) satisfy checker

    Function provides very generic checking for following laws:
        pure id <*> v = v
        pure (.) <*> u <*> v <*> w = u <*> (v <*> w)
        pure f <*> pure x = pure (f x)
        u <*> pure y = pure ($ y) <*> u

    Satisfying is checked by simple equals, e.g.
        cls.pure(func) % cls.pure(value) == cls.pure(func(value)).
    It raises assert AssertCheckingFailed in case test failure.
    """

    # only callable
    assert callable(func), AssertNotCallable()
    # only Applicative
    assert all(isinstance(i, AbstractApplicative) for i in (
        instance_value, instance_func1, instance_func2)), AssertWrongArgumentType("AbstractApplicative")
    # the same instance
    # assert items_has_same_parent_by_method(
    #     "__pow__", (instance_value, instance_func1, instance_func2)), AssertWrongArgumentType(
    #         "the same class as other arguments have")

    cls = type(instance_value)

    # identity: pure id <*> v = v
    assert (cls.pure(id_) % instance_value) == instance_value, AssertCheckingFailed(
        "law <fpure id <*> v = v> failed")

    # composition: pure(.) <*> u <*> v <*> w = u <*> (v <*> w)
    assert cls.pure(compose) % instance_func2 % instance_func1 % instance_value == instance_func2 % (
        instance_func1 % instance_value), AssertCheckingFailed(
            "law <pure(.) <*> u <*> v <*> w = u <*> (v <*> w)> failed")

    # homomorphism: pure f <*> pure x = pure(f x)
    assert (cls.pure(func) % cls.pure(value)) == cls.pure(func(value)), AssertCheckingFailed(
        "law <u <*> pure y = pure($ y) <*> u> failed")

    # interchange: u <*> pure y = pure($ y) <*> u
    assert (instance_func1 % cls.pure(value)) == (cls.pure(lambda f: f(value)) % instance_func1), AssertCheckingFailed(
        "law <u <*> pure y = pure ($ y) <*> u> failed")

    return True


def monad_simple_satisfy_check(instance: AbstractMonad, func1: Callable, func2: Callable, value: Any) -> bool:
    """
    Very simple `>>` (compose two actions passing any value
        produced by the first as an argument to the second)
        satisfy checker

    Function provides very generic checking for following laws:
        pure a >>= k = k a
        m >>= pure = m
        m >>= (\\x -> k x >>= h) = (m >>= k) >>= h

    Satisfying is checked by simple equals, e.g.
        cls.pure(func) % cls.pure(value) == cls.pure(func(value)).
    It raises assert AssertCheckingFailed in case test failure.
    """

    # only callable
    assert callable(func1) and callable(func2), AssertNotCallable()
    # only Monad
    assert isinstance(instance, AbstractMonad), AssertWrongArgumentType(
        "AbstractMonad")

    cls = type(instance)

    # pure a >>= k = k a
    assert cls.pure(value) >> func1 == func1(value), AssertCheckingFailed(
        "law <pure a >>= k = k a> failed")

    # m >>= pure = m
    assert instance >> cls.pure == instance, AssertCheckingFailed(
        "law <m >>= pure = m> failed")

    # m >>= (\x -> k x >>= h) = (m >>= k) >>= h
    assert instance >> (lambda x: func1(x) >> func2) == (instance >> func1) >> func2, AssertCheckingFailed(
        "law <m >>= (\\x -> k x >>= h) = (m >>= k) >>= h> failed")

    return True
