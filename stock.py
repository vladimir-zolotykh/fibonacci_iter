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


class Typed(Field):
    def validate(self, instance, val):
        if not isinstance(val, self._expected):
            raise TypeError(f"{val!r} is not of type {self._expected}")


class Unsigned(Field):
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

    def validate(self, instance, val):
        if not isinstance(val, self._expected):
            raise TypeError(f"{val!r} must be of type {self._expected}")


class Float(Typed):
    _expected = float

    # def validate(self, instance, val):
    #     print(f"{val = }")
    #     if not isinstance(val, self._expected):
    #         raise TypeError(f"{val!r} is not of type {self._expected}")


class Integer(Typed):
    _expected = int


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    print("UnsignedFloat")

    def validate(self, instance, val):
        super().validate(instance, val)  # Float.validate
        super(Typed, self).validate(instance, val)  # Unsigned.validate


class SizedString(String, MaxSized):
    def validate(self, instance, val):
        super().validate(instance, val)
        super(Typed, self).validate(instance, val)


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


def test_integer():
    class Stock:
        shares = Integer()

        def __init__(self, shares):
            self.shares = shares

    s = Stock(50)
    assert s.shares == 50
    with pytest.raises(TypeError, match="'50' is not of type <class 'int'>"):
        s.shares = "50"


def test_float():
    class Stock:
        price = Float()

        def __init__(self, price):
            self.price = 91.1

    s = Stock(91.1)
    assert s.price == 91.1
    with pytest.raises(TypeError, match="'too much' is not of type <class 'float'>"):
        s.price = "too much"


def test_sizedstring(stock):
    assert stock.name == "ACME"
    with pytest.raises(TypeError, match="12.2 must be of type <class 'str'>"):
        stock.name = 12.2
    with pytest.raises(ValueError, match=""):
        stock.name = "ABRACADABRA"


def test_unsignedfloat(stock):
    assert stock.price == 91.1
    with pytest.raises(TypeError, match="foo"):
        stock.price = -100.10


if __name__ == "__main__":
    s = Stock("ACME", 50, 91.1)
    print(s.name, s.shares, s.price)
