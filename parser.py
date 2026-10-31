#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re
import pytest


class Token:
    _tokens = {}
    _pats = []

    def __new__(cls, name, pat="", val=""):
        toks = __class__._tokens
        pats = __class__._pats
        if name not in toks:
            tok = super().__new__(cls)
            tok.name = name
            tok.val = val
            tok.pat = pat
            if pat:
                pats.append(pat)
            if name != "NUM":
                toks[name] = tok
            else:
                return tok
        return toks[name]

    def __repr__(self):
        return f"Token({self.name}, {self.val})"

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
            yield Token(match.lastgroup, val=match.group(1))


if __name__ == "__main__":
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)


def test_iter_tokens(capsys):
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
    assert (
        capsys.readouterr().out
        == r"""\
Token(NUM, \d+, )
Token(PLUS, \+, )
Token(LPAREN, \(, )
Token(NUM, \d+, )
Token(MUL, \*, )
Token(NUM, \d+, )
Token(RPAREN, \), )
Token(PLUS, \+, )
Token(NUM, \d+, )

    """
    )
