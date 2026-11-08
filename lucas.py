#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""Tower of Hanoi game"""
import sys
from array import array
from copy import deepcopy
import pytest

pegs = [array("i"), array("i"), array("i")]
num_moves: int = 0


def init_pegs(num_disks: int = 3):
    assert num_disks in range(10)
    pegs[0] = array("i", list(range(num_disks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")


def validate(src: int, dst: int):
    assert {src, dst}.issubset(set(range(3)))
    if not pegs[src]:
        return
    disk = pegs[src][-1]
    if not pegs[dst]:
        return
    under = pegs[dst][-1]
    if disk >= under:
        raise ValueError(f"Cannot put {disk} over {under}")


def move(src: int, dst: int):
    global num_moves
    assert {src, dst}.issubset(set(range(3)))
    validate(src, dst)
    pegs[dst].append(pegs[src].pop())
    num_moves += 1


def solve(n: int, src: int, dst: int, aux: int):
    assert 0 in range(9)
    assert {src, dst}.issubset(set(range(3)))
    if n < 1:  # n < 0
        return
    solve(n - 1, src, aux, dst)
    move(src, dst)
    solve(n - 1, aux, dst, src)


@pytest.mark.parametrize("num_disks", (3, 4, 5, 6, 7, 8, 9))
def test_solve(num_disks):
    init_pegs(num_disks)
    orig = deepcopy(pegs[0])
    solve(num_disks, 0, 2, 1)
    assert orig == pegs[2]


if __name__ == "__main__":
    pytest.main(sys.argv)
