from financial import main
import pytest


def test_total():
    result = main("MSFT", "Total Revenue")
    assert result[0] == "Total Revenue"
    assert result[1] == "261,802,000.00"


def test_tuple():
    result = main("MSFT", "Total Revenue")
    assert type(result) is tuple


def test_exception():
    with pytest.raises(Exception):
        main("foo", "Total Revenue")


if __name__ == "__main__":
    test_total()
    test_tuple()
    test_exception()
