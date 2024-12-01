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
### Pass 2  
- **Input**: Intermediate file produced by Pass 1.  
- **Output**:  
  1. Assembly listing (including symbol table at the bottom) written to a file with a `.lst` extension (same name as source program).  
  2. Object program written to a file with a `.obj` extension (same name as source program).


- There should be line numbers on every line of the output
---
## Notes

In the records list, sort them by type 
- Header records
- Text Records
- Modification Records
- End Records
---
![](A4_Pass_2%20-%20Assember%20Design.png)


---
# Overview of Pass 2

**Pass 2** of the assembler uses the intermediate file from Pass 1, symbol and literal tables, and opcode information to generate the final object program. The main tasks include:

1. **Reading the Intermediate File**: Parsing instructions and associated data.
2. **Generating Object Code**: Translating instructions into machine code, resolving symbols and literals.
3. **Handling Records**: Creating header, text, modification, and end records.
4. **Error Checking**: Detecting and reporting errors such as undefined symbols, illegal addressing modes, and address out of range.
5. **Writing the Object Program**: Assembling all records into the final output.

---

# Detailed Class Designs and Responsibilities
## 1. IntermediateFileReader
### Responsibilities:
- **Parse Intermediate File**: Read and parse the intermediate file into structured data.
- **Provide Access**: Allow iteration over parsed lines for processing.
### Attributes:
- `file_name`: The name of the intermediate file.
- `parsed_lines`: A list of `SourceCodeLine` objects representing each line.
### Methods:
- `__init__(self, file_name)`: Initializes the reader and parses the file.
- `parse_line(self, line)`: Parses a single line into components.
- `__iter__(self)`: Returns an iterator over `parsed_lines`.

**Implementation Details**:
- **Parsing Logic**: Use consistent parsing rules matching how the intermediate file was written in Pass 1.
- **SourceCodeLine**: A data structure holding line number, address, label, opcode, operands, and any comments or errors.
---
### Types of lines
#### Empty Line
- Check if it is empty
- Discard or ignore
#### Source Code Line

#### Error Source Code Line
#### Title Lines
- Check if it starts with a `===`
#### Divider Line
- Check if it has more than three `_`s like `___`
- Discard or ignore
#### Symbol Table Section
- Starts by having a `===SYM_START===`
	- Sends us to process the Symbol Table
- Ends with a `===SYM_END===`
	- Stops parsing symbol table

#### Symbol Table Line

#### Literal Table Section
- Starts with a `===LIT_START===`
	- Starts parsing literal table
- Ends with a `===LIT_END===`
	- Stops parsing literal table
#### Program Length Line
- Starts with a `===PROG_LEN_START===`
- Ends with a `===PROG_LEN_END===`
---
### Pass2Parser
- Strip the line into parts
- Check if empty or if Divider Line
	- Then ignore or discard
- Check if it is a Divider line
	- Ignore and discard
- Check if it is a code line
	- Send to `parse_p2_code_lines`
- Check if it starts with a `===`
	- Check if it starts with `===SYM_START===`
		- Send to `parse_p2_symbol_lines`
	- Check if it starts with a `===LIT_START===`
		- Send to `parse_p2_literal_lines`
	- Check if it starts with a `===PROG_LEN_START===`
		- Send to `parse_p2_program_length_lines`
- Else
	- Give error
### `parse_p2_code_line`
- split
- if 3rd part is `p2_is_Error_Line`
	- ignore and discard
- 1st part is line number
- 2nd part is Line address
- if 3rd part ends with `:`
	- then it is a label
	- if 4th part
		- it is an opcode
		- if 5th part
			- it is an operand
- else 3rd part is a opcode
	- if 4th part
		- it is an operand

### `parse_p2_code_lines`


### `p2_is_Error_Line`
if is starts or has `[ERROR` on the 3rd part
- return true

### `parse_p2_symbol_lines`
While the line =! `===SYM_END===`
- split line
- 1st part as Symbol
- 2nd part as Value
- 3rd part as RFlag
- 4th part as I Flag
- 4th part as MFlag
### `parse_p2_literal_lines`
While the line =! `===LIT_END===`
- split the line
- Assign first part as the literal
- 2nd part as Value
- 3rd part as Length
- 4th part as Address
### `parse_p2_program_length_lines`
While the line =! `===PROG_LEN_END===`
- Split the line
- If the first part == `Program Length (DEC): `
	- Take the second part as the program length in decimal
- If the first part == `Program Length (HEX):`
	- Take the second part as the program length in hex
---
## 2. ObjectCodeGenerator
**Responsibilities**:
- **Generate Object Code**: Translate each instruction into machine code.
- **Resolve Symbols and Literals**: Use symbol and literal tables to resolve addresses.
- **Handle Instruction Formats and Addressing Modes**: Support various instruction formats and addressing modes.
- **Error Checking**: Detect and report undefined symbols, illegal addressing modes, and address out of range errors.
**Attributes**:
- `symbol_table`: Reference to the symbol table.
- `literal_table`: Reference to the literal table.
- `opcode_handler`: Provides opcode information.
- `error_handler`: Logs errors encountered during code generation.
**Methods**:
- `__init__(self, symbol_table, literal_table, opcode_handler, error_handler)`
- `generate_object_code(self, source_line)`: Main method to generate object code for a line.
- `resolve_operand(self, operand, current_address)`: Resolves an operand, returning its value and relocation info.
- `handle_format_n(self, source_line, opcode_info)`: Generates object code based on instruction format.
- `check_address_range(self, target_address, format_type, current_address)`: Checks if the target address is within the allowable range for the format.
- `detect_illegal_addressing(self, source_line)`: Detects illegal addressing modes and logs errors.
**Implementation Details**:
- **Instruction Formats**:
    - **Format 1**: 1-byte instructions.
    - **Format 2**: 2-byte instructions with registers.
    - **Format 3**: 3-byte instructions with 12-bit displacement.
    - **Format 4**: 4-byte instructions with 20-bit address.
- **Addressing Modes**:
    - **Immediate** (`#`), **Indirect** (`@`), **Simple** (no prefix), **Indexed** (`,X`), **Extended** (`+`).
- **Error Checking**:
    - **Undefined Symbol**: If a symbol is not in the symbol table.
    - **Illegal Addressing**: If an addressing mode is not allowed for an instruction.
    - **Address Out of Range**: If the target address cannot be encoded in the instruction format.
---
## 3. TextRecordManager
**Responsibilities**:
- **Collect Object Codes**: Group generated object codes into text records.
- **Manage Record Length**: Ensure text records do not exceed 30 bytes.
- **Handle Record Continuity**: Start new records when necessary (e.g., non-contiguous addresses).
**Attributes**:
- `text_records`: A list of text record strings.
- `current_record`: A buffer for the current text record's object codes.
- `current_start_address`: The starting address of the current text record.
**Methods**:
- `__init__(self)`
- `add_object_code(self, address, object_code)`: Adds object code to the current text record.
- `finalize_current_record(self)`: Finalizes the current text record and stores it.
- `get_text_records(self)`: Returns all finalized text records.
**Implementation Details**:
- **Record Format**: `T^StartAddress^Length^ObjectCodes`
- **Length Constraint**: Each text record's object code length must not exceed 60 hexadecimal digits (30 bytes).
---
## 4. ModificationRecordManager
**Responsibilities**:
- **Track Modification Records**: Keep track of addresses needing modification.
- **Generate Modification Records**: Create records for relocation during linking/loading.
**Attributes**:
- `modification_records`: A list of modification record strings.
**Methods**:
- `__init__(self)`
- `add_modification(self, address, length)`: Records a modification at a given address.
- `get_modification_records(self)`: Returns all modification records.
**Implementation Details**:
- **Record Format**: `M^Address^Length`
- **Usage**: For format 4 instructions and any symbols requiring relocation.
---
## 5. ObjectProgramWriter
**Responsibilities**:
- **Assemble Object Program**: Combine all records into the final object program.
- **Write to Output File**: Write the assembled program to a file.
**Attributes**:
- `header_record`: The header record string.
- `text_records`: List of text record strings.
- `modification_records`: List of modification record strings.
- `end_record`: The end record string.
**Methods**:
- `__init__(self, header_record, text_records, modification_records, end_record)`
- `write_to_file(self, file_name)`: Writes the object program to a file.
**Implementation Details**:
- **Header Record Format**: `H^ProgramName^StartAddress^ProgramLength`
- **End Record Format**: `E^FirstExecutableInstructionAddress`

---
# Detailed Steps for Pass 2

## Step 1: Initialize and Load Tables
- **Symbol Table**:
    - Use `SymbolTableDriver` to build the symbol table from the symbol definitions.
- **Literal Table**:
    - Use `LiteralTableDriver` to build the literal table, ensuring all literals have assigned addresses.
- **Opcode Handler**:
    - Ensure the `OpcodeHandler` provides opcode mnemonics, machine codes, formats, and allowed addressing modes.
- **Error Handler**:
    - Initialize `ErrorLogHandler` to track errors during Pass 2.
---
## Step 2: Read and Parse the Intermediate File
- **Initialize `IntermediateFileReader`**:
    - Read the intermediate file line by line.
- **Parse Each Line**:
    - Extract the address, label, opcode, operands, and any comments or errors.
    - Create `SourceCodeLine` objects representing each line.
---
## Step 3: Prepare for Object Code Generation
- **Initialize Generators and Managers**:
    - `ObjectCodeGenerator`: For generating object code.
    - `TextRecordManager`: For managing text records.
    - `ModificationRecordManager`: For tracking modification records.
- **Set Location Counter**:
    - Initialize `LocationCounter` to keep track of addresses if necessary.
---
## Step 4: Process Each Line
### Loop Over Each `SourceCodeLine`
```python
for source_line in intermediate_reader:
    # Skip lines that are comments or have errors from Pass 1
    if source_line.is_comment() or source_line.has_errors():
        continue

    # Handle directives that don't generate object code (e.g., START, END, BASE, NOBASE)
    if source_line.is_directive():
        handle_directive(source_line)
        continue

    # Generate object code
    object_code = object_code_generator.generate_object_code(source_line)

    if object_code:
        # Add object code to text record
        text_record_manager.add_object_code(source_line.address, object_code)

        # Handle modification records
        if source_line.requires_modification():
            modification_record_manager.add_modification(source_line.address + modification_offset, modification_length)
    else:
        # Log error if object code could not be generated
        error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
```

### Handling Directives
- **START**:
    - Set the starting address for the program.
- **END**:
    - Indicates the end of the program; finalize any remaining records.
- **LTORG**:
    - Assign addresses to literals in the current literal pool and output them.
- **EQU**:
    - Evaluate expressions and update the symbol table accordingly.
- **BASE/NOBASE**:
    - Manage base register settings for addressing modes.
---
## Step 5: Generate Object Code for Each Instruction
**In `ObjectCodeGenerator.generate_object_code(source_line)`**
1. **Get Opcode Information**:
    - Retrieve opcode details from `opcode_handler` based on `source_line.opcode`.
2. **Resolve Operands**:
    - For each operand, call `resolve_operand(operand, current_address)`.
    - **Undefined Symbol Error**: If the symbol is not in the symbol table, log an error.
3. **Check Addressing Modes**:
    - Verify that the addressing mode is legal for the instruction.
    - **Illegal Addressing Error**: If an invalid addressing mode is used, log an error.
4. **Calculate Target Address**:
    - Compute the target address based on the operand and addressing mode.
5. **Check Address Range**:
    - For formats with limited displacement (e.g., format 3 with 12-bit displacement), ensure the target address is within range.
    - **Address Out of Range Error**: If the address is out of range, attempt to use base-relative addressing or format 4; if not possible, log an error.
6. **Generate Object Code**:
    - Assemble the object code based on the instruction format, opcode, addressing mode, and target address.
7. **Update Modification Records**:
    - For instructions that require relocation (e.g., format 4 or external references), add entries to `ModificationRecordManager`.
---
## Step 6: Manage Text Records
- **Add Object Codes**:
    - Use `TextRecordManager.add_object_code(address, object_code)` to add object code to the current text record.
- **Finalize Records**:
    - If the text record reaches the maximum length or the next address is non-contiguous, finalize the current record.
---
## Step 7: Manage Modification Records
- **Add Modification Entries**:
    - Use `ModificationRecordManager.add_modification(address, length)` to record any necessary relocations.
- **Modification Entries Criteria**:
    - Typically needed for format 4 instructions and symbols defined in other control sections (for linking).
---
## Step 8: Finalize and Collect Records
- **Finalize Remaining Text Records**:
    - Call `text_record_manager.finalize_current_record()` to ensure all records are finalized.
- **Collect All Records**:
    - **Header Record**:
        - Create based on program name, start address, and program length.
    - **Text Records**:
        - Retrieve from `text_record_manager.get_text_records()`.
    - **Modification Records**:
        - Retrieve from `modification_record_manager.get_modification_records()`.
    - **End Record**:
        - Create based on the starting execution address (typically the address of the first executable instruction).
---
## Step 9: Write the Object Program
- **Initialize `ObjectProgramWriter`** with all the collected records.
- **Write to File**:
    - Use `object_program_writer.write_to_file(output_file_name)` to write the object program.
---
## Step 10: Error Handling and Logging
- **Undefined Symbol Error (Pass 2)**:
    - **Detection**: When `resolve_operand` fails to find a symbol in the symbol table.
    - **Handling**:
        - Log an error message specifying the symbol and line number.
        - Skip object code generation for that instruction.
- **Illegal Addressing Error (Pass 2)**:
    - **Detection**: When an addressing mode is not valid for the instruction.
    - **Handling**:
        - Log an error indicating the illegal addressing mode used.
        - Skip object code generation for that instruction.
- **Address Out of Range Error (Pass 2)**:
    - **Detection**: When the displacement or address cannot be encoded in the instruction format.
    - **Handling**:
        - Attempt to adjust addressing mode (e.g., use base-relative addressing).
        - If not possible, log an error and skip object code generation.
- **Error Logging**:
    - Use `ErrorLogHandler` to record and display all errors encountered.
    - Include line numbers, error descriptions, and any relevant context.

---
# Detailed Implementation of Key Components
## Operand Resolution and Addressing Modes
**In `ObjectCodeGenerator.resolve_operand(operand, current_address)`**
1. **Identify Addressing Mode**:
    - **Immediate** (`#`): Operand is a constant value.
    - **Indirect** (`@`): Operand is a memory address stored in a symbol.
    - **Simple**: Direct addressing using symbols.
2. **Strip Addressing Mode Prefixes**:
    - Remove `#` or `@` from the operand.
3. **Check for Literals**:
    - If operand starts with `=`, resolve using the literal table.
4. **Symbol Lookup**:
    - Use `symbol_table.get(operand)` to retrieve the symbol's value and relocation flag.
    - **Undefined Symbol Error**: If symbol not found, log an error.
5. **Calculate Target Address**:
    - For relative addressing modes, calculate displacement.
6. **Check Address Range**:
    - For format 3 (12-bit displacement):
        - PC-relative: Displacement must be between -2048 and +2047.
        - Base-relative: Displacement must be between 0 and +4095.
    - **Address Out of Range Error**: If displacement is out of range, log an error.
7. **Return Resolved Operand**:
    - Return the target address, flags for modification records, and any errors.
---
## Instruction Format Handling
### **Format 3 Example:**
- **Structure**:
    - **Opcode**: 6 bits.
    - **n, i**: 1 bit each for addressing mode.
    - **x**: 1 bit for indexing.
    - **b, p, e**: 1 bit each for addressing flags.
    - **Displacement**: 12 bits.
- **Addressing Flags**:
    - **b**: Base-relative addressing.
    - **p**: PC-relative addressing.
    - **e**: Extended format (set to 0 for format 3).
- **Generating Object Code**:
    - Assemble the bits into a 3-byte object code.
**Format 4 Example**:
- **Similar to Format 3**, but:
    - **e**: Set to 1 to indicate extended format.
    - **Address**: 20 bits.
- **Requires Modification Record**:
    - For relocatable addresses in format 4, add an entry to `ModificationRecordManager`.
---
## Error Messages and Codes
- **Undefined Symbol**:
    - **Message**: `Error: Undefined symbol 'symbol' at line X.`
- **Illegal Addressing**:
    - **Message**: `Error: Illegal addressing mode 'mode' used with instruction 'opcode' at line X.`
- **Address Out of Range**:
    - **Message**: `Error: Address out of range for instruction 'opcode' at line X.`
- **Handling in `ErrorLogHandler`**:
    - Implement methods to log these specific errors, including line numbers and context.

---
## Creating Records
### Header Record
- **Format**:
    ```
    H^ProgramName(6)^StartAddress(6 hex digits)^ProgramLength(6 hex digits)
    ```
- **Example**:
    ```
    H^PROG01^001000^00007A
    ```
### Text Record
- **Format**:
    ```
    T^StartAddress(6 hex digits)^RecordLength(2 hex digits)^ObjectCode
    ```
- **Example**:
    ```
    T^001000^1E^1410332810303010153F2F30103F201036
    ```
### Modification Record
- **Format**:
    ```
    M^Address(6 hex digits)^Length(2 hex digits)^OptionalSymbol
    ```
- **Example**:
    ```
    M^001026^05
    ```
### End Record
- **Format**:
    ```
    E^FirstExecutableInstructionAddress(6 hex digits)
    ```
- **Example**:
    ```
    E^001000
    ```
---
# Integration of Existing Classes
### SymbolTable and LiteralTable
- **Usage**:
    - Used extensively in `ObjectCodeGenerator` for resolving symbols and literals.
- **Ensure Correctness**:
    - All symbols and literals should have addresses and relocation flags.
- **Error Handling**:
    - Modify `SymbolTable.get()` and `LiteralTable.search()` to return clear error messages when symbols or literals are undefined.
### OpcodeHandler
- **Enhancements**:
    - Include allowed addressing modes for each opcode.
    - Provide methods to check if an addressing mode is legal for a given opcode.
### ErrorLogHandler
- **Enhancements**:
    - Include methods to log specific errors with context (line number, instruction).
    - Provide a summary of errors at the end of assembly.
---
## Testing and Validation
- **Test Cases for Errors**:
    - Create assembly programs that deliberately trigger each of the specified errors to ensure they are correctly detected and reported.
- **Verification**:
    - Compare generated object code with expected results.
    - Use an assembler simulator to load and execute the object program.

---
# Additional Considerations
### Base Register Management
- **Handling BASE and NOBASE Directives**:
    - Update the base register value when encountering a `BASE` directive.
    - Clear the base register when encountering a `NOBASE` directive.
- **Impact on Addressing**:
    - Use base-relative addressing when PC-relative is not possible.
### Expressions in Operands
- **Evaluate Expressions**:
    - Use `ExpressionEvaluator` to handle operands that are expressions (e.g., `BUFFER+LENGTH`).
- **Relocation Flags**:
    - Determine if the result of an expression is relocatable.
## External References and Definitions
- **Handling EXTREF and EXTDEF**:
    - For programs with multiple control sections, manage external references and definitions.
- **Modification Records for External Symbols**:
    - Modification records must include the symbol name when modifying addresses of external symbols.
### Program Blocks and Control Sections
- **Program Blocks**:
    - If your assembler supports program blocks, manage separate location counters for each block.
- **Control Sections**:
    - Handle separate control sections with their own symbol tables.
---
## **Summary**
By expanding on the design with these detailed steps and class implementations, you can:
- **Effectively Handle Errors**:
    - Ensure all specified errors are detected and appropriately reported.
- **Create Required Records**:
    - Generate header, text, modification, and end records accurately.
- **Leverage Existing Code**:
    - Integrate your existing `SymbolTable`, `LiteralTable`, `ErrorLogHandler`, and other classes into Pass 2.
- **Produce a Correct Object Program**:
    - Generate an object program that can be correctly loaded and executed.
---
## Final Notes
- **Documentation**:
    - Keep your code well-documented with comments explaining complex logic.
- **Modularity**:
    - Design your classes and methods to be modular and reusable.
- **Testing**:
    - Continually test each component as you build it to ensure correctness.
- **Error Handling**:
    - Be thorough in error detection to prevent incorrect object code generation.
- **Ask for Help**:
    - If you encounter difficulties, don't hesitate to seek assistance or clarification.