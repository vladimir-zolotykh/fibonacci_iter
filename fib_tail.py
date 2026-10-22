#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import pytest


def fib_recur(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib_recur(n - 2) + fib_recur(n - 1)


@pytest.mark.parametrize(
    "n, res",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
    ],
)
def test_fib_recur(n, res):
    assert fib_recur(n) == res
