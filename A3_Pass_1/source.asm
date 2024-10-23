        START   0
        LDA     #1000           ; Immediate addressing, Format 3
        +LDA    #30000          ; Immediate addressing, Format 4
        +STA    RESULT          ; Store using Format 4
        ADD     VALUE           ; Direct addressing, Format 3
        +ADD    =X'0F1E2D3C'    ; Literal in Format 4
        +SUB    @ADDRESS        ; Indirect addressing, Format 4
        AND     NUM,X           ; Indexed addressing, Format 3
        +OR     =C'HELLO'       ; Character literal, Format 4
        LDCH    BUF,X           ; Load character, Indexed addressing, Format 3
        +STCH   BUF,X           ; Store character, Indexed addressing, Format 4

        LDB     =X'FF'          ; Load base register, Format 3
        +LDX    VALUE           ; Load index register, Format 4
        LDT     =X'ABCDE'       ; Load T register, Format 3
        LDF     FLVAL           ; Load floating-point register, Format 3
        LDL     +LABEL          ; Load to register L, Format 4

        COMP    #2000           ; Compare immediate, Format 3
        +JEQ    NEXT            ; Jump if equal, Format 4
        JGT     END             ; Jump if greater than, Format 3
        JLT     +LOOP           ; Jump if less than, Format 4

        +JSUB   SUBRTN          ; Jump to subroutine, Format 4
        RSUB                    ; Return from subroutine, Format 3

        ADDR    A, B            ; Add registers, Format 2
        SUBR    T, S            ; Subtract registers, Format 2
        MULR    X, L            ; Multiply registers, Format 2
        DIVR    F, A            ; Divide registers, Format 2

        SHIFTL  T, 4            ; Shift T left 4 times, Format 2
        SHIFTR  S, 2            ; Shift S right 2 times, Format 2
        RMO     A, L            ; Copy contents of register A to register L, Format 2
        CLEAR   X               ; Clear register X, Format 2

        TIXR    S               ; Increment index register, Format 2

        HIO                     ; Halt I/O channel, Format 1
        SIO                     ; Start I/O operation, Format 1
        TIO                     ; Test I/O operation, Format 1

        FIX                     ; Convert float to integer, Format 1
        FLOAT                   ; Convert integer to float, Format 1
        NORM                    ; Normalize floating-point value, Format 1

        +TD     DEVADDR         ; Test device address, Format 4
        +RD     DEVADDR         ; Read device, Format 4
        +WD     DEVADDR         ; Write device, Format 4

        LPS     +PROGADDR       ; Load processor status, Format 4
        SVC     3               ; Supervisor call, Format 2

        STA     MEM             ; Store accumulator, Format 3
        +STB    BASE            ; Store base register, Format 4
        STL     LENGTH          ; Store L register, Format 3
        STX     +INDEX          ; Store index register, Format 4
        +STT    TIMER           ; Store T register, Format 4
        +STF    FLVAL           ; Store floating-point register, Format 4
        +STI    MEM             ; Store immediate value to memory, Format 4
        +STSW   SW              ; Store status word, Format 4
        STCH    CHAR            ; Store character, Format 3
        +SSK    SECVAL          ; Store storage key, Format 4

        BASE    LDBASE          ; Set base register

NEXT    +TIX    INDEX           ; Increment index, Format 4
        +J      LOOP            ; Unconditional jump, Format 4

LOOP    LDCH    BUF             ; Load character, Format 3
        ADD     ONE             ; Add a word value, Format 3
        +JLT    NEXT            ; Jump if less than, Format 4
        RSUB                    ; Return, Format 3

VALUE   WORD    2000            ; Define a word constant
ADDRESS WORD    5000            ; Define a word constant
FLVAL   RESW    1               ; Reserve one word for floating-point value
DEVADDR RESB    1               ; Reserve one byte for device address
MEM     RESW    10              ; Reserve memory
BUF     RESB    256             ; Reserve a buffer of 256 bytes
CHAR    RESB    1               ; Reserve a byte for character storage
SECVAL  RESB    1               ; Reserve a byte for security key storage

TIMER   WORD    0               ; Define a timer word
BASE    WORD    0               ; Define a base register word
INDEX   WORD    0               ; Define an index register word
ONE     WORD    1               ; Define a word constant
LABEL   WORD    6000            ; Define a word constant

SUBRTN  LDA     #3000           ; Load immediate, Format 3
        COMP    #4000           ; Compare immediate, Format 3
        +JLT    RET             ; Jump if less than, Format 4
        ADD     VALUE           ; Add value, Format 3
        +STCH   BUF             ; Store character, Format 4

RET     RSUB                    ; Return, Format 3

RESULT  RESW    1               ; Reserve memory for result
PROGADDR WORD   0               ; Define program address
SW      WORD    0               ; Define status word

END     START                   ; End of the program