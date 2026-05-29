
import ply.lex as lex

# --------------------------------
# Reserved Keywords
# --------------------------------

reserved = {
    'var': 'NUM',
    'printx': 'SHOW',
    'cycle': 'FOR',
    'repeat': 'WHILE',
    'check': 'IF',
    'otherwise': 'ELSE',
    'elif': 'ELIF'
}

# --------------------------------
# Tokens
# --------------------------------

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'LT',
    'GT',
    'LE',
    'GE',
    'EQ',
    'NE'
] + list(reserved.values())

# --------------------------------
# Regular Expression Rules
# --------------------------------

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Ignore spaces and tabs
t_ignore = ' \t'

# --------------------------------
# Identifier Rule
# --------------------------------

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Check reserved words
    t.type = reserved.get(t.value, 'IDENTIFIER')

    return t

# --------------------------------
# Number Rule
# --------------------------------

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# --------------------------------
# Newline Rule
# --------------------------------

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# --------------------------------
# Error Handling
# --------------------------------

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# --------------------------------
# Build Lexer
# --------------------------------

lexer = lex.lex()

if __name__ == '__main__':
    # --------------------------------
    # Read Input File
    # --------------------------------

    with open("sample.dsl", "r") as file:
        data = file.read()

    # Give input to lexer
    lexer.input(data)

    # --------------------------------
    # Print Tokens
    # --------------------------------

    print("\nTOKENS:\n")

    while True:
        tok = lexer.token()

        if not tok:
            break

        print(tok)
