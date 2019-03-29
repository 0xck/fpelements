import inspect
from abc import ABCMeta, abstractmethod
from collections.abc import OrderedDict
from functools import reduce
from typing import Any, Callable, Dict, Tuple, Union

from fpe.asserts import (AssertCurringError, AssertFunctionCompositionError,
                         AssertFunctionWrappingError, AssertNotCallable,
                         AssertWrongArgumentType, AssertWrongType)


# inspect.isbuiltin does not work for all built-ins
# see https://bugs.python.org/issue23525
_unknown_builtin = (dict, help, slice, object, enumerate, staticmethod, int, str,
    bool, bytearray, filter, super, bytes, float, tuple, property, type,
    frozenset, list, range, classmethod, zip, map, reversed, complex,
    memoryview, set)


def _is_variable(func: Callable) -> bool:
    "Checking if function has variable arguments of any kind"

    # only callable
    assert callable(func), AssertNotCallable()
    # only non builtin
    assert func not in _unknown_builtin, AssertWrongArgumentType(
        "builtin functions or methods are not supported")
    assert not inspect.isbuiltin(func), AssertWrongArgumentType(
        "builtin functions or methods are not supported")

    # for working with wrapped functions
    args = inspect.getfullargspec(getattr(func, "func", func))

    return (args[1] is not None) or (args[2] is not None)


def _get_defaults(func: Callable) -> Tuple[Any, ...]:
    """Getting function defaults

    Similar to func.__defaults__
    """

    # only callable
    assert callable(func), AssertNotCallable()
    # only non builtin
    assert func not in _unknown_builtin, AssertWrongArgumentType(
        "builtin functions or methods are not supported")
    assert not inspect.isbuiltin(func), AssertWrongArgumentType(
        "builtin functions or methods are not supported")

    return inspect.getfullargspec(getattr(func, "func", func))[3] or tuple()


def _is_defaults(func: Callable) -> bool:
    """Checking if function has default arguments

    Similar to bool(func.__defaults__)
    """

    # only callable
    assert callable(func), AssertNotCallable()
    # only non builtin
    assert func not in _unknown_builtin, AssertWrongArgumentType(
        "builtin functions or methods are not supported")
    assert not inspect.isbuiltin(func), AssertWrongArgumentType(
        "builtin functions or methods are not supported")

    return bool(_get_defaults(func))


def _get_arg_count(func: Callable) -> int:
    """Getting number of function arguments

    Similar to func.__code__.co_argcount
    """
    # only callable
    assert callable(func), AssertNotCallable()
    # only non builtin
    assert func not in _unknown_builtin, AssertWrongArgumentType(
        "builtin functions or methods are not supported")
    assert not inspect.isbuiltin(func), AssertWrongArgumentType(
        "builtin functions or methods are not supported")

    return len(inspect.getfullargspec(getattr(func, "func", func))[0])


def _func_to_tuple(func: Callable) -> Tuple[Callable, ...]:
    """Return tuple from given function

    It works with ordinary functions and with Function objects.
    Return is always tuple with 1 given function given is not
    FunctionComposition. Otherwise it returns tuple several functions.
    """

    # only callable
    assert callable(func), AssertNotCallable()

    if isinstance(func, FunctionComposition):
        result: Tuple[Callable, ...] = func.func

        # it has to be tuple
        assert isinstance(result, tuple), AssertWrongType(str(type(result)), str(tuple()))

    else:
        result: Tuple[Callable, ...] = (func, )

    return result


def is_curried(func: Callable) -> bool:
    # checking if function is curried function

    # only callable
    assert callable(func), AssertNotCallable()

    return getattr(func, "is_curried", False)


class Function(metaclass=ABCMeta):
    """Abstract class for representation advanced function features

    Function serves as base class for currying and function composition.
    It provides redefined * and | methods for supporting function
    composition syntax.
    """

    @property
    @abstractmethod
    def retracted(self) -> int:
        pass

    @property
    @abstractmethod
    def is_curried(self) -> bool:
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @property
    def func(self) -> Union[Callable, Tuple[Callable, ...]]:
        return self._func

    def __get__(self, obj, _) -> Callable:
        # working with decorated class' methods

        def wrapper(*args, **kwargs):
            return self(obj, *args, **kwargs)

        return wrapper

    @staticmethod
    def _compose(func1: Callable, func2: Callable) -> "FunctionComposition":
        """General composition method: (f, g) = g(f)

        It takes 2 functions and return their composition where func1 executes before func2.
        Composition works on all callable objects, but it consider them as one-argument function,
        and if there are more arguments, then
            if function is curried and waits for one argument, then it executes regular way
            if function is curried and waits for more than one argument, then it retracted given argument and returns curried function
            otherwise TypeError is raised: 'func expected N arguments, got 1'
        """

        composed = FunctionComposition(func1, func2)

        # at least 2 functions in composition
        assert len(composed.func) > 1, AssertFunctionCompositionError(
            "composition must contain at least 2 functions, but current contains {}".format(len(composed.func)))
        # composition must contain only callable
        assert all(callable(i) for i in composed.func), AssertFunctionCompositionError(
            "composition must contains only callable objects")
        # wrong function order or given functions are not in composition
        # checked by compare tail of composition function tuple with union of given functions tuple
        # E.g.
        #   func1.func == (f1, f2, f3, f4), func2 is curried function, then
        #   composition.func == (f1, f2, f3, f4, func2), so that it is compared like
        #   composition.func == func1.func + (func2, ) or
        #   (f1, f2, f3, f4, func2) == (f1, f2, f3, f4) + (func2, )
        assert composed.func == reduce(lambda acc, x: acc + _func_to_tuple(x), (func1, func2), tuple()), AssertFunctionCompositionError(
            "composition does not contain given functions or has them in wrong order")

        return composed

    def __mul__(self, other: Callable) -> "FunctionComposition":
        """Math-style composition method: (g * f) = g(f) for left argument

        Useful when left argument is Function obj and right is any callable.
        Borrowed from (.) :: (b -> c) -> (a -> b) -> a -> c
        """

        return self._compose(other, self)

    def __rmul__(self, other: Callable) -> "FunctionComposition":
        """Math-style composition method: (g * f) = g(f) for right argument.

        Useful when left argument is not Function obj, but callable and right is Function obj.
        Borrowed from (.) :: (b -> c) -> (a -> b) -> a -> c
        """

        return self._compose(self, other)

    def __or__(self, other: Callable) -> "FunctionComposition":
        """Pipe-style composition method: (f | g) = g(f) for left argument

        Useful when left argument is Function obj and right is any callable.
        Reversed composition borrowed from (flip (.)) :: (a -> b) -> (b -> c) -> a -> c
        """

        return self.__rmul__(other)

    def __ror__(self, other: Callable) -> "FunctionComposition":
        """Pipe-style composition method: (f | g) = g(f) for right argument

        Useful when left argument is not Function obj, but callable and right is Function obj.
        Reversed composition borrowed from (flip (.)) :: (a -> b) -> (b -> c) -> a -> c
        """

        return self.__mul__(other)

    def _copy_meta(self, defaults=(None, None, None, None)):

        # assign some meta
        self.__doc__ = getattr(self._func, "__doc__", defaults[0])
        self.__name__ = getattr(self._func, "__name__", defaults[1])
        self.__module__ = getattr(self._func, "__module__", defaults[2])
        self.__qualname__ = getattr(self._func, "__qualname__", defaults[3])

    def __repr__(self):

        return "{}, retracted: function <{}>, number of arguments <{}>".format(
            self.__class__.__name__, self._func, self.retracted)


class CurriedFunctionPositionals(Function):
    """Curring function with positional only arguments representation class

    Thus
        func = CurriedFunctionPositionals(f)
        func(x)(y, z) == func(x, y)(z) == f(x, y, z)
    """

    def __init__(self, func: Callable):

        # only callable
        assert callable(func), AssertNotCallable()
        # only non builtin
        assert (func not in _unknown_builtin) and (not inspect.isbuiltin(func)), AssertCurringError(
            "builtin functions or methods are not supported")
        # func with variable arguments
        assert not _is_variable(func), AssertFunctionWrappingError(
            "functions with variable number of arguments are not supported")
        # at least 2 args required
        assert _get_arg_count(func) > 1, AssertFunctionWrappingError(
            "functions with less than 2 arguments are not supported")
        # only positional arguments
        assert not _is_defaults(func), AssertFunctionWrappingError(
            "function must not have keyword arguments")

        self._func: Callable = func
        self._args: Tuple[Any, ...] = tuple()
        self._original_arg_count: int = _get_arg_count(func)
        self._copy_meta()

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def retracted(self) -> int:
        return len(self._args)

    @property
    def is_curried(self) -> bool:
        return True

    def __call__(self, *args: Any, **kwargs: Any) -> Any:

        # check if all arguments were retracted
        # if yes, then return original function
        if (len(self._args) + len(args)) >= self._original_arg_count:
            return self._func(*(self._args + args))

        curried = self.__class__(self._func)
        curried._args = (self._args + args)[:]

        return curried


class CurriedFunctionDefaults(Function):
    """Curring function with defaults arguments representation class

    Thus
        func = CurriedFunctionDefaults(f)
        func(x)(y=5, z=10) == func(x, y=5) == f(x, y=5, z=10) == func(x, y=5)
    """

    def __init__(self, func: Callable):

        # only callable
        assert callable(func), AssertNotCallable()
        # only non builtin
        assert (func not in _unknown_builtin) and (not inspect.isbuiltin(func)), AssertCurringError(
            "builtin functions or methods are not supported")
        # func with variable arguments
        assert not _is_variable(func), AssertFunctionWrappingError(
            "functions with variable number of arguments are not supported")
        # at least 2 args required
        assert _get_arg_count(func) > 1, AssertFunctionWrappingError(
            "functions with less than 2 arguments are not supported")
        # only positional arguments
        assert _is_defaults(func), AssertFunctionWrappingError(
            "function must have keyword arguments")

        self._func: Callable = func
        self._args: Tuple[Any, ...] = tuple()
        self._original_arg_count: int = _get_arg_count(func)

        # set defaults
        self._original_defaults: Tuple[Any, ...] = _get_defaults(func)
        start: int = self._original_arg_count - len(self._original_defaults)
        end: int = start + len(self._original_defaults)
        self._defaults: Dict[str, Any] = OrderedDict(
            zip(func.__code__.co_varnames[start:end], self._original_defaults))

        # set kwargs with initial defaults
        self._kwargs: Dict[str, Any] = self._defaults.copy()
        self._copy_meta()

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    @property
    def retracted(self) -> int:
        return len(self._args) + len(self._kwargs)

    @property
    def is_curried(self) -> bool:
        return True

    def __call__(self, *args: Any, **kwargs: Any) -> Any:

        # updating keyword arguments with given
        kw: Dict[str, Any] = self._kwargs.copy()
        kw.update(kwargs)

        num_args: int = len(args) + len(self._args)

        # if kwargs are not keyword arguments, then
        # return it with all arguments,
        # let python handles the error itself
        if kwargs and not set(self._defaults).issuperset(set(kwargs)):
            return self._func(*(self._args + args), **kw)

        # if positionals equal or more than all possible arguments
        # let python handles the error itself when extra arguments exist
        if num_args >= self._original_arg_count:
            return self._func(*(self._args + args), **kwargs)

        # if positionals are more than non-defaults,
        # but less than all possible arguments, then
        # borrow necessary from defaults
        if (num_args > (self._original_arg_count - len(self._original_defaults))):

            defaults: Dict[str, Any] = OrderedDict(
                (k, kw[k]) for k in tuple(kw)[-(self._original_arg_count - num_args):])

            return self._func(*(self._args + args), **defaults)

        # if enough or more positionals and keyword arguments
        # let python handles the error itself when extra arguments exist
        if (num_args + len(kw)) >= self._original_arg_count:
            return self._func(*(self._args + args), **kw)

        # curry current with additional arguments
        curried = self.__class__(self._func)
        curried._args = (self._args + args)[:]
        curried._kwargs.update(kwargs)

        return curried


class CurriedFunctionFixedArgumentsNumber(Function):
    """Curring function by using fixed number of positionals representation class

    Thus
        func = CurriedFunctionFixedArgumentsNumber(3, f)
        func(x)(y, z) == func(x, y)(z) == f(x, y, z)

    Warning.
        This approach changed obvious function behavior and may lead to tricky
        and hidden errors, that are hard to troubleshooting.
        Before using make sure you understand principles of its working.

    This works only if enough number of positional arguments are provided.
    Keyword arguments are not handled until that. Check following
    examples, for better understanding:

        f = curry(3)func(a, b, x=0); f(1, 2) #  will not work, due lack of positionals
        f = curry(3)func(a, b, x=0); f(1, 2, x=10) #  will not work, due lack of positionals
        f = curry(3)func(a, b, x=0); f(1, 2, 10) #  will work
        f = curry(2)func(a, b, c, x=0); f(1)(2, 3) #  will not work, due wrong number of fixed
        f = curry(3)func(a, b, c, x=0); f(1, 2)(3) #  will work
        f = curry(3)func(a, b, c, x=0); f(1)(2, 3, x=10) #  will work
        f = curry(3)func(a, b, c, x=0); f(1, 2)(3, 10) #  will work
        f = curry(3)func(a, b, c, x=0, y=1); f(1, 2)(3, 10) #  will work
        f = curry(3)func(a, b, c, x=0, y=1); f(1, 2)(3, 10)(11) #  will work
        f = curry(3)func(x=0, y=1, z=2); f() #  will not work, due lack of positionals
        f = curry(3)func(x=0, y=1, z=2); f(1, 2) #  will not work, due lack of positionals
        f = curry(3)func(x=0, y=1, z=2); f(1, 2, 3) #  will work
        f = curry(3)func(*args); f(1, 2, 3) #  will work
        f = curry(3)func(*args); f(1, 2) #  will not work, due lack of positionals
        f = curry(3)func(a, *args); f(1, 2, 3) #  will work
        f = curry(3)func(a, b, *args); f(1, 2, 3) #  will work
        f = curry(3)func(a, b, *args); f(1, 2)(3, 4)(5) #  will work
        f = curry(3)func(a, b, *args, x=0); f(1)(2, 3, x=10) #  will work
        f = curry(2)func(a, *args, x=0); f(1, x=10) #  will not work, due lack of positionals
    """

    def __init__(self, num: int, func: Callable):

        # only callable
        assert callable(func), AssertNotCallable()
        # wrong arguments number
        assert num > 1, AssertFunctionWrappingError(
            "number of arguments has to be at least 2")

        self._func: Callable = func
        self._args: Tuple[Any, ...] = tuple()
        self._original_arg_count: int = num
        self._copy_meta(defaults=("curried: {}".format(func), None, None, None))

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def retracted(self) -> int:
        return len(self._args)

    @property
    def is_curried(self) -> bool:
        return True

    def __call__(self, *args: Any, **kwargs: Any) -> Any:

        # check if all arguments were retracted
        # if yes, then return original function
        if (len(self._args) + len(args)) >= self._original_arg_count:
            return self._func(*(self._args + args))

        curried = self.__class__(self._original_arg_count, self._func)
        curried._args = (self._args + args)[:]

        return curried

    def __repr__(self):
        return super().__repr__() + ", number of fixed <{}>".format(self._original_arg_count)


class FunctionComposition(Function):
    """Function composition representation class

    Thus FunctionComposition(f, g)(x) == g(f(x))

    Borrowed from (.) :: (b -> c) -> (a -> b) -> a -> c

    Note.
        Composition must satisfy the following laws:
            (h . g) . f = h . (g . f)
            f . id = f
            id . f = f

        Current implementation satisfies these laws.
    """

    def __init__(self, func1: Callable, func2: Callable):

        # only callable
        assert callable(func1) and callable(func2), AssertNotCallable()

        self._func: Tuple[Callable, ...] = _func_to_tuple(func1) + _func_to_tuple(func2)

        # at least 2 functions in composition
        assert len(self._func) > 1, AssertFunctionWrappingError(
            "composition must contain at least 2 functions, but current contains {}".format(len(self._func)))
        # composition must contain only callable
        assert all(callable(i) for i in self._func), AssertFunctionWrappingError(
            "composition must contains only callable objects")

    @property
    def retracted(self) -> int:
        return 0

    @property
    def is_curried(self) -> bool:
        return False

    def __call__(self, value: Any) -> Any:

        result = value

        for f in self._func:
            result = f(result)

        return result

        def __repr__(self):

            return "{}, retracted: functions <{}>".format(self.__class__.__name__, self._func)


class _idFunction(Function):
    """Class for representation id function

    id functions returns given value.

    Thus _idFunction()(x) == x

    Borrowed from id :: a -> a
    """

    @property
    def func(self) -> "_idFunction":
        return self

    @property
    def retracted(self) -> int:
        return 0

    @property
    def is_curried(self) -> bool:
        return False

    def __call__(self, value: Any) -> Any:
        return value

    def __repr__(self):
        return "id"


# id function
id_ = _idFunction()


def _curry_common(func: Callable) -> Union[CurriedFunctionDefaults, CurriedFunctionPositionals]:
    """Curring function for functions with at least 2 positional and keyword arguments

    Thus:
        for positionals: curry(f)(x)(y, z) == curry(f)(x, y)(z) == f(x, y, z)
        for defaults: curry(f)(x)(y=5, z=10) == curry(f)(x, y=5) == f(x, y=5, z=10)
    """

    # only callable
    assert callable(func), AssertNotCallable()
    # only non builtin
    assert (func not in _unknown_builtin) and (not inspect.isbuiltin(func)), AssertCurringError(
        "builtin functions or methods are not supported")

    if _is_defaults(func):
        curried = CurriedFunctionDefaults(func)
        # wrong arguments number
        assert 0 <= curried.retracted <= _get_arg_count(func), AssertCurringError(
            "processed function has wrong argument number")

    else:
        curried = CurriedFunctionPositionals(func)
        # wrong arguments number
        assert 0 <= curried.retracted < _get_arg_count(func), AssertCurringError(
            "processed function has wrong argument number")

    # wrong func
    assert func is curried.func, AssertCurringError(
        "processed function is different from origin")

    return curried


@_curry_common
def _curry_fixed(num: int, func: Callable) -> CurriedFunctionFixedArgumentsNumber:
    """Curring function for functions with given number of positional arguments

    Thus curry(3)(f)(x)(y, z) == curry(3)(f)(x, y)(z) == f(x, y, z)
    """

    curried = CurriedFunctionFixedArgumentsNumber(num, func)

    # wrong arguments number
    assert 0 <= curried.retracted < num, AssertCurringError(
        "processed function has wrong argument number")

    # wrong func
    assert func is curried.func, AssertCurringError(
        "processed function is different from origin")

    return curried


def curry(func_or_num: Union[int, Callable]) -> Union[CurriedFunctionDefaults,
                                                    CurriedFunctionPositionals,
                                                    CurriedFunctionFixedArgumentsNumber]:
    """Decorator for curring function of at least 2 arguments

    Thus:
        for positionals: curry(f)(x)(y, z) == curry(f)(x, y)(z) == f(x, y, z)
        for defaults: curry(f)(x)(y=5, z=10) == curry(f)(x, y=5) == f(x, y=5, z=10)
        for fixed arguments number: curry(3)(f)(x)(y, z) == curry(3)(f)(x, y)(z) == f(x, y, z)
    """

    # only callable
    assert callable(func_or_num) or isinstance(
        func_or_num, int), AssertCurringError(
            "curry decorator passes only callable or number of fixed arguments")

    if isinstance(func_or_num, int):
        return _curry_fixed(func_or_num)

    return _curry_common(func_or_num)


@curry
def compose(func1: Callable, func2: Callable) -> FunctionComposition:
    """Wrapper on Function._compose for getting any 2 functions composed in math-style

    This is math-style composition, so second given function will be executed first.
    Thus compose(g, f)(x) == g(f(x))
    """
    return Function._compose(func2, func1)


@curry
def pipe(func1: Callable, func2: Callable) -> FunctionComposition:
    """Wrapper on Function._compose for getting any 2 functions composed in pipe-style

    This is pipe-style composition, so first given function will be executed first.
    Thus pipe(f, g)(x) == g(f(x))
    """
    return Function._compose(func1, func2)
