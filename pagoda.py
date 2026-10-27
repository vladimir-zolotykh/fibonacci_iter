#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from array import array
from copy import copy

PegsType = list[array]
pegs = [array("i"), array("i"), array("i")]


def init_pegs(pegs: PegsType, num_disks: int) -> None:
    pegs[0] = array("i", list(range(num_disks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")


def validate(pegs: PegsType, src: int, dst: int) -> None:
    disk = pegs[src][-1]
    if not pegs[dst]:
        return  # emtpy peg
    under = pegs[dst][-1]
    if under > disk:
        return  # valid move
    raise RuntimeError(f"Cannot put {disk}#{src} over {under}#{dst}")


def move(pegs: PegsType, src: int, dst: int) -> None:
    validate(pegs, src, dst)
    pegs[dst].append(pegs[src].pop())


def solve(pegs: PegsType, num_disks: int, src: int, dst: int, aux: int) -> None:
    if num_disks <= 0:
        return
    solve(pegs, num_disks - 1, src, aux, dst)
    move(pegs, src, dst)
    solve(pegs, num_disks - 1, aux, dst, src)


def test_solve():
    init_pegs(pegs, 3)
    orig = copy(pegs[0])
    solve(pegs, 3, 0, 2, 1)
    assert orig == pegs[2]


if __name__ == "__main__":
    test_solve()
