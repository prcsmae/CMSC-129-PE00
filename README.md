# Programming Exercise 00 - Expression Evaluation

A Python GUI application that processes simple assignment statements and expressions.


## Features
- **Load File** button — load input code from a `.in` file on disk.
- **Process** button — run the loaded/typed input and display results.
- Editable input text area, read-only output text area.
- **Parser** (`parser.py`) — tokenizes each line, validates it, and converts
  infix expressions to postfix (Shunting Yard).

### Supported input
- Assignment statements (`x = 5`) or bare expressions (`a + b`), one per line.
- Operators: `+ - * / %`, with parentheses. Precedence: `* / %` > `+ -`.
- Variable names: start with a letter, then letters/digits only (no underscores).
- Integer literals only. Anything else is reported as invalid input.

### Example (`sample.in`)
```
x = 5
y = 3
z = x + y * 2        -> postfix: x y 2 * +
a = z / 0            -> division by zero (flagged by evaluator)
b = x - y
c                    -> undefined variable (flagged by evaluator)
```


## Testing
```bash
python test_parser.py
```
Covers valid expressions, operator precedence/associativity, parentheses,
malformed syntax, illegal characters, and invalid variable names.


## Usage
```bash
python main.py
```

## Members
- Jomuad
- Taclindo
- Ojanola third wheel huhu
