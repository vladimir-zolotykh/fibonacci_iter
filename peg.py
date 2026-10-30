#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
from copy import copy, deepcopy
import logging
import pytest


class Peg:
    def __init__(self, num_disks: int = 8):
        self.num_disks = num_disks
        self.data: bytearray = bytearray(num_disks)
        self.ptr: int = -1

    def __copy__(self) -> Self:
        peg = Peg.__new__(Peg)
        peg.num_disks = self.num_disks
        peg.data = self.data.copy()
        peg.ptr = -1
        return peg

    def __eq__(self, other) -> bool:
        if isinstance(other, Peg):
            return self.data == other.data
        else:
            return NotImplemented

    def put_disks(self):
        for x in range(self.num_disks, 0, -1):
            self.push(x)

    def validate(self, disk: int) -> None:
        if self.ptr < 0:
            return
        under: int = self.data[self.ptr]
        logging.info(f"{disk = }, {under = }")
        if under != 0 and disk >= under:
            raise ValueError(
                f"{self.__class__.__name__}.validate: cannot put {disk} over {under}"
            )

    def push(self, disk: int) -> None:
        if self.ptr >= self.num_disks:
            raise IndexError(f"{self.__class__.__name__}.push: index out of range")
        self.validate(disk)
        self.ptr += 1
        self.data[self.ptr] = disk

    def __bool__(self) -> bool:
        # return self.data != bytearray(self.num_disks)
        return self.ptr >= 0

    @property
    def disk(self) -> int:
        if self.ptr < 0:
            raise IndexError(f"{self.__class__.__name__}.disk: index out of range")
        return self.data[self.ptr]

    def pop(self) -> int:
        if self.ptr < 0:
            raise IndexError(f"{self.__class__.__name__}.pop: index out of range")
        b: int = self.data[self.ptr]
        self.ptr -= 1
        return b

    def __repr__(self):
        return f"{self.data[:(self.ptr + 1)]}"


PegsType = list[Peg]


class Board:
    def __init__(self, num_disks: int = 3):
        self.pegs: PegsType = [Peg(num_disks), Peg(num_disks), Peg(num_disks)]
        self.pegs[0].put_disks()
        self.num_moves = 0

    def validate(self, src: int, dst: int) -> None:
        disk = self.pegs[src].disk
        if not self.pegs[dst]:
            return  # emtpy peg
        under = self.pegs[dst].disk
        if under > disk:
            return  # valid move
        raise RuntimeError(f"Cannot put {disk}#{src} over {under}#{dst}")

    def move(self, src: int, dst: int) -> None:
        self.validate(src, dst)
        self.pegs[dst].push(self.pegs[src].pop())
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
    # orig = deepcopy(brd.pegs[0])
    brd.solve(num_disks, 0, 2, 1)
    assert orig == brd.pegs[2]
    assert brd.num_moves == expected_num_moves


if __name__ == "__main__":
    test_solve(3, 7)
