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

test_4 = """
PROGRAM SOMAARR
INTEGER NUMS(5)
INTEGER I, SOMA
SOMA = 0
PRINT *, 'Introduza 5 numeros inteiros:'
DO 30 I = 1, 5
READ *, NUMS(I)
SOMA = SOMA + NUMS(I)
30 CONTINUE
PRINT *, 'A soma dos numeros e: ', SOMA
END"""

test_3 = """
PROGRAM PRIMO
    INTEGER NUM, I
    LOGICAL ISPRIM
    PRINT *, 'Introduza um numero inteiro positivo:'
    READ *, NUM
    ISPRIM = .TRUE.
    I = 2
    20 IF (I .LE. (NUM/2) .AND. ISPRIM) THEN
    IF (MOD(NUM, I) .EQ. 0) THEN
    ISPRIM = .FALSE.
    ENDIF
    I = I + 1
    GOTO 20
    ENDIF
    IF (ISPRIM) THEN
    PRINT *, NUM, ' e um numero primo'
    ELSE
    PRINT *, NUM, ' nao e um numero primo'
    ENDIF
    END
"""

test_2 = """
PROGRAM FATORIAL
    INTEGER N, I, FAT
    PRINT *, 'Introduza um numero inteiro positivo:'
    READ *, N
    FAT = 1
    DO 10 I = 1, N
    FAT = FAT * I
    10 CONTINUE
    PRINT *, 'Fatorial de ', N, ': ', FAT
    END
"""

test_1 = """
PROGRAM HELLO
PRINT *, 'Ola, Mundo!'
END"""

lexer = build_lexer()
ast = parser.parse(test_test_1, lexer = lexer)

# semantic phase
sem = SemanticAnalyzer()
sem.visit(ast)

# codegen
codegen = CodeGenerator(sem.symtab)
vm_code = codegen.generate(ast)

print("\n".join(vm_code))