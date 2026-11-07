#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterable
import sys
from textwrap import dedent
import pytest


def flatten(items: list):
    for x in items:
        if not isinstance(x, str) and isinstance(x, Iterable):
            yield from flatten(x)
        else:
            yield x


def test_flatten(capsys):
    items = ["Dave", "Paula", ["Thomas", "Lewis"]]
    for x in flatten(items):
        print(x)
    assert capsys.readouterr().out == dedent(
        """\
Dave
Paula
Thomas
Lewis
"""
    )


if __name__ == "__main__":
    pytest.main(sys.argv)
