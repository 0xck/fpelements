from fpe.either import Left, Right
from fpe.asserts import AssertNotCallable
from fpe.functions import enrichFunction


FATAL_EXCEPTIONS = (AssertionError, EOFError, GeneratorExit, ImportError, KeyboardInterrupt,
                    MemoryError, NameError, ReferenceError, RuntimeError, SyntaxError, SystemError, SystemExit)


@enrichFunction
def try_(func_or_obj, *args, **kwargs):
    """Function for safely handling 'non-fatal' exceptions.

    Function takes first argument as possible callable or any object,
    rest arguments as positional and key value arguments, that are
    used for calling taken first argument. If first argument is callable,
    then it is called with given arguments and its result is returned as
    Right if exceptions do not occur, otherwise Left which contains caught
    exception. If first argument is not callable and arguments are empty,
    then function returns Right which contains first argument.
    E.g.
        def div(a, b):
            return a//b

        try_(div, 42, 2)  # Right(21)
        try_(div, 42, 0)  # Left(ZeroDivisionError('...'))

        # variant with classical function form demands additional `lambda`
        try_(lambda: div(42, 2))  # Right(21)
        try_(lambda: div(42, 0))  # Left(ZeroDivisionError('...'))

    Note.
        Functions handles only Exception heirs and only part of them.
        See `FATAL_EXCEPTIONS` for checking non-handled exception types.
    """

    assert callable(func_or_obj) or (not callable(func_or_obj) and not (bool(args) or bool(kwargs))
        ), AssertNotCallable("Can not handle non-callable object with arguments.")

    if not callable(func_or_obj):
        return Right(func_or_obj)

    try:
        return Right(func_or_obj(*args, **kwargs))

    except FATAL_EXCEPTIONS:
        raise

    except Exception as exc:
        return Left(exc)
