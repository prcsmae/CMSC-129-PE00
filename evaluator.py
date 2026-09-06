"""
Evaluates postfix expressions and tracks variable state.

    class VariableStore
        def note_used(self, name: str) -> None
            Record that a variable appeared in the input, even if it
            never receives a value.
        def get(self, name: str) -> int
            Return current value, or raise ValueError("Undefined variable ...")
        def set(self, name: str, value: int) -> None
        def list_final_values(self) -> list[str]
            e.g. ["x = 5", "y = 3"], in order of first appearance.

    def evaluate_postfix(postfix_tokens: list[str], store: VariableStore) -> int
        Evaluates against `store`, returns the resulting integer.
        Raise ValueError for undefined variable or division by zero.

On division by zero (or an undefined variable) the caller never reaches
the store.set() for the statement's target, so the target keeps whatever
value it had before.

Integer arithmetic follows C semantics: division truncates toward zero
and the modulo result takes the sign of the left operand.
"""

from parser import OPERATORS

# Placeholder stored for a variable that was used but never assigned.
_UNDEFINED = None


class VariableStore:
    """Holds the most recently assigned value of every variable, in
    order of first appearance in the input."""

    def __init__(self):
        self._values: dict[str, int | None] = {}

    def note_used(self, name: str) -> None:
        if name not in self._values:
            self._values[name] = _UNDEFINED

    def is_defined(self, name: str) -> bool:
        return self._values.get(name, _UNDEFINED) is not _UNDEFINED

    def get(self, name: str) -> int:
        self.note_used(name)
        value = self._values[name]
        if value is _UNDEFINED:
            raise ValueError(f"Undefined variable {name}")
        return value

    def set(self, name: str, value: int) -> None:
        self._values[name] = value

    def list_final_values(self) -> list[str]:
        return [
            f"{name} = {value if value is not _UNDEFINED else '(undefined)'}"
            for name, value in self._values.items()
        ]


def _c_divide(left: int, right: int) -> int:
    """Integer division truncated toward zero, as in C."""
    if right == 0:
        raise ValueError("Division by zero")
    quotient = abs(left) // abs(right)
    return quotient if (left < 0) == (right < 0) else -quotient


def _c_modulo(left: int, right: int) -> int:
    """Remainder consistent with _c_divide, as in C."""
    if right == 0:
        raise ValueError("Division by zero")
    return left - _c_divide(left, right) * right


def _apply(operator: str, left: int, right: int) -> int:
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return _c_divide(left, right)
    if operator == "%":
        return _c_modulo(left, right)
    raise ValueError("Invalid input code")


def evaluate_postfix(postfix_tokens: list[str], store: VariableStore) -> int:
    """Evaluate a postfix token list and return the resulting integer."""
    stack: list[int] = []

    for token in postfix_tokens:
        if token in OPERATORS:
            if len(stack) < 2:
                raise ValueError("Invalid input code")
            right = stack.pop()
            left = stack.pop()
            stack.append(_apply(token, left, right))
        elif token.isdigit():
            stack.append(int(token))
        else:
            stack.append(store.get(token))

    if len(stack) != 1:
        raise ValueError("Invalid input code")
    return stack[0]
