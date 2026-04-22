import ply.yacc as yacc
from f77_lexer import tokens
from utils.AST import Node
import sys

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

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
    'id_list : ID more_ids'
    p[0] = Node('id_list', p[1], p[2])

def p_more_ids_recursive(p):
    'more_ids : COMMA ID more_ids'
    p[0] = Node('more_ids', p[2], p[3])

def p_more_ids_empty(p):
    'more_ids :'
    p[0] = Node('empty')

# statements
def p_stmt_list_recursive(p):
    'stmt_list : stmt_list statement'
    p[0] = Node('stmt_list', p[1], p[2])

def p_stmt_list_empty(p):
    'stmt_list :'
    p[0] = Node('empty')


def p_statement(p):
    '''statement : assignment
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
    p[0] = Node('do', p[2], p[3], p[5], p[7], p[8])

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
def p_condition_rel(p):
    'condition : expression relop expression'
    p[0] = Node('rel', p[2], p[1], p[3])


def p_condition_and(p):
    'condition : condition AND condition'
    p[0] = Node('and', p[1], p[3])


def p_condition_or(p):
    'condition : condition OR condition'
    p[0] = Node('or', p[1], p[3])


def p_condition_not(p):
    'condition : NOT condition'
    p[0] = Node('not', p[2])


def p_condition_paren(p):
    'condition : LPAREN condition RPAREN'
    p[0] = p[2]

# relop
def p_relop_eq(p):
    'relop : EQ'
    p[0] = p[1]

def p_relop_ne(p):
    'relop : NE'
    p[0] = p[1]

def p_relop_lt(p):
    'relop : LT'
    p[0] = p[1]

def p_relop_le(p):
    'relop : LE'
    p[0] = p[1]

def p_relop_gt(p):
    'relop : GT'
    p[0] = p[1]

def p_relop_ge(p):
    'relop : GE'
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
def p_factor(p):
    '''factor : ID
              | INT
              | FLOAT
              | BOOL
              | STRING'''
    p[0] = p[1]


def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# error
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value})")
    else:
        print("Syntax error at EOF")

# build parser
parser = yacc.yacc(debug=True)







