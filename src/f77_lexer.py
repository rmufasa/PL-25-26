import ply.lex as lex

# list of tokens

tokens = (
    # keywords
    'PROGRAM', 'INTEGER', 'REAL', 'LOGICAL',
    'IF', 'THEN', 'ELSE', 'ENDIF',
    'DO', 'CONTINUE', 'GOTO',
    'READ', 'PRINT',
    'FUNCTION', 'SUBROUTINE', 'RETURN', 'END',

    # indentifiers and constants
    'ID', 'INT', 'FLOAT', 'BOOL', 'STRING',

    # operators
    'PLUS', 'MINUS', 'MULT', 'DIV',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR', 'NOT',
    'ASSIGN',

    # symbols
    'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON'
)

# operators and symbols

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_EQ         = r'\.EQ\.'
t_NE         = r'\.NE\.'
t_LT         = r'\.LT\.'
t_LE         = r'\.LE\.'
t_GT         = r'\.GT\.'
t_GE         = r'\.GE\.'
t_AND        = r'\.AND\.'
t_OR         = r'\.OR\.'
t_NOT        = r'\.NOT\.'
t_ASSIGN     = r'='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COMMA      = r','
t_SEMICOLON  = r';'


# keywords as functions 

def t_PROGRAM(t):    r'PROGRAM';    return t
def t_INTEGER(t):    r'INTEGER';    return t
def t_REAL(t):       r'REAL';       return t
def t_LOGICAL(t):    r'LOGICAL';    return t
def t_IF(t):         r'IF';         return t
def t_THEN(t):       r'THEN';       return t
def t_ELSE(t):       r'ELSE';       return t
def t_ENDIF(t):      r'ENDIF';      return t
def t_DO(t):         r'DO';         return t
def t_CONTINUE(t):   r'CONTINUE';   return t
def t_GOTO(t):       r'GOTO';       return t
def t_READ(t):       r'READ';       return t
def t_PRINT(t):      r'PRINT';      return t
def t_FUNCTION(t):   r'FUNCTION';   return t
def t_SUBROUTINE(t): r'SUBROUTINE'; return t
def t_RETURN(t):     r'RETURN';     return t
def t_END(t):        r'END';        return t
def t_BOOL(t): r'\.(TRUE|FALSE)\.'; return t

# strings
def t_STRING(t):
    r"'([^']|'')*'"    
    t.value = t.value[1:-1].replace("''", "'")
    return t


# identifiers
def t_ID(t):
    r'[A-Za-z]\w*'
    return t

# numbers
def t_FLOAT(t):
    r'(\d+\.\d*|\.\d+)([Ee][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# comments
def t_COMMENT(t):
    r'!.*'
    pass # ignore comments


# ignore whitespace and tab
t_ignore = ' \t'

# newline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# error
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

# build lexer
def build_lexer():
    return lex.lex()
