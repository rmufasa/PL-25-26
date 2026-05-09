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