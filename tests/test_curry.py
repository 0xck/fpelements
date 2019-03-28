from itertools import permutations
from unittest import TestCase, main

import hypothesis.strategies as st
from hypothesis import given, assume

from fpe.functions import (CurriedFunctionFixedArgumentsNumber,
                           CurriedFunctionDefaults, CurriedFunctionPositionals,
                           curry)

from .stuff import bin_op_cmp, bin_op_log, bin_op_math, known_builtins, minus_, mul_, plus_


def func_pos(x, y):
    pass


def func_def(x, y=0):
    pass


class TestCurrying(TestCase):

    @given(*(st.integers() for _ in range(5)))
    def test_currying_positional(self, x, y, z, a, b):

        @curry
        def func(x, y, z, a, b):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_positional_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, a, b):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args0_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(*args):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args1_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(x, *args):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args2_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, *args):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args3_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, *args):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args4_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, a, *args):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_positional_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, a, b, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args0_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(*args, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args1_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(x, *args, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args2_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, *args, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args3_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, *args, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_args4_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(x, y, z, a, *args, **kwags):
            return ((x - (y + z)) * a) - b

        result = ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x)(y, z, a, b), result)
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y, z)(a, b), result)
        self.assertEqual(func(x, y, z, a)(b), result)
        self.assertEqual(func(x, y, z)(a)(b), result)
        self.assertEqual(func(x, y)(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

        self.assertEqual(func(*(x, y, z, a, b)), result)
        self.assertEqual(func(x)(*(y, z, a, b)), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(z, a, b), result)
        self.assertEqual(func(x, y)(*(z, a, b)), result)
        self.assertEqual(func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(func(x, y, z)(*(a, b)), result)
        self.assertEqual(func(*(x, y, z))(a, b), result)
        self.assertEqual(func(*(x, y, z, a))(b), result)
        self.assertEqual(func(*(x, y, z))(a)(b), result)
        self.assertEqual(func(*(x, y))(z)(a)(b), result)
        self.assertEqual(func(x)(y)(z)(a)(b), result)
        self.assertEqual(func(*(x, y))(z, a)(b), result)
        self.assertEqual(func(x, y)(*(z, a))(b), result)
        self.assertEqual(func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(func(x, y)(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(func(*(x, y))(z)(a, b), result)
        self.assertEqual(func(x)(*(y, z))(a, b), result)
        self.assertEqual(func(x)(y, z)(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_defaults(self, x, y, z, a, b):

        kwgs = (dict(i) for i in permutations(dict(x=x, y=y, z=z, a=a, b=b).items()))
        result = ((x - (y + z)) * a) - b

        @curry
        def func(x=0, y=0, z=0, a=0, b=0):
            return ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)
        self.assertEqual(func(x, y, z, a), ((x - (y + z)) * a) - 0)
        self.assertEqual(func(x, y, z), ((x - (y + z)) * 0) - 0)
        self.assertEqual(func(x, y), ((x - (y + 0)) * 0) - 0)
        self.assertEqual(func(x), ((x - (0 + 0)) * 0) - 0)
        self.assertEqual(func(), 0)

        for kw in kwgs:
            self.assertEqual(func(**kw), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_defaults_fixed(self, x, y, z, a, b):

        result = ((x - (y + z)) * a) - b

        @curry(5)
        def func(x=0, y=0, z=0, a=0, b=0):
            return ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_defaults_args_fixed(self, x, y, z, a, b):

        @curry(5)
        def func(*args, x=0, y=0, z=0, a=0, b=0):
            return ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), 0)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_defaults_args_fixed_kwargs(self, x, y, z, a, b):

        @curry(5)
        def func(*args, x=0, y=0, z=0, a=0, b=0, **kwargs):
            return ((x - (y + z)) * a) - b

        self.assertEqual(func(x, y, z, a, b), 0)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_class_mtd_positional(self, x, y, z, a, b):

        class C:
            @curry
            def func(self, x, y, z, a, b):
                return ((x - (y + z)) * a) - b

        c = C()

        result = ((x - (y + z)) * a) - b

        self.assertEqual(c.func(x, y, z, a, b), result)
        self.assertEqual(c.func(x)(y, z, a, b), result)
        self.assertEqual(c.func(x, y)(z, a, b), result)
        self.assertEqual(c.func(x, y, z)(a, b), result)
        self.assertEqual(c.func(x, y, z, a)(b), result)
        self.assertEqual(c.func(x, y, z)(a)(b), result)
        self.assertEqual(c.func(x, y)(z)(a)(b), result)
        self.assertEqual(c.func(x)(y)(z)(a)(b), result)
        self.assertEqual(c.func(x, y)(z, a, b), result)
        self.assertEqual(c.func(x, y)(z, a)(b), result)
        self.assertEqual(c.func(x, y)(z)(a, b), result)
        self.assertEqual(c.func(x)(y, z)(a, b), result)
        self.assertEqual(c.func(x)(y, z)(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_class_mtd_positional_fixed(self, x, y, z, a, b):

        class C:
            @curry(6)
            def func(self, x, y, z, a, b):
                return ((x - (y + z)) * a) - b

        c = C()

        result = ((x - (y + z)) * a) - b

        self.assertEqual(c.func(x, y, z, a, b), result)
        self.assertEqual(c.func(x)(y, z, a, b), result)
        self.assertEqual(c.func(x, y)(z, a, b), result)
        self.assertEqual(c.func(x, y, z)(a, b), result)
        self.assertEqual(c.func(x, y, z, a)(b), result)
        self.assertEqual(c.func(x, y, z)(a)(b), result)
        self.assertEqual(c.func(x, y)(z)(a)(b), result)
        self.assertEqual(c.func(x)(y)(z)(a)(b), result)
        self.assertEqual(c.func(x, y)(z, a, b), result)
        self.assertEqual(c.func(x, y)(z, a)(b), result)
        self.assertEqual(c.func(x, y)(z)(a, b), result)
        self.assertEqual(c.func(x)(y, z)(a, b), result)
        self.assertEqual(c.func(x)(y, z)(a)(b), result)

        self.assertEqual(c.func(*(x, y, z, a, b)), result)
        self.assertEqual(c.func(x)(*(y, z, a, b)), result)
        self.assertEqual(c.func(x, y)(*(z, a, b)), result)
        self.assertEqual(c.func(*(x, y))(z, a, b), result)
        self.assertEqual(c.func(x, y)(*(z, a, b)), result)
        self.assertEqual(c.func(*(x, y))(*(z, a, b)), result)
        self.assertEqual(c.func(x, y, z)(*(a, b)), result)
        self.assertEqual(c.func(*(x, y, z))(a, b), result)
        self.assertEqual(c.func(*(x, y, z, a))(b), result)
        self.assertEqual(c.func(*(x, y, z))(a)(b), result)
        self.assertEqual(c.func(*(x, y))(z)(a)(b), result)
        self.assertEqual(c.func(x)(y)(z)(a)(b), result)
        self.assertEqual(c.func(*(x, y))(z, a)(b), result)
        self.assertEqual(c.func(x, y)(*(z, a))(b), result)
        self.assertEqual(c.func(*(x, y))(*(z, a))(b), result)
        self.assertEqual(c.func(x, y)(z)(*(a, b)), result)
        self.assertEqual(c.func(*(x, y))(z)(*(a, b)), result)
        self.assertEqual(c.func(*(x, y))(z)(a, b), result)
        self.assertEqual(c.func(x)(*(y, z))(a, b), result)
        self.assertEqual(c.func(x)(y, z)(*(a, b)), result)
        self.assertEqual(c.func(x)(*(y, z))(*(a, b)), result)
        self.assertEqual(c.func(x)(*(y, z))(a)(b), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_class_mtd_defaults(self, x, y, z, a, b):

        kwgs = (dict(i) for i in permutations(dict(x=x, y=y, z=z, a=a, b=b).items()))
        result = ((x - (y + z)) * a) - b

        class C:
            @curry
            def func(self, x=0, y=0, z=0, a=0, b=0):
                return ((x - (y + z)) * a) - b

        c = C()

        self.assertEqual(c.func(x, y, z, a, b), result)
        self.assertEqual(c.func(x, y, z, a), ((x - (y + z)) * a) - 0)
        self.assertEqual(c.func(x, y, z), ((x - (y + z)) * 0) - 0)
        self.assertEqual(c.func(x, y), ((x - (y + 0)) * 0) - 0)
        self.assertEqual(c.func(x), ((x - (0 + 0)) * 0) - 0)
        self.assertEqual(c.func(), 0)

        for kw in kwgs:
            self.assertEqual(c.func(**kw), result)

    @given(*(st.integers() for _ in range(5)))
    def test_currying_class_mtd_defaults_fixed(self, x, y, z, a, b):

        result = ((x - (y + z)) * a) - b

        class C:
            @curry(6)
            def func(self, x=0, y=0, z=0, a=0, b=0):
                return ((x - (y + z)) * a) - b

        c = C()

        self.assertEqual(c.func(x, y, z, a, b), result)

    def test_curring_errors(self):

        with self.assertRaises(AssertionError):
            @curry
            def func():
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(*args):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y, *args):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y=0, *args):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(**kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y=0, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(*args, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y, *args, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry
            def func(x, y=0, *args, **kwags):
                pass

    @given(st.integers(max_value=1))
    def test_curring_fixed_errors(self, x):

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(*args):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y, *args):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y=0, *args):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(**kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y=0, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(*args, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y, *args, **kwags):
                pass

        with self.assertRaises(AssertionError):
            @curry(x)
            def func(x, y=0, *args, **kwags):
                pass

    @given(st.integers(), st.integers())
    def test_currying_builtin_cmp_log(self, x, y):

        for f in bin_op_cmp+bin_op_log:

            cf = curry(2)(f)
            result = f(x, y)

            self.assertEqual(cf(x, y), result)
            self.assertEqual(cf(x)(y), result)

    @given(st.integers(), st.integers().filter(lambda x: x != 0))
    def test_currying_builtin_math(self, x, y):

        for f in bin_op_math[:-1]:

            cf = curry(2)(f)
            result = f(x, y)

            self.assertEqual(cf(x, y), result)
            self.assertEqual(cf(x)(y), result)

    def test_curring_builtin_errors(self):

        # if curried without defining number of arguments
        for f in known_builtins:
            self.assertRaises(AssertionError, curry, f)

    def test_curring_classes(self):

        self.assertIsInstance(curry(func_pos), CurriedFunctionPositionals)
        self.assertIsInstance(curry(func_def), CurriedFunctionDefaults)

        self.assertRaises(AssertionError, CurriedFunctionDefaults, func_pos)
        self.assertRaises(AssertionError, CurriedFunctionDefaults, pow)
        self.assertRaises(AssertionError, CurriedFunctionPositionals, func_def)
        self.assertRaises(AssertionError, CurriedFunctionPositionals, pow)

    @given(st.integers(min_value=2, max_value=128))
    def test_curring_classes_fixed(self, x):

        for f in known_builtins:

            self.assertIsInstance(
                curry(x)(f), CurriedFunctionFixedArgumentsNumber)

        for f in (minus_, mul_, plus_):

            self.assertIsInstance(
                curry(2)(f), CurriedFunctionFixedArgumentsNumber)

    @given(st.integers(min_value=2, max_value=128), st.integers(max_value=1))
    def test_curring_classes_fixed_error(self, x, y):

        for f in known_builtins + (minus_, mul_, plus_):

            self.assertRaises(
                AssertionError, CurriedFunctionFixedArgumentsNumber, y, f)


if __name__ == '__main__':
    main()
