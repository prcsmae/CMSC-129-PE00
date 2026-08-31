"""
Evaluates postfix expressions and tracks variable state.

    class VariableStore
        def get(self, name: str)
            Return current value, or raise ValueError("Undefined variable ...")
        def set(self, name: str, value) -> None
        def list_final_values(self) -> list[str]
            e.g. ["x = 5", "y = 3"], in order first used/assigned.

    def evaluate_postfix(postfix_tokens: list[str], store: VariableStore, original_line: str = "") -> str
        Evaluates against `store`, returns result as a string.
        Raise ValueError for undefined variable or division by zero.
        On division by zero in a statement, the target variable keeps
        its previous value (don't overwrite it).
"""
