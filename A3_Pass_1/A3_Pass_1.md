# Assignment Requirements  
**Assignment 3 & 4 (Pass 1 & Pass 2) - Hamer - Fall 2024**  
- **Pass 1**: Due **Wednesday, October 30**  
- **Pass 2**: Due **Tuesday, December 4**  
---
## Assembly Features
The following is a list of assembler features that you are expected to implement for your assembler.
### Instruction Set
- All the SIC/XE instructions listed in the appendix.
### Instruction Formats
- Formats: 1, 2, 3, 4
### Addressing
- Simple (with or without indexing)
- Indirect
- Immediate
### Additional Features
- Literal operands (types X & C)
- Modules
- Comments
### Assembler Directives
- `START`, `END`, `BYTE`, `WORD`, `RESB`, `RESW`, `BASE`, `EQU`, `EXTDEF`, `EXTREF`
---
### Error Detection (15 bonus points for Pass 1 and 2)
You can assume that each source program is syntactically correct. If you wish to earn bonus points, perform error checking on the following:
1. **Illegal instruction** (Pass 1) – 2 points  
2. **Invalid symbol** (Pass 1) – 3 points  
3. **Undefined symbol** (Pass 2) – 3 points  
4. **Illegal addressing** (Pass 2) – 3 points  
5. **Address out of range** (Pass 2) – 4 points
---
## Input/Output Details
- A file `opcodes` will contain all the instructions available in the assembly language.  
	- Format: `MNEMONIC OPCODE FORMAT`  
	- Example: `LDA 00 3` (3 means format 3 or 4)
- Input to pass 1 will consist of a free format SIC/XE source program. Read the name of the file containing the source program from the command line. Input to pass 2 will be the intermediate file produced by pass1. Output from each pass of the assembler will consist of the following
### Pass 1  
- **Input**: A free-format SIC/XE source program (file name read from the command line).
	- Read the name of the file containing the source program from the command line
- **Output**:  
  1. Source listing with line numbers and LC values (for testing purposes, also write this to the screen).  
  2. Symbol table.  
  3. Literal table.
### Pass 2  
- **Input**: Intermediate file produced by Pass 1.  
- **Output**:  
  1. Assembly listing (including symbol table at the bottom) written to a file with a `.lst` extension (same name as source program).  
  2. Object program written to a file with a `.obj` extension (same name as source program).


- There should be line numbers on every line of the output

---
# Example Output and Input
The output from **Pass 1** of your assembler consists of three main parts:
1. **Source Listing with Line Numbers and Location Counter (LC) Values**
2. **Symbol Table**
3. **Literal Table**
## Example 1 - Gen from o1-preview
### Source Listing with Line Numbers and LC Values
Let's say the input assembly source program is as follows:
```assembly
START   1000
COPY    START   0
FIRST   LDA     #0
        STA     BUFFER,X
        BYTE    C'EOF'
        RESB    4096
BUFFER  RESW    10
        END     FIRST
```
The **Pass 1 output** would include:
#### Source Listing:
```assembly
1      1000   START   1000
2      1000   COPY    START   0
3      1000   FIRST   LDA     #0
4      1003           STA     BUFFER,X
5      1006           BYTE    C'EOF'
6      1007           RESB    4096
7      2007   BUFFER  RESW    10
8      2029           END     FIRST
```
- **Line Numbers**: For each source line.
- **LC Values**: Location Counter values next to each line. The LC starts at `1000` (as specified by `START 1000`).
- **Instructions and Directives**: As they appear in the source program, with their corresponding LC values.
---
### Symbol Table
The **Symbol Table** shows all the symbols (labels) and their addresses. After Pass 1, the symbols will have been assigned their respective LC values.
For the above program, the **Symbol Table** would look like:
```
Symbol     Address
---------------------
COPY       1000
FIRST      1000
BUFFER     2007
```
- **COPY**: Assigned the address `1000` (start of program).
- **FIRST**: Assigned the same address (`1000`) as it’s the first instruction.
- **BUFFER**: Defined after reserving bytes and words, its address is `2007`.
---
### Literal Table
The **Literal Table** stores literals used in the source code, which will be resolved and assigned addresses later. In the example, we have one literal.
For this program, the **Literal Table** might be:
```
Literal     Address     Length
---------------------------------
C'EOF'      1006        3
```
- **C'EOF'**: The character literal `EOF` is defined on line 5, with a length of 3 bytes (1 byte per character) and is assigned LC value `1006`.
---
### Explanation of the Components:
1. **Source Listing**:
   - This lists the lines of the source code along with the corresponding location counters (LC values). These LC values represent where each instruction or directive will be placed in memory.
2. **Symbol Table**: The symbol table contains the addresses of labels (symbols) defined in the program. These symbols are used by the assembler in Pass 2 to resolve addresses for instructions like `STA BUFFER,X`.
3. **Literal Table**:
   - The literal table stores values like `C'EOF'` that are used directly in the code. In Pass 1, you gather these literals and determine their memory placement, which will be used in Pass 2.

---
# Example
Source listing
```assembly
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

```


## Pass1 Output
```assembly
1       000000          START      0           
2       000000          LDA        #1000       
3       000003          +LDA       #30000      
4       000007          +STA       RESULT      
5       00000B          ADD        VALUE       
6       00000E          +ADD       =X'0F1E2D3C'
7       000012          +SUB       @ADDRESS    
8       000016          AND        NUM,X       
9       000019          +OR        =C'HELLO'   
10      00001D          LDCH       BUF,X       
11      000020          +STCH      BUF,X       
12      000024          LDB        =X'FF'      
13      000027          +LDX       VALUE       
14      00002B          LDT        =X'ABCDE'   
15      00002E          LDF        FLVAL       
16      000031          LDL        +LABEL      
17      000035          COMP       #2000       
18      000038          +JEQ       NEXT        
19      00003C          JGT        END         
20      00003F          +JLT       LOOP        
21      000043          +JSUB      SUBRTN      
22      000047          RSUB                   
23      00004A          ADDR       A, B        
24      00004C          SUBR       T, S        
25      00004E          MULR       X, L        
26      000050          DIVR       F, A        
27      000052          SHIFTL     T, 4        
28      000054          SHIFTR     S, 2        
29      000056          RMO        A, L        
30      000058          CLEAR      X           
31      00005A          TIXR       S           
32      00005C          HIO                    
33      00005D          SIO                    
34      00005E          TIO                    
35      00005F          FIX                    
36      000060          FLOAT                  
37      000061          NORM                   
38      000062          +TD        DEVADDR     
39      000066          +RD        DEVADDR     
40      00006A          +WD        DEVADDR     
41      00006E          LPS        +PROGADDR   
42      000072          SVC        3           
43      000074          STA        MEM         
44      000077          +STB       BASE        
45      00007B          STL        LENGTH      
46      00007E          STX        +INDEX      
47      000082          +STT       TIMER       
48      000086          +STF       FLVAL       
49      00008A          +STI       MEM         
50      00008E          +STSW      SW          
51      000092          STCH       CHAR        
52      000095          +SSK       SECVAL      
53      000099          BASE       LDBASE      
54      00009B  NEXT    +TIX       INDEX       
55      00009F          +J         LOOP        
56      0000A3  LOOP    LDCH       BUF         
57      0000A6          ADD        ONE         
58      0000A9          +JLT       NEXT        
59      0000AD          RSUB                   
60      0000B0  VALUE   WORD       2000        
61      0000B3  ADDRESS WORD       5000        
62      0000B6  FLVAL   RESW       1           
63      0000B9  DEVADDR RESB       1           
64      0000BA  MEM     RESW       10          
65      0000C4  BUF     RESB       256         
66      0001C4  CHAR    RESB       1           
67      0001C5  SECVAL  RESB       1           
68      0001C6  TIMER   WORD       0           
69      0001C9  BASE    WORD       0           
70      0001CC  INDEX   WORD       0           
71      0001CF  ONE     WORD       1           
72      0001D2  LABEL   WORD       6000        
73      0001D5  SUBRTN  LDA        #3000       
74      0001D8          COMP       #4000       
75      0001DB          +JLT       RET         
76      0001DF          ADD        VALUE       
77      0001E2          +STCH      BUF         
78      0001E6  RET     RSUB                   
79      0001E9  RESULT  RESW       1           
80      0001EC  PROGADDRWORD       0           
81      0001EF  SW      WORD       0           
82      0001F2  END     START                  

```
---

### **Design Plan for Pass 1 of the Assembler Project**

The goal of **Pass 1** in an assembler is to scan through the assembly source code, generate symbol and literal tables, and assign memory addresses using a **Location Counter (LOCCTR)**. Here's how we can design a Python program to achieve this:

---

### **1. Overview of Pass 1**

Pass 1 performs the following major tasks:

1. **Initialize the LOCCTR**: Set the starting address from the **START** directive or **0** by default.
2. **Parse Each Line of Assembly Code**: Extract labels, opcodes, operands, and other details.
3. **Build Symbol Table**: Add labels to the symbol table with their respective addresses.
4. **Manage the Literal Table**: Store literals found in the source and assign addresses later.
5. **Update the LOCCTR**: Increment the LOCCTR based on the instruction size.
6. **Generate Intermediate File**: Output an intermediate representation to use in **Pass 2**.

---

### **2. Core Classes and Modules**

#### **2.1. AssemblyInstruction**

- **Purpose**: Represents a single line of assembly code.
- **Attributes**:
  - `line_number`: The line number in the source file.
  - `address`: The memory address assigned to the instruction (set by LOCCTR).
  - `label`: The label of the instruction, if present.
  - `opcode`: The operation code or assembler directive.
  - `operands`: The operands of the instruction.
  - `object_code`: The object code generated (if any).
  - `comment`: Any comment on the line.
- **Methods**:
  - `is_comment()`: Checks if the line is a comment.
  - `has_label()`: Checks if a label exists.
  - `__str__()`: Provides a string representation for debugging.

#### **2.2. SymbolTable**

- **Purpose**: Stores labels and their corresponding memory addresses.
- **Attributes**:
  - `symbols`: A dictionary with labels as keys and addresses as values.
- **Methods**:
  - `add_label(label, address)`: Adds a label with its address to the table. Logs errors for duplicates.
  - `get_address(label)`: Retrieves the address for a given label.
  - `display()`: Displays the symbol table.

#### **2.3. LiteralTable**

- **Purpose**: Manages the storage and address assignment of literals.
- **Attributes**:
  - `literals`: A dictionary with literal names as keys and details (e.g., value, length, address) as values.
- **Methods**:
  - `add_literal(literal, value, length)`: Adds a literal to the table.
  - `assign_addresses(start_address)`: Assigns addresses to literals starting from `start_address`.
  - `display()`: Displays the literal table.

#### **2.4. LOCCTR (Location Counter)**

- **Purpose**: Manages memory address assignments during Pass 1.
- **Attributes**:
  - `current_address`: Tracks the current memory address.
- **Methods**:
  - `initialize(start_address)`: Sets the starting address.
  - `increment(bytes)`: Increments the LOCCTR by a given number of bytes.
  - `get_current_address()`: Returns the current value of the LOCCTR.

#### **2.5. Parser**

- **Purpose**: Parses each line of the source file into components.
- **Methods**:
  - `parse_line(line)`: Splits a line into label, opcode, operands, and comments.
  - `handle_directives(opcode, operands)`: Processes assembler directives like **START**, **END**, **BYTE**, **WORD**, etc.
  - `identify_literals(operands)`: Extracts literals from operands for insertion into the literal table.

#### **2.6. IntermediateFileGenerator**

- **Purpose**: Generates an intermediate file for Pass 2.
- **Methods**:
  - `write_line(line)`: Writes a formatted line to the intermediate file.
  - `close_file()`: Closes the file after writing all lines.

#### **2.7. ErrorHandler**

- **Purpose**: Handles and logs errors and warnings during Pass 1.
- **Methods**:
  - `log_error(message)`: Logs an error message.
  - `log_warning(message)`: Logs a warning message.
  - `display_errors()`: Displays all errors and warnings.

---

### **3. Workflow for Pass 1**

#### **3.1. Initialize Components**

- **Symbol Table**, **Literal Table**, **LOCCTR**, **ErrorHandler**, and **IntermediateFileGenerator** are initialized.
- Set the LOCCTR to `0` or the address specified by the **START** directive.

#### **3.2. Read Source File Line by Line**

1. **Open the Source File** and read each line.
2. **Skip Comments**: If the line starts with a comment character (e.g., `.`), skip further processing.
3. **Parse Line**: Use the `Parser` class to extract components like label, opcode, operands, and comments.

#### **3.3. Handle Labels**

- If a label exists:
  - **Check for Duplicates**: If already in the symbol table, log an error.
  - **Add to Symbol Table**: Add the label with the current value of the LOCCTR.

#### **3.4. Handle Opcodes and Directives**

1. **Directives**:
   - **START**: Initialize the LOCCTR.
   - **END**: Mark the end of the source file. Handle any unprocessed literals.
   - **BYTE/WORD/RESW/RESB**: Adjust the LOCCTR based on the directive type and size.
   - **EQU**: Handle label-value assignment based on expressions.
2. **Opcodes**:
   - Calculate instruction size based on the opcode.
   - Increment the LOCCTR based on the calculated size.

#### **3.5. Handle Literals**

- **Identify Literals**: For operands starting with `=`, add to the literal table.
- **Assign Addresses to Literals**: At the end of Pass 1, assign addresses to literals starting from the next available memory address.

#### **3.6. Update LOCCTR**

- **Calculate Instruction Size**: Use the opcode and operands to determine the instruction size.
- **Increment LOCCTR**: Adjust the LOCCTR accordingly.

#### **3.7. Generate Intermediate File**

- Write each parsed line and associated information to the intermediate file.
- Include addresses, labels, opcodes, operands, and any other details needed for Pass 2.

#### 3.8. Error Handling

- If any errors are detected (e.g., duplicate labels, invalid opcodes), log them using the `ErrorHandler`.
- Display all errors and warnings at the end of Pass 1.

---

### **4. Detailed Interaction Between Classes**

#### 4.1. Main Driver (Pass1Driver)
- **Purpose**: Orchestrates the workflow for Pass 1.
- **Process**:
  1. **Initialize Components**: Creates instances of symbol table, literal table, etc.
  2. **Read Source File**: Iterates through each line.
  3. **Parse Line**: Calls `Parser` to extract components.
  4. **Handle Labels/Opcodes/Directives**:
     - Add labels to the symbol table.
     - Handle opcodes and adjust the LOCCTR.
     - Process assembler directives.
  5. **Handle Literals**: Adds literals to the literal table and assigns addresses.
  6. **Write Intermediate File**: Outputs a line-by-line intermediate representation.
  7. **Log and Display Errors**: Calls `ErrorHandler` to log and display errors.

#### 4.2. Interaction Flow
1. **Pass1Driver** reads a line from the source file.
2. Calls **Parser.parse_line()** to extract components.
3. If there's a label, calls **SymbolTable.add_label()**.
4. For opcodes and directives, updates the **LOCCTR**.
5. For literals, calls **LiteralTable.add_literal()**.
6. Writes the intermediate line using **IntermediateFileGenerator.write_line()**.
7. Logs any errors using **ErrorHandler.log_error()**.

---
### 5. Example Design Diagram
```
+--------------------+
|   Pass1Driver      | <-----------------+----------------+
|--------------------|                   |                |
| + initialize()     |                   |                |
| + run_pass1()      |                   |                |
| + parse_line()     |                   |                |
| + handle_label()   |                   |                |
| + handle_opcode()  |                   |                |
+--------------------+                   |                |
        |                                |                |
        |                                |                |
        v                                v                v
+--------------------+          +----------------+   +-----------------+
|  SymbolTable       |          |   Parser       |   |   ErrorHandler  |
|--------------------|          |----------------|   |-----------------|
| + add_label()      |          | + parse_line() |   | + log_error()   |
| + get_address()    |          | + parse_opcode()|  | + display()     |
+--------------------+          +----------------+   +-----------------+
        ^                                |
        |                                |
        v                                |
+--------------------+                   v
|   LOCCTR           |           +----------------------+
|--------------------|           | LiteralTable         |
| + initialize()     |           |----------------------|
| + increment()      |           | + add_literal()      |


| + get_address()    |           | + assign_addresses() |
+--------------------+           +----------------------+
```

---

### **6. Summary of Design**

- **Modular Structure**: Clearly defined classes for different parts of Pass 1.
- **Separation of Concerns**: Each class handles a specific aspect of the assembler, improving maintainability.
- **Error Handling**: Centralized error logging for easy debugging.
- **Intermediate File**: Proper intermediate file generation for seamless transition to Pass 2.

This design provides a robust structure to handle the requirements of **Pass 1** efficiently and lays the foundation for **Pass 2**. Let me know if you have any questions or need adjustments!