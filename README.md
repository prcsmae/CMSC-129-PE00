# Programming Exercise 00 - Expression Evaluation

A Python GUI application that processes simple assignment statements and expressions.


## Program Description

The program reads a sequence of input codes, converts the expression part of each
code into postfix notation, evaluates it, and reports the results. An input code
is either:

- a **statement** of the form `var = expression`, whose evaluated value is stored
  in the target variable `var`; or
- a bare **expression**, which is evaluated and reported but stored nowhere.

The value of a variable inside an expression is the value most recently assigned
to it by a preceding code.

Input codes are either typed into the input text area or loaded from an external
`.in` file, where every line is one input code. The interface is built with
Tkinter, which ships with the standard library, so nothing needs to be installed.

### Supported input
- Assignment statements (`x = 5`) or bare expressions (`a + b`), one per line.
- Operators: `+ - * / %`, with parentheses. Precedence: `* / %` > `+ -`,
  equal precedence associates to the left.
- Variable names: start with a letter, then letters/digits only (no underscores).
- Integer literals only. Anything else is reported as invalid input.
- Integer arithmetic follows C: `/` truncates toward zero and `%` takes the sign
  of its left operand, so `(3 - 10) / 2` is `-3` and `(3 - 10) % 2` is `-1`.

### Errors detected

| Error | Meaning | Effect |
|---|---|---|
| `Invalid input code` | The line is not a well-formed statement or expression | The line produces no value |
| `Undefined variable <name>` | The variable had no value before this code | The line produces no value |
| `Division by zero` | The right operand of `/` or `%` evaluated to zero | The line produces no value; if it was a statement, the target variable keeps the value it had before |

A bad line never stops the run — it is reported and processing continues with the
next line.


## Output Format

For each input code, one block of three lines:

```
Line: <the input code as given>
Postfix: <the postfix notation of the code>
Result: <the code with its expression replaced by the value>
```

After the blocks come the variables used with their final values, then the errors
found. Each set is separated from the previous one by an empty line.

Running the program on `sample.in`:

```
Line: x = 5
Postfix: x = 5
Result: x = 5

Line: y = 3
Postfix: y = 3
Result: y = 3

Line: z = x + y * 2
Postfix: z = x y 2 * +
Result: z = 11

Line: a = z / 0
Postfix: a = z 0 /
Result: ERROR - Division by zero

Line: b = x - y
Postfix: b = x y -
Result: b = 2

Line: c
Postfix: c
Result: ERROR - Undefined variable c

-------------------------------------------

Variables used:
x = 5
y = 3
z = 11
a = (undefined)
b = 2
c = (undefined)

-------------------------------------------

Errors found:
Line 4: Division by zero
Line 6: Undefined variable c
```


## Modules and Functions

The program follows a structured, layered design. Each module has one
responsibility and depends only on the layers beneath it. All source files sit in
a single directory; no subfolders are needed to compile or run the program.

```
main.py  ->  gui.py  ->  processor_interface.py  ->  parser.py
                                                 ->  evaluator.py
```

### `main.py` — entry point

| Function | Description |
|---|---|
| *(module body)* | Imports `run` from `gui` and calls it when the file is executed directly. Keeps the launch point separate from the interface code. |

### `gui.py` — user interface

Builds the window and handles every user interaction. It performs no parsing or
evaluation of its own; it only passes the input lines down and displays the
string it gets back.

| Function / method | Description |
|---|---|
| `class App(tk.Tk)` | The main application window. Two panels side by side, each with a text area and a button below it. |
| `App._build_left_panel()` | Creates the `Input lines:` caption, the editable input text area with its scrollbar, and the **Load File** button. |
| `App._build_right_panel()` | Creates the read-only output text area with its scrollbar and the **Process** button. |
| `App._on_input_change()` | Enables the **Process** button when the input text area holds non-whitespace text and disables it otherwise. |
| `App._watch_input()` | Re-checks the input area every 200 ms so the **Process** button stays correct however the text arrived — typing, a menu paste or a drag and drop. |
| `App.on_load_file()` | Opens a file dialog over any directory, rejects any file whose extension is not `.in`, reads the file, and replaces the whole content of the input text area. Read failures are reported in a message box. |
| `App.on_process()` | Reads the input area, refuses to run when it is empty, splits it into lines, calls `process_input`, and replaces the whole content of the output text area. |
| `run()` | Instantiates `App` and enters the Tkinter main loop, so the program stays open until the user closes the window. |

### `processor_interface.py` — orchestration

Drives one full pass over the input and assembles the output text. This is the
only module where the parser and the evaluator meet.

| Function | Description |
|---|---|
| `process_input(lines)` | Processes every non-empty line in order against one shared `VariableStore` and returns the complete output string. Collects the per-line blocks, the final variable values, and the error list, then joins the three sets with blank lines. |
| `_parse_line(line, store)` | Tokenizes, validates and converts one code to postfix. Registers every variable of the line with the store so it appears under *Variables used* even if evaluation later fails. Returns `(target, postfix_tokens)`. |
| `_evaluate_line(target, postfix, store)` | Evaluates the postfix tokens and, for a statement, stores the value in the target variable. Because a failure raises before the store is written, a failed statement leaves its target at its previous value. |
| `_format_postfix(target, postfix)` | Renders the postfix notation of the whole code, keeping the `var =` prefix in front of the converted expression for a statement. |
| `_format_result(target, value)` | Renders the given code with its expression part replaced by the resulting value: `z = 11` for a statement, `11` for a bare expression. |

### `parser.py` — lexical and syntactic analysis

Turns raw text into validated tokens and converts infix to postfix. It knows
nothing about variable values.

| Function | Description |
|---|---|
| `tokenize(line)` | Breaks a raw line into tokens: variable names, integer literals, operators, `=` and parentheses. Whitespace is skipped. Raises `ValueError("Invalid input code")` on an illegal character, on a name containing an underscore, and on a number immediately followed by a letter such as `1abc`. |
| `validate_code(tokens)` | Accepts either `var = expression`, requiring exactly one `=` with a single valid variable on its left, or a bare expression. Raises `ValueError("Invalid input code")` otherwise. |
| `_validate_expression(tokens)` | Scans the expression tokens tracking whether an operand or an operator is expected next, and tracking parenthesis depth. Catches consecutive operators, a missing operator between operands, a dangling operator, empty parentheses, and unbalanced parentheses. |
| `split_code(tokens)` | Splits a validated token list into `(target_variable, expression_tokens)`. The target is `None` for a bare expression. |
| `collect_variables(tokens)` | Returns the variable names in a token list in order of first appearance, without duplicates. |
| `infix_to_postfix(tokens)` | Converts an expression to postfix using the shunting-yard algorithm. |
| `_is_number` / `_is_variable` | Token classification helpers. |
| `_invalid()` | Raises the single `ValueError("Invalid input code")` used throughout the module. |

### `evaluator.py` — evaluation and variable state

Computes values from postfix tokens and remembers what each variable holds.

| Class / function | Description |
|---|---|
| `class VariableStore` | Holds the most recently assigned value of every variable, in order of first appearance in the input. |
| `VariableStore.note_used(name)` | Records that a variable appeared in the input even if it never receives a value, so it still shows up under *Variables used*. |
| `VariableStore.get(name)` | Returns the current value, or raises `ValueError("Undefined variable <name>")` when the variable has never been assigned. |
| `VariableStore.set(name, value)` | Stores a new value, replacing any previous one. |
| `VariableStore.is_defined(name)` | Reports whether the variable currently holds a value. |
| `VariableStore.list_final_values()` | Returns the `name = value` lines for the *Variables used* set, marking never-assigned variables as `(undefined)`. |
| `evaluate_postfix(tokens, store)` | Evaluates postfix tokens with an operand stack: literals and variable values are pushed, an operator pops two operands and pushes the result. Returns the single remaining value. |
| `_apply(operator, left, right)` | Applies one binary operator to two integers. |
| `_c_divide(left, right)` | Integer division truncated toward zero; raises `ValueError("Division by zero")` when the divisor is zero. |
| `_c_modulo(left, right)` | Remainder consistent with `_c_divide`; raises the same error on a zero divisor. |

### Supporting files

| File | Description |
|---|---|
| `test_parser.py` | Covers tokenizing, validation and conversion: precedence, associativity, parentheses, malformed syntax, illegal characters and invalid variable names. |
| `test_evaluator.py` | Covers arithmetic, C division and modulo semantics, most-recent-value lookup, all three error kinds, retention of a target variable's previous value after a division by zero, and the output format. |
| `sample.in` | A sample input file exercising assignments, a complex expression, a division by zero and an undefined variable. |


## Control Flow

### Program startup
1. The user runs `main.py` (or the packaged executable).
2. `main.py` calls `gui.run()`.
3. `run()` builds the `App` window: input text area with **Load File**, output
   text area with **Process**.
4. The **Process** button starts disabled because the input area is empty.
5. Tkinter's main loop takes over. The program stays open, and the user may load
   files and process input any number of times, until the window is closed.

### Loading an input file
1. The user clicks **Load File**.
2. A file dialog opens, able to reach any directory on the computer.
3. If the user cancels, nothing changes.
4. If the chosen file does not end in `.in`, an error box appears and nothing
   changes.
5. The file is read. On a read failure an error box appears and nothing changes.
6. The content replaces everything in the input text area.
7. The **Process** button becomes enabled.

The user may instead type or edit codes directly in the input text area, with the
same effect on the **Process** button.

### Processing the input
1. The user clicks **Process**. The button is only active when the input area
   holds non-whitespace text.
2. `on_process()` splits the input area into lines and calls `process_input`.
3. `process_input` creates one empty `VariableStore` for the whole run, so state
   carries across lines but not across clicks.
4. For each line, in order, skipping blank lines:
   1. `tokenize` breaks the line into tokens.
   2. `validate_code` checks the token sequence.
   3. `split_code` separates the target variable from the expression.
   4. Every variable of the line is registered with the store.
   5. `infix_to_postfix` converts the expression, and the postfix line is
      formatted.
   6. `evaluate_postfix` computes the value, reading variable values from the
      store.
   7. For a statement, the value is written to the target variable.
   8. The block `Line:` / `Postfix:` / `Result:` is appended.
   9. If any step raised a `ValueError`, the message is recorded with its line
      number and the block's `Result:` reports the error instead of a value. The
      postfix line is still shown whenever the conversion itself succeeded, as in
      `a = z 0 /` for a division by zero.
5. After the last line, `list_final_values()` produces the *Variables used* set.
6. The three sets — the per-line blocks, the variables, the errors — are joined
   with blank lines between them.
7. `on_process()` replaces everything in the output text area with that string.
   The output area is read-only, so the user cannot alter it.

### Error handling
A `ValueError` from any stage is caught once, in the per-line loop of
`process_input`. This keeps the failure local: the line is reported as an error
and processing continues with the next line. Because the exception propagates out
of the evaluation before the store is written, a statement that fails leaves its
target variable exactly as it was — which is what the specification requires for
a division by zero.


## Usage
```bash
python main.py
```
Requires Python 3.10 or newer. Tkinter is part of the standard library, so no
packages need to be installed.


## Testing
```bash
python test_parser.py
python test_evaluator.py
```


## Work Distribution

| Member | Responsibilities |
|---|---|
| Jomuad | |
| Ojanola | |
| Taclindo | |
