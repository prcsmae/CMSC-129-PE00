"""
Connects the GUI to the parser and the evaluator.

process_input(lines) runs every input code through
tokenize -> validate_code -> infix_to_postfix -> evaluate_postfix and
formats the three output sets required by the specification:

    1. one block per input code (the code, its postfix form, its result)
    2. the variables used and their final values
    3. the errors found during processing

The sets are separated by a blank line.
"""

from typing import List

from parser import (
    tokenize,
    validate_code,
    infix_to_postfix,
    split_code,
    collect_variables,
)
from evaluator import VariableStore, evaluate_postfix

SEPARATOR = "-" * 43


def _format_postfix(target: str | None, postfix: List[str]) -> str:
    """Postfix notation of the whole code: the assignment target, when
    present, stays in front of the converted expression."""
    body = " ".join(postfix)
    return f"{target} = {body}" if target else body


def _format_result(target: str | None, value: int) -> str:
    """The given code with its expression part replaced by the value."""
    return f"{target} = {value}" if target else str(value)


def _parse_line(line: str, store: VariableStore) -> tuple[str | None, List[str]]:
    """Tokenize, validate and convert one input code to postfix. Returns
    (target, postfix_tokens) and raises ValueError("Invalid input code")
    if the code is malformed."""
    tokens = tokenize(line)
    validate_code(tokens)

    target, expression = split_code(tokens)

    # Register every variable of the code so that it is listed under
    # "Variables used" even if the evaluation later fails.
    for name in collect_variables(tokens):
        store.note_used(name)

    return target, infix_to_postfix(expression)


def _evaluate_line(target: str | None, postfix: List[str], store: VariableStore) -> str:
    """Evaluate one converted code and store the value when the code is a
    statement. Raises ValueError on an undefined variable or a division
    by zero; because the exception propagates before store.set() runs, a
    failed statement leaves its target at its previous value."""
    value = evaluate_postfix(postfix, store)
    if target:
        store.set(target, value)
    return _format_result(target, value)


def process_input(lines: List[str]) -> str:
    """
    Takes the raw input lines and returns a single formatted string
    ready to be placed directly into the output text area.
    """
    store = VariableStore()
    blocks: List[str] = []
    errors: List[str] = []

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue

        # The postfix form is reported whenever the conversion succeeds,
        # even if evaluating it afterwards fails.
        postfix_text = "(none)"
        try:
            target, postfix = _parse_line(line, store)
            postfix_text = _format_postfix(target, postfix)
            result_text = _evaluate_line(target, postfix, store)
        except ValueError as error:
            errors.append(f"Line {line_number}: {error}")
            result_text = f"ERROR - {error}"

        blocks.append(
            f"Line: {line}\nPostfix: {postfix_text}\nResult: {result_text}"
        )

    variables_used = store.list_final_values()

    parts: List[str] = []
    if blocks:
        parts.append("\n\n".join(blocks))
    parts.append(SEPARATOR)
    parts.append(
        "Variables used:\n"
        + ("\n".join(variables_used) if variables_used else "(none)")
    )
    parts.append(SEPARATOR)
    parts.append(
        "Errors found:\n" + ("\n".join(errors) if errors else "(none)")
    )

    return "\n\n".join(parts)
