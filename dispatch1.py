#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from textwrap import dedent


def dispatch1(default_func):
    registry = {object: default_func}

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
            return func  # ``def _()''

        return inner

    wrapper.register = register
    wrapper.registry = registry
    wrapper.dispatch = dispatch

    return wrapper


@dispatch1
def show(x):
    print(f"{x} is {type(x)} [not dispatchable]")


@show.register(int)
def _(x):
    print(f"{x} is int")


@show.register(float)
def _(x):
    print(f"{x} is float")


@show.register(str)
def _(x):
    print(f"{x} is str")


def test_dispatch1(capsys):
    main()
    assert capsys.readouterr().out == dedent(
        """\
12 is int
13.45 is float
foo is str
{'a': 1, 'b': 2} is <class 'dict'> [not dispatchable]
"""
    )


def main():
    show(12)
    show(13.45)
    show("foo")
    show({"a": 1, "b": 2})


if __name__ == "__main__":
    main()
