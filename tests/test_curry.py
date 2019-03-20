# import sys
from itertools import permutations
from unittest import TestCase, main
import operator
from hypothesis import given
import hypothesis.strategies as st
from fpe.functions import curry, _unknown_builtin, CurriedFunctionDefaults, CurriedFunctionPositionals, CurriedBuiltinFunctionFixedArguments


builtins = (
    abs, min, setattr, all, dir, hex, next, any, divmod, id, sorted, ascii,
    input, oct, bin, eval, open, exec, isinstance, ord, sum, issubclass, pow,
    iter, print, callable, format, len, chr, vars, getattr, locals, repr, compile,
    globals, hasattr, max, round, delattr, hash)

bin_op_cmp = (operator.lt, operator.le, operator.eq, operator.ne, operator.ge, operator.gt)

bin_op_math = (operator.add, operator.floordiv, operator.truediv,
               operator.sub, operator.mul, operator.mod, operator.pow)

bin_op_log = (operator.and_, operator.or_, operator.xor)

bin_op_bin = (operator.rshift, operator.lshift)

seq_op = (operator.concat, operator.contains,
          operator.delitem, operator.getitem, operator.setitem)

known_builtins = builtins + _unknown_builtin + bin_op_cmp + bin_op_math + bin_op_log + bin_op_bin + seq_op


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
        self.assertEqual(func(x, y)(z, a, b), result)
        self.assertEqual(func(x, y)(z, a)(b), result)
        self.assertEqual(func(x, y)(z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a, b), result)
        self.assertEqual(func(x)(y, z)(a)(b), result)

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
        self.assertRaises(AssertionError, CurriedFunctionPositionals, func_def)

    @given(st.integers(min_value=2, max_value=128), st.integers(max_value=1))
    def test_curring_classes_builtin_error(self, x, y):

        self.assertRaises(
            AssertionError, CurriedBuiltinFunctionFixedArguments, y, pow)
        self.assertRaises(
            AssertionError, CurriedBuiltinFunctionFixedArguments, x, func_pos)
        self.assertRaises(
            AssertionError, CurriedBuiltinFunctionFixedArguments, x, func_def)

        self.assertIsInstance(
            curry(x)(map), CurriedBuiltinFunctionFixedArguments)

    @given(st.integers(min_value=2, max_value=128))
    def test_curring_classes_builtin(self, x):

        for f in known_builtins:

            self.assertIsInstance(
                curry(x)(f), CurriedBuiltinFunctionFixedArguments)


if __name__ == '__main__':
    main()
