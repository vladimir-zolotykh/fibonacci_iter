import pytest
from peg import Peg


def test_peg_push():
    p = Peg(8)
    p.push(3)
    p.push(2)
    with pytest.raises(ValueError, match="cannot put 3 over 2"):
        p.push(3)


def test_peg_empty():
    p = Peg(8)
    assert str(p) == "bytearray(b'')"


def test_peg123():
    p = Peg(8)
    for x in range(3, 0, -1):
        p.push(x)
    for x in range(1, 4):
        assert p.pop() == x
    with pytest.raises(IndexError, match="index out of range"):
        p.pop()


def test_peg1_8():
    p = Peg(8)
    for i in range(8, 0, -1):
        p.push(i)
    assert p.data == bytearray(reversed(bytearray(b"\x01\x02\x03\x04\x05\x06\x07\x08")))
