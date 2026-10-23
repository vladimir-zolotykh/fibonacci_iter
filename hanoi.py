#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from copy import copy
from array import array
import pytest


pegs: [array("i"), array("i"), array("i")]
PegType = array
PegsType = list[PegType]


def init_pegs(pegs: PegsType, ndisks: int = 3):
    pegs[0] = array("i", list(range(ndisks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")


def move(pegs: PegsType, src: int, dst: int) -> None:
    validate(pegs, src, dst)
    dst.append(src.pop())


def validate(pegs: PegsType, src: int, dst: int) -> None:
    disk = src[-1:]
    under = dst[-1:]
    if under > disk:
        return
    raise RuntimeError(f"Cannot put {disk} #src on {under} #{dst}")


def solve(pegs: PegsType, n: int, src: int, dst: int, aux: int) -> None:
    if n <= 0:
        return
    solve(pegs, n - 1, src, aux, dst)
    move(pegs, src, dst)
    solve(pegs, n - 1, aux, dst, src)


@pytest.mark.parametrize(
    "n",
    [
        3,
    ],
)
def test_solve(n):
    init_pegs(pegs, n)
    orig = copy(pegs[0])
    solve(n, pegs, 0, 2, 1)
    assert pegs[2] == orig
