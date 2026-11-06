#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from textwrap import dedent
import pytest


def arg1dispatch(func):
    registry = {object: func}

    def dispatch(cls):
        for typ in cls.__mro__:
            if typ in registry:
                return registry[typ]
        return registry[object]

    def wrapper(arg, *args, **kwargs):
        impl = dispatch(type(arg))
        return impl(arg, *args, **kwargs)

    def register(typ):
        def inner(func):
            registry[typ] = func
            return func

        return inner

    wrapper.register = register
    wrapper.registry = registry
    wrapper.dispatch = dispatch

    return wrapper


@arg1dispatch
def show(x):
    print(f"{x} is neither int, str, float")


# registry[int] = _
@show.register(int)
def _(x):
    print(f"{x} is int")


@show.register(str)
def _(x):
    print(f"{x} is str")


@show.register(float)
def _(x):
    print(f"{x} is float")


def test_arg1dispatch_mro(capsys):
    class A:
        def __repr__(self):
            return f"<{type(self).__name__} object>"

    class B(A):
        pass

    class C(B):
        pass

    @show.register(A)
    def _(x):
        print(f"{x} is A")

    @show.register(C)
    def _(x):
        print(f"{x} is C")

    show(C())
    show(B())
    show(A())
    assert capsys.readouterr().out == dedent(
        """\
<C object> is C
<B object> is A
<A object> is A
"""
    )


def test_arg1dispatch_main(capsys):
    main()
    assert capsys.readouterr().out == dedent(
        """\
9 is int
hello is str
3.14159 is float
{'a': 1} is neither int, str, float
"""
    )


def main():
    show(9)
    show("hello")
    show(3.14159)
    show({"a": 1})


if __name__ == "__main__":
    main()
