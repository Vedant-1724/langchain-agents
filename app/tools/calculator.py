
"""Safe arithmetic calculator for the LangChain agent."""

import ast
import operator
from typing import Union

Number = Union[int, float]

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

MAX_EXPRESSION_LENGTH = 200
MAX_ABSOLUTE_EXPONENT = 100
MAX_RESULT_MAGNITUDE = 1e100


def _evaluate(node: ast.AST) -> Number:
    """Evaluate only explicitly permitted arithmetic AST nodes."""

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(
            node.value, (int, float)
        ):
            raise ValueError("Only numeric constants are allowed.")
        return node.value

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported arithmetic operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        if isinstance(node.op, ast.Pow):
            if abs(right) > MAX_ABSOLUTE_EXPONENT:
                raise ValueError("Exponent exceeds the allowed limit.")

        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            if right == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")

        result = operation(left, right)

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")

        return _validate_result(result)

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operator.")
        return _validate_result(operation(_evaluate(node.operand)))

    raise ValueError("Only arithmetic expressions are allowed.")


def _validate_result(value: Number) -> Number:
    """Reject results that are not finite or are excessively large."""

    import math

    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Result must be finite.")

    if abs(value) > MAX_RESULT_MAGNITUDE:
        raise ValueError("Result exceeds the allowed magnitude.")

    return value


def calculate(expression: str) -> Number:
    """Safely calculate a basic arithmetic expression.

    Supports +, -, *, /, //, %, **, parentheses and unary signs.
    Does not execute Python statements or arbitrary functions.
    """

    if not isinstance(expression, str):
        raise TypeError("Expression must be a string.")

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression cannot be empty.")

    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid arithmetic expression.") from exc

    return _evaluate(tree.body)
