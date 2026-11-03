import pytest
from factorial_tail import factorial_recur, factorial_iter, factorial_tail


@pytest.mark.parametrize(
    "n, fact",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
    ],
)
def test_factorial(n, fact):
    assert factorial_recur(n) == fact
    assert factorial_iter(n) == fact
    assert factorial_tail(n) == fact
