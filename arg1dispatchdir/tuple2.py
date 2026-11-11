#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("fields", [])
        for name, index in enumerate(fields):
            setattr(cls, name, property(itemgetter(index)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls.fields)) != len(args):
            raise TypeError(f"{cls.__name__} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Exercise(Tuple):
    fields = ["name", "weight", "reps"]


if __name__ == "__main__":
    e = Exercise("squat", 86, 2)
    print(e)
