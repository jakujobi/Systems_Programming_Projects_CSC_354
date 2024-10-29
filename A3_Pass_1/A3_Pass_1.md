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
# Example 2
Source listing
```assembly
        START   0
        LDA     #1000           ; Immediate addressing, Format 3
        +LDA    #30000          ; Immediate addressing, Format 4
        +STA    RESULT          ; Store using Format 4
        ADD     VALUE           ; Direct addressing, Format 3
        +ADD    =0x0F1E2D3C     ; Literal in Format 4
        +SUB    @ADDRESS        ; Indirect addressing, Format 4
        AND     NUM,X           ; Indexed addressing, Format 3
        +OR     =0cHELLO        ; Character literal, Format 4
        LDCH    BUF,X           ; Load character, Indexed addressing, Format 3
        +STCH   BUF,X           ; Store character, Indexed addressing, Format 4

        LDB     =0xFF           ; Load base register, Format 3
        +LDX    VALUE           ; Load index register, Format 4
        LDT     =0xABCDE        ; Load T register, Format 3
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

        +LPS     PROGADDR       ; Load processor status, Format 4
        SVC     3               ; Supervisor call, Format 2

        STA     MEM             ; Store accumulator, Format 3
        +STB    BASE            ; Store base register, Format 4
        STL     LENGTH          ; Store L register, Format 3
        +STX     INDEX          ; Store index register, Format 4
        +STT    TIMER           ; Store T register, Format 4
        +STF    FLVAL           ; Store floating-point register, Format 4
        +STI    MEM             ; Store immediate value to memory, Format 4
        +STSW   SW              ; Store status word, Format 4
        STCH    CHAR            ; Store character, Format 3
        +SSK    SECVAL          ; Store storage key, Format 4

        BASE    LDBASE          ; Set base register

NEXT:   +TIX    INDEX           ; Increment index, Format 4
        +J      LOOP            ; Unconditional jump, Format 4

LOOP:   LDCH    BUF             ; Load character, Format 3
        ADD     ONE             ; Add a word value, Format 3
        +JLT    NEXT            ; Jump if less than, Format 4
        RSUB                    ; Return, Format 3

VALUE:  WORD    2000            ; Define a word constant
ADDRESS: WORD    5000            ; Define a word constant
FLVAL:  RESW    1               ; Reserve one word for floating-point value
DEVADDR: RESB    1               ; Reserve one byte for device address
MEM:    RESW    10              ; Reserve memory
BUF:    RESB    256             ; Reserve a buffer of 256 bytes
CHAR:   RESB    1               ; Reserve a byte for character storage
SECVAL: RESB    1               ; Reserve a byte for security key storage

TIMER:  WORD    0               ; Define a timer word
BASE:   WORD    0               ; Define a base register word
INDEX:  WORD    0               ; Define an index register word
ONE:    WORD    1               ; Define a word constant
LABEL:  WORD    6000            ; Define a word constant

SUBRTN: LDA     #3000           ; Load immediate, Format 3
        COMP    #4000           ; Compare immediate, Format 3
        +JLT    RET             ; Jump if less than, Format 4
        ADD     VALUE           ; Add value, Format 3
        +STCH   BUF             ; Store character, Format 4

RET:    RSUB                    ; Return, Format 3

RESULT: RESW    1               ; Reserve memory for result
PROGADDR: WORD   0               ; Define program address
SW:     WORD    0               ; Define status word

END:    START                   ; End of the program

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

# Core Classes and Modules

## `SourceCodeLine`
Here are the list of directives
directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'EQU', 'ORG', 'EXTDEF', 'EXTREF']
### Properties & Attributes
The `SourceCodeLine` should have attributes that cover all possible aspects of an assembly line. The goal is to have a comprehensive representation that can be easily manipulated by the assembler.
#### Core Attributes
- **`line_number`** (`int`):
    - The line number in the source file.
    - Useful for error reporting and debugging.
- **`address`** (`int` or `None`):
    - The memory address assigned to the instruction (set during pass 1).
    - Can be `None` if not yet assigned.
- **`label`** (`str` or `None`):
    - The label associated with the instruction, if present.
    - Labels are typically used for jumps, data definitions, etc.
- **`opcode`** (`str` or `None`):
    - The operation code or assembler directive (e.g., `LDA`, `START`, `BYTE`).
    - This distinguishes between instructions and directives.
- **`instr_format`** (`int` or `None`):
    - Represents the format of the instruction (e.g., 1, 2, 3, 4).
    - Helps in calculating instruction length and object code generation.
- **`operands`** (`list` of `str`):
    - The operands associated with the instruction (e.g., `#LENGTH`, `BUFFER,X`).
    - This should be a list to support instructions with multiple operands.
- **`object_code`** (`str` or `None`):
    - The final object code generated for this line.
    - Will be set in pass 2 of the assembler.
- **`comment`** (`str`):
    - Stores any comment associated with the line.
    - Useful for preserving comments when generating listings.
- **`is_comment`** (`bool`):
    - Indicates whether the entire line is a comment.
- **`errors`** (`list` of `str`):
    - A list of error messages associated with this line.
    - Enables error tracking and reporting.
- **`line_text`** (`str`):
    - The original line text as read from the source file.
    - Useful for reconstructing listings and for debugging.
#### Derived Attributes
These attributes are derived from the core attributes and can be helpful for quick access and identification.
- **`instruction_length`** (`int`):
    - The calculated length of the instruction based on its format.
    - Helps in location counter (LOCCTR) updates during pass 1.
- **`is_directive`** (`bool`):
    - Indicates if the line contains an assembler directive (e.g., `START`, `END`, `BYTE`).
- **`is_instruction`** (`bool`):
    - Indicates if the line contains an actual machine instruction mnemonic.
- **`is_extended_format`** (`bool`):
    - Indicates if the instruction is in extended format (format 4), usually prefixed with `+`.
- **`operand_count`** (`int`):
    - Number of operands present in the line.
    - Useful for validation and error handling.
- **`is_indexed_addressing`** (`bool`):
    - Indicates if the addressing mode is indexed (e.g., `BUFFER,X`).
### 2. Methods
#### Basic Methods
- **`__init__()`**:
    - Initializes the object with the necessary attributes.
- **`__str__()`**:
    - Provides a detailed string representation of the line for debugging or output.
#### Validation & Error Management Methods
- **`add_error(error_message)`**:
    - Adds an error message to the list of errors for the line.
- **`has_errors()`**:
    - Returns `True` if there are errors associated with this line, otherwise `False`.
#### Line Attribute Checkers
- **`has_label()`**:
    - Returns `True` if a label is present.
- **`is_directive()`**:
    - Returns `True` if the opcode is an assembler directive.
- **`is_instruction()`**:
    - Returns `True` if the opcode is a machine instruction.
- **`is_extended_format()`**:
    - Returns `True` if the instruction is in extended format.
- **`is_indexed_addressing()`**:
    - Returns `True` if the addressing mode is indexed.
#### Derived Attribute Methods
- **`calculate_instruction_length()`**:
    - Calculates the instruction length based on the format and sets the `instruction_length` attribute.
- **`get_operand_count()`**:
    - Returns the number of operands present.
#### Utility Methods
- **`clear_errors()`**:
    - Clears all stored errors for the line.
- **`set_operands(operands)`**:
    - Allows for setting the operands dynamically.
- **`set_address(address)`**:
    - Sets the address of the line and ensures it’s valid.
- **`update_object_code(code)`**:
    - Updates the object code for the line.
## `OpcodeHandler`
The `OpcodeHandler` class is responsible for loading, managing, and interacting with opcodes in an assembler. It provides methods for retrieving opcode details, validating opcodes, and printing the opcode table.
### 1. Purpose
The `OpcodeHandler` class serves to:
- Load opcodes from an external file.
- Store opcode details like mnemonic, hexadecimal code, and format.
- Provide methods to access, validate, and interact with opcodes.
- Integrate error logging and file management through helper classes (`ErrorLogHandler` and `FileExplorer`).
### Attributes
- **`opcodes`** (`dict`): 
  - Stores opcodes with their details, where the keys are opcode mnemonics and values are dictionaries containing format and hex information.
  - Example: `{'ADD': {'format': 3, 'hex': 0x18}}`.
  - This is the central data structure for managing opcode information.
- **`file_explorer`** (`FileExplorer`): 
  - An instance of `FileExplorer` that handles file operations.
  - Used to read the opcodes from a specified file.
- **`logger`** (`ErrorLogHandler`): 
  - An instance of `ErrorLogHandler` to log errors and actions.
  - Used to log loading, retrieval, and validation of opcodes.
- **`file_path`** (`str`): 
  - Stores the path to the opcode file to be loaded.
  - Defaults to `'opcodes.txt'` but can be customized.
### Methods
#### Initialization & Loading
- **`__init__(file_path='opcodes.txt', logger=None)`**:
  - Initializes the class attributes.
  - Creates instances of `FileExplorer` and `ErrorLogHandler` if not provided.
  - Calls `_load_opcodes()` to load the opcode file.
- **`_load_opcodes()`**:
  - Private method that reads the opcode file using `FileExplorer`.
  - Parses each line to extract mnemonic, hex code, and format.
  - Logs actions and errors using `ErrorLogHandler`.
#### Opcode Management
- **`get_opcode(name)`**:
  - Retrieves the opcode information for the specified mnemonic.
  - Raises a `ValueError` if the opcode is not found and logs the error.
- **`get_format(name)`**:
  - Returns the format of the specified opcode.
  - Internally calls `get_opcode(name)` to fetch the format.
- **`get_hex(name)`**:
  - Returns the hexadecimal value of the specified opcode.
  - Internally calls `get_opcode(name)` to fetch the hex code.
- **`is_opcode(name)`**:
  - Checks if the specified mnemonic exists in the opcode dictionary.
  - Returns `True` if it exists, otherwise `False`.
  - Allows for quick validation of opcode presence without full retrieval.
#### Utility Methods
- **`print_opcodes()`**:
  - Prints all loaded opcodes in a tabular format.
  - Displays mnemonic, hex code, and format for each opcode.
  - Helps in debugging and verification.
#### Error Handling & Logging
- The class uses `ErrorLogHandler` to manage error logging throughout the process.
- Errors are logged when:
  - The file cannot be found or read.
  - The opcode format or hex code is invalid.
  - A mnemonic is not found during retrieval.
- Actions are also logged, such as successful loading and retrieval of opcodes.
### How It Works
1. **Initialization**:
   - When an instance of `OpcodeHandler` is created, it initializes attributes and calls `_load_opcodes()` to populate the opcode dictionary.
2. **Loading Opcodes**:
   - The `_load_opcodes()` method reads the specified opcode file using `FileExplorer`.
   - Each line is parsed to extract the mnemonic, hex code, and format.
   - If parsing succeeds, the opcode is added to the dictionary; otherwise, an error is logged.
3. **Retrieving Opcode Information**:
   - The `get_opcode()`, `get_format()`, and `get_hex()` methods allow for fetching specific details about an opcode.
   - If the mnemonic is not found, the method raises a `ValueError` and logs an error.
4. **Printing Opcodes**:
   - The `print_opcodes()` method outputs all loaded opcodes in a human-readable format, useful for debugging or verification.


## `ParsingHandler`
The **ParsingHandler** is responsible for parsing a line of assembly code into its individual components, such as label, opcode, operands, and comments. The goal is to convert the raw line of code into a structured format, specifically updating a given `SourceCodeLine` instance.
### Core Attributes
- **`source_line`** (`SourceCodeLine`):
  - The `SourceCodeLine` instance to be updated with the parsed components of the line.
- **`line_text`** (`str`):
  - The raw line of assembly code that needs to be parsed.
- **`regex_pattern`** (`str`):
  - A regex pattern used for parsing the line into label, opcode, operands, and comments.
### Regex Pattern
The regex pattern is designed to parse labels, opcodes, operands, and comments efficiently:
```regex
^(\w+)?\s*(\+?[A-Z]+)?\s*(.*?)(\s*\.\s*.*)?$
```
- **Explanation**:
  - `^(\w+)?`: Matches a label, which is any word character (letters, digits, or underscores), at the start of the line.
  - `\s*`: Matches any whitespace that separates components.
  - `(\+?[A-Z]+)?`: Matches the opcode, which can be prefixed with a `+` for extended format and contains uppercase letters.
  - `\s*`: Matches whitespace between components.
  - `(.*?)`: Matches the operands, which can be anything between the opcode and comment.
  - `(\s*\.\s*.*)?$`: Matches comments, which start with the comment symbol (`.`) and include any following characters.
### Methods
#### Initialization & Setup
- **`__init__(self, source_line, line_text)`**:
  - Initializes the ParsingHandler with a `SourceCodeLine` instance and a line of assembly code.
  - Sets up the regex pattern for parsing.
  - Attributes:
    - `source_line`: An instance of `SourceCodeLine` to store parsed results.
    - `line_text`: The raw line of code to parse.
#### Parsing Methods
- **`parse_line(self)`**:
	- Main method to parse the line into components: label, opcode, operands, and comments.
	- Uses the regex pattern to break down the line into these components and updates the `SourceCodeLine` instance.
	- Handles empty lines and comment-only lines appropriately.
	- If the line contains only a comment, sets `is_comment` to `True` in `SourceCodeLine`.
- **`extract_label(self, match)`**:
	- Extracts the label from the regex match and updates the `label` attribute of `SourceCodeLine`.
- **`extract_opcode(self, match)`**:
	- Extracts the opcode from the regex match and updates the `opcode` attribute of `SourceCodeLine`.
- **`extract_operands(self, match)`**:
	- Extracts the operands from the regex match, splits them if needed, and updates the `operands` list in `SourceCodeLine`.
- **`extract_comment(self, match)`**:
	- Extracts the comment from the regex match and updates the `comment` attribute of `SourceCodeLine`.
- **`handle_empty_line(self)`**:
	- Handles lines that are empty or contain only whitespace. Sets the `is_comment` attribute to `True`.
- **`handle_comment_line(self)`**:
	- Handles lines that are comment-only and sets `is_comment` to `True` in `SourceCodeLine`.
#### Utility Methods
- **`reset_source_line(self)`**:
  - Clears the attributes of `SourceCodeLine` before parsing a new line.
  - Ensures that previous data doesn’t interfere with the new parsing process.
#### Testing Method
- **`test(cls)`**:
	- A class method to test various parsing scenarios for `ParsingHandler`.
	- It will create instances of `SourceCodeLine` and use different lines of assembly code as input.
	- It will cover the following scenarios:
		1. **Parsing a line with a label, opcode, and operands**.
		2. **Parsing a line with only a label**.
		3. **Parsing a line with only an opcode**.
		4. **Parsing a line with an opcode and operands**.
		5. **Parsing a comment-only line**.
		6. **Parsing an empty line**.
		7. **Parsing a line with an extended format opcode** (e.g., `+LDA`).
		8. **Parsing a line with indexed addressing** (e.g., `BUFFER,X`).
		9. **Parsing a line with indirect addressing** (e.g., `@BUFFER`).
		10. **Parsing a line with immediate addressing** (e.g., `#BUFFER`).
  - The method should print results for each test, indicating whether the parsing was successful and how the `SourceCodeLine` attributes were updated.
### Example of How Parsing Works
#### Input
```assembly
LOOP:   LDA   BUFFER,X   . Load A register with BUFFER indexed
```
#### Parsing Breakdown
- **Label**: `LOOP`
- **Opcode**: `LDA`
- **Operands**: `BUFFER,X`
- **Comment**: `. Load A register with BUFFER indexed`
#### Updated `SourceCodeLine`
- `label`: `LOOP`
- `opcode`: `LDA`
- `operands`: `['BUFFER,X']`
- `comment`: `. Load A register with BUFFER indexed`
### Class Summary
The **ParsingHandler** will focus solely on parsing. It breaks down the line and updates the attributes of the provided `SourceCodeLine` instance. It is not responsible for validation; the `LineValidator` will handle any validation checks.

## `SourceProcessor`

## `LocationCounter`

## `LineValidator`

## `AssemblerPass1` (Driver Class)

---
# Existing Classes
## `SymbolTable`
## `LiteralTable`
## `FileExplorer`
## `ErrorLogHandler`


---

## 3. Workflow for Pass 1

### 3.1. Initialize Components
- **Symbol Table**, **Literal Table**, **LOCCTR**, **ErrorHandler**, and **IntermediateFileGenerator** are initialized.
- Set the LOCCTR to `0` or the address specified by the **START** directive.
### 3.2. Read Source File Line by Line
1. **Open the Source File** and read each line.
2. **Skip Comments**: If the line starts with a comment character (e.g., `.`), skip further processing.
3. **Parse Line**: Use the `Parser` class to extract components like label, opcode, operands, and comments.
### 3.3. Handle Labels
- If a label exists:
  - **Check for Duplicates**: If already in the symbol table, log an error.
  - **Add to Symbol Table**: Add the label with the current value of the LOCCTR.
### 3.4. Handle Opcodes and Directives
1. **Directives**:
   - **START**: Initialize the LOCCTR.
   - **END**: Mark the end of the source file. Handle any unprocessed literals.
   - **BYTE/WORD/RESW/RESB**: Adjust the LOCCTR based on the directive type and size.
   - **EQU**: Handle label-value assignment based on expressions.
2. **Opcodes**:
   - Calculate instruction size based on the opcode.
   - Increment the LOCCTR based on the calculated size.
### 3.5. Handle Literals
- **Identify Literals**: For operands starting with `=`, add to the literal table.
- **Assign Addresses to Literals**: At the end of Pass 1, assign addresses to literals starting from the next available memory address.
### 3.6. Update LOCCTR
- **Calculate Instruction Size**: Use the opcode and operands to determine the instruction size.
- **Increment LOCCTR**: Adjust the LOCCTR accordingly.
### 3.7. Generate Intermediate File
- Write each parsed line and associated information to the intermediate file.
- Include addresses, labels, opcodes, operands, and any other details needed for Pass 2.
### 3.8. Error Handling
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

----
# Questions and info
Make the assembler directories to be in the program. Can be a class
- What characters should not be allowed at all in the line
- What if the file is empty
- Can a line only have a label?
	- Can a line only have a label and an opcode?
- Check if the line starts with END
- Try spli
