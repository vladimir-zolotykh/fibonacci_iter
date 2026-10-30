#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re


class Token:
    _symbols = {}

    def __new__(cls, name, pat="", val=""):
        syms = __class__._symbols
        if name not in syms:
            sym = super().__new__(cls)
            sym.name = name
            sym.val = val
            sym.pat = pat
            syms[name] = sym
        return syms[name]

    @classmethod
    def masterpat(cls) -> str:
        return "|".join("(?P<{name}>{pat})" for name, pat in cls._symbols.items())


NUM = Token("NUM", r"\d+")
LPAREN = Token("LPAREN", r"\(")
RPAREN = Token("RPAREN", r"\)")
PLUS = Token("PLUS", r"\+")
MINUS = Token("MINUS", r"-")
MUL = Token("MUL", r"\*")
DIV = Token("DIV", "/")
WS = Token("WS", r"\s+")


def iter_tokens(sexpr: str = "2 + (3 * 4) + 5") -> Iterator[Token]:
    for match in re.finditer(Token.masterpat(), sexpr):
        if match.lastgroup != "WS":
            yield Token(match.lastgroup, match.group(0))


if __name__ == "__main__":
    for tok in re.finditer(Token.masterpat(), "2 + (3 * 4) + 5"):
        print(tok)
