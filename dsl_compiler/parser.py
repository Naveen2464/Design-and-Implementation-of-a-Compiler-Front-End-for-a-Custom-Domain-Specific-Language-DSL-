import ply.yacc as yacc
from lexer_updated import tokens, lexer as lexer_obj

# --------------------------------
# TAC CODE STORAGE
# --------------------------------

tac_code = []

temp_count = 1
label_count = 1

# --------------------------------
# Symbol Table
# --------------------------------

symbol_table = {}

# --------------------------------
# Compiler Report Storage
# --------------------------------

lexical_tokens = []
syntax_messages = []
syntax_errors = []
semantic_messages = []
semantic_errors = []

# --------------------------------
# Generate Temporary Variables
# --------------------------------

def new_temp():
    global temp_count

    temp_name = f"t{temp_count}"
    temp_count += 1
    return temp_name

# --------------------------------
# Generate Labels
# --------------------------------

def new_label():
    global label_count

    label_name = f"L{label_count}"
    label_count += 1
    return label_name

# --------------------------------
# Condition Helpers
# --------------------------------

def reverse_condition(condition):
    reversed_map = {
        '==': '!=',
        '!=': '==',
        '<': '>=',
        '>': '<=',
        '<=': '>',
        '>=': '<'
    }

    if isinstance(condition, (tuple, list)) and len(condition) == 3:
        left, op, right = condition
        return f"{left} {reversed_map.get(op, op)} {right}"

    if isinstance(condition, str):
        parts = condition.split()
        if len(parts) == 3:
            left, op, right = parts
            return f"{left} {reversed_map.get(op, op)} {right}"

    return str(condition)


def format_condition(condition):
    if isinstance(condition, (tuple, list)) and len(condition) == 3:
        left, op, right = condition
        return f"{left} {op} {right}"

    if isinstance(condition, str):
        return condition

    return " ".join(str(item) for item in condition)


def build_else_clause(else_clause, end_label):
    if else_clause is None:
        return []

    clause_type = else_clause[0]

    if clause_type == 'otherwise':
        return else_clause[1]

    if clause_type == 'elif':
        condition = else_clause[1]
        then_code = else_clause[2]
        next_clause = else_clause[3]
        next_label = new_label()

        code = [f"if {reverse_condition(format_condition(condition))} goto {next_label}"]
        code.extend(then_code)
        code.append(f"goto {end_label}")
        code.append(f"{next_label}:")
        code.extend(build_else_clause(next_clause, end_label))
        return code

    return []

# --------------------------------
# Grammar Rules
# --------------------------------

# Program
def p_program(p):
    '''
    program : statements
    '''

    tac_code.extend(p[1])

# --------------------------------
# Multiple Statements
# --------------------------------

def p_statements_multiple(p):
    '''
    statements : statement statements
    '''

    p[0] = p[1] + p[2]


def p_statements_single(p):
    '''
    statements : statement
    '''

    p[0] = p[1]

# --------------------------------
# Statement Types
# --------------------------------

def p_statement(p):
    '''
    statement : declaration
              | assignment
              | print_statement
              | repeat_statement
              | cycle_statement
              | check_statement
    '''

    p[0] = p[1]

# --------------------------------
# Declaration
# --------------------------------

def p_declaration(p):
    '''
    declaration : NUM IDENTIFIER ASSIGN expression
    '''

    variable_name = p[2]
    code = []

    if variable_name in symbol_table:
        semantic_errors.append(f"Variable '{variable_name}' already declared")
    else:
        symbol_table[variable_name] = "num"
        expr_code, expr_val = p[4]
        code.extend(expr_code)
        code.append(f"{variable_name} = {expr_val}")
        semantic_messages.append(f"Declared variable '{variable_name}'")
        syntax_messages.append("Valid Declaration")

    p[0] = code

# --------------------------------
# Assignment
# --------------------------------

def p_assignment(p):
    '''
    assignment : IDENTIFIER ASSIGN expression
    '''

    variable_name = p[1]
    code = []

    if variable_name not in symbol_table:
        semantic_errors.append(f"Variable '{variable_name}' not declared")
    else:
        expr_code, expr_val = p[3]
        code.extend(expr_code)
        code.append(f"{variable_name} = {expr_val}")
        semantic_messages.append(f"Assigned value to '{variable_name}'")
        syntax_messages.append("Valid Assignment")

    p[0] = code

# --------------------------------
# Print Statement
# --------------------------------

def p_print_statement(p):
    '''
    print_statement : SHOW IDENTIFIER
    '''

    variable_name = p[2]
    code = []

    if variable_name not in symbol_table:
        semantic_errors.append(f"Variable '{variable_name}' not declared")
    else:
        code.append(f"printx {variable_name}")
        semantic_messages.append(f"Print statement validated for '{variable_name}'")
        syntax_messages.append("Valid Print Statement")

    p[0] = code

# --------------------------------
# Repeat Statement
# --------------------------------

def p_repeat_statement(p):
    '''
    repeat_statement : WHILE LPAREN condition RPAREN LBRACE statements RBRACE
    '''

    condition_code, condition_value = p[3]
    body_code = p[6]
    start_label = new_label()
    end_label = new_label()
    code = [f"{start_label}:"]
    code.extend(condition_code)
    code.append(f"if {reverse_condition(format_condition(condition_value))} goto {end_label}")
    code.extend(body_code)
    code.append(f"goto {start_label}")
    code.append(f"{end_label}:")

    semantic_messages.append("Validated WHILE loop")
    syntax_messages.append("Valid WHILE Loop")
    p[0] = code

# --------------------------------
# Cycle Statement
# --------------------------------

def p_cycle_statement(p):
    '''
    cycle_statement : FOR LPAREN assignment SEMICOLON condition SEMICOLON assignment RPAREN LBRACE statements RBRACE
    '''

    init_code = p[3]
    condition_code, condition_value = p[5]
    update_code = p[7]
    body_code = p[10]
    start_label = new_label()
    end_label = new_label()
    code = []
    code.extend(init_code)
    code.append(f"{start_label}:")
    code.extend(condition_code)
    code.append(f"if {reverse_condition(format_condition(condition_value))} goto {end_label}")
    code.extend(body_code)
    code.extend(update_code)
    code.append(f"goto {start_label}")
    code.append(f"{end_label}:")

    semantic_messages.append("Validated FOR loop")
    syntax_messages.append("Valid FOR Loop")
    p[0] = code

# --------------------------------
# Check Statement
# --------------------------------

def p_check_statement(p):
    '''
    check_statement : IF LPAREN condition RPAREN LBRACE statements RBRACE else_clause
    '''

    condition_code, condition_value = p[3]
    then_code = p[6]
    else_clause = p[8]
    false_label = new_label()
    end_label = new_label()
    code = []
    code.extend(condition_code)
    code.append(f"if {reverse_condition(format_condition(condition_value))} goto {false_label}")
    code.extend(then_code)

    if else_clause is not None:
        code.append(f"goto {end_label}")
        code.append(f"{false_label}:")
        code.extend(build_else_clause(else_clause, end_label))
        code.append(f"{end_label}:")
        semantic_messages.append("Validated IF-ELSE statement")
        syntax_messages.append("Valid IF-ELSE Statement")
    else:
        code.append(f"{false_label}:")
        semantic_messages.append("Validated IF statement")
        syntax_messages.append("Valid IF Statement")

    p[0] = code

# --------------------------------
# Else Clause
# --------------------------------

def p_else_clause_otherwise(p):
    '''
    else_clause : ELSE LBRACE statements RBRACE
    '''

    p[0] = ('otherwise', p[3])


def p_else_clause_elif(p):
    '''
    else_clause : ELIF LPAREN condition RPAREN LBRACE statements RBRACE else_clause
    '''

    p[0] = ('elif', p[3], p[6], p[8])


def p_else_clause_empty(p):
    '''
    else_clause :
    '''

    p[0] = None

# --------------------------------
# Conditions
# --------------------------------

def p_condition(p):
    '''
    condition : expression LT expression
              | expression GT expression
              | expression LE expression
              | expression GE expression
              | expression EQ expression
              | expression NE expression
    '''

    left_code, left_val = p[1]
    right_code, right_val = p[3]
    p[0] = (left_code + right_code, (left_val, p[2], right_val))

# --------------------------------
# Expressions
# --------------------------------

def p_expression_plus(p):
    '''
    expression : expression PLUS term
    '''

    left_code, left_val = p[1]
    right_code, right_val = p[3]
    temp = new_temp()
    code = left_code + right_code + [f"{temp} = {left_val} + {right_val}"]
    p[0] = (code, temp)


def p_expression_minus(p):
    '''
    expression : expression MINUS term
    '''

    left_code, left_val = p[1]
    right_code, right_val = p[3]
    temp = new_temp()
    code = left_code + right_code + [f"{temp} = {left_val} - {right_val}"]
    p[0] = (code, temp)


def p_expression_term(p):
    '''
    expression : term
    '''

    p[0] = p[1]

# --------------------------------
# Terms
# --------------------------------

def p_term_multiply(p):
    '''
    term : term MULTIPLY factor
    '''

    left_code, left_val = p[1]
    right_code, right_val = p[3]
    temp = new_temp()
    code = left_code + right_code + [f"{temp} = {left_val} * {right_val}"]
    p[0] = (code, temp)


def p_term_divide(p):
    '''
    term : term DIVIDE factor
    '''

    left_code, left_val = p[1]
    right_code, right_val = p[3]
    temp = new_temp()
    code = left_code + right_code + [f"{temp} = {left_val} / {right_val}"]
    p[0] = (code, temp)


def p_term_factor(p):
    '''
    term : factor
    '''

    p[0] = p[1]

# --------------------------------
# Factors
# --------------------------------

def p_factor_number(p):
    '''
    factor : NUMBER
    '''

    p[0] = ([], p[1])


def p_factor_identifier(p):
    '''
    factor : IDENTIFIER
    '''

    variable_name = p[1]

    if variable_name not in symbol_table:
        semantic_errors.append(f"Variable '{variable_name}' not declared")

    p[0] = ([], variable_name)


def p_factor_group(p):
    '''
    factor : LPAREN expression RPAREN
    '''

    p[0] = p[2]

# --------------------------------
# Error Handling
# --------------------------------

def p_error(p):
    if p:
        syntax_errors.append(f"Missing or invalid token '{p.value}' at line {p.lineno}")
    else:
        syntax_errors.append("Syntax error at EOF")

# --------------------------------
# TAC Interpreter
# --------------------------------

def resolve_value(token, runtime_env):
    if isinstance(token, int):
        return token
    if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
        return int(token)
    return runtime_env.get(token, 0)


def evaluate_condition(condition, runtime_env):
    left, op, right = condition.split()
    left_val = resolve_value(left, runtime_env)
    right_val = resolve_value(right, runtime_env)

    if op == '==':
        return left_val == right_val
    if op == '!=':
        return left_val != right_val
    if op == '<':
        return left_val < right_val
    if op == '>':
        return left_val > right_val
    if op == '<=':
        return left_val <= right_val
    if op == '>=':
        return left_val >= right_val

    return False


def execute_tac(code):
    runtime_env = {}
    labels = {}

    for index, instruction in enumerate(code):
        instruction = instruction.strip()
        if instruction.endswith(':'):
            labels[instruction[:-1]] = index

    ip = 0
    while ip < len(code):
        instruction = code[ip].strip()

        if not instruction or instruction.endswith(':'):
            ip += 1
            continue

        if instruction.startswith('printx '):
            operand = instruction[len('printx '):].strip()
            print(resolve_value(operand, runtime_env))
            ip += 1
            continue

        if instruction.startswith('goto '):
            label = instruction[len('goto '):].strip()
            ip = labels.get(label, ip + 1)
            continue

        if instruction.startswith('if '):
            condition_part, _, label = instruction[3:].partition(' goto ')
            if evaluate_condition(condition_part.strip(), runtime_env):
                ip = labels.get(label.strip(), ip + 1)
                continue
            ip += 1
            continue

        if '=' in instruction:
            target, expr = [part.strip() for part in instruction.split('=', 1)]
            parts = expr.split()

            if len(parts) == 1:
                runtime_env[target] = resolve_value(parts[0], runtime_env)
            elif len(parts) == 3:
                left_val = resolve_value(parts[0], runtime_env)
                operator = parts[1]
                right_val = resolve_value(parts[2], runtime_env)

                if operator == '+':
                    runtime_env[target] = left_val + right_val
                elif operator == '-':
                    runtime_env[target] = left_val - right_val
                elif operator == '*':
                    runtime_env[target] = left_val * right_val
                elif operator == '/':
                    runtime_env[target] = left_val // right_val if right_val != 0 else 0
                else:
                    runtime_env[target] = 0
            else:
                runtime_env[target] = 0

        ip += 1

    return runtime_env

# --------------------------------
# Build Parser
# --------------------------------

parser = yacc.yacc()

# --------------------------------
# Read Input File
# --------------------------------

with open("sample.dsl", "r") as file:
    data = file.read()

# --------------------------------
# Parse Input
# --------------------------------

lexer_obj.input(data)

while True:
    tok = lexer_obj.token()
    if not tok:
        break
    lexical_tokens.append(tok)

# Reset lexer before parse
lexer_obj.input(data)
parser.parse(data, lexer=lexer_obj)

if not syntax_errors:
    syntax_messages.append("Valid Program")

# --------------------------------
# Print Compiler Front-End Report
# --------------------------------

print("---------------------------------")
print("LEXICAL ANALYSIS")
print("---------------------------------\n")
print("TOKENS:\n")
for tok in lexical_tokens:
    print(tok)

print("\n---------------------------------")
print("SYNTAX ANALYSIS")
print("---------------------------------\n")
if syntax_errors:
    print("SYNTAX ERROR:")
    for error in syntax_errors:
        print(error)
else:
    for message in syntax_messages:
        print(message)

print("\n---------------------------------")
print("SEMANTIC ANALYSIS")
print("---------------------------------\n")
if semantic_errors:
    print("SEMANTIC ERROR:")
    for error in semantic_errors:
        print(error)
else:
    for message in semantic_messages:
        print(message)

print("\n---------------------------------")
print("SYMBOL TABLE")
print("---------------------------------\n")
print("Variable    Type")
print("----------------")
for variable, datatype in symbol_table.items():
    print(f"{variable:<12}{datatype}")

print("\n---------------------------------")
print("THREE ADDRESS CODE")
print("---------------------------------\n")
for line in tac_code:
    print(line)

print("\n---------------------------------")
print("PROGRAM OUTPUT")
print("---------------------------------\n")
execute_tac(tac_code)

