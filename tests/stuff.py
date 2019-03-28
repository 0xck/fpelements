import operator

import hypothesis.strategies as st

from fpe.functions import _unknown_builtin, compose, curry, id_


# python functions
builtins = (
    abs, min, setattr, all, dir, hex, next, any, divmod, id, sorted, ascii,
    input, oct, bin, eval, open, exec, isinstance, ord, sum, issubclass, pow,
    iter, print, callable, format, len, chr, vars, getattr, locals, repr, compile,
    globals, hasattr, max, round, delattr, hash)

bin_op_cmp = (operator.lt, operator.le, operator.eq,
              operator.ne, operator.ge, operator.gt)

bin_op_math = (operator.add, operator.floordiv, operator.truediv,
               operator.sub, operator.mul, operator.mod, operator.pow)

bin_op_log = (operator.and_, operator.or_, operator.xor)

bin_op_bin = (operator.rshift, operator.lshift)

seq_op = (operator.concat, operator.contains,
          operator.delitem, operator.getitem, operator.setitem)

known_builtins = builtins + _unknown_builtin + bin_op_cmp + \
    bin_op_math + bin_op_log + bin_op_bin + seq_op

# hypothesis stuff
numbers = st.floats(allow_nan=False, allow_infinity=False) | st.integers()
# non seq means non containers
non_seq = st.none() | st.booleans() | st.text() | numbers | st.binary()
# seq means containers
seq = st.lists(non_seq) | st.tuples(non_seq)
# mappings
sets = st.sets(non_seq)
maps = st.dictionaries(st.text() | st.integers(), non_seq | seq | sets)
collections = seq | sets | maps
# all
random_types = non_seq | seq | sets | maps


@curry
def kleisli(cls, f, a):
    return cls(f(a))


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
