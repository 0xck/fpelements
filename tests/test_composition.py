from sys import maxsize
from unittest import TestCase, main

import hypothesis.strategies as st
from hypothesis import given

from fpe.functions import FunctionComposition, compose, id_, pipe

from .stuff import (minus, minus_, mul, negate, plus, plus_, random_types,
                    to_int, to_str)


class TestComposition(TestCase):

    @given(st.integers(), st.integers())
    def test_generic_composition(self, x, y):

        result = mul(x)(minus(x)(plus(x)(y)))

        m_composed = (mul(x) * minus(x) * plus(x))
        self.assertEqual(m_composed(y), result)

        p_composed = (plus(x) | minus(x) | mul(x))
        self.assertEqual(p_composed(y), result)

        fm_composed = compose(minus(x), plus(x)) | mul(x)
        self.assertEqual(fm_composed(y), result)

        fp_composed = pipe(plus(x), minus(x)) | mul(x)
        self.assertEqual(fp_composed(y), result)

    @given(st.integers(), st.integers())
    def test_composition_associativity(self, x, y):

        m_composed1 = (mul(x) * minus(x)) * plus(x)
        m_composed2 = mul(x) * (minus(x) * plus(x))
        self.assertEqual(m_composed1(y), m_composed2(y))

        p_composed1 = plus(x) | (minus(x) | mul(x))
        p_composed2 = (plus(x) | minus(x)) | mul(x)
        self.assertEqual(p_composed1(y), p_composed2(y))

        fm_composed1 = compose(compose(mul(x), minus(x)), plus(x))
        fm_composed2 = compose(mul(x), compose(minus(x), plus(x)))
        self.assertEqual(fm_composed1(y), fm_composed2(y))

        fp_composed1 = compose(plus(x), compose(minus(x), mul(x)))
        fp_composed2 = compose(compose(plus(x), minus(x)), mul(x))
        self.assertEqual(fp_composed1(y), fp_composed2(y))

    @given(st.integers(), st.integers())
    def test_composition_identity(self, x, y):

        result = minus(x, y)

        self.assertEqual((id_ * minus(x))(y), result)
        self.assertEqual((minus(x) * id_)(y), result)
        self.assertEqual((minus(x) | id_)(y), result)
        self.assertEqual((id_ | minus(x))(y), result)
        self.assertEqual(compose(minus(x), id_)(y), result)
        self.assertEqual(compose(id_, minus(x))(y), result)
        self.assertEqual(pipe(minus(x), id_)(y), result)
        self.assertEqual(pipe(id_, minus(x))(y), result)

    @given(st.integers(), st.from_regex(r"(-)?\d{1,15}" if maxsize > 2 ** 32 else r"(-)?\d{1,7}", fullmatch=True))
    def test_composition_foreign(self, x, s):

        funcs_num = (abs, negate, str, to_str, oct, bin, hex, bool, id)
        funcs_str = (int, to_int, float, frozenset, list, set, tuple, bool, id)

        for f in funcs_num:
            result = f(x)

            self.assertEqual((id_ * f)(x), result)
            self.assertEqual((f * id_)(x), result)

            self.assertEqual((id_ | f)(x), result)
            self.assertEqual((f | id_)(x), result)

            self.assertEqual(compose(f, id_)(x), result)
            self.assertEqual(compose(id_, f)(x), result)

            self.assertEqual(pipe(f, id_)(x), result)
            self.assertEqual(pipe(id_, f)(x), result)

        for f in funcs_str:
            result = f(s)

            self.assertEqual((id_ * f)(s), result)
            self.assertEqual((f * id_)(s), result)

            self.assertEqual((id_ | f)(s), result)
            self.assertEqual((f | id_)(s), result)

            self.assertEqual(compose(f, id_)(s), result)
            self.assertEqual(compose(id_, f)(s), result)

            self.assertEqual(pipe(f, id_)(s), result)
            self.assertEqual(pipe(id_, f)(s), result)

    def test_composition_class(self):

        self.assertIsInstance((plus * minus), FunctionComposition)
        self.assertIsInstance((plus * minus_), FunctionComposition)
        self.assertIsInstance((plus_ * minus), FunctionComposition)
        self.assertIsInstance((id_ * minus), FunctionComposition)
        self.assertIsInstance((plus * id_), FunctionComposition)
        self.assertIsInstance((id_ * minus_), FunctionComposition)
        self.assertIsInstance((plus_ * id_), FunctionComposition)
        self.assertIsInstance((id_ * id_), FunctionComposition)

        self.assertIsInstance((plus | minus), FunctionComposition)
        self.assertIsInstance((plus | minus_), FunctionComposition)
        self.assertIsInstance((plus_ | minus), FunctionComposition)
        self.assertIsInstance((id_ | minus), FunctionComposition)
        self.assertIsInstance((plus | id_), FunctionComposition)
        self.assertIsInstance((id_ | minus_), FunctionComposition)
        self.assertIsInstance((plus_ | id_), FunctionComposition)
        self.assertIsInstance((id_ | id_), FunctionComposition)

        self.assertIsInstance(compose(plus, minus), FunctionComposition)
        self.assertIsInstance(compose(plus, minus_), FunctionComposition)
        self.assertIsInstance(compose(plus_, minus), FunctionComposition)
        self.assertIsInstance(compose(id_, minus), FunctionComposition)
        self.assertIsInstance(compose(plus, id_), FunctionComposition)
        self.assertIsInstance(compose(id_, minus_), FunctionComposition)
        self.assertIsInstance(compose(plus_, id_), FunctionComposition)
        self.assertIsInstance(compose(id_, id_), FunctionComposition)

        self.assertIsInstance(pipe(plus, minus), FunctionComposition)
        self.assertIsInstance(pipe(plus, minus_), FunctionComposition)
        self.assertIsInstance(pipe(plus_, minus), FunctionComposition)
        self.assertIsInstance(pipe(id_, minus), FunctionComposition)
        self.assertIsInstance(pipe(plus, id_), FunctionComposition)
        self.assertIsInstance(pipe(id_, minus_), FunctionComposition)
        self.assertIsInstance(pipe(plus_, id_), FunctionComposition)
        self.assertIsInstance(pipe(id_, id_), FunctionComposition)

    @given(random_types, random_types)
    def test_composition_class_negative(self, f1, f2):

        self.assertRaises(AssertionError, FunctionComposition, f1, f2)
        self.assertRaises(AssertionError, FunctionComposition, f2, f1)
        self.assertRaises(AssertionError, FunctionComposition, f1, plus)
        self.assertRaises(AssertionError, FunctionComposition, f1, plus_)
        self.assertRaises(AssertionError, FunctionComposition, plus, f2)
        self.assertRaises(AssertionError, FunctionComposition, plus_, f2)


if __name__ == '__main__':
    main()
