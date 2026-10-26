#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import pytest
from functools import wraps


class Field(ABC):
    def __set_name__(self, owner, name):
        self.sys_name = f"sys_{name}"
        self.usr_name = f"usr_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.sys_name]

    def __set__(self, instance, val):
        self.validate(val)
        instance.__dict__[self.sys_name] = val

    @abstractmethod
    def validate(self, val):
        pass


def show_validate(label):
    def decorate(func):
        @wraps(func)
        def wrapper(self, val):
            print(f"***** {label}.validate({val})")
            res = func(self, val)
            return res

        return wrapper

    return decorate


class Typed(Field):
    @show_validate("Typed")
    def validate(self, val):
        if not isinstance(val, self._expected):
            raise TypeError(f"{val!r} is not of type {self._expected}")
        super().validate(val)


class Unsigned(Field):
    @show_validate("Unsigned")
    def validate(self, val):
        if val < 0:
            raise ValueError(f"{val!r} must not be signed")
        super().validate(val)


class MaxSized(Field):
    def __init__(self, size=8):
        self.size = size

    @show_validate("MaxSized")
    def validate(self, val):
        if len(val) > self.size:
            raise ValueError(
                f"{val!r} must not exceed {self.size} characters in lenght"
            )
        super().validate(val)


class String(Typed):
    _expected = str

    @show_validate("String")
    def validate(self, val):
        super().validate(val)


class Float(Typed):
    _expected = float

    @show_validate("Float")
    def validate(self, val):
        super().validate(val)


class Integer(Typed):
    _expected = int

    @show_validate("Integer")
    def validate(self, val):
        super().validate(val)


class UnsignedInteger(Integer, Unsigned):
    @show_validate("UnsignedInteger")
    def validate(self, val):
        super().validate(val)


class UnsignedFloat(Float, Unsigned):
    @show_validate("UnsignedFloat")
    def validate(self, val):
        super().validate(val)


class SizedString(String, MaxSized):
    @show_validate("SizedString")
    def validate(self, val):
        super().validate(val)


class Stock:
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


def test_unsignedinteger():
    s = Stock("ACME", 50, 91.1)
    print("+++++")
    # s.shares = "few"
    s.shares = -10


if __name__ == "__main__":
    test_unsignedinteger()
    exit(1)
    s = Stock("ACME", 50, 91.1)
    print(s.name, s.shares, s.price)
