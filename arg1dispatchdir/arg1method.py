#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import update_wrapper
from functools import singledispatch


class singledispatchmethod:
    """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """

    def __init__(self, func):
        if not callable(func) and not hasattr(func, "__get__"):
            raise TypeError(f"{func!r} is not callable or a descriptor")

        self.dispatcher = singledispatch(func)
        self.func = func

    def register(self, cls, method=None):
        """Registers a new implementation for the given *cls*."""
        return self.dispatcher.register(cls, func=method)

    def __get__(self, obj, cls=None):
        def _method(*args, **kwargs):
            method = self.dispatcher.dispatch(args[0].__class__)
            return method.__get__(obj, cls)(*args, **kwargs)

        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.register = self.register
        update_wrapper(_method, self.func)
        return _method

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, "__isabstractmethod__", False)


class Negator:
    @singledispatchmethod
    def neg(self, arg):
        raise NotImplementedError

    @neg.register
    def _(self, arg: int):
        return -arg

    @neg.register
    def _(self, arg: bool):
        return not arg


if __name__ == "__main__":

    n = Negator()
    print(n.neg(10))
    print((n.neg(True)))
