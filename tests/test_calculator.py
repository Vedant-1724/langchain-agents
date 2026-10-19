
"""Tests for the safe arithmetic calculator."""

import pytest

from app.tools.calculator import calculate


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3", 5),
        ("18 * 7", 126),
        ("10 - 3", 7),
        ("20 / 4", 5),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-5 + 8", 3),
        ("2 ** 10", 1024),
        ("18.5 + 1.5", 20.0),
        ("18475 * 3629 - 47281", 66998494),
    ],
)
def test_calculate_valid_expressions(expression, expected):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "hello",
        "import os",
        "__import__('os').system('whoami')",
        "open('secret.txt')",
        "2 ** 101",
    ],
)
def test_rejects_invalid_or_unsafe_expressions(expression):
    with pytest.raises((ValueError, TypeError)):
        calculate(expression)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("10 / 0")


def test_expression_too_long():
    with pytest.raises(ValueError, match="too long"):
        calculate("1+" * 150 + "1")
