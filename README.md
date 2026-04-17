# Mini Interpreter with Python and C

This project is a small interpreted programming language built with Python and C.

The parser and evaluator are written in Python with `PLY`, while variable storage is backed by a C dynamic library loaded through `cffi`.

## Overview

The language currently supports:

- variable assignment
- integer, float, string, and boolean values
- arithmetic with `+` and `-`
- comparisons with `==`, `!=`, `<`, `>`, `<=`, `>=`
- conditional statements with `si`, `alors`, and `sinon`
- multi-line blocks with `{ ... }`
- grouped expressions with parentheses

Example:

```txt
a = 1
b = 2
c = 5

si ((a + b) < c) alors {
    message = "ok"
} sinon {
    message = "not ok"
}

message
```

## Project Structure

- `lexer.py`: lexer, parser, and interpreter entry point
- `ast_nodes.py`: AST node definitions and evaluation logic
- `variableC_interface.py`: Python/C bridge using `cffi`
- `variable.c` and `variable.h`: variable management in C
- `hashmap.c` and `hashmap.h`: hashmap implementation used by the runtime
- `vg-01.dll`: compiled C runtime library
- `parsetab.py`: auto-generated parser table by PLY

## How It Works

1. `lexer.py` tokenizes and parses the source code with PLY.
2. The parser builds an abstract syntax tree.
3. `ast_nodes.py` evaluates that tree.
4. Variables are stored in a C hashmap through the DLL.

This means the language is currently interpreted, not compiled.

## Language Syntax

### Assignment

```txt
x = 10
name = "hello"
value = 3.14
```

### Arithmetic

```txt
a = 1 + 2
b = (a - 1)
c = ((1 + 2) - 1)
```

### Comparisons

```txt
a == 1
a != 2
a < 10
a <= 10
a > 0
a >= 0
```

### Conditionals

```txt
si a == 1 alors {
    result = "true branch"
} sinon {
    result = "false branch"
}
```

### Nested Conditionals

```txt
si a < 10 alors {
    si b > 2 alors {
        result = "nested"
    }
}
```

## Requirements

- Python 3
- `ply`
- `cffi`
- a compiled `vg-01.dll`

Install Python dependencies with:

```bash
pip install ply cffi
```

## Building the C Runtime

The C runtime can be compiled from:

- `variable.c`
- `hashmap.c`

Example command:

```bash
gcc -shared -o vg-01.dll variable.c hashmap.c
```

You may need to adapt the command depending on your compiler and environment.

## Running the Interpreter

At the moment, `lexer.py` contains a small hardcoded example inside `__main__`.

Run it with:

```bash
python lexer.py
```

You can also import the interpreter class from Python:

```python
from lexer import Interpreter

interpreter = Interpreter()
result = interpreter.run("""
a = 1
si a == 1 alors {
    b = "ok"
} sinon {
    b = "no"
}
b
""")

print(result)
```

## Current Limitations

- keywords are currently in French: `si`, `alors`, `sinon`
- no loops yet
- no functions yet
- no logical operators like `and` / `or` yet
- memory management on the C side still needs cleanup and hardening
- parser generation currently reports one classic shift/reduce conflict related to `else`

## Future Ideas

- logical operators
- loops
- user-defined functions
- local scopes
- better error messages
- cleaner memory management in the C runtime

## Status

This is an educational interpreter project and is still in active development.
