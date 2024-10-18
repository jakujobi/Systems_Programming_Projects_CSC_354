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

---
