#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def fib_recur(n: int) -> int:
    if n < 2:
        return n
    else:
        return fib_recur(n - 2) + fib_recur(n - 1)


def fib_iter(n: int) -> int:
    res = {}
    for i in range(n + 1):
        if i < 2:
            res[i] = i
        else:
            res[i] = res[i - 2] + res[i - 1]
    return res[n]


def fib_tail(n: int, i: int = 0, res={}) -> int:
    if i > n:
        return res[n]
    else:
        if i < 2:
            res[i] = i
        else:
            res[i] = res[i - 2] + res[i - 1]
        return fib_tail(n, i + 1, res)
