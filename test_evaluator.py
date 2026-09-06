"""
Tests for evaluator.py and processor_interface.py: evaluation, variable
state, and the three error kinds required by the specification.

Run directly:  python test_evaluator.py
"""

from parser import tokenize, validate_code, infix_to_postfix, split_code
from evaluator import VariableStore, evaluate_postfix
from processor_interface import process_input

failures = []


def run(lines: list[str]) -> VariableStore:
    """Feed codes through the full pipeline, ignoring errors."""
    store = VariableStore()
    for line in lines:
        try:
            tokens = tokenize(line)
            validate_code(tokens)
            target, expression = split_code(tokens)
            value = evaluate_postfix(infix_to_postfix(expression), store)
            if target:
                store.set(target, value)
        except ValueError:
            pass
    return store


def check_value(lines: list[str], name: str, expected: int) -> None:
    store = run(lines)
    try:
        actual = store.get(name)
    except ValueError as e:
        failures.append(f"{lines}: {name} -> unexpected error {e}")
        return
    if actual != expected:
        failures.append(f"{lines}: {name} expected {expected}, got {actual}")


def check_error(lines: list[str], message: str) -> None:
    """The last code in `lines` must fail with exactly `message`."""
    store = run(lines[:-1])
    line = lines[-1]
    try:
        tokens = tokenize(line)
        validate_code(tokens)
        target, expression = split_code(tokens)
        evaluate_postfix(infix_to_postfix(expression), store)
        failures.append(f"{line!r}: expected error {message!r}, got none")
    except ValueError as e:
        if str(e) != message:
            failures.append(f"{line!r}: expected {message!r}, got {str(e)!r}")


# ---------------- arithmetic ----------------
check_value(["x = 2 + 3"], "x", 5)
check_value(["x = 10 - 4"], "x", 6)
check_value(["x = 6 * 7"], "x", 42)
check_value(["x = 9 / 2"], "x", 4)
check_value(["x = 9 % 2"], "x", 1)
check_value(["x = 2 + 3 * 4"], "x", 14)          # precedence
check_value(["x = (2 + 3) * 4"], "x", 20)        # parentheses
check_value(["x = 8 / 4 / 2"], "x", 1)           # left associativity
check_value(["x = 100 - 10 - 5"], "x", 85)

# C semantics: truncate toward zero, remainder follows the left operand
check_value(["x = (3 - 10) / 2"], "x", -3)
check_value(["x = (3 - 10) % 2"], "x", -1)

# ---------------- variable state ----------------
check_value(["x = 5", "y = 3", "z = x + y * 2"], "z", 11)
check_value(["x = 1", "x = x + 1", "x = x + 1"], "x", 3)   # most recent value
check_value(["x = 5", "y = x", "x = 9"], "y", 5)           # value, not alias

# ---------------- errors ----------------
check_error(["c"], "Undefined variable c")
check_error(["a = b + 1"], "Undefined variable b")
check_error(["x = 5", "y = x / 0"], "Division by zero")
check_error(["x = 5", "y = x % 0"], "Division by zero")
check_error(["x = 5", "y = 3", "z = x / (y - 3)"], "Division by zero")

# ---------------- division by zero keeps the previous value ----------------
check_value(["a = 10", "a = a / 0"], "a", 10)
check_value(["a = 10", "a = a % 0"], "a", 10)
check_value(["a = 10", "a = a / 0", "b = a + 1"], "b", 11)

# ---------------- output formatting ----------------
output = process_input(["x = 5", "y = x + 1", "z = y / 0", "q$"])

for expected in [
    "Line: x = 5",
    "Postfix: x = 5",
    "Result: x = 5",
    "Postfix: y = x 1 +",
    "Result: y = 6",
    "Postfix: z = y 0 /",           # postfix shown even though evaluation failed
    "Variables used:",
    "Errors found:",
    "Line 3: Division by zero",
    "Line 4: Invalid input code",
]:
    if expected not in output:
        failures.append(f"output missing line {expected!r}")

# a bare expression has no target, so its result is the value alone
bare = process_input(["x = 4", "x * 3"])
if "Result: 12" not in bare:
    failures.append("bare expression result not formatted as a plain value")

# the sets are separated by blank lines
if "\n\n" not in output:
    failures.append("output sets are not separated by an empty line")

if failures:
    print("FAILURES:")
    for f in failures:
        print(" -", f)
    raise SystemExit(1)
print("All evaluator tests passed.")
