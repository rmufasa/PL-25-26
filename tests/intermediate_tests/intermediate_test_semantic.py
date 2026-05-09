from f77_parser import parser
from f77_lexer import build_lexer
from SemanticAnalyzer import SemanticAnalyzer


def run_test(name, program, should_pass=True):
    print(f"\n=== {name} ===")
    try:
        lexer = build_lexer()
        ast = parser.parse(program, lexer=lexer)
        sem = SemanticAnalyzer()
        sem.visit(ast)

        if should_pass:
            print("PASS")
        else:
            print("FAILED (should have errored but didn't)")

    except Exception as e:
        if should_pass:
            print("FAILED with error:", e)
        else:
            print("Expected error:", e)


def main():

    # ----------------------------
    # 1. Declaration tests
    # ----------------------------
    run_test("Valid declaration", """
    PROGRAM T
    INTEGER X
    X = 5
    END
    """, True)

    run_test("Duplicate declaration", """
    PROGRAM T
    INTEGER X
    INTEGER X
    END
    """, False)

    run_test("Duplicate var different type", """
    PROGRAM T
    INTEGER X
    REAL X
    END
    """, False)

    run_test("Array vs scalar conflict", """
    PROGRAM T
    INTEGER A
    INTEGER A(5)
    END
    """, False)


    # ----------------------------
    # 2. Undeclared / misuse
    # ----------------------------
    run_test("Undeclared variable", """
    PROGRAM T
    X = 5
    END
    """, False)

    run_test("Array used as scalar", """
    PROGRAM T
    INTEGER A(5)
    A = 10
    END
    """, False)

    run_test("Scalar used as array", """
    PROGRAM T
    INTEGER A
    A(1) = 10
    END
    """, False)


    # ----------------------------
    # 3. Assignment tests
    # ----------------------------
    run_test("Valid assignment", """
    PROGRAM T
    INTEGER X
    X = 5
    END
    """, True)

    run_test("Type mismatch assignment", """
    PROGRAM T
    INTEGER X
    X = .TRUE.
    END
    """, False)

    run_test("Array element assignment valid", """
    PROGRAM T
    INTEGER A(5)
    A(1) = 10
    END
    """, True)

    run_test("Array element type mismatch", """
    PROGRAM T
    INTEGER A(5)
    A(1) = .TRUE.
    END
    """, False)


    # ----------------------------
    # 4. Expression tests
    # ----------------------------
    run_test("Invalid arithmetic", """
    PROGRAM T
    INTEGER X
    X = 5 + .TRUE.
    END
    """, False)

    run_test("Unary minus valid", """
    PROGRAM T
    INTEGER X
    X = -5
    END
    """, True)

    run_test("Unary minus invalid", """
    PROGRAM T
    INTEGER X
    X = - .TRUE.
    END
    """, False)


    # ----------------------------
    # 5. Logical expressions
    # ----------------------------

    run_test("Nested logical expression", """
    PROGRAM T
    LOGICAL X
    X = .TRUE. .AND. .FALSE. .OR. .TRUE.
    END
    """, True)

    run_test("Mixed logic arithmetic", """
    PROGRAM T
    LOGICAL X
    X = (.TRUE. + 5)
    END
    """, False)


    # ----------------------------
    # 6. Relational expressions
    # ----------------------------
    run_test("Invalid comparison", """
    PROGRAM T
    LOGICAL X
    X = 5 .EQ. .TRUE.
    END
    """, False)


    # ----------------------------
    # 7. IF tests
    # ----------------------------
    run_test("IF with non-logical condition", """
    PROGRAM T
    INTEGER X
    X = 5
    IF (X) THEN
    X = 10
    ENDIF
    END
    """, False)

    run_test("Valid IF", """
    PROGRAM T
    LOGICAL X
    X = .TRUE.
    IF (X) THEN
    X = .FALSE.
    ENDIF
    END
    """, True)

    run_test("Nested IF", """
    PROGRAM T
    LOGICAL X
    X = .TRUE.
    IF (X) THEN
        IF (X) THEN
            X = .FALSE.
        ENDIF
    ENDIF
    END
    """, True)


    # ----------------------------
    # 8. DO loop tests
    # ----------------------------
    run_test("DO with non-integer variable", """
    PROGRAM T
    REAL I
    DO 10 I = 1, 5
    10 CONTINUE
    END
    """, False)

    run_test("DO label mismatch", """
    PROGRAM T
    INTEGER I
    DO 10 I = 1, 5
    20 CONTINUE
    END
    """, False)

    run_test("Valid DO", """
    PROGRAM T
    INTEGER I
    DO 10 I = 1, 5
    10 CONTINUE
    END
    """, True)

    run_test("DO non-numeric bounds", """
    PROGRAM T
    INTEGER I
    LOGICAL X
    X = .TRUE.
    DO 10 I = X, 5
    10 CONTINUE
    END
    """, False)


    # ----------------------------
    # 9. READ tests
    # ----------------------------
    run_test("READ undeclared", """
    PROGRAM T
    READ *, X
    END
    """, False)

    run_test("Valid READ", """
    PROGRAM T
    INTEGER X
    READ *, X
    END
    """, True)

    run_test("READ multiple vars valid", """
    PROGRAM T
    INTEGER X
    REAL Y
    READ *, X, Y
    END
    """, True)


    # ----------------------------
    # 10. GOTO tests
    # ----------------------------
    run_test("Valid GOTO", """
    PROGRAM T
10 CONTINUE
    GOTO 10
    END
    """, True)

    run_test("Invalid GOTO", """
    PROGRAM T
    GOTO 99
    END
    """, False)


    # ----------------------------
    # 11. Full integration stress test
    # ----------------------------
    run_test("Full mini program", """
    PROGRAM T
    INTEGER I
    REAL A(5)
    LOGICAL FLAG

    FLAG = .TRUE.

    DO 10 I = 1, 5
        A(I) = I * 2
10 CONTINUE

    IF (FLAG .AND. .TRUE.) THEN
        A(1) = 10
    ENDIF

    END
    """, True)


if __name__ == "__main__":
    main()