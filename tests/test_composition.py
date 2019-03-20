from sys import maxsize
from unittest import TestCase, main
from hypothesis import given
import hypothesis.strategies as st
from fpe.functions import curry, id_, compose, FunctionComposition


@curry
def mul(x, y):
    return x * y


@curry
def plus(x, y):
    return x + y


@curry
def minus(x, y):
    return y - x


def to_str(x):
    return str(x)


def to_int(x):
    return int(x)


def negate(x):
    return -(x)


def mul_(x, y):
    return x * y


def plus_(x, y):
    return x + y


def minus_(x, y):
    return y - x


numbers = st.floats(allow_nan=False, allow_infinity=False) | st.integers()
non_seq = st.none() | st.booleans() | st.text() | numbers
seq = st.lists(non_seq) | st.tuples(non_seq)
random_types = non_seq | seq | st.dictionaries(st.text() | st.integers(), non_seq | seq)


class TestComposition(TestCase):

    @given(st.integers(), st.integers())
    def test_generic_composition(self, x, y):

        result = mul(x)(minus(x)(plus(x)(y)))

        m_composed = (mul(x) * minus(x) * plus(x))
        self.assertEqual(m_composed(y), result)

        p_composed = (plus(x) | minus(x) | mul(x))
        self.assertEqual(p_composed(y), result)

        f_composed = compose(plus(x), minus(x)) | mul(x)
        self.assertEqual(f_composed(y), result)

    @given(st.integers(), st.integers())
    def test_composition_associativity(self, x, y):

        m_composed1 = (mul(x) * minus(x)) * plus(x)
        m_composed2 = mul(x) * (minus(x) * plus(x))
        self.assertEqual(m_composed1(y), m_composed2(y))

        p_composed1 = plus(x) | (minus(x) | mul(x))
        p_composed2 = (plus(x) | minus(x)) | mul(x)
        self.assertEqual(p_composed1(y), p_composed2(y))

        f_composed1 = compose(plus(x), compose(minus(x), mul(x)))
        f_composed2 = compose(compose(plus(x), minus(x)), mul(x))
        self.assertEqual(f_composed1(y), f_composed2(y))

    @given(st.integers(), st.integers())
    def test_composition_identity(self, x, y):

        result = minus(x, y)

        self.assertEqual((id_ * minus(x))(y), result)
        self.assertEqual((minus(x) * id_)(y), result)
        self.assertEqual((minus(x) | id_)(y), result)
        self.assertEqual((id_ | minus(x))(y), result)
        self.assertEqual(compose(minus(x), id_)(y), result)
        self.assertEqual(compose(id_, minus(x))(y), result)

    @given(st.integers(), st.from_regex(r"(-)?\d{1,15}" if maxsize > 2 ** 32 else r"(-)?\d{1,7}", fullmatch=True))
    def test_composition_foreign(self, x, s):

        funcs_num = (abs, negate, str, to_str, oct, bin, hex, bool, id)
        funcs_str = (int, to_int, float, frozenset, list, set, tuple, bool, id)

        for f in funcs_num:
            result = f(x)

            m_composed_l = (id_ * f)
            m_composed_r = (f * id_)
            self.assertEqual(m_composed_l(x), result)
            self.assertEqual(m_composed_r(x), result)

            p_composed_l = (id_ | f)
            p_composed_r = (f | id_)
            self.assertEqual(p_composed_l(x), result)
            self.assertEqual(p_composed_r(x), result)

            self.assertEqual(compose(f, id_)(x), result)
            self.assertEqual(compose(id_, f)(x), result)

        for f in funcs_str:
            result = f(s)

            m_composed_l = (id_ * f)
            m_composed_r = (f * id_)
            self.assertEqual(m_composed_l(s), result)
            self.assertEqual(m_composed_r(s), result)

            p_composed_l = (id_ | f)
            p_composed_r = (f | id_)
            self.assertEqual(p_composed_l(s), result)
            self.assertEqual(p_composed_r(s), result)

            self.assertEqual(compose(f, id_)(s), result)
            self.assertEqual(compose(id_, f)(s), result)

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

    @given(random_types, random_types)
    def test_composition_class_negative(self, f1, f2):

        self.assertRaises(AssertionError, FunctionComposition, f1, f2)
        self.assertRaises(AssertionError, FunctionComposition, f2, f1)
        self.assertRaises(AssertionError, FunctionComposition, f1, plus)
        self.assertRaises(AssertionError, FunctionComposition, f1, plus_)
        self.assertRaises(AssertionError, FunctionComposition, plus, f2)
        self.assertRaises(AssertionError, FunctionComposition, plus_, f2)

    @given(random_types)
    def test_id(self, x):

        self.assertEqual(id_(x), x)


if __name__ == '__main__':
    main()
