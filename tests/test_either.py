from operator import neg
from unittest import TestCase, main

import hypothesis.strategies as st
from hypothesis import assume, given

from fpe.either import (Either, Left, Right, either, fromLeft, fromRight,
                        lefts, rights)
from fpe.functor import fmap
from fpe.misc.satisfying_checks import (applicative_simple_satisfy_check,
                                        associative_operation_simple_satisfy_check,
                                        fmap_simple_satisfy_check,
                                        monad_simple_satisfy_check)

from .stuff import (compose, id_, kleisli, known_builtins, minus, mul, plus,
                    random_types, to_str)


random_lefts = st.builds(Left, random_types)
random_rights = st.builds(Right, random_types)
random_eithers = random_lefts | random_rights

seq_left = st.lists(random_lefts) | st.tuples(random_lefts)
seq_right = st.lists(random_rights) | st.tuples(random_rights)
seq_random = st.lists(random_eithers) | st.tuples(random_eithers)

int_rights = st.builds(Right, st.integers())
int_eithers = st.builds(Left, st.integers()) | int_rights

kleisli_left = kleisli(Left)
kleisli_right = kleisli(Right)


class TestEither(TestCase):

    @given(random_types)
    def test_pure(self, x):

        self.assertIsInstance(Either.pure(x), Right)

    @given(random_types, random_types)
    def test_class_left(self, x, y):

        left = Left(x)

        self.assertIsInstance(left, Left)
        self.assertTrue(bool(left))
        self.assertEqual(left, Left(x))
        self.assertNotEqual(left, x)
        self.assertNotEqual(left, y)
        assume(x != y)
        self.assertNotEqual(left, Left(y))

    @given(random_types, random_types)
    def test_class_right(self, x, y):

        right = Right(x)

        self.assertIsInstance(right, Right)
        self.assertTrue(bool(right))
        self.assertEqual(right, Right(x))
        self.assertNotEqual(right, x)
        self.assertNotEqual(right, y)
        assume(x != y)
        self.assertNotEqual(right, Right(y))

    @given(st.integers(), random_lefts, random_lefts)
    def test_left_laws(self, x, left_y, left_z):

        left = Left(x)

        self.assertTrue(associative_operation_simple_satisfy_check(
            left, left_y, left_z))

        self.assertTrue(fmap_simple_satisfy_check(left, abs, neg))

        self.assertTrue(applicative_simple_satisfy_check(left, Left(neg), Left(abs), neg, x))

        self.assertTrue(monad_simple_satisfy_check(
            left, kleisli_left(neg), kleisli_left(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            left, kleisli_right(neg), kleisli_left(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            left, kleisli_left(neg), kleisli_right(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            left, kleisli_right(neg), kleisli_right(abs), x))

    @given(st.integers(), random_rights, random_rights)
    def test_rigth_laws(self, x, right_y, right_z):

        right = Right(x)

        self.assertTrue(associative_operation_simple_satisfy_check(
            right, right_y, right_z))

        self.assertTrue(fmap_simple_satisfy_check(right, abs, neg))

        self.assertTrue(applicative_simple_satisfy_check(right, Right(neg), Right(abs), neg, x))

        self.assertTrue(monad_simple_satisfy_check(
            right, kleisli_left(neg), kleisli_left(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            right, kleisli_right(neg), kleisli_left(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            right, kleisli_left(neg), kleisli_right(abs), x))
        self.assertTrue(monad_simple_satisfy_check(
            right, kleisli_right(neg), kleisli_right(abs), x))

    @given(st.integers(), random_eithers, random_eithers)
    def test_either_laws(self, x, either_y, either_z):

        right = Right(x)
        left = Left(x)

        self.assertTrue(associative_operation_simple_satisfy_check(
            left, either_y, either_z))

        self.assertTrue(associative_operation_simple_satisfy_check(
            right, either_y, either_z))

        self.assertTrue(applicative_simple_satisfy_check(
            left, Left(neg), Right(abs), neg, x))
        self.assertTrue(applicative_simple_satisfy_check(
            left, Right(neg), Left(abs), neg, x))

        self.assertTrue(applicative_simple_satisfy_check(
            right, Left(neg), Right(abs), neg, x))
        self.assertTrue(applicative_simple_satisfy_check(
            right, Right(neg), Left(abs), neg, x))

    @given(seq_random)
    def test_lefts(self, e):

        self.assertSequenceEqual(lefts(e), [i._value for i in e if isinstance(i, Left)])

    @given(seq_random)
    def test_rights(self, e):

        self.assertSequenceEqual(rights(e), [i._value for i in e if isinstance(i, Right)])

    @given(random_eithers)
    def test_eithers(self, e):

        left = lambda _: 0
        right = lambda _: 1

        self.assertEqual(either(left, right, e), 1 if isinstance(e, Right) else 0)

    @given(int_eithers, st.integers())
    def test_fromleft(self, e, x):

        self.assertEqual(fromLeft(x, e), x if isinstance(e, Right) else e._value)

    @given(int_eithers, st.integers())
    def test_fromright(self, e, x):

        self.assertEqual(fromRight(x, e), x if isinstance(e, Left) else e._value)

    @given(random_lefts, random_types)
    def test_fmap_left(self, e, junk):

        for f in known_builtins:

            self.assertIs(e.fmap(f), e)
            self.assertIs(e.fmap(f)._value, e._value)

            self.assertIs(fmap(f, e), e)
            self.assertIs(fmap(f, e)._value, e._value)
            self.assertRaises(AssertionError, fmap, junk, e)
            self.assertRaises(AssertionError, fmap, f, junk)
            self.assertRaises(AssertionError, fmap, junk, junk)

    @given(int_rights, random_types)
    def test_fmap_right(self, e, junk):

        for f in (neg, abs, id_, hash, round, id):

            self.assertEqual(e.fmap(f)._value, f(e._value))
            self.assertEqual(e.fmap(f), Right(f(e._value)))
            self.assertRaises(AssertionError, e.fmap, junk)

            self.assertEqual(fmap(f, e)._value, f(e._value))
            self.assertEqual(fmap(f, e), Right(f(e._value)))
            self.assertRaises(AssertionError, fmap, junk, e)
            self.assertRaises(AssertionError, fmap, f, junk)
            self.assertRaises(AssertionError, fmap, junk, junk)

    @given(st.integers(), st.integers())
    def test_applicative(self, x, y):

        left_x = Left(x)
        left_y = Left(y)
        right_x = Right(x)
        right_y = Right(y)

        for f in (plus, minus, mul):

            self.assertEqual(Either.pure(f) % right_x % right_x, Right(f(x, x)))
            self.assertEqual(Either.pure(f) % right_x % right_y, Right(f(x, y)))
            self.assertEqual(Either.pure(f) % right_y % right_x, Right(f(y, x)))
            self.assertEqual(Either.pure(f) % right_y % right_y, Right(f(y, y)))

            self.assertEqual(Either.pure(f) % left_x % left_x, left_x)
            self.assertEqual(Either.pure(f) % left_x % left_y, left_x)
            self.assertEqual(Either.pure(f) % left_y % left_x, left_y)
            self.assertEqual(Either.pure(f) % left_y % left_y, left_y)

            self.assertEqual(Either.pure(f) % right_x % left_x, left_x)
            self.assertEqual(Either.pure(f) % right_x % left_y, left_y)
            self.assertEqual(Either.pure(f) % right_y % left_x, left_x)
            self.assertEqual(Either.pure(f) % right_y % left_y, left_y)

            self.assertEqual(Either.pure(f) % left_x % right_x, left_x)
            self.assertEqual(Either.pure(f) % left_x % right_y, left_x)
            self.assertEqual(Either.pure(f) % left_y % right_x, left_y)
            self.assertEqual(Either.pure(f) % left_y % right_y, left_y)

        for f in (neg, abs, id_, hash, round, id, to_str):

            self.assertEqual(Either.pure(f) % right_x, Right(f(x)))
            self.assertEqual(Either.pure(f) % left_x, left_x)

    @given(st.integers(), st.integers())
    def test_monad(self, x, y):

        left_x = Left(x)
        left_y = Left(y)
        right_x = Right(x)
        right_y = Right(y)

        for f in (neg, abs, id_, hash, round, id, to_str):

            func = compose(Either.pure, f)

            self.assertEqual(left_x >> func, left_x)
            self.assertEqual(right_x >> func, Right(f(x)))

        for f in (plus, minus, mul):

            func = compose(Either.pure, f)

            self.assertEqual((right_x >> func) % right_y, Right(f(x, y)))
            self.assertEqual((right_y >> func) % right_x, Right(f(y, x)))
            self.assertEqual((right_x >> func) % right_x, Right(f(x, x)))
            self.assertEqual((right_y >> func) % right_y, Right(f(y, y)))

            self.assertEqual((left_x >> func) % left_y, left_x)
            self.assertEqual((left_y >> func) % left_x, left_y)
            self.assertEqual((left_x >> func) % left_x, left_x)
            self.assertEqual((left_y >> func) % left_y, left_y)


if __name__ == '__main__':
    main()
