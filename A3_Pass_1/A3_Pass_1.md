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
### Final Info
In **Pass 1**, you don't generate object code; instead, you focus on gathering necessary information (LC values, symbols, literals) for **Pass 2**, which will generate the final assembly listing and object code.

---
## Example 2