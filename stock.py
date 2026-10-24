#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import pytest


class Field(ABC):
    def __set_name__(self, owner, name):
        self.sys_name = f"sys_{name}"
        self.usr_name = f"usr_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.sys_name]

    def __set__(self, instance, val):
        self.validate(instance, val)
        instance.__dict__[self.sys_name] = val

    @abstractmethod
    def validate(self, instance, val):
        pass


class Typed:
    def validate(self, instance, val):
        if not isinstance(val, self._expected):
            raise TypeError(f"{val!r} is not of type {self._expected}")


class Unsigned:
    def validate(self, instancem, val):
        if val < 0:
            raise ValueError(f"{val!r} must not be signed")


class MaxSized(Field):
    def __init__(self, size=8):
        self.size = size

    def validate(self, instancem, val):
        if len(val) > self.size:
            raise ValueError(
                f"{val!r} must not exceed {self.size} characters in lenght"
            )


class String(Typed):
    _expected = str


class Float(Typed):
    _expected = float


class Integer(Typed):
    _expected = int


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class SizedString(String, MaxSized):
    pass


class Stock:
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


@pytest.fixture
def stock():
    return Stock("ACME", 50, 91.1)


def test_sizedstring(stock):
    assert stock.name == "ACME"


if __name__ == "__main__":
    s = Stock("ACME", 50, 91.1)
    print(s.name, s.shares, s.price)
