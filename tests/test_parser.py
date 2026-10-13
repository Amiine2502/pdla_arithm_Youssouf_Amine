import pytest
from lark.exceptions import UnexpectedInput

from arithmp.parser import Parser


@pytest.fixture
def parser() -> Parser:
    return Parser()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("42", 42.0),
        ("1.5", 1.5),
        ("3 + 4", 7.0),
        ("10 - 4", 6.0),
        ("3 * 4", 12.0),
        ("10 / 4", 2.5),
        ("7 % 3", 1.0),
        ("2 ^ 3", 8.0),
    ],
)
def test_basic_operations(parser: Parser, expression: str, expected: float) -> None:
    assert parser.parse(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14.0),  # * avant +
        ("(2 + 3) * 4", 20.0),  # parenthèses
        ("10 - 4 - 3", 3.0),  # associativité à gauche
        ("2 ^ 3 ^ 2", 512.0),  # ^ associatif à droite : 2^(3^2)
        ("-2 ^ 2", -4.0),  # ^ avant le moins unaire
    ],
)
def test_precedence(parser: Parser, expression: str, expected: float) -> None:
    assert parser.parse(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("-5", -5.0),
        ("+5", 5.0),
        ("--5", 5.0),
        ("3 * -2", -6.0),
    ],
)
def test_unary_operators(parser: Parser, expression: str, expected: float) -> None:
    assert parser.parse(expression) == pytest.approx(expected)


def test_division_by_zero(parser: Parser) -> None:
    with pytest.raises(ZeroDivisionError):
        parser.parse("1 / 0")


@pytest.mark.parametrize("expression", ["3 +", "* 2", "(1 + 2", "1 2"])
def test_invalid_syntax(parser: Parser, expression: str) -> None:
    with pytest.raises(UnexpectedInput):
        parser.parse(expression)