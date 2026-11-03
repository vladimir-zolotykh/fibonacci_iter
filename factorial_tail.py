#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def factorial_recur(n):
    if n == 0:
        return 1
    else:
        return factorial_recur(n - 1) * n


def factorial_iter(n):
    res = 1
    if n in (0, 1):
        return res
    else:
        for k in range(1, n + 1):
            res *= k
        return res


def factorial_tail(n, res=1):
    if n in (0, 1):
        return res
    else:
        return factorial_tail(n - 1, res * n)
