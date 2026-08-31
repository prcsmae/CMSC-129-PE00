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
