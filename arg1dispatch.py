#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


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


if __name__ == "__main__":
    show(9)
    show("hello")
    show(3.14159)
