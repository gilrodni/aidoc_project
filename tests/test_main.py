import pytest

from main import add

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (10, -10, 0),
    (10, 10, 20),
])
def test_add(a, b, expected):
    assert add(a, b) == expected