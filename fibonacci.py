#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fib_recur(n):
    if n < 2:
        return n
    else:
        return fib_recur(n - 2) + fib_recur(n - 1)


def fib_iter(n, res: dict[int, int] = {0: 0, 1: 1}):
    if n in (0, 1):
        return res[n]
    for k in range(2, n + 1):
        res[k] = res[k - 2] + res[k - 1]
    return res[n]


def fib_tail(n, k=2, res={0: 0, 1: 1}):
    if n in (0, 1):
        return res[n]
    if k < n + 1:
        res[k] = res[k - 2] + res[k - 1]
        return fib_tail(n, k + 1, res)
    return res[n]


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
def test_fib(n, res):
    assert fib_recur(n) == res
    assert fib_iter(n) == res
    assert fib_tail(n) == res
