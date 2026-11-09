#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
import warnings
from textwrap import dedent
import re
import pytest


class BunchMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        defaults = {}

        def __init__(self, **kwargs):
            for key, val in defaults.items():
                if key in kwargs:
                    val = kwargs.pop(key)
                setattr(self, key, val)
            if kwargs:
                warnings.warn("Not all kwargs are used")

        def __repr__(self):
            args = ", ".join(
                f"{key}={val!r}"
                for key, default in defaults.items()
                if (val := getattr(self, key)) != default
            )
            return f"{type(self).__name__}({args})"

        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                if key in ("__init__", "__repr__"):
                    raise TypeError("Cannot overwrite __init__, __repr__")
            else:
                defaults[key] = val
        newdict = {"__slots__": defaults, "__init__": __init__, "__repr__": __repr__}
        return super().__new__(mcls, clsname, bases, newdict)


class Bunch(metaclass=BunchMeta):
    pass


class Exercise(Bunch):
    name = "squat"
    weight = 82.5
    reps = 2


def test_exercise_warn():
    with pytest.raises(UserWarning, match="Not all kwargs are used"):
        Exercise(job="Junior engineer")


def test_init_overwrite():
    with pytest.raises(TypeError, match="Cannot overwrite __init__, __repr__"):

        class Exercise(Bunch):
            def __init__(self):
                pass


def test_exercise(capsys):
    p = Exercise()
    print(p)
    p = Exercise(name="bench press", weight=77.5, reps=3)
    print(p)
    assert capsys.readouterr().out == dedent(
        """\
Exercise()
Exercise(name='bench press', weight=77.5, reps=3)
"""
    )


if __name__ == "__main__":
    pytest.main(sys.argv)
