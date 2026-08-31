"""
This file contains stubs for now so the GUI can be built and tested. 
Swap in the real logic using the commented-out section below
once parser.py / evaluator.py are ready.
"""

from typing import List

# TODO: uncomment once implemented
# from parser import tokenize, validate_code, infix_to_postfix
# from evaluator import evaluate_postfix, VariableStore


def process_input(lines: List[str]) -> str:
    """
    Takes the raw input lines and returns a single formatted string 
    ready to be placed directly into the output text area.
    """
   
    blocks = []
    variables_used: List[str] = []
    errors: List[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        postfix_stub = f"<postfix of '{line}'>"
        result_stub = f"<result of '{line}'>"
        blocks.append(f"Line: {line}\nPostfix: {postfix_stub}\nResult: {result_stub}")

    separator = "-" * 40

    parts = []
    if blocks:
        parts.append("\n\n".join(blocks))
    parts.append(separator)
    parts.append("Variables used:\n" + ("\n".join(variables_used) if variables_used else "(none)"))
    parts.append(separator)
    parts.append("Errors found:\n" + ("\n".join(errors) if errors else "(none)"))

    return "\n\n".join(parts)
 

    # ============ REAL IMPLEMENTATION (uncomment + adapt once parser/evaluator exist) ==
    # store = VariableStore()
    # blocks = []
    # errors = []
    #
    # for raw_line in lines:
    #     line = raw_line.strip()
    #     if not line:
    #         continue
    #     try:
    #         tokens = tokenize(line)
    #         validate_code(tokens)
    #         postfix = infix_to_postfix(tokens)
    #         result = evaluate_postfix(postfix, store, original_line=line)
    #         blocks.append(f"Line: {line}\nPostfix: {postfix}\nResult: {result}")
    #     except ValueError as e:
    #         errors.append(str(e))
    #
    # separator = "-" * 40
    # variables_used = store.list_final_values()  
    #
    # parts = []
    # if blocks:
    #     parts.append("\n\n".join(blocks))
    # parts.append(separator)
    # parts.append("Variables used:\n" + ("\n".join(variables_used) if variables_used else "(none)"))
    # parts.append(separator)
    # parts.append("Errors found:\n" + ("\n".join(errors) if errors else "(none)"))
    #
    # return "\n\n".join(parts)
    # ====================================================================================
