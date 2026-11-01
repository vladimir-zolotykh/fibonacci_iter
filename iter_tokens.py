#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self, Iterator, Callable, Any
import re


class Symbol:
    _symbols = {}

    def __new__(cls, name: str, pat: str = ""):
        syms = __class__._symbols
        if name not in syms:
            sym = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            syms[name] = sym
        return syms[name]

    def __hash__(self):
        return hash(self.name)

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
        return "|".join(f"(?P<{name}>{sym.pat})" for name, sym in cls._symbols.items())


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
        assert isinstance(sym, Symbol)
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
        assert isinstance(val, float)
        super().__init__(sym)
        self.val = val

    def __repr__(self):
        return f"TokenNum({self.val})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    for match in re.finditer(Symbol.masterpat(), sexpr):
        if (grp := match.lastgroup) != "WS":
            if grp == "NUM":
                # yield TokenNum(Symbol(grp), match.group(grp))
                yield TokenNum(NUM, float(match.group(grp)))
            else:
                yield Token(Symbol(grp))


class Node:
    _node_map: dict[Symbol, type(object)] = {}

    @classmethod
    def get_node(cls) -> Self:
        return cls._node_map[cls]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "_op"):
            __class__._node_map[getattr(cls, "_op")] = cls

    def __eq__(self, other: Any) -> bool:
        return (
            self.__dict__ == other.__dict__
            if isinstance(other, Node)
            else NotImplemented
        )


class Num(Node):
    def __init__(self, val: float):
        self.val = val

    def __repr__(self) -> str:
        return f"Num({self.val})"


class BinOp(Node):
    def __init__(self, left: Node, right: Node) -> Node:
        super().__init__(self._op)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.left)}, {repr(self.right)})"


class Plus(BinOp):
    _op = PLUS


class Minus(BinOp):
    _op: Symbol = MINUS


class Mul(BinOp):
    _op: Symbol = MUL


class Div(BinOp):
    _op: Symbol = DIV


class Parser:
    def __init__(self):
        self.tokens = None
        self.tok = None

    def parse(self, sexpr: str) -> Node:
        self.tokens = iter_tokens(sexpr)
        self.tok = self._advance()
        return self.expr()

    def iter_ops(self, ops: tuple[Symbol, ...], func: Callable) -> Node:
        res: Node = func()
        while (tok := self.tok) and tok in ops:
            self._consume()
            res = Node.get_node(tok)(res, func())
        return res

        pass

    def expr(self) -> Node:
        return self.iter_ops((PLUS, MINUS), self.term)

    def term(self) -> Node:
        return self.iter_ops((MUL, DIV), self.factor)

    def factor(self) -> Node:
        if self.tok == LPAREN:
            self._consume()
            res = self.expr()
            self._expect(RPAREN)
        else:
            res = Num(self.tok)
            self._consume()
        return res

    def _advance(self) -> Token:
        self.tok = next(self.tokens, None)
        return self.tok

    def _expect(self, expected: Token) -> None:
        if self.tok != expected:
            raise SyntaxError(f"{self.tok!r}: Invalid token, expected {expected}")
        self._consume()

    def _consume(self) -> None:
        self.tok = next(self.tokens, None)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    p = Parser()
    n: Node = p.parse(sexpr)
    print(n)
