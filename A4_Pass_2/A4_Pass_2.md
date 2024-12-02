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
## 1. IntermediateFileParser
---
### Objective
- **Design an `IntermediateFileParser` class** that can parse the intermediate file generated from Pass 1.
- **Handle various line types**: code lines, error lines, symbol table entries, literal table entries, program length lines, and other special lines.
- **Provide methods** to parse and store the data in a structured manner for use in Pass 2.
---
### Understanding the Input
The intermediate file contains a mix of:
1. **Code Lines**: Contain line numbers, addresses, labels, opcodes, operands, and comments.
2. **Error Lines**: Similar to code lines but include error messages.
3. **Divider Lines**: Lines with underscores `___` used as separators.
4. **Title Lines**: Lines starting with `===`, indicating sections like symbol table, literal table, and program length.
5. **Symbol Table Entries**: Between `===SYM_START===` and `===SYM_END===`.
6. **Literal Table Entries**: Between `===LIT_START===` and `===LIT_END===`.
7. **Program Length Entries**: Between `===PROG_LEN_START===` and `===PROG_LEN_END===`.
8. **Empty Lines**: Lines that are blank or contain only whitespace.

---
### Class Responsibilities
- **Read and parse the intermediate file** line by line.
- **Identify and handle different line types**, parsing each appropriately.
- **Store parsed data** in structured data structures for use in Pass 2.
- **Provide methods** to access the parsed data.
### Attributes
- `file_name`: The name of the intermediate file.
- `code_lines`: A list of `SourceCodeLine` objects representing code lines.
- `symbol_table`: A dictionary or object representing the symbol table.
- `literal_table`: A dictionary or object representing the literal table.
- `program_length`: The length of the program (both decimal and hexadecimal).
- `errors`: A list of errors encountered during parsing.
### Methods
1. `__init__(self, file_name)`: Initializes the reader and starts parsing the file.
2. `parse_file(self)`: Reads the file and processes each line.
3. `parse_line(self, line)`: Determines the type of the line and calls the appropriate parsing method.
4. `parse_code_line(self, line)`: Parses regular code lines.
5. `parse_error_line(self, line)`: Parses error lines.
6. `parse_symbol_table(self, lines)`: Parses symbol table entries.
7. `parse_literal_table(self, lines)`: Parses literal table entries.
8. `parse_program_length(self, lines)`: Parses program length entries.
9. `is_divider_line(self, line)`: Checks if a line is a divider line (e.g., `______`).
10. `is_title_line(self, line)`: Checks if a line is a title line (e.g., starts with `===`).
11. `get_code_lines(self)`: Returns the list of parsed code lines.
12. `get_symbol_table(self)`: Returns the symbol table.
13. `get_literal_table(self)`: Returns the literal table.
14. `get_program_length(self)`: Returns the program length.
---
### Implementation Details
#### 1. `__init__(self, file_name)`
- **Purpose**: Initialize the `IntermediateFileReader` with the given file name and start parsing.
- **Actions**:
    - Set `self.file_name`.
    - Initialize `self.code_lines`, `self.symbol_table`, `self.literal_table`, `self.program_length`, and `self.errors`.
    - Call `self.parse_file()`.
#### 2. `parse_file(self)`
- **Purpose**: Read the file and process each line.
- **Actions**:
    - Open the file and read lines into a list.
    - Initialize an index `i` to keep track of the current line number.
    - Loop through the lines, processing each one:
        - Strip whitespace from the line.
        - Skip empty lines or divider lines.
        - If the line is a title line, handle the corresponding section.
        - Else, call `self.parse_line(line)`.
#### 3. `parse_line(self, line)`
- **Purpose**: Determine the type of the line and parse it accordingly.
- **Actions**:
    - If the line starts with a number (line number), it's a code line or error line.
        - If `[ERROR` is present in the line, call `self.parse_error_line(line)`.
        - Else, call `self.parse_code_line(line)`.
    - Else, log an error indicating an unrecognized line format.
### 4. `parse_code_line(self, line)`
- **Purpose**: Parse a regular code line and store it as a `SourceCodeLine` object.
- **Actions**:
    - Split the line into parts using whitespace as the delimiter.
    - Extract the line number and address.
    - Determine if a label is present.
        - If the third part ends with `:`, it's a label.
    - Extract the opcode and operands.
    - Handle comments at the end of the line.
    - Create a `SourceCodeLine` object with the extracted data and add it to `self.code_lines`.
### 5. `parse_error_line(self, line)`
- **Purpose**: Parse an error line and store the error information.
- **Actions**:
    - Similar to `parse_code_line`, but extract the error message.
    - Store the error in `self.errors`.
    - Optionally, create a `SourceCodeLine` object with an error flag.
### 6. `parse_symbol_table(self, lines)`
- **Purpose**: Parse symbol table entries between `===SYM_START===` and `===SYM_END===`.
- **Actions**:
    - Loop through the lines until `===SYM_END===` is encountered.
    - Skip any divider lines.
    - Extract symbol, value, RFlag, IFlag, and MFlag from each line.
    - Store the symbols in `self.symbol_table`.
### 7. `parse_literal_table(self, lines)`
- **Purpose**: Parse literal table entries between `===LIT_START===` and `===LIT_END===`.
- **Actions**:
    - Similar to `parse_symbol_table`, but extract literals, values, lengths, and addresses.
    - Store the literals in `self.literal_table`.
### 8. `parse_program_length(self, lines)`
- **Purpose**: Parse program length entries between `===PROG_LEN_START===` and `===PROG_LEN_END===`.
- **Actions**:
    - Extract the program length in decimal and hexadecimal.
    - Store the lengths in `self.program_length`.
### 9. `is_divider_line(self, line)`
- **Purpose**: Check if a line is a divider line (contains three or more underscores).
- **Return**: `True` if it's a divider line, `False` otherwise.
### 10. `is_title_line(self, line)`
- **Purpose**: Check if a line is a title line (starts with `===`).
- **Return**: `True` if it's a title line, `False` otherwise.
### **11. Accessor Methods**
- **Purpose**: Provide access to the parsed data:
    - `get_code_lines()`
    - `get_symbol_table()`
    - `get_literal_table()`
    - `get_program_length()`

---
### Handling Different Line Types
#### Empty Lines
- **Detection**: Line is empty after stripping whitespace.
- **Action**: Ignore and continue to the next line.
#### Divider Lines
- **Detection**: Line contains three or more underscores (`___`).
- **Action**: Ignore and continue.
#### Title Lines
- **Detection**: Line starts with `===`.
- **Action**: Determine the type of section and call the corresponding parsing method:
    - `===SYM_START===`: Call `parse_symbol_table()`.
    - `===LIT_START===`: Call `parse_literal_table()`.
    - `===PROG_LEN_START===`: Call `parse_program_length()`.
#### Code Lines
- **Detection**: Line starts with a number (line number).
- **Action**: Call `parse_code_line()`.
#### Error Lines
- **Detection**: Line contains `[ERROR` in the third part after splitting.
- **Action**: Call `parse_error_line()`.
#### Symbol Table Entries
- **Detection**: Between `===SYM_START===` and `===SYM_END===`.
- **Action**: Call `parse_symbol_table()`.
#### Literal Table Entries
- **Detection**: Between `===LIT_START===` and `===LIT_END===`.
- **Action**: Call `parse_literal_table()`.
#### Program Length Lines
- **Detection**: Between `===PROG_LEN_START===` and `===PROG_LEN_END===`.
- **Action**: Call `parse_program_length()`.
---
### Implementing Parsing Methods
#### Parsing Code Lines
```python
def parse_code_line(self, line):
    parts = line.strip().split()
    if len(parts) < 2:
        self.errors.append(f"Invalid code line format: '{line}'")
        return

    line_number = parts[0]
    address = parts[1]
    index = 2

    # Initialize variables
    label = ''
    opcode = ''
    operands = ''
    comment = ''
    error = ''

    # Check if the third part is a label
    if len(parts) > index and parts[index].endswith(':'):
        label = parts[index][:-1]  # Remove the colon
        index += 1

    # Check for opcode
    if len(parts) > index:
        opcode = parts[index]
        index += 1

    # Check for operands
    if len(parts) > index:
        # Collect the rest as operands or comments
        operands_or_comment = ' '.join(parts[index:])
        # Split operands and comments if '#' is used for comments
        if '#' in operands_or_comment:
            operands, comment = operands_or_comment.split('#', 1)
            operands = operands.strip()
            comment = comment.strip()
        else:
            operands = operands_or_comment.strip()

    # Create SourceCodeLine object
    source_line = SourceCodeLine(
        line_number=line_number,
        address=address,
        label=label,
        opcode=opcode,
        operands=operands,
        comment=comment,
        error=error
    )
    self.code_lines.append(source_line)
```

#### Parsing Error Lines
```python
def parse_error_line(self, line):
    # Error lines may have an error message in square brackets
    parts = line.strip().split()
    if len(parts) < 3:
        self.errors.append(f"Invalid error line format: '{line}'")
        return

    line_number = parts[0]
    address = parts[1]
    error_message = ''
    index = 2

    # Collect the error message
    while index < len(parts) and not parts[index].endswith(']'):
        error_message += parts[index] + ' '
        index += 1
    if index < len(parts):
        error_message += parts[index]
        index += 1
    error_message = error_message.strip('[] ')

    # Proceed to parse the rest of the line as a code line
    if index < len(parts) and parts[index].endswith(':'):
        label = parts[index][:-1]
        index += 1
    else:
        label = ''

    opcode = ''
    operands = ''
    comment = ''

    if index < len(parts):
        opcode = parts[index]
        index += 1
    if index < len(parts):
        operands = ' '.join(parts[index:])

    # Create SourceCodeLine object with error
    source_line = SourceCodeLine(
        line_number=line_number,
        address=address,
        label=label,
        opcode=opcode,
        operands=operands,
        comment=comment,
        error=error_message
    )
    self.code_lines.append(source_line)
    self.errors.append(f"Line {line_number}: {error_message}")
```

#### Parsing Symbol Table
```python
def parse_symbol_table(self, lines_iterator):
    for line in lines_iterator:
        line = line.strip()
        if line == '===SYM_END===':
            break
        if self.is_divider_line(line) or not line:
            continue
        parts = line.split()
        if len(parts) >= 5:
            symbol = parts[0]
            value = parts[1]
            rflag = parts[2]
            iflag = parts[3]
            mflag = parts[4]
            self.symbol_table[symbol] = {
                'value': value,
                'rflag': rflag,
                'iflag': iflag,
                'mflag': mflag
            }
        else:
            self.errors.append(f"Invalid symbol table line: '{line}'")
```
#### Parsing Literal Table
```python
def parse_literal_table(self, lines_iterator):
    for line in lines_iterator:
        line = line.strip()
        if line == '===LIT_END===':
            break
        if self.is_divider_line(line) or not line:
            continue
        parts = line.split()
        if len(parts) >= 4:
            literal = parts[0]
            value = parts[1]
            length = parts[2]
            address = parts[3]
            self.literal_table[literal] = {
                'value': value,
                'length': length,
                'address': address
            }
        else:
            self.errors.append(f"Invalid literal table line: '{line}'")
```

#### Parsing Program Length
```python
def parse_program_length(self, lines_iterator):
    for line in lines_iterator:
        line = line.strip()
        if line == '===PROG_LEN_END===':
            break
        if not line:
            continue
        if line.startswith('Program Length (DEC):'):
            parts = line.split(':')
            if len(parts) == 2:
                self.program_length['decimal'] = parts[1].strip()
        elif line.startswith('Program Length (HEX):'):
            parts = line.split(':')
            if len(parts) == 2:
                self.program_length['hexadecimal'] = parts[1].strip()
        else:
            self.errors.append(f"Invalid program length line: '{line}'")
```
---
### Complete `IntermediateFileReader` Class
```python
class IntermediateFileReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.code_lines = []
        self.symbol_table = {}
        self.literal_table = {}
        self.program_length = {'decimal': None, 'hexadecimal': None}
        self.errors = []
        self.parse_file()

    def parse_file(self):
        with open(self.file_name, 'r') as f:
            lines = f.readlines()
        lines_iterator = iter(lines)
        for line in lines_iterator:
            line = line.strip()
            if not line or self.is_divider_line(line):
                continue
            if self.is_title_line(line):
                if line == '===SYM_START===':
                    self.parse_symbol_table(lines_iterator)
                elif line == '===LIT_START===':
                    self.parse_literal_table(lines_iterator)
                elif line == '===PROG_LEN_START===':
                    self.parse_program_length(lines_iterator)
                else:
                    # Unknown section; skip or log error
                    self.errors.append(f"Unknown section title: '{line}'")
            else:
                self.parse_line(line)
    def parse_line(self, line):
        parts = line.strip().split()
        if not parts:
            return
        if parts[0].isdigit():
            # Line starts with a line number
            if '[ERROR' in line:
                self.parse_error_line(line)
            else:
                self.parse_code_line(line)
        else:
            # Unrecognized line format
            self.errors.append(f"Unrecognized line format: '{line}'")
    # ... [Other methods as previously defined] ...

    # Define is_divider_line, is_title_line, and accessor methods

    def is_divider_line(self, line):
        return line.startswith('___')

    def is_title_line(self, line):
        return line.startswith('===')

    def get_code_lines(self):
        return self.code_lines

    def get_symbol_table(self):
        return self.symbol_table

    def get_literal_table(self):
        return self.literal_table

    def get_program_length(self):
        return self.program_length

    def get_errors(self):
        return self.errors
```


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
### 1. Overview

The `ObjectCodeGenerator` is a core component of the assembler's Pass 2. Its primary function is to translate each assembly instruction into machine code (object code) while resolving symbols and literals using the symbol and literal tables. It handles various instruction formats and addressing modes, and performs error checking to ensure the correctness of the generated code.
### 2. Responsibilities
- **Generate Object Code**: Translate each instruction into its corresponding machine code.
- **Resolve Symbols and Literals**: Use the symbol and literal tables to resolve addresses and values.
- **Handle Instruction Formats and Addressing Modes**: Support formats 1 to 4 and various addressing modes (immediate, indirect, simple, indexed, extended).
- **Error Checking**: Detect and report undefined symbols, illegal addressing modes, and address out-of-range errors.
- **Collaborate with Managers**: Work with `TextRecordManager` and `ModificationRecordManager` to manage object code records and modification records.
### 3. Attributes
- `symbol_table`: Reference to the symbol table (`SymbolTable` instance).
- `literal_table`: Reference to the literal table (`LiteralTableList` instance).
- `opcode_handler`: Provides opcode information (could be an `OpcodeTable` instance).
- `error_handler`: Logs errors encountered during code generation (`ErrorLogHandler` instance).
- `text_record_manager`: Manages text records (`TextRecordManager` instance).
- `modification_record_manager`: Manages modification records (`ModificationRecordManager` instance).
- `program_length`: The length of the program (integer).
- `current_address`: The current address during object code generation.
- `base_register_value`: The value of the base register, if base-relative addressing is used.
- `nixbpe_flags`: Flags for instruction encoding (n, i, x, b, p, e).
### 4. Methods
#### Initialization
- `__init__(self, symbol_table, literal_table, opcode_handler, error_handler, program_length)`
    - Initializes the `ObjectCodeGenerator` with references to necessary tables and handlers.
    - Initializes `text_record_manager` and `modification_record_manager`.
#### Main Methods
- `generate_object_code(self, source_lines)`
    - Iterates over each `SourceCodeLine` in `source_lines`.
    - For each line, determines the type (instruction, directive, comment) and processes accordingly.
    - Updates `current_address` based on instruction length.
    - Handles errors and logs them using `error_handler`.
- `process_instruction(self, source_line)`
    - Main method to generate object code for an instruction line.
    - Fetches opcode information using `opcode_handler`.
    - Determines instruction format and calls the appropriate handler.
- `process_directive(self, source_line)`
    - Handles assembly directives such as `BYTE`, `WORD`, `RESB`, `RESW`, `BASE`, `NOBASE`.
    - Generates object code for `BYTE` and `WORD`.
    - Updates `current_address` for `RESB` and `RESW`.
    - Handles base register setup for `BASE` and `NOBASE`.
#### Instruction Format Handlers
- `handle_format1(self, source_line, opcode_info)`
    - Generates object code for format 1 instructions (1 byte).
    - Object code is simply the opcode.
- `handle_format2(self, source_line, opcode_info)`
    - Generates object code for format 2 instructions (2 bytes).
    - Parses register operands and encodes them.
- `handle_format3(self, source_line, opcode_info)`
    - Generates object code for format 3 instructions (3 bytes).
    - Handles addressing modes and calculates displacement.
    - Sets `nixbpe_flags` accordingly.
- `handle_format4(self, source_line, opcode_info)`
    - Generates object code for format 4 instructions (4 bytes).
    - Handles extended addressing (e flag set).
    - Adds entries to `modification_record_manager` if necessary.
#### Supporting Methods
- `resolve_operand(self, operand, current_address)`
    - Resolves an operand, returning its value and relocation info.
    - Checks symbol and literal tables.
    - Handles immediate and indirect addressing.
- `calculate_displacement(self, target_address, current_address)`
    - Calculates displacement for format 3 instructions.
    - Determines if PC-relative or base-relative addressing can be used.
    - Returns displacement and sets appropriate flags.
- `check_address_range(self, target_address, format_type, current_address)`
    - Checks if the target address is within the allowable range for the instruction format.
    - Logs an error if the address is out of range.
- `detect_illegal_addressing(self, source_line, opcode_info)`
    - Detects illegal addressing modes for the given instruction.
    - Logs errors for unsupported addressing modes.
- `update_current_address(self, instruction_length)`
    - Updates `current_address` by adding the instruction length.
- `log_error(self, message, line_number)`
    - Logs an error message using `error_handler`.
### 5. Implementation Details
#### Instruction Formats
- **Format 1**:
    - Length: 1 byte.
    - Object code: Opcode only.
- **Format 2**:
    - Length: 2 bytes.
    - Object code: Opcode + Register codes.
    - Registers are encoded using predefined codes (e.g., A=0, X=1, L=2, etc.).
- **Format 3**:
    - Length: 3 bytes.
    - Object code: Opcode + nixbpe flags + 12-bit displacement.
    - Supports PC-relative and base-relative addressing.
    - Displacement range: -2048 to +2047 (12-bit signed).
- **Format 4**:
    - Length: 4 bytes.
    - Object code: Opcode + nixbpe flags + 20-bit address.
    - Supports extended addressing mode.
    - Requires modification records for relocation.
#### Addressing Modes
- **Immediate Addressing** (`#`):
    - Operand is a constant or an expression.
    - `n` (indirect bit) = 0, `i` (immediate bit) = 1.
- **Indirect Addressing** (`@`):
    - Operand is a memory address.
    - `n` = 1, `i` = 0.
- **Simple (Direct) Addressing** (no prefix):
    - Operand is a symbol or address.
    - `n` = 1, `i` = 1.
- **Indexed Addressing** (`,X`):
    - Uses index register X.
    - `x` (index bit) = 1.
- **Extended Format** (`+`):
    - Indicates format 4 instruction.
    - `e` (extended bit) = 1.
#### Error Checking
- **Undefined Symbol**:
    - If a symbol is not found in the symbol table.
    - Logs an error and marks the line as invalid.
- **Illegal Addressing**:
    - If an addressing mode is not allowed for an instruction (e.g., immediate addressing with a format 1 instruction).
    - Logs an error.
- **Address Out of Range**:
    - If the target address cannot be encoded within the displacement field.
    - Suggests using format 4 or base-relative addressing if possible.
### 6. Interaction with Other Classes
#### TextRecordManager
- **Purpose**:
    - Collects and manages object codes to form text records.
    - Ensures each text record does not exceed 30 bytes of object code.
- **Interaction**:
    - After generating object code for a line, `ObjectCodeGenerator` calls `text_record_manager.add_object_code(address, object_code)`.
    - `text_record_manager` handles the grouping of object codes into text records.
#### ModificationRecordManager
- **Purpose**:
    - Tracks addresses that require modification during linking/loading (relocation).
    - Generates modification records for format 4 instructions and relocatable expressions.
- **Interaction**:
    - When a format 4 instruction or relocatable operand is encountered, `ObjectCodeGenerator` calls `modification_record_manager.add_modification(address, length)`.
    - The `length` specifies the number of half-bytes to modify (e.g., 5 for format 4 addresses).

#### ObjectProgramWriter
- **Purpose**:
    - Assembles the final object program by combining the header record, text records, modification records, and end record.
    - Writes the object program to an output file.
- **Interaction**:
    - Once code generation is complete, `ObjectCodeGenerator` provides the header record, text records (from `text_record_manager`), modification records (from `modification_record_manager`), and end record to `ObjectProgramWriter`.
    - `ObjectProgramWriter` assembles these components and writes them to the file.
### 7. Detailed Method Descriptions
#### generate_object_code(self, source_lines)
- **Process**:
    - Initialize `current_address` to the program's starting address.
    - Loop through each `source_line` in `source_lines`.
        - If `source_line` is a comment or empty line, skip processing.
        - If `source_line` has errors, log the error and skip processing.
        - If `source_line` is an instruction:
            - Call `process_instruction(source_line)`.
        - If `source_line` is a directive:
            - Call `process_directive(source_line)`.
        - Update `current_address` using `update_current_address(instruction_length)`.
#### process_instruction(self, source_line)
- **Process**:
    - Retrieve opcode mnemonic from `source_line`.
    - Use `opcode_handler` to get `opcode_info` (opcode value, instruction format, allowed addressing modes).
    - Call `detect_illegal_addressing(source_line, opcode_info)`.
        - If illegal addressing is detected, log an error and return.
    - Based on instruction format, call the corresponding handler:
        - Format 1: `handle_format1(source_line, opcode_info)`
        - Format 2: `handle_format2(source_line, opcode_info)`
        - Format 3: `handle_format3(source_line, opcode_info)`
        - Format 4: `handle_format4(source_line, opcode_info)`
    - After generating the object code, add it to the text record:
        - `text_record_manager.add_object_code(current_address, object_code)`
#### handle_format3(self, source_line, opcode_info)
- **Process**:
    - Initialize `nixbpe_flags` to `[0, 0, 0, 0, 0, 0]` (n, i, x, b, p, e).
    - Set `e` flag to 0 (since it's format 3).
    - Process operand and addressing modes using `process_addressing_modes(operand, nixbpe_flags)`.
    - Resolve operand address using `resolve_operand(operand, current_address)`.
        - If operand is undefined, log an error.
    - Calculate displacement using `calculate_displacement(target_address, current_address)`.
        - If displacement cannot be calculated, suggest using format 4.
    - Construct object code:
        - Opcode (6 bits) + nixbpe flags (6 bits) + displacement (12 bits).
#### resolve_operand(self, operand, current_address)
- **Process**:
    - Check for literals (if operand starts with `=`).
        - Retrieve address from `literal_table`.
    - Check for symbols in `symbol_table`.
        - Retrieve address.
    - If operand is a constant (immediate value), convert to integer.
    - Handle expressions (e.g., `symbol + offset`).
    - Return the resolved address/value and relocation info.
#### calculate_displacement(self, target_address, current_address)
- **Process**:
    - Calculate displacement: `displacement = target_address - (current_address + 3)`
        - `+3` is the length of the instruction.
    - Check if displacement is within -2048 to +2047.
        - If yes, set `p` flag to 1.
    - If not, check if base-relative addressing can be used:
        - Displacement: `displacement = target_address - base_register_value`
        - If displacement is within 0 to 4095, set `b` flag to 1.
    - If neither, return `None` (displacement cannot be calculated).
### 8. Error Handling
- **Undefined Symbols**:
    - When an operand cannot be resolved, log an error: `"Undefined symbol '{operand}' at line {line_number}."`
    - Mark the `source_line` as having errors.
- **Illegal Addressing Modes**:
    - If the addressing mode is not allowed for the instruction, log an error: `"Illegal addressing mode for instruction '{opcode}' at line {line_number}."`
- **Address Out of Range**:
    
    - If displacement cannot be encoded in the instruction format, log an error: `"Displacement out of range for operand '{operand}' at line {line_number}."`
- **Invalid Operands**:
    
    - If operands are missing or incorrect, log an error: `"Invalid operands for instruction '{opcode}' at line {line_number}."`
### 9. Finalization and Output
- **After Processing All Lines**:
    - Generate the header record:
        - Program name, starting address, program length.
    - Generate the end record:
        - Address of the first executable instruction.
    - Provide all records to `ObjectProgramWriter`:
        - `header_record`
        - `text_records` from `text_record_manager`
        - `modification_records` from `modification_record_manager`
        - `end_record`
    - `ObjectProgramWriter` assembles the final object program and writes it to the output file.

### **10. Pseudocode Example**

```plaintext
ObjectCodeGenerator:

initialize(symbol_table, literal_table, opcode_handler, error_handler, program_length)
initialize text_record_manager
initialize modification_record_manager
current_address = starting address

function generate_object_code(source_lines):
    for source_line in source_lines:
        if source_line is comment or empty:
            continue
        if source_line has errors:
            log_error("Errors in source line, skipping.", source_line.line_number)
            continue
        if source_line is instruction:
            process_instruction(source_line)
        else if source_line is directive:
            process_directive(source_line)
        update_current_address(source_line.instruction_length)

function process_instruction(source_line):
    opcode_info = opcode_handler.get_info(source_line.opcode_mnemonic)
    if opcode_info is None:
        log_error("Invalid opcode.", source_line.line_number)
        return
    detect_illegal_addressing(source_line, opcode_info)
    if source_line has errors:
        return
    switch opcode_info.format:
        case 1:
            handle_format1(source_line, opcode_info)
        case 2:
            handle_format2(source_line, opcode_info)
        case 3:
            handle_format3(source_line, opcode_info)
        case 4:
            handle_format4(source_line, opcode_info)
    add object code to text_record_manager

function handle_format3(source_line, opcode_info):
    set e flag to 0
    process addressing modes and set n, i, x flags
    resolve operand to get target_address
    calculate displacement
    if displacement is None:
        log_error("Displacement out of range.", source_line.line_number)
        return
    construct object code
    source_line.object_code = object code

function resolve_operand(operand, current_address):
    if operand is literal:
        get address from literal_table
    else if operand is symbol:
        get address from symbol_table
    else if operand is constant:
        convert operand to integer
    else:
        log_error("Undefined symbol.", source_line.line_number)
    return address

function calculate_displacement(target_address, current_address):
    displacement = target_address - (current_address + 3)
    if displacement in range -2048 to +2047:
        set p flag to 1
        return displacement
    else if base_register_value is set:
        displacement = target_address - base_register_value
        if displacement in range 0 to 4095:
            set b flag to 1
            return displacement
    return None
```

---

## **Conclusion**

By integrating the `ObjectCodeGenerator` with `TextRecordManager`, `ModificationRecordManager`, and `ObjectProgramWriter`, we've updated the plan to reflect a modular and organized approach to object code generation. The design focuses on pseudocode and planning, detailing responsibilities, attributes, methods, and interactions between classes.

This comprehensive plan should serve as a solid foundation for implementing the `ObjectCodeGenerator` and related components in your assembler. It ensures that each part of the system is well-defined and that their interactions are clearly outlined.

If you have any further questions or need clarification on specific aspects of the design, please feel free to ask!
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