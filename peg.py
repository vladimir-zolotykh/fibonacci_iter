#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Peg:
    def __init__(self, num_disks: int = 8):
        self.num_disks = num_disks
        self.data: bytearray = bytearray(num_disks)
        self.ptr: int = -1

    def push(self, disk: int) -> None:
        if self.ptr >= self.num_disks:
            raise IndexError(f"{self.__class__}: index out of range")
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


def test_peg123():
    p = Peg(8)
    t = range(1, 4)
    for x in t:
        p.push(x)
    for x in range(3, 0, -1):
        assert p.pop() == x
    with pytest.raises(IndexError, match="index out of range"):
        p.pop()
