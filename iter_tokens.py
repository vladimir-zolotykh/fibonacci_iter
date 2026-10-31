#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re
from textwrap import dedent


class Symbol:
    _symbols = {}

    def __new__(cls, name, pat=""):
        syms = __class__._symbols
        if name not in syms:
            sym = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            syms[name] = sym
        return syms[name]

    def __eq__(self, other) -> bool:
        return (
            self.__dict__ == other.__dict__
            if isinstance(other, Symbol)
            else NotImplemented
        )

    def __repr__(self):
        return f"Symbol({self.name})"

    @classmethod
    def masterpat(cls) -> str:
        return "|".join(sym.pat for sym in cls._symbols)


LPAREN = Symbol("LPAREN", r"\(")
RPAREN = Symbol("RPAREN", r"\)")
PLUS = Symbol("PLUS", r"\+")
MINUS = Symbol("MINUS", r"-")
MUL = Symbol("MUL", r"\*")
DIV = Symbol("DIV", r"/")
WS = Symbol("WS", r"\s+")
NUM = Symbol("NUM", r"\d+")


class Token:
    def __init__(self, sym: Symbol):
        self.sym = sym

    def __eq__(self, other):
        return (
            self.__dict__ == other.__dict__
            if isinstance(other, Token)
            else NotImplemented
        )

    def __repr__(self):
        return f"Token({self.sym.name})"


class TokenNum(Token):
    def __init__(self, sym: Symbol, val: float):
        super().__init__(sym)
        self.val = val

    def __repr__(self):
        return f"TokenNum({self.val})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(Symbol.masterpat(), sexpr):
        if (grp := match.lastgroup) != "WS":
            if grp == "NUM":
                yield TokenNum(grp, match.group(grp))
            else:
                yield Token(grp)


if __name__ == "__main__":
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)


def test_iter_tokens(capsys):
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
    assert capsys.readouterr().out == dedent(
        """\
TokenNum(2)
Token(PLUS)
Token(LPAREN)
TokenNum(3)
Token(MUL)
TokenNum(4)
Token(RPAREN)
Token(PLUS)
TokenNum(5)
        """
    )
