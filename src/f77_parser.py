import ply.yacc as yacc
from f77_lexer import tokens
from utils.AST import Node
import sys

start = 'program'

# program
def p_program(p):
    'program : PROGRAM ID decl_list stmt_list END'
    p[0] = Node('program', p[2], p[3], p[4])

# declarations
def p_decl_list_recursive(p):
    'decl_list : decl_list declaration'
    p[0] = Node('decl_list', p[1], p[2])

def p_decl_list_empty(p):
    'decl_list :'
    p[0] = Node('empty')

def p_declaration(p):
    'declaration : type id_list'
    p[0] = Node('decl', p[1], p[2])

def p_type(p):
    '''type : INTEGER
            | REAL
            | LOGICAL'''
    p[0] = p[1]

def p_id_list(p):
    'id_list : id_element more_ids'
    p[0] = Node('id_list', p[1], p[2])

def p_more_ids_recursive(p):
    'more_ids : COMMA id_element more_ids'
    p[0] = Node('more_ids', p[2], p[3])

def p_more_ids_empty(p):
    'more_ids :'
    p[0] = Node('empty')

def p_id_element(p):
    '''id_element : ID 
                  | ID LPAREN expr_list RPAREN'''
    if len(p) == 2:
        p[0] = Node('id', p[1])
    else:
        p[0] = Node('id_array', p[1], p[3])


# statements
def p_stmt_list_recursive(p):
    'stmt_list : stmt_list statement'
    p[0] = Node('stmt_list', p[1], p[2])

def p_stmt_list_empty(p):
    'stmt_list :'
    p[0] = Node('empty')

def p_statement(p):
    'statement : opt_label basic_statement'
    p[0] = Node('stmt', p[1], p[2])

def p_opt_label(p):
    '''opt_label : INT'''
    p[0] = p[1]

def p_opt_label_empty(p):
    '''opt_label : '''
    p[0] = Node('empty')

def p_basic_statement(p):
    '''basic_statement : assignment
                           | print_stmt
                           | read_stmt
                           | do_loop
                           | if_stmt
                           | goto_stmt
                           | continue_stmt'''
    p[0] = p[1]

# assignment
def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = Node('assign', p[1], p[3])

# print/read
def p_print_stmt(p):
    'print_stmt : PRINT MULT COMMA expr_list'
    p[0] = Node('print', p[4])


def p_read_stmt(p):
    'read_stmt : READ MULT COMMA id_list'
    p[0] = Node('read', p[4])

# expression lists
def p_expr_list(p):
    'expr_list : expression more_exprs'
    p[0] = Node('expr_list', p[1], p[2])


def p_more_exprs_recursive(p):
    'more_exprs : COMMA expression more_exprs'
    p[0] = Node('more_exprs', p[2], p[3])

def p_more_exprs_empty(p):
    'more_exprs :'
    p[0] = Node('empty')

# do loop
def p_do_loop(p):
    'do_loop : DO INT ID ASSIGN expression COMMA expression stmt_list INT CONTINUE'
    p[0] = Node('do', p[2], p[3], p[5], p[7], p[8], p[9])

# if statement
def p_if_stmt(p):
    'if_stmt : IF LPAREN condition RPAREN THEN stmt_list else_part ENDIF'
    p[0] = Node('if', p[3], p[6], p[7])


def p_else_part(p):
    'else_part : ELSE stmt_list'
    p[0] = Node('else', p[2])

def p_else_part_empty(p):
    'else_part :'
    p[0] = Node('empty')

# goto / continue
def p_goto_stmt(p):
    'goto_stmt : GOTO INT'
    p[0] = Node('goto', p[2])


def p_continue_stmt(p):
    'continue_stmt : CONTINUE'
    p[0] = Node('continue')

# conditions 
def p_condition(p):
    'condition : or_expr'
    p[0] = p[1]


def p_or_expr(p):
    '''or_expr : or_expr OR and_expr
               | and_expr'''
    if len(p) == 4:
        p[0] = Node('or', p[1], p[3])
    else:
        p[0] = p[1]

def p_and_expr(p):
    '''and_expr : and_expr AND not_expr
                | not_expr'''
    if len(p) == 4:
        p[0] = Node('and', p[1], p[3])
    else:
        p[0] = p[1]

def p_not_expr(p):
    '''not_expr : NOT not_expr
                | rel_expr'''
    if len(p) == 3:
        p[0] = Node('not', p[2])
    else:
        p[0] = p[1]

def p_rel_expr(p):
    '''rel_expr : expression relop expression
                | expression'''                   
    if len(p) == 4:
        p[0] = Node('rel', p[2], p[1], p[3])
    else:
        p[0] = p[1]
         

# relop
def p_relop_eq(p):
    '''relop : EQ
             | NE
             | LT
             | LE
             | GT
             | GE'''
    p[0] = p[1]

# expressions
def p_expression(p):
    'expression : term expression_tail'
    node = p[1]
    for op, val in p[2]:
        node = Node(op, node, val)
    p[0] = node


def p_expression_tail_plus(p):
    'expression_tail : PLUS term expression_tail'
    p[0] = [('plus', p[2])] + p[3]


def p_expression_tail_minus(p):
    'expression_tail : MINUS term expression_tail'
    p[0] = [('minus', p[2])] + p[3]


def p_expression_tail_empty(p):
    'expression_tail :'
    p[0] = []

# terms
def p_term(p):
    'term : factor term_tail'
    node = p[1]
    for op, val in p[2]:
        node = Node(op, node, val)
    p[0] = node


def p_term_tail_mult(p):
    'term_tail : MULT factor term_tail'
    p[0] = [('mul', p[2])] + p[3]


def p_term_tail_div(p):
    'term_tail : DIV factor term_tail'
    p[0] = [('div', p[2])] + p[3]


def p_term_tail_empty(p):
    'term_tail :'
    p[0] = []

# factor 
def p_factor_id(p):
    'factor : ID'
    p[0] = Node('id', p[1])

def p_factor_int(p):
    'factor : INT'
    p[0] = Node('int', p[1])

def p_factor_float(p):
    'factor : FLOAT'
    p[0] = Node('float', p[1])

def p_factor_bool(p):
    'factor : BOOL'
    p[0] = Node('bool', p[1])

def p_factor_string(p):
    'factor : STRING'
    p[0] = Node('string', p[1])


def p_factor_paren(p):
    'factor : LPAREN condition RPAREN'
    p[0] = p[2]

def p_factor_func(p):
    'factor : ID LPAREN expr_list RPAREN'
    p[0] = Node('call', p[1], p[3])

# error
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value})")
    else:
        print("Syntax error at EOF")

# build parser
parser = yacc.yacc(debug=True, debugfile='parser.out')






