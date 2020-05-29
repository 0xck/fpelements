from abc import abstractmethod
from collections.abc import Sequence

from fpe.asserts import AssertEmptyValue, AssertWrongArgumentType
from fpe.functions import enrichFunction
from fpe.misc.checks import get_common_parents
from fpe.semigroup import AbstractSemigroup


class AbstractMonoid(AbstractSemigroup):
    """An abstract class which represents a Monoid conception."""

    @property
    @abstractmethod
    def empty(self):
        """Identity of & (associative operation)

        Borrowed from mempty :: a
        """
        pass

    @staticmethod
    @enrichFunction
    def mconcat(seq: Sequence):
        """mconcat function folds a sequence using the monoid with & (associative operation)

        Borrowed from mconcat :: [a] -> a
        Note.
            Actually mconcat does not demand non-empty sequence, but in current implementation
            if sequence is empty this is not possible to know which value will have to be returned,
            due function knows nothing about containerized type.
        """

        # only sequence
        assert isinstance(seq, Sequence), AssertWrongArgumentType("Sequence")
        # non empty sequence
        assert len(seq), AssertEmptyValue()
        # every item has to have same class or common parent that is an AbstractMonoid
        assert all(any(issubclass(j, AbstractMonoid) for j in get_common_parents(seq[0], i)) for i in seq), AssertWrongArgumentType(
            "{} for every item and has common parent with other".format(AbstractMonoid))

        result = seq[0].empty

        for i in seq:
            result = result & i

        return result


@enrichFunction
def mconcat(seq: Sequence):
    """Common mconcat function

    mconcat folds a sequence using the monoid with & (associative operation)
    Borrowed from mconcat :: [a] -> a

    Note.
        Actually mconcat does not demand non-empty sequence, but in current implementation
        if sequence is empty this is not possible to know which value will have to be returned,
        due function knows nothing about containerized type.
    """

    # only sequence
    assert isinstance(seq, Sequence), AssertWrongArgumentType("Sequence")
    # non empty sequence
    assert len(seq), AssertEmptyValue()
    # only AbstractMonoid
    assert isinstance(seq[0], AbstractMonoid), AssertWrongArgumentType("AbstractMonoid")

    return seq[0].mconcat(seq)
