#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re


token_specs = {
    name: f"(?P<{name}>{pat})"
    for name, pat in {
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "PLUS": r"\+",
        "MINUS": r"-",
        "MUL": r"\*",
        "DIV": r"/",
        "WS": r"\s+",
        "NUM": r"\d+",
    }.items()
}


def masterpat() -> str:
    return "|".join(token_specs.values())


class Token:
    def __init__(self, name: str, val: str | float):
        self.name = name
        self.val = val

    def __eq__(self, other):
        return (
            self.__dict__ == other.__dict__
            if isinstance(other, Token)
            else NotImplemented
        )

    def __repr__(self):
        return f"Token({self.name}, {self.val})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(masterpat(), sexpr):
        if (grp := match.lastgroup) != "WS":
            yield Token(grp, match.group(grp))


if __name__ == "__main__":
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
