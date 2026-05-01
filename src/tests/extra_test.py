from f77_parser import parser
from f77_lexer import build_lexer
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator



test_test_1 = """
PROGRAM TESTFLOW
INTEGER X

X = 1

10 IF (X .LE. 10) THEN

    IF (X .GT. 8) THEN
        PRINT *, X, ' is BIG'
    ELSE
        IF (X .EQ. 3 .OR. X .EQ. 7) THEN
            PRINT *, X, ' is SPECIAL'
        ELSE
            PRINT *, X, ' is NORMAL'
        ENDIF
    ENDIF

    X = X + 1
    GOTO 10

ENDIF

PRINT *, 'DONE'
END
"""

test_test_2 = """
PROGRAM BOOL_EXPR
LOGICAL A, B

A = .TRUE.
B = .FALSE.

IF (A .AND. B) THEN
    PRINT *, 'AND WRONG'
ELSE
    PRINT *, 'AND OK'
ENDIF

IF (A .OR. B) THEN
    PRINT *, 'OR OK'
ELSE
    PRINT *, 'OR WRONG'
ENDIF
END
"""

test_test_3 = """
PROGRAM REL_TEST
INTEGER A, B

A = 5
B = 5

IF (A .EQ. B) THEN PRINT *, 'EQ OK' ENDIF
IF (A .LE. B) THEN PRINT *, 'LE OK' ENDIF
IF (A .GE. B) THEN PRINT *, 'GE OK' ENDIF
IF (A .LT. B) THEN PRINT *, 'LT FAIL' ENDIF
IF (A .GT. B) THEN PRINT *, 'GT FAIL' ENDIF
END
"""

test_test_4 = """
PROGRAM LOOP_BOOL
INTEGER I
LOGICAL FLAG

I = 1
FLAG = .TRUE.

10 IF (I .LE. 5 .AND. FLAG) THEN
    PRINT *, I

    IF (I .EQ. 3) THEN
        FLAG = .FALSE.
    ENDIF

    I = I + 1
    GOTO 10
ENDIF

PRINT *, 'DONE'
END
"""

test_test_5 = """
PROGRAM FULLTEST
INTEGER I, J, S, A(5)
LOGICAL OK

PRINT *, 'START'

S = 0
OK = .TRUE.

READ *, J

DO 10 I = 1, 5
    A(I) = I * J
    S = S + A(I)
10 CONTINUE

PRINT *, 'SUM = ', S

IF (S .GT. 50 .AND. OK) THEN
    PRINT *, 'BIG SUM'
ELSE
    PRINT *, 'SMALL SUM'
ENDIF

IF (.NOT. OK .OR. S .EQ. 0) THEN
    PRINT *, 'INVALID STATE'
ELSE
    PRINT *, 'STATE OK'
ENDIF

I = 1

20 IF (I .LE. 5) THEN

    IF (A(I) .EQ. J .OR. A(I) .GT. 10) THEN
        PRINT *, I, 'SPECIAL'
    ELSE
        PRINT *, I, 'NORMAL'
    ENDIF

    IF (I .EQ. 3) THEN
        OK = .FALSE.
    ENDIF

    I = I + 1
    GOTO 20

ENDIF

IF (OK) THEN
    PRINT *, 'FINISHED CLEAN'
ELSE
    PRINT *, 'FINISHED DIRTY'
ENDIF

END
"""


test_test_6 = """
PROGRAM TESTNEW
INTEGER I, N
LOGICAL OK

OK = .TRUE.
N = 3

DO 10 I = 1, 5

    IF (.NOT. OK .OR. I .EQ. N) THEN
        PRINT *, I
    ENDIF

    IF (I .GT. 3) THEN
        OK = .FALSE.
    ENDIF

10 CONTINUE

END
"""



# expected outputs (in VM)
# test_test_1
"""
1 is NORMAL
2 is NORMAL
3 is SPECIAL
4 is NORMAL
5 is NORMAL
6 is NORMAL
7 is SPECIAL
8 is NORMAL
9 is BIG
10 is BIG
DONE
"""

# test_test_2
"""
AND OK
OR OK
"""

# test_test_3
"""
EQ OK
LE OK
GE OK
"""

# test_test_4
"""
1
2
3
DONE
"""

# test_test_5 (input: 10)
"""
START
SUM = 150
BIG SUM
STATE OK
1 NORMAL
2 NORMAL
3 SPECIAL
4 SPECIAL
5 SPECIAL
FINISHED DIRTY
"""

# test_test_6
"""
3
5
"""

lexer = build_lexer()
ast = parser.parse(test_test_6, lexer = lexer)

# semantic phase
sem = SemanticAnalyzer()
sem.visit(ast)

# codegen
codegen = CodeGenerator(sem.symtab)
vm_code = codegen.generate(ast)

print("\n".join(vm_code))