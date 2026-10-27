#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from array import array
from copy import copy
import pytest

PegsType = list[array]
pegs = [array("i"), array("i"), array("i")]
num_moves: int = 0


def init_pegs(pegs: PegsType, num_disks: int) -> None:
    global num_moves
    pegs[0] = array("i", list(range(num_disks, 0, -1)))
    pegs[1] = array("i")
    pegs[2] = array("i")
    num_moves = 0


def validate(pegs: PegsType, src: int, dst: int) -> None:
    disk = pegs[src][-1]
    if not pegs[dst]:
        return  # emtpy peg
    under = pegs[dst][-1]
    if under > disk:
        return  # valid move
    raise RuntimeError(f"Cannot put {disk}#{src} over {under}#{dst}")


def move(pegs: PegsType, src: int, dst: int) -> None:
    global num_moves
    validate(pegs, src, dst)
    pegs[dst].append(pegs[src].pop())
    num_moves += 1


def solve(pegs: PegsType, num_disks: int, src: int, dst: int, aux: int) -> None:
    if num_disks <= 0:
        return
    solve(pegs, num_disks - 1, src, aux, dst)
    move(pegs, src, dst)
    solve(pegs, num_disks - 1, aux, dst, src)


def test_validate():
    init_pegs(pegs, 3)
    move(pegs, 0, 1)
    with pytest.raises(RuntimeError, match="Cannot put 2#0 over 1#1"):
        move(pegs, 0, 1)


@pytest.mark.parametrize(
    "num_disks, expected_num_moves",
    [
        (3, 7),
        (4, 15),
        (5, 31),
        (6, 63),
        (7, 127),
        (8, 255),
    ],
)
def test_solve(num_disks, expected_num_moves):
    init_pegs(pegs, num_disks)
    orig = copy(pegs[0])
    solve(pegs, num_disks, 0, 2, 1)
    assert orig == pegs[2]
    assert num_moves == expected_num_moves


if __name__ == "__main__":
    test_solve()
