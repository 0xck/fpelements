"""Module provides only some imports from other components of package.
It makes access to often used components more easy."""

from fpe.base import even, flip, odd
from fpe.builtins import (getattr_, hasattr_, isinstance_, issubclass_, iter_,
                          next_, setattr_)
from fpe.either import Either, Left, Right, isLeft, isRight
from fpe.exceptions import try_
from fpe.functions import (compose, curry, enrichFunction, id_, pipe,
                           staticCurry)
from fpe.itertools import (collect, drop, dropWhile, map_, partition, take,
                           takeWhile, zip_, zipPad, zipWith, zipWithPad)
from fpe.maybe import Just, Maybe, Nothing, Nothing_, isJust, isNothing
from fpe.seqtools import count, elem, first, foldl, foldl_
