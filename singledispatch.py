#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def singledispatch(func):
    registry = {object: func}

    def dispatch(cls):
        for typ in cls.__mro__:
            if typ in registry:
                return registry[typ]
        return registry[object]

    def wrapper(arg, *args, **kwargs):
        implementation = dispatch(type(arg))
        return implementation(arg, *args, **kwargs)

    def register(typ):
        def inner(func):
            registry[typ] = func
            return wrapper

        return inner

    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = registry

    return wrapper


@singledispatch
def show(x):
    print(f"{x} is object")


@show.register(int)
def show(x):
    print(f"{x} is int")


@show.register(str)
def show(x):
    print(f"{x} is str")


@show.register(float)
def show(x):
    print(f"{x} is float")


if __name__ == "__main__":
    show(42)
    show("hello")
    show(3.14)
