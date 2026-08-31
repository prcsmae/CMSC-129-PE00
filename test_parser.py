"""
Tests for parser.py: tokenize, validate_code, infix_to_postfix.

Run directly:  python test_parser.py
Or with pytest: pytest test_parser.py
"""

from parser import tokenize, validate_code, infix_to_postfix

failures = []


def check_valid_postfix(line: str, expected: list[str]) -> None:
    try:
        tokens = tokenize(line)
        validate_code(tokens)
        postfix = infix_to_postfix(tokens)
        if postfix != expected:
            failures.append(f"{line!r}: expected {expected}, got {postfix}")
    except ValueError as e:
        failures.append(f"{line!r}: unexpected error {e}")


def check_invalid(line: str) -> None:
    try:
        tokens = tokenize(line)
        validate_code(tokens)
        failures.append(f"{line!r}: expected ValueError, got none")
    except ValueError:
        pass


# ---------------- valid expressions ----------------
check_valid_postfix("x = 5", ["5"])  # assignment stripped
check_valid_postfix("z = x + y * 2", ["x", "y", "2", "*", "+"])
check_valid_postfix("a + b", ["a", "b", "+"])
check_valid_postfix("a - b - c", ["a", "b", "-", "c", "-"])
check_valid_postfix("8 / 4 / 2", ["8", "4", "/", "2", "/"])
check_valid_postfix("(a + b) * (c - d)", ["a", "b", "+", "c", "d", "-", "*"])
check_valid_postfix("a % b", ["a", "b", "%"])
check_valid_postfix("x = (y + 3) * 2", ["y", "3", "+", "2", "*"])
check_valid_postfix("a+b*c-d", ["a", "b", "c", "*", "+", "d", "-"])
check_valid_postfix("2 + 3 * 4 % 5", ["2", "3", "4", "*", "5", "%", "+"])
check_valid_postfix("result1 = value2 * 10", ["value2", "10", "*"])

# ---------------- invalid syntax ----------------
check_invalid("")
check_invalid("   ")
check_invalid("x + + y")
check_invalid("x +")
check_invalid("+ x")
check_invalid("x =")
check_invalid("= 5")
check_invalid("x = = y")
check_invalid("x = 5 =")
check_invalid("(x + y")
check_invalid("x + y)")
check_invalid("()")
check_invalid("(a)(b)")
check_invalid("a b")
check_invalid("5 = x")

# ---------------- illegal characters / invalid names ----------------
check_invalid("x_1 = 5")
check_invalid("a$b")
check_invalid("1abc = 2")
check_invalid("x @ y")
check_invalid("x = 5.0")
check_invalid("y = 2#3")
check_invalid("x = a,b")

if failures:
    print("FAILURES:")
    for f in failures:
        print(" -", f)
    raise SystemExit(1)
print("All parser tests passed.")