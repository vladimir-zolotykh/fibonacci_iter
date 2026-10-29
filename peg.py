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
