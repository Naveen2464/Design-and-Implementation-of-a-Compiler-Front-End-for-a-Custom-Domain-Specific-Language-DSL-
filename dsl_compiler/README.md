# Design and Implementation of a Compiler Front-End for a Custom Domain-Specific Language (DSL)

![DSL Compiler Banner](https://img.shields.io/badge/Project-Compiler_Front--End-3b82f6?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

This project is a complete front-end compiler implementation for a custom Domain-Specific Language (DSL) built using Python and PLY (Python Lex-Yacc). It also features a sleek, interactive web-based simulator powered by Flask to write code and visualize each step of the compilation process in real-time.

## 🚀 Features

- **Custom DSL Syntax**: A unique language designed with custom keywords for variables, printing, and control flow.
- **Lexical Analysis (Scanner)**: Tokenizes the input source code, correctly identifying identifiers, numbers, operators, and reserved keywords.
- **Syntax Analysis (Parser)**: Validates the token stream against a defined Context-Free Grammar (CFG) using an LALR(1) parser.
- **Semantic Analysis**: Enforces scoping, type rules, and checks for undeclared or doubly declared variables.
- **Symbol Table Management**: Dynamically tracks variable declarations and their types throughout the compilation.
- **Three-Address Code (TAC) Generation**: Translates the high-level DSL into intermediate TAC for optimization and execution.
- **TAC Interpreter**: Executes the generated TAC instructions directly to produce output.
- **Web Interface**: A beautiful, dark-themed web GUI that lets you write DSL code and inspect the output of every compilation stage side-by-side.

## 🛠️ Technology Stack

- **Core Compiler**: Python 3
- **Lexer & Parser Generator**: [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply)
- **Web Backend**: Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

---

## 📖 Language Syntax & Grammar

The custom DSL uses specific keywords to replace standard programming constructs:

- **Variables**: `var` instead of `int` or `let`
- **Output**: `printx` instead of `print` or `console.log`
- **Conditional (If/Else)**: `check`, `elif`, and `otherwise`
- **For Loop**: `cycle`
- **While Loop**: `repeat`

### Example DSL Program:

```text
var a = 0
var b = 10
var c = 0

cycle (a = 0; a < b; a = a + 1) {
    check (a == 5) {
        c = c + a
    } otherwise {
        c = c + 1
    }

    repeat (c < 5) {
        c = c + 1
    }
}

printx c
```

---

## 📂 Project Structure

```text
📁 dsl_compiler
├── 📄 app.py              # Flask web server and API for the compiler
├── 📄 lexer_updated.py    # Lexical Analyzer (Tokens & Regex rules)
├── 📄 parser.py           # Syntax Analyzer, Semantic Analyzer, TAC Generator & Interpreter
├── 📄 sample.dsl          # Sample DSL source code file used for testing
├── 📄 sample1.dsl         # Additional sample DSL file
├── 📄 grammar.txt         # Documentation of the Context-Free Grammar used
├── 📁 templates
│   └── 📄 index.html      # Web GUI frontend
└── 📄 README.md           # Project Documentation
```

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.7 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/Naveen2464/Design-and-Implementation-of-a-Compiler-Front-End-for-a-Custom-Domain-Specific-Language-DSL-.git
cd Design-and-Implementation-of-a-Compiler-Front-End-for-a-Custom-Domain-Specific-Language-DSL-/dsl_compiler
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
The required packages are `Flask` for the web server and `ply` for the compiler.
```bash
pip install flask ply
```

---

## 💻 How to Compile and Execute

You can compile and execute your custom DSL code using one of the following two methods:

### Method 1: Using the Web GUI (Recommended)
The project features an interactive web simulator that makes it extremely easy to visualize the compilation process.

1. **Start the Web Server**:
   Run the `app.py` file from your terminal:
   ```bash
   python app.py
   ```
2. **Open the Interface**:
   Open your preferred web browser and go to:
   ```text
   http://localhost:5000
   ```
3. **Compile and Execute**:
   - Write your DSL code in the provided text editor on the left panel.
   - Click the **"Run Compiler"** button.
   - The web app will automatically compile the code, generate the TAC, and execute it. 
   - You can view the final output in the **"Output"** tab, or navigate through the other tabs to see the Lexical, Syntax, Semantic, and Symbol Table data.

### Method 2: Using the Command Line
If you prefer the terminal, you can directly run the Python parser.

1. **Write your Code**:
   Open the `sample.dsl` file in any text editor and write your custom DSL code. Save the file.
   
2. **Run the Compiler (Parser)**:
   In your terminal, run the `parser.py` script:
   ```bash
   python parser.py
   ```
3. **View the Execution Output**:
   The compiler will process `sample.dsl` and output the results directly to the terminal. It will sequentially show the Lexical Tokens, Syntax Validation, Semantic Errors (if any), Symbol Table, Three-Address Code, and finally execute the code under the **"PROGRAM OUTPUT"** section.

---

## 🔍 Output Stages Explained

When a program is compiled, it passes through the following phases:

1. **Lexical Analysis**: The source text is broken down into a stream of tokens (e.g., `NUM`, `IDENTIFIER`, `ASSIGN`). Invalid characters throw a lexical error.
2. **Syntax Analysis**: The parser verifies that the sequence of tokens forms a valid structure according to the DSL's grammar.
3. **Semantic Analysis**: Checks logical rules—ensuring variables are declared before they are used or printed, and preventing duplicate declarations. 
4. **Symbol Table**: Displays the memory allocation map, showing the names and data types of all active variables.
5. **Three-Address Code (TAC)**: A low-level intermediate representation of the code, broken down into simple operations using temporary variables and labels for jumps (`goto`).
6. **Program Output**: The built-in TAC interpreter runs the generated TAC instructions and prints the final output of your `printx` statements.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](../../issues) if you want to contribute. 

## 📝 License

This project is open-source and available under the MIT License.