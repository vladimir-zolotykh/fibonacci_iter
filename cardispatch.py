#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from textwrap import dedent
import pytest


def cardispatch(default):
    registry = {object: default}

    def dispatch(cls):
        for typ in cls.__mro__:
            if typ in registry:
                return registry[typ]
        return registry[object]

    def wrapper(arg1, *args, **kwargs):
        impl = dispatch(type(arg1))
        return impl(arg1, *args, **kwargs)

    def register(typ):
        def inner(func):
            registry[typ] = func
            return func

        return inner

    wrapper.register = register
    wrapper.registry = registry
    wrapper.dispatch = dispatch
    return wrapper


@cardispatch
def show(x):
    print(f"type of {x} is unknown")


@show.register(int)
def _(x):
    print(f"{x} is int")


@show.register(float)
def _(x):
    print(f"{x} is float")


@show.register(str)
def _(x):
    print(f"{x} is str")


def main():
    show(11)
    show(31.4159)
    show("foo")
    show({"a": 1, "b": 2})


def test_cardispatch(capsys):
    main()
    assert capsys.readouterr().out == dedent(
        """\
11 is int
31.4159 is float
foo is str
type of {'a': 1, 'b': 2} is unknown
"""
    )


if __name__ == "__main__":
    main()
