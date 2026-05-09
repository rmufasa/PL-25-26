from f77_parser import parser
from f77_lexer import build_lexer


def run_test(name, program, should_pass=True):
    print(f"\n=== {name} ===")
    try:
        lexer = build_lexer()
        ast = parser.parse(program, lexer = lexer)

        if not should_pass:
            print("FAILED (should have errored but didn't)")
        else:
            print("PASS")

    except SyntaxError as e:
        if should_pass:
            print("FAILED with syntax error:", e)
        else:
            print("Expected error:", e)

    except Exception as e:
        if should_pass:
            print("FAILED with error:", e)
        else:
            print("Expected error:", e)


def main():

    # ----------------------------
    # 1. Minimal program
    # ----------------------------
    run_test("Minimal program", """
    PROGRAM T
    END
    """, True)

    # ----------------------------
    # 2. Declaration + assignment
    # ----------------------------
    run_test("Declaration and assignment", """
    PROGRAM T
    INTEGER X
    X = 5
    END
    """, True)

    # ----------------------------
    # 3. Arithmetic expression
    # ----------------------------
    run_test("Arithmetic expression", """
    PROGRAM T
    INTEGER X
    X = 5 + 3 * 2
    END
    """, True)

    # ----------------------------
    # 4. IF statement
    # ----------------------------
    run_test("Simple IF", """
    PROGRAM T
    LOGICAL X
    X = .TRUE.
    IF (X) THEN
    X = .FALSE.
    ENDIF
    END
    """, True)

    # ----------------------------
    # 5. IF with logical ops
    # ----------------------------
    run_test("IF with AND/OR", """
    PROGRAM T
    LOGICAL X
    X = .TRUE.
    IF (X .AND. .FALSE. .OR. .TRUE.) THEN
    X = .FALSE.
    ENDIF
    END
    """, True)

    # ----------------------------
    # 6. DO loop
    # ----------------------------
    run_test("DO loop", """
    PROGRAM T
    INTEGER I
    DO 10 I = 1, 5
    10 CONTINUE
    END
    """, True)

    # ----------------------------
    # 7. PRINT
    # ----------------------------
    run_test("PRINT", """
    PROGRAM T
    INTEGER X
    X = 5
    PRINT *, X
    END
    """, True)

    # ----------------------------
    # 8. READ
    # ----------------------------
    run_test("READ", """
    PROGRAM T
    INTEGER X
    READ *, X
    END
    """, True)

    # ----------------------------
    # 9. Syntax error (missing ENDIF)
    # ----------------------------
    run_test("Missing ENDIF", """
    PROGRAM T
    LOGICAL X
    IF (X) THEN
    X = .TRUE.
    END
    """, False)

    # ----------------------------
    # 10. Invalid expression
    # ----------------------------
    run_test("Bad expression", """
    PROGRAM T
    INTEGER X
    X = + 5
    END
    """, False)


if __name__ == "__main__":
    main()