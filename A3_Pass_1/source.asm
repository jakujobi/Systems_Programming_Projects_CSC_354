PROG:   START  1000
FIRST:  STL    ReTADR        .first comment
        LdB    #LENGTH
        BaSE   LENGTH
        lDA    DATA,X
        COMp   LENGTH
        +JEQ   END
LOOP:   ADDR   A, B
        SUBR   X,L
        MULR   S, T
        DIVR   SW, PC
        AND    DATA
        OR     COUNT
        SHIFTL B, 4
        SHIFTR F, P .bad
        TIXR   T
        CLEAR  X
        JSUB   PRINT
        LDT    @#DATA,X
        LDX    @#DATA
idkwhatimdoingonthislinespace: 
ikcwhatimdoingonthisline:
        +LDCH  CHARZ,X
        +STCH  @CHARZ
HERE:   +LDF   #FLOATZ
        +STF   @#FLOATZ
        +STCH  @CHARZ,X
        +LDF   #FLOATZ,X
        +STF   @#FLOATZ,X
        MULF   COUNT .random comment
        ADDF   RETADR
        ADD    #2
        DIV    3
        MUL    #5
        SUB    4
        SUBF   =0x45
        DIVF   =0cdw
        COMPF  DATa
        J      LOOP
        JLT    LOOP
        JGT    LOOP
        +TD    DEVICE
        RD     DEVICE      .tabs here
        +WD    DEVICE
        FIX
        FLOAT
        HIO
        STB    #FOUR
        STI    @FOUR
        STS    #@FOUR
        STT    #ONE,X
        STX    @ONE,X
        NORM
        SVC    1
        SVC    #HERE
        SIO
EQUAL:  EQU    HERE
ALPHA:  EQU    #1000
BETA:   EQU    ALPHA
        ADD    ALPHA-@BETA
        ADD    ALPHA+#BETA
        ADD    @EQUAL+HERE
        ADD    #EQUAL-HERE
        ADD    ALPHA-HERE,X
        ADD    HERE-ALPHA,X
        ADD    ALPHA+HERE
        ADD    HERE+ALPHA
        ADD    16+HERE
        ADD    HERE+#16
        ADD    #HERE+ALPHA
        TIO
        RMO    B
        LPS    BREAK
        SSK    DEVICE
        COMPR  A, 5 .bad
        TIX    COUNT
        CLEAR  S
        RSUB
        LDA    WHAT
        BAD    #3
        STSW   FOUR
PRINT:  LDS    LENGTH
        STA    RETADR
        LDL    CHARZ
        RSUB

DATA:   BYTE   =0Xf1
DATA:   BYTE   =0XF1
DA_2:   BYTE   =0XF11
DAT3:   BYTE   =0XG1
DAT4:   BYTE   =X'G1'
!BAD:   BYTE   d
1BAD:   BYTE   =
_GOOD:  BYTE   1
t123456789: BYTE 1
t1234567890: BYTE 1
GOO:    BYTE   1
BA3D:   BYTE   #1
BA#D:   BYTE   1
Z:      BYTE   20
CHARZ:  BYTE   =0CA
FLOATZ: BYTE   =0C'\"1.dD
FOUR:   RESB   #4
HABR:   RESW   637     .should make anything past use B reg
COUNT:  WORD   #1
LENGTH: WORD   4096
ONE:    RESB   1
RETaDR: RESW   #1
BREAK:  RESb   1911     .should make anything past use format 4
DEVICE: BYTE   =0X'\"F8'
        RESB   DATA
        RESB   HERE-ALPHA
        RESB   ALpHA-7777
ZA:     EQU    ALPHA-BETA
ZB:     EQU    ALPHA+BETA
ZC:     EQU    EQUAL+HERE
ZD:     EQU    eQUAL-HERE
ZE:     EQU    ALPHA-HERE
ZF:     EQU    HERE-ALPHA
ZG:     EQU    ALPHA+HERE
ZH:     EQU    HERE+ALPHA
ZI:     EQU    16+HERE
ZJ:     EQU    HERE+#16
ZK:     EQU    #HERE+ALPHA
ZL:     EQU
        EQU    heir
        EQU    HERE!
        EQU    #HERE
        EXTDEF ENDFUN
        EXTREF OTRFUN
        END    FIRST
