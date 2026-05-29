# Compiler Front-End for a Custom DSL

## Introduction

This project implements the front-end of a custom Domain-Specific Language (DSL) compiler. The compiler performs lexical analysis, syntax analysis, semantic analysis, type checking, and generates Three-Address Code (TAC).

The language now supports custom control-flow keywords to make the syntax unique and domain-specific.

---

# Objectives

The main objectives of this project are:

- Create a domain-specific control flow syntax
- Define the language grammar using Context-Free Grammar (CFG)
- Implement lexical analysis using tokenization
- Perform syntax analysis using parsing
- Implement semantic analysis using symbol tables
- Generate Three-Address Code (TAC)

---

# Features

The custom DSL supports:

- Variable declaration with `var`
- Assignment statements
- Arithmetic expressions
- Custom print statements with `printx`
- Repeat loops with `repeat`
- Cycle loops with `cycle`
- Conditional branches with `check`, `elif`, and `otherwise`
- Text and C-style source analysis utilities via `c_utils.py`

Example DSL syntax:

```text
var a = 5
var b = 10
var c = a + b
printx c

cycle (a = 0; a < b; a = a + 1) {
    check (a == 5) {
        c = c + a
    } otherwise {
        c = c + 1
    }
}

repeat (a < 12) {
    a = a + 1
}
```