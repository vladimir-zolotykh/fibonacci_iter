#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re


class Token:
    _tokens = {}

    def __new__(cls, name, pat="", val=""):
        tokens = __class__._tokens
        if name not in tokens:
            tok = super().__new__(cls)
            tok.name = name
            tok.val = val
            tok.pat = pat
            tokens[name] = tok
        return tokens[name]

    def __repr__(self):
        return f"Token({self.name}, {self.pat}, {self.val})"

    @classmethod
    def masterpat(cls) -> str:
        return "|".join(f"(?P<{name}>{tok.pat})" for name, tok in cls._tokens.items())


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
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
