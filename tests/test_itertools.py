from sys import maxsize
from unittest import TestCase, main
from itertools import dropwhile, takewhile, islice, zip_longest

from hypothesis import given
import hypothesis.strategies as st

from fpe.base import odd
from fpe.itertools import drop, take, dropWhile, takeWhile, zipWith, zipPad, zipWithPad

from .stuff import plus


seq_of_int = st.lists(st.integers()) | st.tuples(st.integers()) | st.dictionaries(st.integers(), st.integers())


def plus_3(x, y, z):
    return x + y + z


class TestIterTools(TestCase):

    @given(seq_of_int)
    def test_dropwile(self, s):

        self.assertSequenceEqual(list(dropWhile(lambda x: odd(x), s)),
                                list(dropwhile(lambda x: odd(x), s)))

    @given(seq_of_int)
    def test_takewile(self, s):

        self.assertSequenceEqual(list(takeWhile(lambda x: odd(x), s)),
                                list(takewhile(lambda x: odd(x), s)))

    @given(seq_of_int, st.integers().filter(lambda x: 0 <= x <= maxsize))
    def test_take(self, s, x):

        self.assertSequenceEqual(list(take(x, s)), list(islice(s, x)))

    @given(seq_of_int, st.integers().filter(lambda x: 0 <= x <= maxsize))
    def test_drop(self, s, x):

        self.assertSequenceEqual(list(drop(x, s)), list(islice(s, x, None)))

    @given(seq_of_int, seq_of_int, seq_of_int)
    def test_zipwith(self, s1, s2, s3):

        self.assertSequenceEqual(list(zipWith(plus, s1, s2)),
                                 list(map(plus, s1, s2)))

        self.assertSequenceEqual(list(zipWith(plus_3, s1, s2, s3)),
                                 list(map(plus_3, s1, s2, s3)))

    @given(seq_of_int, seq_of_int, seq_of_int)
    def test_zippad(self, s1, s2, s3):

        self.assertSequenceEqual(list(zipPad(0, s1, s2)),
                                 list(zip_longest(s1, s2, fillvalue=0)))

        self.assertSequenceEqual(list(zipPad(0, s1, s2, s3)),
                                 list(zip_longest(s1, s2, s3, fillvalue=0)))

    @given(seq_of_int, seq_of_int, seq_of_int)
    def test_zipwithpad(self, s1, s2, s3):

        self.assertSequenceEqual(list(zipWithPad(plus, 0, s1, s2)),
                                 list(plus(*i) for i in zip_longest(s1, s2, fillvalue=0)))

        self.assertSequenceEqual(list(zipWithPad(plus_3, 0, s1, s2, s3)),
                                 list(plus_3(*i) for i in zip_longest(s1, s2, s3, fillvalue=0)))


if __name__ == "__main__":
    main()
