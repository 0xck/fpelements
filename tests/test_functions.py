from unittest import TestCase, main

from hypothesis import given
import hypothesis.strategies as st

from fpe.base import flip, odd, even
from fpe.functions import id_
from fpe.logic import ite
from fpe.seqtools import elem

from .stuff import random_types, non_seq, collections


class TestFunctions(TestCase):

    @given(random_types)
    def test_id(self, x):

        self.assertIs(id_(x), x)

    @given(random_types, random_types)
    def test_flip(self, x, y):

        @flip
        def func(a, b):
            return a, b

        self.assertEqual(func(x, y), (y, x))

        @flip
        @flip
        def func(a, b):
            return a, b

        self.assertEqual(func(x, y), (x, y))

        with self.assertRaises(AssertionError):
            func = flip(x)

        with self.assertRaises(TypeError):
            @flip
            def func():
                return
            value = func()

        with self.assertRaises(TypeError):
            @flip
            def func(a):
                return a
            value = func(x)

        with self.assertRaises(TypeError):
            @flip
            def func(a, b, c):
                return a, b, c
            value = func(x, y, 0)

    @given(random_types, random_types)
    def test_ite(self, x, y):

        true = lambda _: True
        false = lambda _: False

        always_x = ite(true, y)
        always_y = ite(false, y)
        depends_on_x = ite(bool, y)

        self.assertIs(always_x(x), x)
        self.assertIs(always_y(x), y)

        if bool(x):
            self.assertIs(depends_on_x(x), x)
        else:
            self.assertIs(depends_on_x(x), y)

    @given(collections, non_seq)
    def test_elem(self, s, x):

        self.assertEqual(elem(x, s), x in s)

    @given(st.integers())
    def test_even_odd(self, x):

        self.assertEqual(even(x), not x % 2)
        self.assertEqual(odd(x), bool(x % 2))
        self.assertEqual(odd(x), not even(x))


if __name__ == '__main__':
    main()
