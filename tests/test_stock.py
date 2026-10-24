import pytest
from stock import Float, Integer, SizedString, UnsignedFloat, UnsignedInteger


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
    with pytest.raises(TypeError, match="12.2 must be of type <class 'str'>"):
        stock.name = 12.2
    with pytest.raises(ValueError, match=""):
        stock.name = "ABRACADABRA"
