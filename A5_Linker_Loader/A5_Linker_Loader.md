# Assignment #5 Questions
**Due:**  
- **12-13-24 by 1:00 pm** for full credit  
- **12-20-24 by 1:00 pm** for one week grace period  
**Assignments will not be accepted after 12/20!**
---
For this assignment, you are to write a linker/loader for the object programs produced by your assembler using the format described in the textbook. Write the linker/loader as a separate program. **Do not include it as a separate part of the assembler.** This is to be a stand-alone program.
### Input
Input to the linker/loader will be a variable list of object program names.  
If my executable program were named `linkghh`, I would type the following on the command line:  

```
linkghh prog1.obj prog2.obj prog3.obj
```
This would link `prog1`, `prog2`, and `prog3` together. You must read the names of the object programs from the command line to receive full credit.
### Output
Output will be the absolute machine code that would be in memory following the loading and linking process. Assume a **load address of 03300** (a 5-digit hexadecimal value). Output is to be written to a file named `MEMORY.DAT` and displayed on the monitor in a format similar to the following:

```
      0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F  
03300 XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX  
03310 XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX  
03320 XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX
```
Execution begins at address **XXXXXX**.

---
### Additional Notes
- Each `XX` pair is replaced by 1 byte of object code produced by the linker/loader.  
- Signify unknown memory locations by **question marks (`??`)**. This is needed when storage is reserved but not initialized (e.g., `RESW 1` would produce 3 question mark pairs).  
- You may assume that the output file will have at most 50 lines.  
- Display the output file to the monitor in a neat and readable format.
---
# Algorithms

## Pass 1: Algorithm for a Linking Loader

```pascal
begin
  get PROGADDR from operating system
  set CSADDR to PROGADDR {for the first control section}
  
  while not end of input do
    begin
      read next input record {Header record for control section}
      set CSLTH to control section length
      search ESTAB for control section name
      
      if found then
        set error flag {duplicate external symbol}
      else
        enter control section name into ESTAB with value CSADDR

      while record type ≠ 'E' do
        begin
          read next input record
          
          if record type = 'D' then
            for each symbol in the record do
              begin
                search ESTAB for symbol name
                
                if found then
                  set error flag {duplicate external symbol}
                else
                  enter symbol into ESTAB with value (CSADDR + indicated address)
              end {for each symbol}
        end {while record type ≠ 'E'}
        
      add CSLTH to CSADDR {starting address for the next control section}
    end {while not EOF}
end {Pass 1}
````

---
## Pass 2: Algorithm for a Linking Loader

```pascal
begin
  set CSADDR to PROGADDR
  set EXECADDR to PROGADDR
  
  while not end of input do
    begin
      read next input record {Header record}
      set CSLTH to control section length
      
      while record type ≠ 'E' do
        begin
          read next input record
          
          if record type = 'T' then
            begin
              {If object code is in character form, convert it into internal representation}
              move object code from record to location (CSADDR + specified address)
            end {if 'T'}
          else if record type = 'M' then
            begin
              search ESTAB for modifying symbol name
              
              if found then
                add or subtract symbol value at location (CSADDR + specified address)
              else
                set error flag {undefined external symbol}
            end {if 'M'}
        end {while record type ≠ 'E'}
      
      if an address is specified (in the End record) then
        set EXECADDR to (CSADDR + specified address)
      
      add CSLTH to CSADDR
    end {while not EOF}
  
  jump to location given by EXECADDR {to start execution of the loaded program}
end {Pass 2}
```

---
### Explanation of Key Components:
1. **Pass 1**:
    - Reads the object program headers and defines symbols in the External Symbol Table (ESTAB).
    - Calculates the starting address for each control section.
    - Handles duplicate symbol definitions by setting error flags.
2. **Pass 2**:
    - Resolves addresses using ESTAB and processes Text (`T`) and Modification (`M`) records.
    - Updates the memory image with absolute machine code.
    - Handles execution starting address specified in the End (`E`) record.
---
# Classes
## 1. RecordParser
2. 

linker_loader/
├── main.py                # Entry point (handles command-line args, orchestrates passes)
├── pass_one.py            # Contains Pass 1 logic
├── pass_two.py            # Contains Pass 2 logic
├── record_parser.py       # Helper utilities to parse H, D, T, M, E records
├── symbol_table.py        # Manages the ESTAB (External Symbol Table)
├── memory_manager.py      # Handles representation and manipulation of memory
└── utils.py               # Miscellaneous helper functions