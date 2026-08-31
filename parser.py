"""
Tokenizes input lines and converts infix expressions to postfix.

    def tokenize(line: str) -> list[str]

    def validate_code(tokens: list[str]) -> None
        Raise ValueError("Invalid input code") if the tokens don't form
        a valid statement (var = expression) or bare expression.

    def infix_to_postfix(tokens: list[str]) -> list[str]
        Converts the expression part to postfix

Variable names: start with a letter, then letters/digits only. No
underscores. No keyword restriction.
Operators: + - * / %
"""

OPERATORS = {"+", "-", "*", "/", "%"}


def _invalid():
    raise ValueError("Invalid input code")


def tokenize(line: str) -> list[str]:
    """Break a raw line into tokens: variables, integer values,
    operators, '=', and parentheses."""
    tokens: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch.isspace():
            i += 1
            continue
        if ch in OPERATORS or ch in "()=":
            tokens.append(ch)
            i += 1
            continue
        if ch.isdigit():
            j = i
            while j < n and line[j].isdigit():
                j += 1
            # number immediately followed by a letter => invalid name like 1abc
            if j < n and (line[j].isalpha() or line[j] == "_"):
                _invalid()
            tokens.append(line[i:j])
            i = j
            continue
        if ch.isalpha():
            j = i
            while j < n and (line[j].isalnum()):
                j += 1
            # underscore (or any non-alnum) inside a name is illegal
            if j < n and not line[j].isspace() and line[j] not in OPERATORS and line[j] not in "()=":
                _invalid()
            tokens.append(line[i:j])
            i = j
            continue
        _invalid()
    return tokens


def _is_number(token: str) -> bool:
    return token.isdigit()


def _is_variable(token: str) -> bool:
    return bool(token) and token[0].isalpha() and token.isalnum() and token.isidentifier()


def _validate_expression(tokens: list[str]) -> None:
    if not tokens:
        _invalid()
    prev = None  # None at start; 'operand' or 'operator' after
    depth = 0
    for tok in tokens:
        if tok == "(":
            if prev == "operand":
                _invalid()  # missing operator before '('
            depth += 1
            prev = "operator"  # '(' acts like an operator position
        elif tok == ")":
            if prev != "operand":
                _invalid()  # empty parens or dangling operator
            if depth == 0:
                _invalid()  # unmatched ')'
            depth -= 1
            prev = "operand"
        elif tok in OPERATORS:
            if prev != "operand":
                _invalid()  # consecutive/dangling operator
            prev = "operator"
        elif _is_number(tok) or _is_variable(tok):
            if prev == "operand":
                _invalid()  # missing operator between operands
            prev = "operand"
        else:
            _invalid()
    if depth != 0:
        _invalid()  # unmatched '('
    if prev != "operand":
        _invalid()  # dangling operator at end


def validate_code(tokens: list[str]) -> None:
    """Validate a token list as either 'var = expression' or a bare
    expression. Raise ValueError("Invalid input code") otherwise."""
    if not tokens:
        _invalid()

    if "=" in tokens:
        # exactly one '=', at index 1, LHS a single variable
        if tokens.count("=") != 1 or len(tokens) < 3:
            _invalid()
        eq = tokens.index("=")
        lhs = tokens[:eq]
        if len(lhs) != 1 or not _is_variable(lhs[0]):
            _invalid()
        _validate_expression(tokens[eq + 1:])
    else:
        _validate_expression(tokens)


def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Convert an expression token list to postfix via Shunting Yard.
    If the tokens form an assignment, the assignment is stripped and
    the expression part is converted."""
    if "=" in tokens:
        tokens = tokens[tokens.index("=") + 1:]

    precedence = {"*": 3, "/": 3, "%": 3, "+": 2, "-": 2}
    output: list[str] = []
    stack: list[str] = []

    for tok in tokens:
        if tok in precedence:
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[tok]:
                output.append(stack.pop())
            stack.append(tok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                _invalid()  # unmatched ')'
            stack.pop()  # discard '('
        else:
            output.append(tok)

    while stack:
        top = stack.pop()
        if top == "(":
            _invalid()  # unmatched '('
        output.append(top)

    return output
