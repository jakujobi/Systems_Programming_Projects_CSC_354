```asm
1          00000     PROG:       START      1000    
2          003E8     FIRST:      STL        ReTADR    first comment    
3          003EB                 LDB        #LENGTH    
4          003EE     [ERROR: Invalid opcode mnemonic: 'BASE'. ]                BASE       LENGTH    
5          003EE                 LDA        DATA,X    
6          003F1                 COMP       LENGTH    
7          003F4                 +JEQ       END    
8          003F8     LOOP:       ADDR       A, B    
9          003FA                 SUBR       X,L    
10         003FC                 MULR       S, T    
11         003FE                 DIVR       SW, PC    
12         00400                 AND        DATA    
13         00403                 OR         COUNT    
14         00406                 SHIFTL     Y, 4    
15         00408                 SHIFTR     F, P    bad    
16         0040A                 TIXR       T    
17         0040C                 CLEAR      X    
18         0040E                 JSUB       PRINT    
19         00411                 LDT        @#DATA,X    
20         00414                 LDX        @#DATA    
21         00417     [ERROR: 'IDKWHATIMDOINGONTHISLINESPACE' length exceeds 10 characters.]    idkwhatimdoingonthislinespace:            
22         00417     [ERROR: 'IKCWHATIMDOINGONTHISLINE' length exceeds 10 characters.]    ikcwhatimdoingonthisline:            
23         00417                 +LDCH      CHARZ,X    
24         0041B                 +STCH      @CHARZ    
25         0041F     HERE:       +LDF       #FLOATZ    
26         00423                 +STF       @#FLOATZ    
27         00427                 +STCH      @CHARZ,X    
28         0042B                 +LDF       #FLOATZ,X    
29         0042F                 +STF       @#FLOATZ,X    
30         00433                 MULF       COUNT    random comment    
31         00436                 ADDF       RETADR    
32         00439                 ADD        #2    
33         0043C                 DIV        3    
34         0043F                 MUL        #5-4    
35         00442                 SUB        HERE-LOOP    
36         00445                 LDA        ALPHA+LOOP    
37         00448                 SUBF       =0x45    
38         0044B                 DIVF       =0cdw    
39         0044E                 SUBF       0xf3    
40         00451                 DIVF       =0xCs    
41         00454                 COMPF      DATa    
42         00457                 EXTREF     GOTEM    
43         00457                 J          GOTEM    
44         0045A                 JLT        LOOP    
45         0045D                 JGT        LOOP    
46         00460                 +TD        DEVICE    
47         00464                 RD         DEVICE    tabs here    
48         00467                 +WD        DEVICE    
49         0046B                 FIX        
50         0046C                 FLOAT      
51         0046D                 HIO        
52         0046E                 STB        #FOUR    
53         00471                 STI        @FOUR    
54         00474                 STS        #@FOUR    
55         00477                 STT        #ONE,X    
56         0047A                 STX        @ONE,X    
57         0047D                 NORM       
58         0047E                 RMO        B    
59         00480                 SVC        #HERE    
60         00482                 SIO        
61         00483     [ERROR: Invalid expression for EQU directive: 'HERE']    EQUAL:      EQU        HERE    
62         00483     ALPHA:      EQU        #1000    
63         00483     [ERROR: Invalid expression for EQU directive: 'ALPHA']    BETA:       EQU        ALPHA    
64         00483                 ADD        ALPHA-@BETA    
65         00486                 ADD        ALPHA+#BETA    
66         00489                 ADD        @EQUAL+HERE    
67         0048C                 ADD        #EQUAL-HERE    
68         0048F                 ADD        ALPHA-HERE,X    
69         00492                 ADD        HERE-ALPHA,X    
70         00495                 ADD        ALPHA+HERE    
71         00498                 ADD        HERE+ALPHA    
72         0049B                 ADD        16+HERE    
73         0049E                 ADD        HERE+#16    
74         004A1                 ADD        #HERE+ALPHA    
75         004A4                 TIO        
76         004A5                 SVC        @ALPHA    
77         004A7                 LPS        BREAK    
78         004AA                 SSK        DEVICE    
79         004AD                 COMPR      A, 5    bad    
80         004AF                 TIX        COUNT    
81         004B2                 CLEAR      S    
82         004B4                 RSUB       
83         004B7                 LDA        WHAT    
84         004BA     [ERROR: Invalid opcode mnemonic: 'BAD'. ]                BAD        #3    
85         004BA                 STSW       FOUR    
86         004BD     PRINT:      LDS        LENGTH    
87         004C0                 STA        RETADR    
88         004C3                 LDL        CHARZ    
89         004C6                 RSUB       
90         004C9                            
91         004C9                            . ha BLANK    
92         004C9     DATA:       BYTE       0Xf1    
93         004CA     DATA:       BYTE       0XF1    
94         004CB     DATA:       BYTE       =0XF1    
95         004CB     DA_2:       BYTE       0XF11    
96         004CB     DAT3:       BYTE       0XG1    
97         004CC     DAT4:       BYTE       X'G1'    
98         004CC     [ERROR: '!BAD' must start with a letter.; Label '!BAD' contains invalid character '!'. ]    !BAD:       BYTE       d    
99         004CC     [ERROR: '1BAD' must start with a letter.]    1BAD:       BYTE       =    
100        004CC     [ERROR: '_GOOD' must start with a letter.]    _GOOD:      BYTE       1    
101        004CC     t123456789: BYTE       1    
102        004CC     [ERROR: 'T1234567890' length exceeds 10 characters.]    t1234567890: BYTE       1    
103        004CC     GOO:        BYTE       1    
104        004CC     BA3D:       BYTE       #1    
105        004CC     [ERROR: Label 'BA#D' contains invalid character '#'. ]    BA#D:       BYTE       1    
106        004CC     Z:          BYTE       20    
107        004CC     CHARZ:      BYTE       0CA    
108        004CC     FLOATZ:     BYTE       0C'\"1    dD    
109        004CF     FOUR:       RESB       #4    
110        004D3     HABR:       RESW       637    should make anything past use B reg    
111        00C4A     COUNT:      WORD       #1    
112        00C4D     LENGTH:     WORD       4096    
113        00C50                 WORD       COUNT    
114        00C53                 WORD       COUNT-HABR    
115        00C56     ONE:        RESB       1    
116        00C57     RETaDR:     RESW       #1    
117        00C5A     FIVE:       RESW       #3    partial line comment - ignore (actual tabs here)    
118        00C63     BREAK:      RESB       1911    should make anything past use format 4    
119        013DA     DEVICE:     BYTE       0X'\"F8'    
120        013DD                 RESB       DATA    
121        013DD                 RESB       HERE-ALPHA    
122        013DD                 RESB       ALpHA-7777    
123        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA-BETA']    ZA:         EQU        ALPHA-BETA    
124        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA+BETA']    ZB:         EQU        ALPHA+BETA    
125        013DD     [ERROR: Invalid expression for EQU directive: 'EQUAL+HERE']    ZC:         EQU        EQUAL+HERE    
126        013DD     [ERROR: Invalid expression for EQU directive: 'eQUAL-HERE']    ZD:         EQU        eQUAL-HERE    
127        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA-HERE']    ZE:         EQU        ALPHA-HERE    
128        013DD     [ERROR: Invalid expression for EQU directive: 'HERE-ALPHA']    ZF:         EQU        HERE-ALPHA    
129        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA+HERE']    ZG:         EQU        ALPHA+HERE    
130        013DD     [ERROR: Invalid expression for EQU directive: 'HERE+ALPHA']    ZH:         EQU        HERE+ALPHA    
131        013DD     [ERROR: Invalid expression for EQU directive: '16+HERE']    ZI:         EQU        16+HERE    
132        013DD     [ERROR: Invalid expression for EQU directive: 'HERE+#16']    ZJ:         EQU        HERE+#16    
133        013DD     [ERROR: Invalid expression for EQU directive: '#HERE+ALPHA']    ZK:         EQU        #HERE+ALPHA    
134        013DD     [ERROR: Invalid expression for EQU directive: '']    ZL:         EQU        
135        013DD     [ERROR: Invalid expression for EQU directive: 'heir']    TEST:       EQU        heir    
136        013DD     T2:         EQU        *    
137        013DD     [ERROR: Invalid expression for EQU directive: 'HERE!']                EQU        HERE!    
138        013DD     [ERROR: Invalid expression for EQU directive: '#HERE']                EQU        #HERE    
139        013DD     [ERROR: Invalid expression for EQU directive: '=0CABC']    ZZ:         EQU        =0CABC    
140        013DD                 EXTDEF     ZA, ZB,DEVICE, ZD,ZE,ZF,AH,Zz    
141        013DD                 EXTDEF     ZG    
142        013DD                 EXTREF     OTRFUN,AAA ,AAB    
143        013DD                 WORD       DEVICE-AAA    
144        013E0                 WORD       AAA-AAB    
145        013E3                 JSUB       PRINT    
146        013E6                 JSUB       TEST    
147        013E9                 JSUB       OTRFUN    
148        013EC                 +JSUB      OTRFUN    
149        013F0                 LDA        OTRFUN    
150        013F3                 +LDA       TEST    
151        013F7                 LDA        =0x45    
152        013FA                 LDA        =0Cdw    
153        013FD                 END        PROG    


===SYM_START===

______________________________________________
Symbol Table:
______________________________________________
Symbol     Value      RFlag  IFlag  MFlag 
______________________________________________
ALPH       00483      1      1      1     
BA3D       004CC      1      1      0     
BETA       00483      1      1      0     
BREA       00C63      1      1      0     
CHAR       004CC      1      1      0     
COUN       00C4A      1      1      0     
DAT3       004CB      1      1      0     
DAT4       004CC      1      1      0     
DATA       004C9      1      1      1     
DA_2       004CB      1      1      0     
DEVI       013DA      1      1      0     
EQUA       00483      1      1      0     
FIRS       003E8      1      1      0     
FIVE       00C5A      1      1      0     
FLOA       004CC      1      1      0     
FOUR       004CF      1      1      0     
GOO        004CC      1      1      0     
HABR       004D3      1      1      0     
HERE       0041F      1      1      0     
LENG       00C4D      1      1      0     
LOOP       003F8      1      1      0     
ONE        00C56      1      1      0     
PRIN       004BD      1      1      0     
PROG       003E8      1      1      0     
RETA       00C57      1      1      0     
T123       004CC      1      1      0     
T2         013DD      1      1      1     
TEST       013DD      1      1      0     
Z          004CC      1      1      0     
ZA         013DD      1      1      0     
ZB         013DD      1      1      0     
ZC         013DD      1      1      0     
ZD         013DD      1      1      0     
ZE         013DD      1      1      0     
ZF         013DD      1      1      0     
ZG         013DD      1      1      0     
ZH         013DD      1      1      0     
ZI         013DD      1      1      0     
ZJ         013DD      1      1      0     
ZK         013DD      1      1      0     
ZL         013DD      1      1      0     
ZZ         013DD      1      1      0     
______________________________________________

===SYM_END===


===LIT_START===
Literal Table:
Literal    Value      Length Address 
=0x45      45         1      None    
=0cdw      6477       2      None    
=0XF1      F1         1      None    
=0CABC     414243     3      None    
===LIT_END===


===PROG_LEN_START===
Program Length (DEC): 4117
Program Length (HEX): 01015

===PROG_LEN_END===

```