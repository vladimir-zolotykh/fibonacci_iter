#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import pytest


def fib_recur(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib_recur(n - 2) + fib_recur(n - 1)


def fib_iter(n: int) -> int:
    res = {0: 0, 1: 1}
    for i in range(n + 1):
        if i < 2:
            res[i] = i
        else:
            res[i] = res[i - 2] + res[i - 1]
    return res[n]


def fib_tail(n: int, res={0: 0, 1: 1}) -> int:
    if n < 2:
        return res[n]
    else:
        res[n] = res[n - 1] + res[n - 2]
        print(f"    {res = }")
        return fib_tail(n - 1, res)


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
def test_fib_iter(n, res):
    assert fib_iter(n) == res


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
