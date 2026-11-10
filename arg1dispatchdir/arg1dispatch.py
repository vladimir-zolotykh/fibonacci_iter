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
    print(f"{x!r} is {type(x)}")


@show.register(int)
def _(x):
    print(f"{x!r} is {type(x).__name__}")


@show.register(bool)
def _(x):
    print(f"{x!r} is {type(x).__name__}")


@show.register(float)
def _(x):
    print(f"{x!r} is {type(x).__name__}")


def main():
    show(10)
    show(True)
    show(3.14)
    show({"a": 1})


if __name__ == "__main__":
    main()
