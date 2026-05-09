from f77_lexer import build_lexer


def test_input(name, data):
    print(f"\n=== {name} ===")
    lexer = build_lexer()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type:10} | {repr(tok.value)}")


def main():

    # ----------------------------
    # 1. Basic program structure
    # ----------------------------
    test_input("Basic program", """
    PROGRAM T
    INTEGER X
    END
    """)

    # ----------------------------
    # 2. Identifiers and numbers
    # ----------------------------
    test_input("Identifiers and numbers", """
    X = 123
    Y = 3.14
    Z = .5
    """)

    # ----------------------------
    # 3. Logical constants
    # ----------------------------
    test_input("Logical constants", """
    .TRUE. .FALSE.
    """)

    # ----------------------------
    # 4. Logical operators
    # ----------------------------
    test_input("Logical operators", """
    .AND. .OR. .NOT.
    """)

    # ----------------------------
    # 5. Relational operators
    # ----------------------------
    test_input("Relational operators", """
    .EQ. .NE. .LT. .LE. .GT. .GE.
    """)

    # ----------------------------
    # 6. Arithmetic expression
    # ----------------------------
    test_input("Arithmetic expression", """
    X = 5 + 3 * 2
    """)

    # ----------------------------
    # 7. IF condition (critical test)
    # ----------------------------
    test_input("IF condition", """
    IF (X .AND. .TRUE.) THEN
    X = .FALSE.
    ENDIF
    """)

    # ----------------------------
    # 8. DO loop
    # ----------------------------
    test_input("DO loop", """
    DO 10 I = 1, 5
    10 CONTINUE
    """)

    # ----------------------------
    # 9. Strings
    # ----------------------------
    test_input("Strings", """
    PRINT *, 'Hello'
    PRINT *, 'It''s fine'
    """)

    # ----------------------------
    # 10. Comments
    # ----------------------------
    test_input("Comments", """
    X = 5 ! this is a comment
    """)


if __name__ == "__main__":
    main()