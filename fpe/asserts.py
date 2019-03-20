from typing import Any


class AssertError:

    @property
    def error(self) -> Any:
        return self._error

    def __init__(self, error: Any):
        self._error = error

    def __repr__(self):
        return "{}: <{}>".format(self.__class__.__name__, self.error)


class AssertWrongArgumentType(AssertError):

    def __init__(self, correct: str):
        super().__init__("Argument has to be " + correct)


class AssertNotCallable(AssertError):

    def __init__(self):
        super().__init__("Item has to be callable")


class AssertEmptyValue(AssertError):

    def __init__(self):
        super().__init__("Item must not be empty")


class AssertCurringError(AssertError):

    def __init__(self, error: str):
        super().__init__(error)


class AssertFunctionWrappingError(AssertError):

    def __init__(self, error: str):
        super().__init__(error)


class AssertFunctionCompositionError(AssertError):

    def __init__(self, error: str):
        super().__init__(error)


class AssertWrongArgumentsNumber(AssertError):

    def __init__(self, correct: str):
        super().__init__("Number of arguments has to be: " + correct)


class AssertWrongValue(AssertError):

    def __init__(self, wrong: str, correct: str):
        super().__init__("Item's value {} has to be {}".format(wrong, correct))


class AssertWrongType(AssertError):

    def __init__(self, wrong: str, correct: str):
        super().__init__("Item's type {} has to be {}".format(wrong, correct))


class AssertCheckingFailed(AssertError):

    def __init__(self, error: str):
        super().__init__(error)
