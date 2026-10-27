#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from array import array
from copy import copy
import pytest

PegsType = list[array]
pegs = [array("i"), array("i"), array("i")]
num_moves: int = 0


class Board:
    def __init__(self, num_disks: int = 3):
        self.pegs: PegsType = [array("i"), array("i"), array("i")]
        self.pegs[0] = array("i", list(range(num_disks, 0, -1)))
        self.pegs[1] = array("i")
        self.pegs[2] = array("i")
        self.num_moves = 0

    def validate(self, src: int, dst: int) -> None:
        disk = self.pegs[src][-1]
        if not self.pegs[dst]:
            return  # emtpy peg
        under = self.pegs[dst][-1]
        if under > disk:
            return  # valid move
        raise RuntimeError(f"Cannot put {disk}#{src} over {under}#{dst}")

    def move(self, src: int, dst: int) -> None:
        self.validate(src, dst)
        self.pegs[dst].append(self.pegs[src].pop())
        self.num_moves += 1

    def solve(self, num_disks: int, src: int, dst: int, aux: int) -> None:
        if num_disks <= 0:
            return
        self.solve(num_disks - 1, src, aux, dst)
        self.move(src, dst)
        self.solve(num_disks - 1, aux, dst, src)


def test_validate():
    brd = Board(3)
    brd.move(0, 1)
    with pytest.raises(RuntimeError, match="Cannot put 2#0 over 1#1"):
        brd.move(0, 1)


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
    brd = Board(num_disks)
    orig = copy(brd.pegs[0])
    brd.solve(num_disks, 0, 2, 1)
    assert orig == brd.pegs[2]
    assert brd.num_moves == expected_num_moves


if __name__ == "__main__":
    test_solve()
