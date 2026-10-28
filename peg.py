#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import logging
import pytest


class Peg:
    def __init__(self, num_disks: int = 8):
        self.num_disks = num_disks
        self.data: bytearray = bytearray(num_disks)
        self.ptr: int = -1

    def validate(self, disk: int) -> None:
        if self.ptr < 0:
            return
        under: int = self.data[self.ptr]
        logging.info(f"{disk = }, {under = }")
        if under != 0 and disk >= under:
            raise ValueError(f"{self.__class__}: cannot put {disk} over {under}")

    def push(self, disk: int) -> None:
        if self.ptr >= self.num_disks:
            raise IndexError(f"{self.__class__}: index out of range")
        self.validate(disk)
        self.ptr += 1
        self.data[self.ptr] = disk

    def pop(self) -> int:
        if self.ptr < 0:
            raise IndexError(f"{self.__class__}: index out of range")
        b: int = self.data[self.ptr]
        self.ptr -= 1
        return b

    def __repr__(self):
        return f"{self.data[:(self.ptr + 1)]}"


def test_peg_push():
    p = Peg(8)
    p.push(3)
    p.push(2)
    with pytest.raises(ValueError, match="cannot put 3 over 2"):
        p.push(3)


def test_peg_empty():
    p = Peg(8)
    assert str(p) == "bytearray(b'')"


def test_peg123():
    p = Peg(8)
    # t = range(1, 4)
    # for x in t:
    for x in range(3, 0, -1):
        p.push(x)
    # for x in range(3, 0, -1):
    for x in range(1, 4):
        assert p.pop() == x
    with pytest.raises(IndexError, match="index out of range"):
        p.pop()


def test_peg1_8():
    p = Peg(8)
    # for i in range(1, 9):
    for i in range(8, 0, -1):
        p.push(i)
    assert p.data == bytearray(reversed(bytearray(b"\x01\x02\x03\x04\x05\x06\x07\x08")))
    # with pytest.raises(IndexError, match="index out of range"):
    #     p.push(9)
