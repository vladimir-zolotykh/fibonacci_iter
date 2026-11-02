#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def factorial_recur(n):
    if n == 0:
        return 1
    else:
        return factorial_recur(n - 1) * n


@pytest.mark.parametrize(
    "n, fact",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
    ],
)
def test_factorial_recur(n, fact):
    assert factorial_recur(n) == fact
