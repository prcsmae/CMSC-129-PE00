"""
Verification harness for the 7 test .in files.

Every expected postfix string, result, variable value and error below was
computed BY HAND (independently of the program code) and compared against
the exact output of processor_interface.process_input().
"""

from processor_interface import process_input

SEP = "-" * 43
ERRORS_HEADER = "Errors found:\n"
VARS_HEADER = "Variables used:\n"


def blocks(entries):
    """entries: list of (code, postfix, result) triples."""
    return "\n\n".join(
        f"Line: {code}\nPostfix: {postfix}\nResult: {result}"
        for code, postfix, result in entries
    )


def output(entries, variables, errors):
    error_section = "\n".join(errors) if errors else "(none)"
    return "\n\n".join([
        blocks(entries),
        SEP,
        VARS_HEADER + "\n".join(variables),
        SEP,
        ERRORS_HEADER + error_section,
    ])


INV = "ERROR - Invalid input code"
UNDEF = lambda v: f"ERROR - Undefined variable {v}"
DIV0 = "ERROR - Division by zero"

CASES = {
    "test_simple.in": output(
        [
            ("x = 42", "x = 42", "x = 42"),
            ("5 + 3", "5 3 +", "8"),
            ("y = 100 - 20", "y = 100 20 -", "y = 80"),
            ("2 * 7", "2 7 *", "14"),
        ],
        ["x = 42", "y = 80"],
        [],
    ),
    "test_precedence.in": output(
        [
            ("a = 2 + 3 * 4", "a = 2 3 4 * +", "a = 14"),
            ("b = 2 * 3 + 4", "b = 2 3 * 4 +", "b = 10"),
            ("c = 20 - 8 / 4", "c = 20 8 4 / -", "c = 18"),
            ("d = 2 + 3 * 4 - 1", "d = 2 3 4 * + 1 -", "d = 13"),
            ("e = 100 / 10 / 2", "e = 100 10 / 2 /", "e = 5"),
            ("f = 10 - 4 - 3", "f = 10 4 - 3 -", "f = 3"),
            ("g = 17 % 5", "g = 17 5 %", "g = 2"),
            ("h = 10 % 4 * 2", "h = 10 4 % 2 *", "h = 4"),
            ("i = 2 * 6 % 4", "i = 2 6 * 4 %", "i = 0"),
        ],
        ["a = 14", "b = 10", "c = 18", "d = 13",
         "e = 5", "f = 3", "g = 2", "h = 4", "i = 0"],
        [],
    ),
    "test_variables.in": output(
        [
            ("x = 5", "x = 5", "x = 5"),
            ("y = x + 3", "y = x 3 +", "y = 8"),
            ("x = y * 2", "x = y 2 *", "x = 16"),
            ("z = x - y", "z = x y -", "z = 8"),
            ("result = x + y + z", "result = x y + z +", "result = 32"),
        ],
        ["x = 16", "y = 8", "z = 8", "result = 32"],
        [],
    ),
    "test_invalid.in": output(
        [
            ("5 + * 3", "(none)", INV),
            ("2 + + 2", "(none)", INV),
            ("x =", "(none)", INV),
            ("= 5", "(none)", INV),
            ("x y", "(none)", INV),
            ("x = 5 $ 3", "(none)", INV),
            ("1abc + 2", "(none)", INV),
            ("a_1 = 3", "(none)", INV),
            ("(x + 5", "(none)", INV),
            ("x = (1 + 2) * 3", "x = 1 2 + 3 *", "x = 9"),
            (")", "(none)", INV),
        ],
        ["x = 9"],
        [f"Line {n}: Invalid input code"
         for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11)],
    ),
    "test_undefined.in": output(
        [
            ("a = b + 5", "a = b 5 +", UNDEF("b")),
            ("b = 10", "b = 10", "b = 10"),
            ("c = b + a", "c = b a +", UNDEF("a")),
            ("d = 5", "d = 5", "d = 5"),
            ("e = d + f + 2", "e = d f + 2 +", UNDEF("f")),
            ("g = e", "g = e", UNDEF("e")),
        ],
        ["a = (undefined)", "b = 10", "c = (undefined)", "d = 5",
         "e = (undefined)", "f = (undefined)", "g = (undefined)"],
        ["Line 1: Undefined variable b",
         "Line 3: Undefined variable a",
         "Line 5: Undefined variable f",
         "Line 6: Undefined variable e"],
    ),
    "test_divzero.in": output(
        [
            ("x = 100", "x = 100", "x = 100"),
            ("x = x / 0", "x = x 0 /", DIV0),
            ("y = 7 % 0", "y = 7 0 %", DIV0),
            ("y = 50 / 10", "y = 50 10 /", "y = 5"),
            ("z = 10 / (5 - 5)", "z = 10 5 5 - /", DIV0),
            ("w = 0 / 5", "w = 0 5 /", "w = 0"),
            ("v = 5", "v = 5", "v = 5"),
            ("v = v / 0", "v = v 0 /", DIV0),
        ],
        ["x = 100", "y = 5", "z = (undefined)", "w = 0", "v = 5"],
        ["Line 2: Division by zero",
         "Line 3: Division by zero",
         "Line 5: Division by zero",
         "Line 8: Division by zero"],
    ),
    "test_mixed.in": output(
        [
            ("x = 5", "x = 5", "x = 5"),
            ("y = 3", "y = 3", "y = 3"),
            ("a = (x + y) * 2", "a = x y + 2 *", "a = 16"),
            ("b = x + y * 2", "b = x y 2 * +", "b = 11"),
            ("c = (x + y) * (x - y)", "c = x y + x y - *", "c = 16"),
            ("d = 100 / (2 + 3) % 4", "d = 100 2 3 + / 4 %", "d = 0"),
            ("e = ((1 + 2) * (3 + 4))", "e = 1 2 + 3 4 + *", "e = 21"),
            ("f =", "(none)", INV),
            ("g = ((2 + 3)", "(none)", INV),
            ("final = a + b + c", "final = a b + c +", "final = 43"),
        ],
        ["x = 5", "y = 3", "a = 16", "b = 11", "c = 16", "d = 0",
         "e = 21", "final = 43"],
        ["Line 8: Invalid input code",
         "Line 9: Invalid input code"],
    ),
}


def main():
    failures = 0
    for filename, expected in CASES.items():
        with open(filename, encoding="utf-8") as f:
            lines = f.read().splitlines()
        actual = process_input(lines)
        if actual == expected:
            print(f"PASS  {filename}")
        else:
            failures += 1
            print(f"FAIL  {filename}")
            exp_lines, act_lines = expected.splitlines(), actual.splitlines()
            for i in range(max(len(exp_lines), len(act_lines))):
                e = exp_lines[i] if i < len(exp_lines) else "<missing>"
                a = act_lines[i] if i < len(act_lines) else "<missing>"
                if e != a:
                    print(f"  line {i + 1}:\n    expected: {e!r}\n    actual:   {a!r}")
    total = len(CASES)
    print(f"\n{total - failures}/{total} test files passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
