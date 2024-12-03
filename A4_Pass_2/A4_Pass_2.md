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
## 1. `IntermediateFileParser`
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

---

## 2. `ObjectCodeGenerator`

### Responsibilities:
- **Generate Object Code**: Translate each instruction into machine code.
- **Resolve Symbols and Literals**: Use symbol and literal tables to resolve addresses.
- **Handle Instruction Formats and Addressing Modes**: Support various instruction formats and addressing modes.
- **Manage Location Counter**: Utilize `LocationCounter` to track and verify addresses during object code generation.
- **Error Checking**: Detect and report undefined symbols, illegal addressing modes, and address out of range errors.

### Attributes:
- `symbol_table`: Reference to the symbol table.
- `literal_table`: Reference to the literal table.
- `opcode_handler`: Provides opcode information.
- `error_handler`: Logs errors encountered during code generation.
- `text_record_manager`: Manages text records.
- `modification_record_manager`: Manages modification records.
- `location_counter`: Reference to the `LocationCounter` for address management.
- `base_register_value`: The value of the base register, if base-relative addressing is used.
- `nixbpe_flags`: Flags for instruction encoding (n, i, x, b, p, e).

**Methods**:
- `__init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter)`
- `generate_object_code(self, source_lines)`: Main method to generate object code for all lines.
- `generate_object_code_for_line(self, source_line)`: Generates object code for a single line.
- `resolve_operand(self, operand, current_address)`: Resolves an operand, returning its value and relocation info.
- `handle_format1(self, source_line, opcode_info)`: Generates object code based on format 1 instructions.
- `handle_format2(self, source_line, opcode_info)`: Generates object code based on format 2 instructions.
- `handle_format3(self, source_line, opcode_info)`: Generates object code based on format 3 instructions.
- `handle_format4(self, source_line, opcode_info)`: Generates object code based on format 4 instructions.
- `calculate_displacement(self, target_address, current_address)`: Calculates displacement for format 3 instructions.
- `check_address_range(self, displacement, format_type)`: Checks if the displacement is within allowable range.
- `detect_illegal_addressing(self, source_line, opcode_info)`: Detects illegal addressing modes and logs errors.
- `encode_object_code(self, opcode, nixbpe_flags, displacement, format_type)`: Encodes the final object code.
- `set_base_register(self, register)`: Sets the base register value.
- `unset_base_register(self)`: Unsets the base register value.
- `generate_object_code_for_literal(self, literal)`: Generates object code for a literal.

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
- **Location Counter Integration**:
    - Utilize `LocationCounter` to verify the `current_address` against the address in `SourceCodeLine`.
    - Update `LocationCounter` after generating object code to maintain accurate tracking.

### 1. Overview

The `ObjectCodeGenerator` is a core component of the assembler's Pass 2. Its primary function is to translate each assembly instruction into machine code (object code) while resolving symbols and literals using the symbol and literal tables. It handles various instruction formats and addressing modes, manages address tracking through the `LocationCounter`, and performs error checking to ensure the correctness of the generated code.

### 2. Responsibilities
- **Generate Object Code**: Translate each instruction into its corresponding machine code.
- **Resolve Symbols and Literals**: Use the symbol and literal tables to resolve addresses and values.
- **Handle Instruction Formats and Addressing Modes**: Support formats 1 to 4 and various addressing modes (immediate, indirect, simple, indexed, extended).
- **Manage Location Counter**: Utilize `LocationCounter` to track and verify addresses during object code generation.
- **Error Checking**: Detect and report undefined symbols, illegal addressing modes, and address out-of-range errors.
- **Collaborate with Managers**: Work with `TextRecordManager` and `ModificationRecordManager` to manage object code records and modification records.
### 3. Attributes
- `symbol_table`: Reference to the symbol table (`SymbolTable` instance).
- `literal_table`: Reference to the literal table (`LiteralTableList` instance).
- `opcode_handler`: Provides opcode information (`OpcodeHandler` instance).
- `error_handler`: Logs errors encountered during code generation (`ErrorLogHandler` instance).
- `text_record_manager`: Manages text records (`TextRecordManager` instance).
- `modification_record_manager`: Manages modification records (`ModificationRecordManager` instance).
- `location_counter`: Reference to the `LocationCounter` (`LocationCounter` instance) for address management.
- `base_register_value`: The value of the base register, if base-relative addressing is used (integer).
- `nixbpe_flags`: Flags for instruction encoding (list of integers representing n, i, x, b, p, e).

### 4. Methods
#### Initialization
- `__init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter)`
    - **Description**: Initializes the `ObjectCodeGenerator` with references to necessary tables and handlers.
    - **Parameters**:
        - `symbol_table`: Instance of `SymbolTable`.
        - `literal_table`: Instance of `LiteralTableList`.
        - `opcode_handler`: Instance of `OpcodeHandler`.
        - `error_handler`: Instance of `ErrorLogHandler`.
        - `location_counter`: Instance of `LocationCounter`.
    - **Process**:
        - Assigns all references to attributes.
        - Initializes `base_register_value` to `None`.
        - Initializes `nixbpe_flags` as a list `[0, 0, 0, 0, 0, 0]`.
#### Main Methods
- `generate_object_code(self, source_lines)`
    - **Description**: Iterates over each `SourceCodeLine` in `source_lines` and generates object code.
    - **Parameters**:
        - `source_lines`: List of `SourceCodeLine` instances.
    - **Process**:
        - Loop through each `source_line` in `source_lines`.
            - If `source_line` is a comment or has errors, skip processing.
            - If `source_line` is an instruction, call `generate_object_code_for_line(source_line)`.
            - If `source_line` is a directive, handle it accordingly (handled outside this method).
            - Update the `LocationCounter` based on instruction length after object code generation.
    - **Interaction**:
        - Collaborates with `TextRecordManager` and `ModificationRecordManager` to add object and modification records.

- `generate_object_code_for_line(self, source_line)`
    - **Description**: Generates object code for a single `SourceCodeLine`.
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
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
            - `text_record_manager.add_object_code(source_line.address, object_code)`
        - If the instruction requires modification (e.g., format 4), add a modification record:
            - `modification_record_manager.add_modification(address, length)`
    - **Returns**:
        - The generated `object_code` as a hexadecimal string, or `None` if an error occurred.
#### Instruction Format Handlers
- `handle_format1(self, source_line, opcode_info)`
    - **Description**: Generates object code for format 1 instructions (1 byte).
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
        - `opcode_info`: Dictionary containing opcode details.
    - **Process**:
        - Object code is simply the opcode.
        - Convert opcode to a two-digit hexadecimal string.
    - **Returns**:
        - Object code as a hexadecimal string (e.g., `'B4'`).

- `handle_format2(self, source_line, opcode_info)`
    - **Description**: Generates object code for format 2 instructions (2 bytes).
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
        - `opcode_info`: Dictionary containing opcode details.
    - **Process**:
        - Parse register operands from `source_line`.
        - Use predefined register codes (e.g., A=0, X=1, L=2, etc.).
        - Encode the object code as `opcode + reg1_code + reg2_code`.
    - **Returns**:
        - Object code as a four-digit hexadecimal string (e.g., `'90A0'`).

- `handle_format3(self, source_line, opcode_info)`
    - **Description**: Generates object code for format 3 instructions (3 bytes).
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
        - `opcode_info`: Dictionary containing opcode details.
    - **Process**:
        - Initialize `nixbpe_flags` to `[1, 1, 0, 0, 0, 0]` for simple addressing.
        - Process addressing modes (immediate, indirect, indexed) and set flags accordingly.
        - Resolve operand to obtain target address using `resolve_operand`.
        - Calculate displacement using `calculate_displacement`.
            - Determine if PC-relative or base-relative addressing is used.
            - Set `b` and/or `p` flags based on displacement.
        - Check if displacement is within range using `check_address_range`.
            - If out of range, log an error.
        - Encode object code with opcode, flags, and displacement.
    - **Returns**:
        - Object code as a six-digit hexadecimal string (e.g., `'18A3F0'`).

- `handle_format4(self, source_line, opcode_info)`
    - **Description**: Generates object code for format 4 instructions (4 bytes).
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
        - `opcode_info`: Dictionary containing opcode details.
    - **Process**:
        - Set the `e` flag to `1` to indicate extended format.
        - Initialize `nixbpe_flags` accordingly.
        - Resolve operand to obtain target address using `resolve_operand`.
            - If operand is external, mark for modification.
        - Encode object code with opcode, flags, and 20-bit address.
        - Add a modification record to handle relocations.
    - **Returns**:
        - Object code as an eight-digit hexadecimal string (e.g., `'4C000036'`).

#### Supporting Methods
- `resolve_operand(self, operand, current_address)`
    - **Description**: Resolves an operand to its address or value.
    - **Parameters**:
        - `operand`: The operand string from the source line.
        - `current_address`: The current address from `LocationCounter`.
    - **Process**:
        - Check if the operand is a literal (starts with `=`).
            - Retrieve the address from `literal_table`.
        - Check if the operand is a symbol.
            - Retrieve the address from `symbol_table`.
        - Check if the operand is an immediate value (numeric).
            - Convert to integer.
        - Handle expressions (e.g., `SYMBOL + 5`).
            - Evaluate using `symbol_table`.
        - Return the resolved address/value and relocation info (`'A'` for absolute, `'R'` for relocatable).
    - **Returns**:
        - Tuple containing `(resolved_value: int, relocation: str)`.

- `calculate_displacement(self, target_address, current_address)`
    - **Description**: Calculates displacement for format 3 instructions.
    - **Parameters**:
        - `target_address`: The resolved address of the operand.
        - `current_address`: The current address from `LocationCounter`.
    - **Process**:
        - Calculate displacement: `displacement = target_address - (current_address + 3)`
            - `+3` accounts for the length of the instruction.
        - Check if displacement is within `-2048` to `+2047` (12-bit signed).
            - If yes, set `p` flag to `1` for PC-relative.
        - If not, check if base-relative addressing can be used:
            - Calculate base displacement: `displacement = target_address - base_register_value`
            - Check if displacement is within `0` to `4095` (12-bit unsigned).
                - If yes, set `b` flag to `1` for base-relative.
        - If neither, return `None` indicating displacement out of range.
    - **Returns**:
        - Displacement as an integer or `None` if out of range.

- `check_address_range(self, displacement, format_type)`
    - **Description**: Checks if the displacement is within the allowable range for the instruction format.
    - **Parameters**:
        - `displacement`: The calculated displacement value.
        - `format_type`: The instruction format (3 or 4).
    - **Process**:
        - For format 3:
            - Displacement must be within `-2048` to `+2047`.
        - For format 4:
            - Address must fit within 20 bits.
        - If the displacement/address is out of range, log an error.
    - **Returns**:
        - `True` if within range, `False` otherwise.

- `detect_illegal_addressing(self, source_line, opcode_info)`
    - **Description**: Detects illegal addressing modes for the given instruction and logs errors.
    - **Parameters**:
        - `source_line`: Instance of `SourceCodeLine`.
        - `opcode_info`: Dictionary containing opcode details.
    - **Process**:
        - Determine the addressing mode used in `source_line`.
        - Check if the addressing mode is allowed for the instruction based on `opcode_info`.
        - If not allowed, log an error.
    - **Returns**:
        - `None` (logs errors internally).

- `encode_object_code(self, opcode, nixbpe_flags, displacement, format_type)`
    - **Description**: Encodes the final object code based on opcode, flags, and displacement.
    - **Parameters**:
        - `opcode`: The opcode value as an integer.
        - `nixbpe_flags`: List of flags `[n, i, x, b, p, e]`.
        - `displacement`: The displacement value as an integer.
        - `format_type`: The instruction format (3 or 4).
    - **Process**:
        - Convert opcode to binary (6 bits).
        - Combine `nixbpe_flags` into binary (6 bits).
        - Convert displacement to binary:
            - Format 3: 12 bits.
            - Format 4: 20 bits.
        - Concatenate all parts into a single binary string.
        - Convert the binary string to a hexadecimal string.
        - Pad with leading zeros if necessary to match the required length.
    - **Returns**:
        - Encoded object code as a hexadecimal string.

- `set_base_register(self, register)`
    - **Description**: Sets the base register value for base-relative addressing.
    - **Parameters**:
        - `register`: The register name as a string (e.g., `'B'`).
    - **Process**:
        - Retrieve the register's value from `REGISTER_CODES`.
        - Set `base_register_value` to the symbol table's value for the register.
        - Log the action.
    - **Returns**:
        - `None`.

- `unset_base_register(self)`
    - **Description**: Unsets the base register value, disabling base-relative addressing.
    - **Parameters**:
        - None.
    - **Process**:
        - Set `base_register_value` to `None`.
        - Log the action.
    - **Returns**:
        - `None`.

- `generate_object_code_for_literal(self, literal)`
    - **Description**: Generates object code for a literal.
    - **Parameters**:
        - `literal`: Instance of a Literal (from `LiteralTableList`).
    - **Process**:
        - Determine the type of literal (e.g., character, hexadecimal).
        - Convert the literal to its hexadecimal representation.
        - Return the object code.
    - **Returns**:
        - Object code as a hexadecimal string.

### Implementation Details
#### Instruction Formats
- **Format 1**:
    - **Length**: 1 byte.
    - **Object Code**: Opcode only.
    - **Example**: `FIX` → Opcode: `C4` → Object Code: `C4`.

- **Format 2**:
    - **Length**: 2 bytes.
    - **Object Code**: Opcode + Register codes.
    - **Registers**: Encoded using predefined codes (e.g., A=0, X=1, L=2, etc.).
    - **Example**: `ADDR A, X` → Opcode: `90` + `1` (A) + `0` (X) → Object Code: `9010`.

- **Format 3**:
    - **Length**: 3 bytes.
    - **Object Code**: Opcode (6 bits) + `nixbpe` flags (6 bits) + displacement (12 bits).
    - **Addressing Modes**:
        - **PC-relative**: `p` flag set.
        - **Base-relative**: `b` flag set.
    - **Displacement Range**: `-2048` to `+2047`.
    - **Example**: `LDA ALPHA` → Opcode: `00` + flags + displacement.

- **Format 4**:
    - **Length**: 4 bytes.
    - **Object Code**: Opcode (6 bits) + `nixbpe` flags (6 bits) + address (20 bits).
    - **Addressing Mode**: Extended (`e` flag set).
    - **Example**: `+JSUB SUBROUTINE` → Opcode: `48` + flags + address.

#### Addressing Modes
- **Immediate Addressing** (`#`):
    - Operand is a constant or an expression.
    - `n` (indirect bit) = `0`, `i` (immediate bit) = `1`.
    - Example: `LDA #5`.

- **Indirect Addressing** (`@`):
    - Operand is a memory address.
    - `n` = `1`, `i` = `0`.
    - Example: `LDA @BUFFER`.

- **Simple (Direct) Addressing** (no prefix):
    - Operand is a symbol or address.
    - `n` = `1`, `i` = `1`.
    - Example: `LDA BUFFER`.

- **Indexed Addressing** (`,X`):
    - Uses index register X.
    - `x` (index bit) = `1`.
    - Example: `LDA BUFFER,X`.

- **Extended Format** (`+`):
    - Indicates format 4 instruction.
    - `e` (extended bit) = `1`.
    - Example: `+JSUB SUBROUTINE`.

#### Error Checking
- **Undefined Symbols**:
    - If a symbol is not found in the `symbol_table`, log an error: `"Undefined symbol '{operand}' at line {line_number}."`
    - Mark the `source_line` as having errors.

- **Illegal Addressing Modes**:
    - If an addressing mode is not allowed for an instruction based on `opcode_info`, log an error: `"Illegal addressing mode for instruction '{opcode}' at line {line_number}."`

- **Address Out of Range**:
    - If displacement or address cannot be encoded in the instruction format, log an error: `"Displacement out of range for operand '{operand}' at line {line_number}."`
    - Suggest using format 4 or base-relative addressing if possible.

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
#### LocationCounter
- **Purpose**:
    - Manages the current address (`LOCCTR`) and program length.
    - Verifies address consistency and updates addresses based on instruction lengths.
- **Interaction**:
    - `ObjectCodeGenerator` uses `location_counter.get_current_address_int()` to verify and manage addresses.
    - After generating object code, `ObjectCodeGenerator` updates the `location_counter` with `location_counter.increment_by_decimal(instruction_length)`.
#### ObjectProgramWriter
- **Purpose**:
    - Assembles the final object program by combining the header record, text records, modification records, and end record.
    - Writes the object program to an output file.
- **Interaction**:
    - Once code generation is complete, `ObjectCodeGenerator` provides the header record, text records (from `text_record_manager`), modification records (from `modification_record_manager`), and end record to `ObjectProgramWriter`.
    - `ObjectProgramWriter` assembles these components and writes them to the file.

### Detailed Method Descriptions
#### generate_object_code(self, source_lines)
- **Process**:
    1. Initialize `current_address` using `location_counter.get_current_address_int()`.
    2. Iterate over each `source_line` in `source_lines`.
        - If `source_line` is a comment or has errors, skip processing.
        - If `source_line` is an instruction, call `generate_object_code_for_line(source_line)`.
        - If `source_line` is a directive, handle it outside this method (managed by `AssemblerPass2`).
        - After processing, update `current_address` based on instruction length using `location_counter.increment_by_decimal(instruction_length)`.
#### generate_object_code_for_line(self, source_line)
- **Process**:
    1. Retrieve opcode mnemonic from `source_line`.
    2. Use `opcode_handler` to get `opcode_info` (opcode value, instruction format, allowed addressing modes).
    3. Call `detect_illegal_addressing(source_line, opcode_info)`.
        - If illegal addressing is detected, log an error and return `None`.
    4. Based on instruction format, call the corresponding handler:
        - Format 1: `handle_format1(source_line, opcode_info)`
        - Format 2: `handle_format2(source_line, opcode_info)`
        - Format 3: `handle_format3(source_line, opcode_info)`
        - Format 4: `handle_format4(source_line, opcode_info)`
    5. If object code is generated, add it to the text record:
        - `text_record_manager.add_object_code(source_line.address, object_code)`
    6. If the instruction requires modification (e.g., format 4), add a modification record:
        - `modification_record_manager.add_modification(address, length)`
    7. Return the generated `object_code`.
#### handle_format1(self, source_line, opcode_info)
- **Process**:
    1. Object code is simply the opcode.
    2. Convert opcode to a two-digit hexadecimal string.
    3. Return the object code.
- **Example**:
    - `FIX` → Opcode: `C4` → Object Code: `'C4'`.

#### handle_format2(self, source_line, opcode_info)
- **Process**:
    1. Parse register operands from `source_line`.
        - Example: `ADDR A, X` → Registers: `A`, `X`.
    2. Use predefined register codes (e.g., A=0, X=1, L=2, etc.).
    3. Encode the object code as `opcode + reg1_code + reg2_code`.
        - Format: `Opcode (1 byte) + Register1 (4 bits) + Register2 (4 bits)`.
    4. Convert to a four-digit hexadecimal string.
    5. Return the object code.
- **Example**:
    - `ADDR A, X` → Opcode: `90` + `1` (A) + `0` (X) → Object Code: `'9010'`.

#### handle_format3(self, source_line, opcode_info)
- **Process**:
    1. Initialize `nixbpe_flags` to `[1, 1, 0, 0, 0, 0]` for simple addressing (`n=1`, `i=1`, `x=0`, `b=0`, `p=0`, `e=0`).
    2. Process addressing modes:
        - **Immediate** (`#`): Set `n=0`, `i=1`.
        - **Indirect** (`@`): Set `n=1`, `i=0`.
        - **Indexed** (`,X`): Set `x=1`.
    3. Resolve operand to obtain `target_address` using `resolve_operand`.
        - If operand is undefined, log an error and return `None`.
    4. Calculate displacement using `calculate_displacement(target_address, current_address)`.
        - If displacement is `None` (out of range), log an error and return `None`.
        - If PC-relative, set `p=1`.
        - If base-relative, set `b=1`.
    5. Check if displacement is within range using `check_address_range`.
        - If not, log an error and return `None`.
    6. Encode the object code with opcode, flags, and displacement using `encode_object_code`.
    7. Return the generated object code.
- **Example**:
    - `LDA ALPHA` → Opcode: `00` + `nixbpe` flags + `displacement` → Object Code: `'001A3F'`.
#### handle_format4(self, source_line, opcode_info)
- **Process**:
    1. Set the `e` flag to `1` to indicate extended format.
    2. Initialize `nixbpe_flags` to `[1, 1, 0, 0, 0, 1]` (`n=1`, `i=1`, `x=0`, `b=0`, `p=0`, `e=1`).
    3. Resolve operand to obtain `target_address` using `resolve_operand`.
        - If operand is undefined, log an error and return `None`.
    4. Check if the address fits within 20 bits:
        - If not, log an error and return `None`.
    5. Encode the object code with opcode, flags, and address using `encode_object_code`.
    6. Add a modification record to handle relocations:
        - `modification_record_manager.add_modification(address + 1, 5)` (assuming address increments appropriately).
    7. Return the generated object code.
- **Example**:
    - `+JSUB SUBROUTINE` → Opcode: `48` + `nixbpe` flags + `address` → Object Code: `'4C000036'`.
#### resolve_operand(self, operand, current_address)
- **Process**:
    1. Check if the operand is a literal (starts with `=`):
        - Retrieve the address from `literal_table`.
    2. Check if the operand is a symbol:
        - Retrieve the address from `symbol_table`.
    3. Check if the operand is an immediate value (numeric):
        - Convert to integer.
    4. Handle expressions (e.g., `SYMBOL + 5`):
        - Evaluate using `symbol_table`.
    5. Determine relocation info:
        - `'A'` for absolute.
        - `'R'` for relocatable.
    6. Return the resolved address/value and relocation info.
- **Returns**:
    - Tuple containing `(resolved_value: int, relocation: str)`.
#### calculate_displacement(self, target_address, current_address)
- **Process**:
    1. Calculate displacement: `displacement = target_address - (current_address + 3)`
        - `+3` accounts for the length of the instruction.
    2. Check if displacement is within `-2048` to `+2047` (12-bit signed).
        - If yes, set `p` flag to `1` for PC-relative.
    3. If not, check if base-relative addressing can be used:
        - Calculate base displacement: `displacement = target_address - base_register_value`.
        - Check if displacement is within `0` to `4095` (12-bit unsigned).
            - If yes, set `b` flag to `1` for base-relative.
    4. If neither, return `None` indicating displacement out of range.
    5. Return the displacement value.
- **Returns**:
    - Displacement as an integer or `None` if out of range.
#### check_address_range(self, displacement, format_type)
- **Process**:
    1. For format 3:
        - Displacement must be within `-2048` to `+2047`.
    2. For format 4:
        - Address must fit within 20 bits (`0` to `1048575`).
    3. If the displacement/address is out of range, log an error.
    4. Return `True` if within range, `False` otherwise.
- **Returns**:
    - `True` if within range, `False` otherwise.
#### detect_illegal_addressing(self, source_line, opcode_info)
- **Process**:
    1. Determine the addressing mode used in `source_line` (e.g., immediate, indirect).
    2. Check if the addressing mode is allowed for the instruction based on `opcode_info`.
    3. If not allowed, log an error: `"Illegal addressing mode for instruction '{opcode}' at line {line_number}."`
    4. Mark the `source_line` as having errors.
    5. Return `None` (errors are logged internally).
#### encode_object_code(self, opcode, nixbpe_flags, displacement, format_type)
- **Process**:
    1. Convert opcode to binary (6 bits): `opcode_bin = format(opcode, '06b')`.
    2. Combine `nixbpe_flags` into binary (6 bits): `flags_bin = ''.join(str(flag) for flag in nixbpe_flags)`.
    3. Convert displacement to binary:
        - Format 3: 12 bits.
        - Format 4: 20 bits.
        - Handle signed displacement for format 3.
    4. Concatenate all parts into a single binary string: `object_code_bin = opcode_bin + flags_bin + displacement_bin`.
    5. Convert the binary string to a hexadecimal string: `object_code_hex = format(int(object_code_bin, 2), 'X')`.
    6. Pad with leading zeros if necessary to match the required length:
        - Format 3: 6 hexadecimal digits.
        - Format 4: 8 hexadecimal digits.
    7. Return the encoded object code.
- **Returns**:
    - Encoded object code as a hexadecimal string.

#### set_base_register(self, register)
- **Process**:
    1. Validate the register name against `REGISTER_CODES`.
        - If invalid, log an error and return `None`.
    2. Retrieve the address/value of the register from `symbol_table`.
    3. Set `base_register_value` to the retrieved address.
    4. Log the action: `"Base register set to {register} with value {value:X}."`
    5. Return `None`.
#### unset_base_register(self)
- **Process**:
    1. Set `base_register_value` to `None`.
    2. Log the action: `"Base register unset."`
    3. Return `None`.
#### generate_object_code_for_literal(self, literal)
- **Process**:
    1. Determine the type of literal (e.g., character, hexadecimal).
    2. Convert the literal to its hexadecimal representation.
        - For character literals (`=C'EOF'`), convert each character to its ASCII hexadecimal value.
        - For hexadecimal literals (`=X'F1'`), use the provided value.
    3. Return the object code.
- **Returns**:
    - Object code as a hexadecimal string.
### Error Handling
- **Undefined Symbols**:
    - When an operand cannot be resolved, log an error: `"Undefined symbol '{operand}' at line {line_number}."`
    - Mark the `source_line` as having errors to skip object code generation.

- **Illegal Addressing Modes**:
    - If the addressing mode is not allowed for the instruction, log an error: `"Illegal addressing mode for instruction '{opcode}' at line {line_number}."`
    - Mark the `source_line` as having errors to skip object code generation.

- **Address Out of Range**:
    - If displacement cannot be encoded in the instruction format, log an error: `"Displacement out of range for operand '{operand}' at line {line_number}."`
    - Suggest using format 4 or base-relative addressing if possible.

- **Invalid Operands**:
    - If operands are missing or incorrect, log an error: `"Invalid operands for instruction '{opcode}' at line {line_number}."`
    - Mark the `source_line` as having errors to skip object code generation.
### 9. Finalization and Output
- **After Processing All Lines**:
    1. Generate the header record:
        - Program name, starting address, program length.
    2. Generate the end record:
        - Address of the first executable instruction.
    3. Provide all records to `ObjectProgramWriter`:
        - `header_record`
        - `text_records` from `text_record_manager`
        - `modification_records` from `modification_record_manager`
        - `end_record`
    4. `ObjectProgramWriter` assembles these components and writes them to the output file.
### 10. Pseudocode Example
Below is a detailed pseudocode example for the updated `ObjectCodeGenerator` class, incorporating the `LocationCounter`.

```python
class ObjectCodeGenerator:
    """
    Translates assembly instructions into machine code (object code).
    Resolves symbols and literals, handles different instruction formats and addressing modes,
    manages the location counter, and performs error checking.
    """
    
    def __init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter):
        """
        Initializes the ObjectCodeGenerator with necessary references.
        
        :param symbol_table: Instance of SymbolTable.
        :param literal_table: Instance of LiteralTableList.
        :param opcode_handler: Instance of OpcodeHandler.
        :param error_handler: Instance of ErrorLogHandler.
        :param location_counter: Instance of LocationCounter.
        """
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_handler = opcode_handler
        self.error_handler = error_handler
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        self.location_counter = location_counter
        self.base_register_value = None
        self.nixbpe_flags = [0, 0, 0, 0, 0, 0]  # [n, i, x, b, p, e]
    
    def generate_object_code(self, source_lines):
        """
        Generates object code for all source lines.
        
        :param source_lines: List of SourceCodeLine instances.
        """
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_instruction():
                object_code = self.generate_object_code_for_line(source_line)
                if object_code:
                    self.text_record_manager.add_object_code(source_line.address, object_code)
                    if self.requires_modification(source_line):
                        modification_offset, modification_length = self.get_modification_details(source_line)
                        self.modification_record_manager.add_modification(
                            address=source_line.address + modification_offset,
                            length=modification_length
                        )
            # Directives are handled by AssemblerPass2
    
    def generate_object_code_for_line(self, source_line):
        """
        Generates object code for a single source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            self.error_handler.log_error(f"Undefined opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Detect illegal addressing
        self.detect_illegal_addressing(source_line, opcode_info)
        if source_line.has_errors():
            return None
        
        # Handle based on instruction format
        format_type = opcode_info['format']
        if format_type == 1:
            object_code = self.handle_format1(source_line, opcode_info)
        elif format_type == 2:
            object_code = self.handle_format2(source_line, opcode_info)
        elif format_type == 3:
            object_code = self.handle_format3(source_line, opcode_info)
        elif format_type == 4:
            object_code = self.handle_format4(source_line, opcode_info)
        else:
            self.error_handler.log_error(f"Unsupported instruction format '{format_type}' for opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        return object_code
    
    def handle_format1(self, source_line, opcode_info):
        """
        Handles format 1 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string.
        """
        opcode = opcode_info['opcode']
        object_code = f"{opcode:02X}"
        return object_code
    
    def handle_format2(self, source_line, opcode_info):
        """
        Handles format 2 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string.
        """
        opcode = opcode_info['opcode']
        operands = source_line.operands.split(',')
        if len(operands) != 2:
            self.error_handler.log_error(f"Incorrect number of registers for format 2 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        reg1 = operands[0].strip().upper()
        reg2 = operands[1].strip().upper()
        reg1_code = self.validate_register(reg1, source_line)
        reg2_code = self.validate_register(reg2, source_line)
        if reg1_code is None or reg2_code is None:
            return None
        object_code = f"{opcode:02X}{reg1_code:X}{reg2_code:X}"
        return object_code
    
    def handle_format3(self, source_line, opcode_info):
        """
        Handles format 3 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags
        self.nixbpe_flags = [1, 1, 0, 0, 0, 0]  # Default: simple addressing
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # Calculate displacement
        displacement = self.calculate_displacement(resolved_value, current_address)
        if displacement is None:
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Check address range
        if not self.check_address_range(displacement, 3):
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 3)
        return object_code
    
    def handle_format4(self, source_line, opcode_info):
        """
        Handles format 4 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags for extended format
        self.nixbpe_flags = [1, 1, 0, 0, 0, 1]  # e=1
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # For format 4, address is absolute or relocatable
        displacement = resolved_value
        
        # Check address range for format 4 (20 bits)
        if displacement < 0 or displacement > 0xFFFFF:
            self.error_handler.log_error(f"Address out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 4)
        
        # Add modification record for relocation
        self.modification_record_manager.add_modification(
            address=current_address + 1,  # Assuming the address starts at the next byte
            length=5  # Number of half-bytes to modify
        )
        
        return object_code
    
    def resolve_operand(self, operand, current_address):
        """
        Resolves an operand to its address or value.
        
        :param operand: Operand string.
        :param current_address: Current address from LocationCounter.
        :return: Tuple (resolved_value, relocation_info)
        """
        relocation_info = 'A'  # Default to absolute
        
        if operand.startswith('='):
            # Literal
            literal = self.literal_table.get_literal(operand)
            if not literal:
                self.error_handler.log_error(f"Literal '{operand}' not found in literal table.")
                return (None, None)
            resolved_value = literal.address
            relocation_info = 'R'
        elif operand.isdigit():
            # Immediate numeric value
            resolved_value = int(operand)
        else:
            # Symbol
            symbol = self.symbol_table.get_symbol(operand)
            if not symbol:
                return (None, None)
            resolved_value = symbol.value
            relocation_info = 'R' if symbol.is_relocatable else 'A'
        
        return (resolved_value, relocation_info)
    
    def calculate_displacement(self, target_address, current_address):
        """
        Calculates displacement for format 3 instructions.
        
        :param target_address: The resolved address of the operand.
        :param current_address: The current address from LocationCounter.
        :return: Displacement as an integer or None if out of range.
        """
        displacement = target_address - (current_address + 3)
        
        if -2048 <= displacement <= 2047:
            # PC-relative addressing
            self.nixbpe_flags[4] = 1  # Set p flag
            return displacement & 0xFFF  # 12-bit signed
        elif self.base_register_value is not None:
            displacement = target_address - self.base_register_value
            if 0 <= displacement <= 4095:
                # Base-relative addressing
                self.nixbpe_flags[3] = 1  # Set b flag
                return displacement
        return None
    
    def check_address_range(self, displacement, format_type):
        """
        Checks if the displacement is within the allowable range for the instruction format.
        
        :param displacement: The calculated displacement value.
        :param format_type: The instruction format (3 or 4).
        :return: True if within range, False otherwise.
        """
        if format_type == 3:
            return -2048 <= displacement <= 4095  # Considering both PC and base-relative
        elif format_type == 4:
            return 0 <= displacement <= 0xFFFFF  # 20-bit address
        return False
    
    def detect_illegal_addressing(self, source_line, opcode_info):
        """
        Detects illegal addressing modes for the given instruction.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        """
        operand = source_line.operands
        addressing_mode = self.identify_addressing_mode(operand)
        allowed_modes = opcode_info.get('allowed_addressing_modes', [])
        
        if addressing_mode not in allowed_modes:
            self.error_handler.log_error(f"Illegal addressing mode '{addressing_mode}' for instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            source_line.mark_error()
    
    def identify_addressing_mode(self, operand):
        """
        Identifies the addressing mode based on the operand prefix/suffix.
        
        :param operand: Operand string.
        :return: Addressing mode as a string ('immediate', 'indirect', 'simple', 'indexed').
        """
        if operand.startswith('#'):
            return 'immediate'
        elif operand.startswith('@'):
            return 'indirect'
        elif ',X' in operand.upper():
            return 'indexed'
        else:
            return 'simple'
    
    def process_addressing_modes(self, operand, flags, source_line):
        """
        Processes the addressing modes and sets the nixbpe flags accordingly.
        
        :param operand: Operand string.
        :param flags: List of nixbpe flags.
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (processed_operand, flags)
        """
        operand = operand.strip()
        
        # Immediate addressing
        if operand.startswith('#'):
            flags[0] = 0  # n
            flags[1] = 1  # i
            operand = operand[1:].strip()
        
        # Indirect addressing
        elif operand.startswith('@'):
            flags[0] = 1  # n
            flags[1] = 0  # i
            operand = operand[1:].strip()
        
        # Simple addressing
        else:
            flags[0] = 1  # n
            flags[1] = 1  # i
        
        # Indexed addressing
        if ',X' in operand.upper():
            flags[2] = 1  # x
            operand = operand.upper().replace(',X', '').strip()
        
        return (operand, flags)
    
    def encode_object_code(self, opcode, flags, displacement, format_type):
        """
        Encodes the final object code based on opcode, flags, and displacement.
        
        :param opcode: Opcode as an integer.
        :param flags: List of nixbpe flags.
        :param displacement: Displacement value as an integer.
        :param format_type: Instruction format (3 or 4).
        :return: Encoded object code as a hexadecimal string.
        """
        # Convert opcode to binary (6 bits)
        opcode_bin = format(opcode, '06b')
        
        # Convert nixbpe flags to binary (6 bits)
        flags_bin = ''.join(str(flag) for flag in flags)
        
        # Convert displacement to binary
        if format_type == 3:
            displacement_bin = format(displacement & 0xFFF, '012b')  # 12 bits
        elif format_type == 4:
            displacement_bin = format(displacement, '020b')  # 20 bits
        else:
            displacement_bin = '0' * 12  # Default
        
        # Concatenate all parts
        object_code_bin = opcode_bin + flags_bin + displacement_bin
        
        # Convert binary to hexadecimal
        object_code_hex = format(int(object_code_bin, 2), 'X').upper()
        
        # Pad with leading zeros
        if format_type == 3:
            object_code_hex = object_code_hex.zfill(6)
        elif format_type == 4:
            object_code_hex = object_code_hex.zfill(8)
        
        return object_code_hex
    
    def validate_register(self, register, source_line):
        """
        Validates the register name and returns its code.
        
        :param register: Register name as a string.
        :param source_line: Instance of SourceCodeLine.
        :return: Register code as an integer or None if invalid.
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid register '{register}' at line {source_line.line_number}.")
            source_line.mark_error()
            return None
        return REGISTER_CODES[register]
    
    def set_base_register(self, register):
        """
        Sets the base register value for base-relative addressing.
        
        :param register: Register name as a string (e.g., 'B').
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid base register '{register}'.")
            return
        symbol = register  # Assuming register symbols are defined in the symbol table
        symbol_entry = self.symbol_table.get_symbol(symbol)
        if not symbol_entry:
            self.error_handler.log_error(f"Symbol for base register '{register}' not found in symbol table.")
            return
        self.base_register_value = symbol_entry.value
        self.error_handler.log_action(f"Base register set to {register} with value {self.base_register_value:X}.")
    
    def unset_base_register(self):
        """
        Unsets the base register value, disabling base-relative addressing.
        """
        self.base_register_value = None
        self.error_handler.log_action("Base register unset.")
    
    def generate_object_code_for_literal(self, literal):
        """
        Generates object code for a literal.
        
        :param literal: Instance of a Literal (from LiteralTableList).
        :return: Object code as a hexadecimal string.
        """
        if literal.type == 'C':
            # Convert each character to its ASCII hexadecimal value
            object_code = ''.join([format(ord(char), '02X') for char in literal.value])
        elif literal.type == 'X':
            # Use the hexadecimal value directly
            object_code = literal.value.upper()
        else:
            self.error_handler.log_error(f"Unsupported literal type '{literal.type}' for literal '{literal.name}'.")
            return None
        return object_code
    
    def requires_modification(self, source_line):
        """
        Determines if the instruction requires a modification record.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Boolean indicating if modification is required.
        """
        # Typically, format 4 instructions require modification
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            return False
        return opcode_info['format'] == 4
    
    def get_modification_details(self, source_line):
        """
        Retrieves modification details for a source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (modification_offset, modification_length).
        """
        # Assuming the modification occurs at the address after the opcode byte
        # and spans the next 5 half-bytes (20 bits)
        modification_offset = 1  # Address offset where modification starts
        modification_length = 5  # Number of half-bytes to modify
        return (modification_offset, modification_length)
```

### 5. Integration with `LocationCounter`

The integration of `LocationCounter` into the `ObjectCodeGenerator` ensures accurate address tracking and validation throughout the object code generation process. Here's how the integration impacts various parts of the `ObjectCodeGenerator`:

#### a. **Address Verification**
Before generating object code for a `SourceCodeLine`, verify that the `address` in the `SourceCodeLine` matches the current address from `LocationCounter`. This ensures consistency between Pass 1 and Pass 2.

```python
def generate_object_code_for_line(self, source_line):
    # Verify address consistency
    expected_address = self.location_counter.get_current_address_int()
    if source_line.address != expected_address:
        self.error_handler.log_error(
            f"Address mismatch at line {source_line.line_number}: expected {expected_address:X}, found {source_line.address:X}."
        )
        source_line.mark_error()
        return None
    # Proceed with object code generation
    # ...
```
#### b. **Updating `LocationCounter`**
After successfully generating object code for a line, update the `LocationCounter` to reflect the new current address.
```python
def generate_object_code_for_line(self, source_line):
    # ... [object code generation logic] ...
    
    if object_code:
        # Add object code to text record
        self.text_record_manager.add_object_code(source_line.address, object_code)
        
        # Update LocationCounter based on instruction length
        instruction_length = source_line.instruction_length  # Assuming this attribute exists
        self.location_counter.increment_by_decimal(instruction_length)
        
        # Handle modification records if necessary
        if self.requires_modification(source_line):
            modification_offset, modification_length = self.get_modification_details(source_line)
            self.modification_record_manager.add_modification(
                address=source_line.address + modification_offset,
                length=modification_length
            )
    else:
        # Log error if object code could not be generated
        self.error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
```
#### c. **Handling Directives Affecting Addresses**
Directives such as `LTORG` assign addresses to literals and require updating the `LocationCounter`. The `ObjectCodeGenerator` interacts with the `LocationCounter` during the processing of these directives.

```python
def handle_format4(self, source_line, opcode_info):
    # ... [object code generation logic] ...
    
    if object_code:
        # Add object code to text record
        self.text_record_manager.add_object_code(source_line.address, object_code)
        
        # Update LocationCounter
        instruction_length = 4  # Format 4 instructions are 4 bytes
        self.location_counter.increment_by_decimal(instruction_length)
        
        # Add modification record
        if self.requires_modification(source_line):
            modification_offset, modification_length = self.get_modification_details(source_line)
            self.modification_record_manager.add_modification(
                address=source_line.address + modification_offset,
                length=modification_length
            )
```

### 6. Example Workflow Incorporating `LocationCounter`
1. **Initialization**:
    - `AssemblerPass2` initializes all components, including `LocationCounter`.
    - `LocationCounter` is set with the starting address from the `START` directive.
2. **Generating Object Code**:
    - For each `SourceCodeLine`, `ObjectCodeGenerator`:
        - Verifies address consistency with `LocationCounter`.
        - Generates object code based on instruction format and addressing mode.
        - Adds object code to `TextRecordManager`.
        - Updates `LocationCounter` with the instruction length.
        - Adds modification records if necessary.
3. **Handling Directives**:
    - Directives like `LTORG` assign addresses to literals, and `ObjectCodeGenerator`:
        - Generates object code for literals.
        - Adds object codes to `TextRecordManager`.
        - Updates `LocationCounter` based on literal lengths.
4. **Finalization**:
    - After processing all lines, `AssemblerPass2`:
        - Finalizes all text records.
        - Creates header and end records using `LocationCounter` to determine program length.
        - Passes all records to `ObjectProgramWriter` for assembling the final object program.
5. **Writing Output**:
    - `ObjectProgramWriter` assembles and writes the object program to the output file.

### 7. Enhanced Error Handling with `LocationCounter`
Integrating `LocationCounter` allows for more robust error detection related to address management:
- **Address Mismatches**:
    - Detect discrepancies between expected and actual addresses in the intermediate file.
    - Log errors specifying the expected and found addresses.
- **Overflows**:
    - Ensure that `LocationCounter` does not exceed address space limits.
    - Log errors if the program exceeds memory constraints.
- **Directive Errors**:
    - Handle errors arising from incorrect usage of directives that affect addresses (e.g., invalid `BASE` register settings).

### 8. Code Example
Below is an example implementation snippet showcasing the integration of `LocationCounter` within the `ObjectCodeGenerator` class.

```python
class ObjectCodeGenerator:
    def __init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter):
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_handler = opcode_handler
        self.error_handler = error_handler
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        self.location_counter = location_counter
        self.base_register_value = None
        self.nixbpe_flags = [0, 0, 0, 0, 0, 0]  # [n, i, x, b, p, e]
    
    def generate_object_code_for_line(self, source_line):
        # Verify address consistency
        expected_address = self.location_counter.get_current_address_int()
        if source_line.address != expected_address:
            self.error_handler.log_error(
                f"Address mismatch at line {source_line.line_number}: expected {expected_address:X}, found {source_line.address:X}."
            )
            source_line.mark_error()
            return None
        
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            self.error_handler.log_error(f"Undefined opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Detect illegal addressing
        self.detect_illegal_addressing(source_line, opcode_info)
        if source_line.has_errors():
            return None
        
        # Handle based on instruction format
        format_type = opcode_info['format']
        if format_type == 1:
            object_code = self.handle_format1(source_line, opcode_info)
        elif format_type == 2:
            object_code = self.handle_format2(source_line, opcode_info)
        elif format_type == 3:
            object_code = self.handle_format3(source_line, opcode_info)
        elif format_type == 4:
            object_code = self.handle_format4(source_line, opcode_info)
        else:
            self.error_handler.log_error(f"Unsupported instruction format '{format_type}' for opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Add object code to text record
        self.text_record_manager.add_object_code(source_line.address, object_code)
        
        # Update LocationCounter based on instruction length
        instruction_length = source_line.instruction_length  # Assuming this attribute exists
        self.location_counter.increment_by_decimal(instruction_length)
        
        # Handle modification records if necessary
        if self.requires_modification(source_line):
            modification_offset, modification_length = self.get_modification_details(source_line)
            self.modification_record_manager.add_modification(
                address=source_line.address + modification_offset,
                length=modification_length
            )
        
        return object_code
```

### 9. Testing the `ObjectCodeGenerator`

To ensure the `ObjectCodeGenerator` functions correctly with `LocationCounter`, implement the following test cases:
#### a. **Address Consistency**
- **Test Case**: Intermediate file has sequential addresses matching `LocationCounter`.
- **Expected Outcome**: Object codes are generated without address mismatch errors.
#### b. **Address Mismatch Detection**
- **Test Case**: Intermediate file contains a line with an address that does not match `LocationCounter`.
- **Expected Outcome**: Error is logged specifying the expected and found addresses.
#### c. **Displacement Calculation**
- **Test Case**: Operand displacement within range for PC-relative and base-relative addressing.
- **Expected Outcome**: Correct displacement is calculated, and appropriate flags are set.

- **Edge Case**: Operand displacement out of range.
- **Expected Outcome**: Error is logged indicating displacement out of range.
#### d. **Format Handling**
- **Test Case**: Instructions of all formats (1 to 4).
- **Expected Outcome**: Object codes are correctly generated for each format.
#### e. **Addressing Modes**
- **Test Case**: Instructions using various addressing modes (immediate, indirect, indexed).
- **Expected Outcome**: Flags are correctly set, and object codes reflect addressing modes.
#### f. **Base Register Usage**
- **Test Case**: Instructions requiring base-relative addressing with `BASE` directive set.
- **Expected Outcome**: Displacement is calculated relative to base register, and `b` flag is set.

- **Edge Case**: `BASE` register not set when required.
- **Expected Outcome**: Error is logged, and displacement calculation fails.
#### g. **Literal Handling**
- **Test Case**: Instructions referencing literals.
- **Expected Outcome**: Object codes for literals are correctly generated and added to text records.
### 10. Documentation and Code Comments
Ensure that all methods within the `ObjectCodeGenerator` class are well-documented with clear docstrings and inline comments explaining their purpose, parameters, and logic. This practice facilitates maintenance and future enhancements.

```python
class ObjectCodeGenerator:
    """
    Translates assembly instructions into machine code (object code).
    Resolves symbols and literals, handles different instruction formats and addressing modes,
    manages the location counter, and performs error checking.
    """
    
    def __init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter):
        """
        Initializes the ObjectCodeGenerator with necessary references.
        
        :param symbol_table: Instance of SymbolTable.
        :param literal_table: Instance of LiteralTableList.
        :param opcode_handler: Instance of OpcodeHandler.
        :param error_handler: Instance of ErrorLogHandler.
        :param location_counter: Instance of LocationCounter.
        """
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_handler = opcode_handler
        self.error_handler = error_handler
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        self.location_counter = location_counter
        self.base_register_value = None
        self.nixbpe_flags = [0, 0, 0, 0, 0, 0]  # [n, i, x, b, p, e]
    
    def generate_object_code(self, source_lines):
        """
        Generates object code for all source lines.
        
        :param source_lines: List of SourceCodeLine instances.
        """
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_instruction():
                object_code = self.generate_object_code_for_line(source_line)
                if object_code:
                    self.text_record_manager.add_object_code(source_line.address, object_code)
                    if self.requires_modification(source_line):
                        modification_offset, modification_length = self.get_modification_details(source_line)
                        self.modification_record_manager.add_modification(
                            address=source_line.address + modification_offset,
                            length=modification_length
                        )
            # Directives are handled by AssemblerPass2
    
    def generate_object_code_for_line(self, source_line):
        """
        Generates object code for a single source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        # Verify address consistency
        expected_address = self.location_counter.get_current_address_int()
        if source_line.address != expected_address:
            self.error_handler.log_error(
                f"Address mismatch at line {source_line.line_number}: expected {expected_address:X}, found {source_line.address:X}."
            )
            source_line.mark_error()
            return None
        
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            self.error_handler.log_error(f"Undefined opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Detect illegal addressing
        self.detect_illegal_addressing(source_line, opcode_info)
        if source_line.has_errors():
            return None
        
        # Handle based on instruction format
        format_type = opcode_info['format']
        if format_type == 1:
            object_code = self.handle_format1(source_line, opcode_info)
        elif format_type == 2:
            object_code = self.handle_format2(source_line, opcode_info)
        elif format_type == 3:
            object_code = self.handle_format3(source_line, opcode_info)
        elif format_type == 4:
            object_code = self.handle_format4(source_line, opcode_info)
        else:
            self.error_handler.log_error(f"Unsupported instruction format '{format_type}' for opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Add object code to text record
        self.text_record_manager.add_object_code(source_line.address, object_code)
        
        # Update LocationCounter based on instruction length
        instruction_length = source_line.instruction_length  # Assuming this attribute exists
        self.location_counter.increment_by_decimal(instruction_length)
        
        # Handle modification records if necessary
        if self.requires_modification(source_line):
            modification_offset, modification_length = self.get_modification_details(source_line)
            self.modification_record_manager.add_modification(
                address=source_line.address + modification_offset,
                length=modification_length
            )
        
        return object_code
    
    def handle_format1(self, source_line, opcode_info):
        """
        Handles format 1 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string.
        """
        opcode = opcode_info['opcode']
        object_code = f"{opcode:02X}"
        return object_code
    
    def handle_format2(self, source_line, opcode_info):
        """
        Handles format 2 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string.
        """
        opcode = opcode_info['opcode']
        operands = source_line.operands.split(',')
        if len(operands) != 2:
            self.error_handler.log_error(f"Incorrect number of registers for format 2 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            source_line.mark_error()
            return None
        reg1 = operands[0].strip().upper()
        reg2 = operands[1].strip().upper()
        reg1_code = self.validate_register(reg1, source_line)
        reg2_code = self.validate_register(reg2, source_line)
        if reg1_code is None or reg2_code is None:
            return None
        object_code = f"{opcode:02X}{reg1_code:X}{reg2_code:X}"
        return object_code
    
    def handle_format3(self, source_line, opcode_info):
        """
        Handles format 3 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags
        self.nixbpe_flags = [1, 1, 0, 0, 0, 0]  # [n, i, x, b, p, e]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # Calculate displacement
        displacement = self.calculate_displacement(resolved_value, current_address)
        if displacement is None:
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Check address range
        if not self.check_address_range(displacement, 3):
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 3)
        return object_code
    
    def handle_format4(self, source_line, opcode_info):
        """
        Handles format 4 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags for extended format
        self.nixbpe_flags = [1, 1, 0, 0, 0, 1]  # [n, i, x, b, p, e]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # For format 4, address is absolute or relocatable
        displacement = resolved_value
        
        # Check address range for format 4 (20 bits)
        if displacement < 0 or displacement > 0xFFFFF:
            self.error_handler.log_error(f"Address out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 4)
        
        # Add modification record for relocation
        self.modification_record_manager.add_modification(
            address=current_address + 1,  # Assuming the address starts at the next byte
            length=5  # Number of half-bytes to modify
        )
        
        return object_code
    
    def resolve_operand(self, operand, current_address):
        """
        Resolves an operand to its address or value.
        
        :param operand: Operand string.
        :param current_address: Current address from LocationCounter.
        :return: Tuple (resolved_value, relocation_info)
        """
        relocation_info = 'A'  # Default to absolute
        
        if operand.startswith('='):
            # Literal
            literal = self.literal_table.get_literal(operand)
            if not literal:
                self.error_handler.log_error(f"Literal '{operand}' not found in literal table.")
                return (None, None)
            resolved_value = literal.address
            relocation_info = 'R'
        elif operand.isdigit():
            # Immediate numeric value
            resolved_value = int(operand)
        else:
            # Symbol
            symbol = self.symbol_table.get_symbol(operand)
            if not symbol:
                return (None, None)
            resolved_value = symbol.value
            relocation_info = 'R' if symbol.is_relocatable else 'A'
        
        return (resolved_value, relocation_info)
    
    def calculate_displacement(self, target_address, current_address):
        """
        Calculates displacement for format 3 instructions.
        
        :param target_address: The resolved address of the operand.
        :param current_address: The current address from LocationCounter.
        :return: Displacement as an integer or None if out of range.
        """
        displacement = target_address - (current_address + 3)
        
        if -2048 <= displacement <= 2047:
            # PC-relative addressing
            self.nixbpe_flags[4] = 1  # Set p flag
            return displacement & 0xFFF  # 12-bit signed
        elif self.base_register_value is not None:
            displacement = target_address - self.base_register_value
            if 0 <= displacement <= 4095:
                # Base-relative addressing
                self.nixbpe_flags[3] = 1  # Set b flag
                return displacement
        return None
    
    def check_address_range(self, displacement, format_type):
        """
        Checks if the displacement is within the allowable range for the instruction format.
        
        :param displacement: The calculated displacement value.
        :param format_type: The instruction format (3 or 4).
        :return: True if within range, False otherwise.
        """
        if format_type == 3:
            return -2048 <= displacement <= 4095  # Considering both PC and base-relative
        elif format_type == 4:
            return 0 <= displacement <= 0xFFFFF  # 20-bit address
        return False
    
    def detect_illegal_addressing(self, source_line, opcode_info):
        """
        Detects illegal addressing modes for the given instruction.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        """
        operand = source_line.operands
        addressing_mode = self.identify_addressing_mode(operand)
        allowed_modes = opcode_info.get('allowed_addressing_modes', [])
        
        if addressing_mode not in allowed_modes:
            self.error_handler.log_error(f"Illegal addressing mode '{addressing_mode}' for instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            source_line.mark_error()
    
    def identify_addressing_mode(self, operand):
        """
        Identifies the addressing mode based on the operand prefix/suffix.
        
        :param operand: Operand string.
        :return: Addressing mode as a string ('immediate', 'indirect', 'simple', 'indexed').
        """
        if operand.startswith('#'):
            return 'immediate'
        elif operand.startswith('@'):
            return 'indirect'
        elif ',X' in operand.upper():
            return 'indexed'
        else:
            return 'simple'
    
    def process_addressing_modes(self, operand, flags, source_line):
        """
        Processes the addressing modes and sets the nixbpe flags accordingly.
        
        :param operand: Operand string.
        :param flags: List of nixbpe flags.
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (processed_operand, flags)
        """
        operand = operand.strip()
        
        # Immediate addressing
        if operand.startswith('#'):
            flags[0] = 0  # n
            flags[1] = 1  # i
            operand = operand[1:].strip()
        
        # Indirect addressing
        elif operand.startswith('@'):
            flags[0] = 1  # n
            flags[1] = 0  # i
            operand = operand[1:].strip()
        
        # Simple addressing
        else:
            flags[0] = 1  # n
            flags[1] = 1  # i
        
        # Indexed addressing
        if ',X' in operand.upper():
            flags[2] = 1  # x
            operand = operand.upper().replace(',X', '').strip()
        
        return (operand, flags)
    
    def encode_object_code(self, opcode, flags, displacement, format_type):
        """
        Encodes the final object code based on opcode, flags, and displacement.
        
        :param opcode: Opcode as an integer.
        :param flags: List of nixbpe flags.
        :param displacement: Displacement value as an integer.
        :param format_type: Instruction format (3 or 4).
        :return: Encoded object code as a hexadecimal string.
        """
        # Convert opcode to binary (6 bits)
        opcode_bin = format(opcode, '06b')
        
        # Convert nixbpe flags to binary (6 bits)
        flags_bin = ''.join(str(flag) for flag in flags)
        
        # Convert displacement to binary
        if format_type == 3:
            # Handle signed displacement for format 3
            if displacement < 0:
                displacement = (1 << 12) + displacement  # Two's complement
            displacement_bin = format(displacement, '012b')  # 12 bits
        elif format_type == 4:
            displacement_bin = format(displacement, '020b')  # 20 bits
        else:
            displacement_bin = '0' * 12  # Default
        
        # Concatenate all parts
        object_code_bin = opcode_bin + flags_bin + displacement_bin
        
        # Convert binary to hexadecimal
        object_code_hex = format(int(object_code_bin, 2), 'X').upper()
        
        # Pad with leading zeros
        if format_type == 3:
            object_code_hex = object_code_hex.zfill(6)
        elif format_type == 4:
            object_code_hex = object_code_hex.zfill(8)
        
        return object_code_hex
    
    def validate_register(self, register, source_line):
        """
        Validates the register name and returns its code.
        
        :param register: Register name as a string.
        :param source_line: Instance of SourceCodeLine.
        :return: Register code as an integer or None if invalid.
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid register '{register}' at line {source_line.line_number}.")
            source_line.mark_error()
            return None
        return REGISTER_CODES[register]
    
    def set_base_register(self, register):
        """
        Sets the base register value for base-relative addressing.
        
        :param register: Register name as a string (e.g., 'B').
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid base register '{register}'.")
            return
        symbol = register  # Assuming register symbols are defined in the symbol table
        symbol_entry = self.symbol_table.get_symbol(symbol)
        if not symbol_entry:
            self.error_handler.log_error(f"Symbol for base register '{register}' not found in symbol table.")
            return
        self.base_register_value = symbol_entry.value
        self.error_handler.log_action(f"Base register set to {register} with value {self.base_register_value:X}.")
    
    def unset_base_register(self):
        """
        Unsets the base register value, disabling base-relative addressing.
        """
        self.base_register_value = None
        self.error_handler.log_action("Base register unset.")
    
    def generate_object_code_for_literal(self, literal):
        """
        Generates object code for a literal.
        
        :param literal: Instance of a Literal (from LiteralTableList).
        :return: Object code as a hexadecimal string.
        """
        if literal.type == 'C':
            # Convert each character to its ASCII hexadecimal value
            object_code = ''.join([format(ord(char), '02X') for char in literal.value])
        elif literal.type == 'X':
            # Use the hexadecimal value directly
            object_code = literal.value.upper()
        else:
            self.error_handler.log_error(f"Unsupported literal type '{literal.type}' for literal '{literal.name}'.")
            return None
        return object_code
    
    def requires_modification(self, source_line):
        """
        Determines if the instruction requires a modification record.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Boolean indicating if modification is required.
        """
        # Typically, format 4 instructions require modification
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            return False
        return opcode_info['format'] == 4
    
    def get_modification_details(self, source_line):
        """
        Retrieves modification details for a source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (modification_offset, modification_length).
        """
        # Assuming the modification occurs at the address after the opcode byte
        # and spans the next 5 half-bytes (20 bits)
        modification_offset = 1  # Address offset where modification starts
        modification_length = 5  # Number of half-bytes to modify
        return (modification_offset, modification_length)
```

### 11. Additional Design Enhancements

#### a. **Handling Base and PC Relative Addressing**
- **Base Register Management**: Implemented via `set_base_register` and `unset_base_register` methods.
- **Displacement Calculation**: Ensures displacement is calculated based on whether PC-relative or base-relative addressing is used.
#### b. **Managing Extended Instructions (Format 4)**
- **Modification Records**: For format 4 instructions, modification records are added to handle relocations.
- **End Record Address**: The end record references the starting address of execution, which may be a format 4 instruction.
#### c. **Supporting Multiple Control Sections**
- **External Definitions and References**: If your assembler supports multiple control sections, manage `EXTDEF` and `EXTREF` directives accordingly.
- **Linking Considerations**: Ensure that modification records account for symbols defined in external control sections.

#### d. **Listing File Generation (Optional)**
- **Purpose**: Create a human-readable listing file that combines source lines with their corresponding object codes and addresses for debugging purposes.
- **Implementation**: Integrate a `ListingFileWriter` class that formats and writes the listing file based on processed `SourceCodeLine` objects.

### 12. Interaction Diagram
```plaintext
ObjectCodeGenerator
    |
    |-- OpcodeHandler
    |-- SymbolTable
    |-- LiteralTable
    |-- ErrorLogHandler
    |-- LocationCounter
    |
    |-- TextRecordManager <-- ObjectCodeGenerator
    |
    |-- ModificationRecordManager <-- ObjectCodeGenerator
```

- **Flow**:
    1. **Address Verification**: `ObjectCodeGenerator` uses `LocationCounter` to verify the current address.
    2. **Opcode Retrieval**: Retrieves opcode information from `OpcodeHandler`.
    3. **Symbol and Literal Resolution**: Resolves operands using `SymbolTable` and `LiteralTable`.
    4. **Object Code Generation**: Generates object code based on instruction format and addressing mode.
    5. **Record Management**: Adds object codes to `TextRecordManager` and modification records to `ModificationRecordManager`.
    6. **Location Counter Update**: Updates `LocationCounter` based on the instruction length.

### 13. Comprehensive Pseudocode Example

```plaintext
class ObjectCodeGenerator:
    def __init__(self, symbol_table, literal_table, opcode_handler, error_handler, location_counter):
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_handler = opcode_handler
        self.error_handler = error_handler
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        self.location_counter = location_counter
        self.base_register_value = None
        self.nixbpe_flags = [0, 0, 0, 0, 0, 0]
    
    def generate_object_code(self, source_lines):
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_instruction():
                object_code = self.generate_object_code_for_line(source_line)
                if object_code:
                    self.text_record_manager.add_object_code(source_line.address, object_code)
                    if self.requires_modification(source_line):
                        modification_offset, modification_length = self.get_modification_details(source_line)
                        self.modification_record_manager.add_modification(
                            address=source_line.address + modification_offset,
                            length=modification_length
                        )
    
    def generate_object_code_for_line(self, source_line):
        expected_address = self.location_counter.get_current_address_int()
        if source_line.address != expected_address:
            self.error_handler.log_error(
                f"Address mismatch at line {source_line.line_number}: expected {expected_address:X}, found {source_line.address:X}."
            )
            source_line.mark_error()
            return None
        
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            self.error_handler.log_error(f"Undefined opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        self.detect_illegal_addressing(source_line, opcode_info)
        if source_line.has_errors():
            return None
        
        format_type = opcode_info['format']
        if format_type == 1:
            object_code = self.handle_format1(source_line, opcode_info)
        elif format_type == 2:
            object_code = self.handle_format2(source_line, opcode_info)
        elif format_type == 3:
            object_code = self.handle_format3(source_line, opcode_info)
        elif format_type == 4:
            object_code = self.handle_format4(source_line, opcode_info)
        else:
            self.error_handler.log_error(f"Unsupported instruction format '{format_type}' for opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        return object_code
    
    def handle_format1(self, source_line, opcode_info):
        opcode = opcode_info['opcode']
        object_code = f"{opcode:02X}"
        return object_code
    
    def handle_format2(self, source_line, opcode_info):
        opcode = opcode_info['opcode']
        operands = source_line.operands.split(',')
        if len(operands) != 2:
            self.error_handler.log_error(f"Incorrect number of registers for format 2 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            source_line.mark_error()
            return None
        reg1 = operands[0].strip().upper()
        reg2 = operands[1].strip().upper()
        reg1_code = self.validate_register(reg1, source_line)
        reg2_code = self.validate_register(reg2, source_line)
        if reg1_code is None or reg2_code is None:
            return None
        object_code = f"{opcode:02X}{reg1_code:X}{reg2_code:X}"
        return object_code
    
    def handle_format3(self, source_line, opcode_info):
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags
        self.nixbpe_flags = [1, 1, 0, 0, 0, 0]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # Calculate displacement
        displacement = self.calculate_displacement(resolved_value, current_address)
        if displacement is None:
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Check address range
        if not self.check_address_range(displacement, 3):
            self.error_handler.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 3)
        return object_code
    
    def handle_format4(self, source_line, opcode_info):
        opcode = opcode_info['opcode']
        operand = source_line.operands
        current_address = self.location_counter.get_current_address_int()
        
        # Initialize nixbpe flags for extended format
        self.nixbpe_flags = [1, 1, 0, 0, 0, 1]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.error_handler.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # For format 4, address is absolute or relocatable
        displacement = resolved_value
        
        # Check address range for format 4 (20 bits)
        if displacement < 0 or displacement > 0xFFFFF:
            self.error_handler.log_error(f"Address out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 4)
        
        # Add modification record for relocation
        self.modification_record_manager.add_modification(
            address=current_address + 1,  # Assuming the address starts at the next byte
            length=5  # Number of half-bytes to modify
        )
        
        return object_code
    
    def resolve_operand(self, operand, current_address):
        """
        Resolves an operand to its address or value.
        
        :param operand: Operand string.
        :param current_address: Current address from LocationCounter.
        :return: Tuple (resolved_value, relocation_info)
        """
        relocation_info = 'A'  # Default to absolute
        
        if operand.startswith('='):
            # Literal
            literal = self.literal_table.get_literal(operand)
            if not literal:
                self.error_handler.log_error(f"Literal '{operand}' not found in literal table.")
                return (None, None)
            resolved_value = literal.address
            relocation_info = 'R'
        elif operand.isdigit():
            # Immediate numeric value
            resolved_value = int(operand)
        else:
            # Symbol
            symbol = self.symbol_table.get_symbol(operand)
            if not symbol:
                return (None, None)
            resolved_value = symbol.value
            relocation_info = 'R' if symbol.is_relocatable else 'A'
        
        return (resolved_value, relocation_info)
    
    def calculate_displacement(self, target_address, current_address):
        """
        Calculates displacement for format 3 instructions.
        
        :param target_address: The resolved address of the operand.
        :param current_address: The current address from LocationCounter.
        :return: Displacement as an integer or None if out of range.
        """
        displacement = target_address - (current_address + 3)
        
        if -2048 <= displacement <= 2047:
            # PC-relative addressing
            self.nixbpe_flags[4] = 1  # Set p flag
            return displacement & 0xFFF  # 12-bit signed
        elif self.base_register_value is not None:
            displacement = target_address - self.base_register_value
            if 0 <= displacement <= 4095:
                # Base-relative addressing
                self.nixbpe_flags[3] = 1  # Set b flag
                return displacement
        return None
    
    def check_address_range(self, displacement, format_type):
        """
        Checks if the displacement is within the allowable range for the instruction format.
        
        :param displacement: The calculated displacement value.
        :param format_type: The instruction format (3 or 4).
        :return: True if within range, False otherwise.
        """
        if format_type == 3:
            return -2048 <= displacement <= 4095  # Considering both PC and base-relative
        elif format_type == 4:
            return 0 <= displacement <= 0xFFFFF  # 20-bit address
        return False
    
    def detect_illegal_addressing(self, source_line, opcode_info):
        """
        Detects illegal addressing modes for the given instruction.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        """
        operand = source_line.operands
        addressing_mode = self.identify_addressing_mode(operand)
        allowed_modes = opcode_info.get('allowed_addressing_modes', [])
        
        if addressing_mode not in allowed_modes:
            self.error_handler.log_error(f"Illegal addressing mode '{addressing_mode}' for instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            source_line.mark_error()
    
    def identify_addressing_mode(self, operand):
        """
        Identifies the addressing mode based on the operand prefix/suffix.
        
        :param operand: Operand string.
        :return: Addressing mode as a string ('immediate', 'indirect', 'simple', 'indexed').
        """
        if operand.startswith('#'):
            return 'immediate'
        elif operand.startswith('@'):
            return 'indirect'
        elif ',X' in operand.upper():
            return 'indexed'
        else:
            return 'simple'
    
    def process_addressing_modes(self, operand, flags, source_line):
        """
        Processes the addressing modes and sets the nixbpe flags accordingly.
        
        :param operand: Operand string.
        :param flags: List of nixbpe flags.
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (processed_operand, flags)
        """
        operand = operand.strip()
        
        # Immediate addressing
        if operand.startswith('#'):
            flags[0] = 0  # n
            flags[1] = 1  # i
            operand = operand[1:].strip()
        
        # Indirect addressing
        elif operand.startswith('@'):
            flags[0] = 1  # n
            flags[1] = 0  # i
            operand = operand[1:].strip()
        
        # Simple addressing
        else:
            flags[0] = 1  # n
            flags[1] = 1  # i
        
        # Indexed addressing
        if ',X' in operand.upper():
            flags[2] = 1  # x
            operand = operand.upper().replace(',X', '').strip()
        
        return (operand, flags)
    
    def encode_object_code(self, opcode, flags, displacement, format_type):
        """
        Encodes the final object code based on opcode, flags, and displacement.
        
        :param opcode: Opcode as an integer.
        :param flags: List of nixbpe flags.
        :param displacement: Displacement value as an integer.
        :param format_type: Instruction format (3 or 4).
        :return: Encoded object code as a hexadecimal string.
        """
        # Convert opcode to binary (6 bits)
        opcode_bin = format(opcode, '06b')
        
        # Convert nixbpe flags to binary (6 bits)
        flags_bin = ''.join(str(flag) for flag in flags)
        
        # Convert displacement to binary
        if format_type == 3:
            # Handle signed displacement for format 3
            if displacement < 0:
                displacement = (1 << 12) + displacement  # Two's complement
            displacement_bin = format(displacement, '012b')  # 12 bits
        elif format_type == 4:
            displacement_bin = format(displacement, '020b')  # 20 bits
        else:
            displacement_bin = '0' * 12  # Default
        
        # Concatenate all parts
        object_code_bin = opcode_bin + flags_bin + displacement_bin
        
        # Convert binary to hexadecimal
        object_code_hex = format(int(object_code_bin, 2), 'X').upper()
        
        # Pad with leading zeros
        if format_type == 3:
            object_code_hex = object_code_hex.zfill(6)
        elif format_type == 4:
            object_code_hex = object_code_hex.zfill(8)
        
        return object_code_hex
    
    def validate_register(self, register, source_line):
        """
        Validates the register name and returns its code.
        
        :param register: Register name as a string.
        :param source_line: Instance of SourceCodeLine.
        :return: Register code as an integer or None if invalid.
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid register '{register}' at line {source_line.line_number}.")
            source_line.mark_error()
            return None
        return REGISTER_CODES[register]
    
    def set_base_register(self, register):
        """
        Sets the base register value for base-relative addressing.
        
        :param register: Register name as a string (e.g., 'B').
        """
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.error_handler.log_error(f"Invalid base register '{register}'.")
            return
        symbol = register  # Assuming register symbols are defined in the symbol table
        symbol_entry = self.symbol_table.get_symbol(symbol)
        if not symbol_entry:
            self.error_handler.log_error(f"Symbol for base register '{register}' not found in symbol table.")
            return
        self.base_register_value = symbol_entry.value
        self.error_handler.log_action(f"Base register set to {register} with value {self.base_register_value:X}.")
    
    def unset_base_register(self):
        """
        Unsets the base register value, disabling base-relative addressing.
        """
        self.base_register_value = None
        self.error_handler.log_action("Base register unset.")
    
    def generate_object_code_for_literal(self, literal):
        """
        Generates object code for a literal.
        
        :param literal: Instance of a Literal (from LiteralTableList).
        :return: Object code as a hexadecimal string.
        """
        if literal.type == 'C':
            # Convert each character to its ASCII hexadecimal value
            object_code = ''.join([format(ord(char), '02X') for char in literal.value])
        elif literal.type == 'X':
            # Use the hexadecimal value directly
            object_code = literal.value.upper()
        else:
            self.error_handler.log_error(f"Unsupported literal type '{literal.type}' for literal '{literal.name}'.")
            return None
        return object_code
    
    def requires_modification(self, source_line):
        """
        Determines if the instruction requires a modification record.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Boolean indicating if modification is required.
        """
        # Typically, format 4 instructions require modification
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            return False
        return opcode_info['format'] == 4
    
    def get_modification_details(self, source_line):
        """
        Retrieves modification details for a source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (modification_offset, modification_length).
        """
        # Assuming the modification occurs at the address after the opcode byte
        # and spans the next 5 half-bytes (20 bits)
        modification_offset = 1  # Address offset where modification starts
        modification_length = 5  # Number of half-bytes to modify
        return (modification_offset, modification_length)
```

### 13. Final Considerations

- **Scalability**: The `ObjectCodeGenerator` is designed to handle large assembly programs efficiently by leveraging modular methods and clear interactions with supporting classes.
  
- **Modularity**: Each method within `ObjectCodeGenerator` has a single responsibility, enhancing maintainability and readability.
  
- **Error Handling**: Comprehensive error checking ensures that all potential issues during object code generation are detected and logged appropriately.
  
- **Integration with `LocationCounter`**: Ensures that address management is consistent and accurate, reducing the likelihood of address-related errors.
  
- **Testing**: Implement thorough unit and integration tests to validate each method's functionality, especially the interactions with `LocationCounter`, `SymbolTable`, and `LiteralTable`.

---
## 3. ``TextRecordManager``

### Overview
The `TextRecordManager` is responsible for organizing the generated object codes into structured text records that conform to the assembler's output format. It ensures that each text record adheres to length constraints and maintains continuity based on the addresses of the instructions. By integrating the `LocationCounter`, the `TextRecordManager` can verify address consistency and manage address-related operations more effectively.

### Responsibilities
- **Collect Object Codes**: Group generated object codes into text records.
- **Manage Record Length**: Ensure each text record does not exceed 30 bytes (60 hexadecimal digits).
- **Handle Record Continuity**: Start new records when object codes are non-contiguous or when length constraints are met.
- **Verify Address Consistency**: Utilize `LocationCounter` to ensure that object codes are placed at the correct addresses.
- **Format Records**: Assemble text records in the specified format for the object program.
- **Provide Records for Output**: Supply all finalized text records to the `ObjectProgramWriter`.
### Attributes
- **`text_records`**:
    - **Type**: `List[str]`
    - **Description**: Stores all finalized text records in the order they are created.
- **`current_record`**:
    - **Type**: `List[str]`
    - **Description**: A buffer holding object codes that are currently being grouped into a text record.
- **`current_start_address`**:
    - **Type**: `int`
    - **Description**: The starting memory address of the current text record.
- **`current_length`**:
    - **Type**: `int`
    - **Description**: The cumulative length (in bytes) of the object codes in the current text record.
- **`MAX_RECORD_LENGTH`**:
    - **Type**: `int`
    - **Description**: The maximum allowed length of a text record (30 bytes).
    - **Value**: `30`
- **`location_counter`**:
    - **Type**: `LocationCounter`
    - **Description**: Reference to the `LocationCounter` instance for address verification and management.

### Methods
#### A. Initialization
1. **`__init__(self, location_counter: LocationCounter)`**
    
    ```python
    def __init__(self, location_counter: LocationCounter):
        self.text_records = []                # List to store finalized text records
        self.current_record = []              # Buffer for object codes in the current text record
        self.current_start_address = None     # Starting address of the current text record
        self.current_length = 0               # Current length of the text record in bytes
        self.MAX_RECORD_LENGTH = 30           # Maximum length of a text record in bytes
        self.location_counter = location_counter  # Reference to the LocationCounter
    ```
    
    - **Purpose**: Sets up the initial state of the `TextRecordManager` with empty records and default values. Integrates the `LocationCounter` for address management.

#### B. Core Functionality

2. **`add_object_code(self, address: int, object_code: str)`**
    
    ```python
    def add_object_code(self, address: int, object_code: str):
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address
        
        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True
        
        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address
        
        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)
        
        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address
        
        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length
    ```
    
    - **Parameters**:
        - `address`: The memory address of the object code.
        - `object_code`: The hexadecimal string representing the machine code.
    - **Purpose**: Adds an object code to the current text record while ensuring length constraints and address continuity. Utilizes the `LocationCounter` to verify address consistency.
3. **`finalize_current_record(self)`**
    
    ```python
    def finalize_current_record(self):
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length
            
            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)
            
            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"
            
            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)
            
            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0
    ```
    
    - **Purpose**: Finalizes the current text record by formatting it and adding it to the list of text records. Resets the buffer and counters for the next record.
4. **`get_text_records(self) -> List[str]`**
    
    ```python
    def get_text_records(self) -> List[str]:
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()
        
        # Return the list of all finalized text records
        return self.text_records
    ```
    
    - **Purpose**: Returns all finalized text records, ensuring that any remaining object codes are included.

#### C. Helper Functions

5. **`is_contiguous(self, last_address: int, new_address: int) -> bool`**
    
    ```python
    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address
    ```
    
    - **Parameters**:
        - `last_address`: The address where the last object code ended.
        - `new_address`: The address of the incoming object code.
    - **Purpose**: Determines if the new object code address is contiguous with the current record.
6. **`calculate_length(self, object_code: str) -> int`**
    
    ```python
    def calculate_length(self, object_code: str) -> int:
        return len(object_code) // 2  # Each pair of hex digits represents one byte
    ```
    
    - **Parameters**:
        - `object_code`: The hexadecimal string representing the machine code.
    - **Purpose**: Calculates the length of the object code in bytes.
7. **`verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int)`**
    
    ```python
    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        if actual_address != expected_address:
            self.location_counter.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary
    ```
    
    - **Parameters**:
        - `expected_address`: The address as per the `LocationCounter`.
        - `actual_address`: The address from the `SourceCodeLine`.
        - `line_number`: The line number in the source code for error reporting.
    - **Purpose**: Verifies that the actual address matches the expected address from the `LocationCounter`.
8. **`log_error(self, message: str)`**
    
    ```python
    def log_error(self, message: str):
        self.location_counter.error_handler.log_error(message)
    ```
    
    - **Parameters**:
        - `message`: The error message to be logged.
    - **Purpose**: Logs an error message using the integrated `ErrorHandler` from the `LocationCounter`.

#### D. Edge Case Handling

9. **Handling Non-Contiguous Addresses**
    
    - **Scenario**: When an object code is not contiguous with the previous one, a new text record should be started.
    - **Implementation**:  
        In the `add_object_code` method, use the `is_contiguous` helper to check continuity. If not contiguous, finalize the current record and start a new one.
10. **Handling Maximum Record Length Exceedance**
    
    - **Scenario**: Adding a new object code exceeds the maximum allowed length of a text record.
    - **Implementation**:  
        In the `add_object_code` method, check if the current length plus the new object code's length exceeds `MAX_RECORD_LENGTH`. If so, finalize the current record and start a new one with the new object code.
11. **Handling Empty Records**
    
    - **Scenario**: Ensuring that no empty records are added to the `text_records` list.
    - **Implementation**:  
        In the `finalize_current_record` method, check if `current_record` is not empty before formatting and adding it to `text_records`.

### Interactions with Other Classes

- **`ObjectCodeGenerator`**:
    - **Role**: Generates object codes for each instruction.
    - **Interaction**: Calls `text_record_manager.add_object_code(address, object_code)` to add generated codes to text records.
- **`ModificationRecordManager`**:
    - **Role**: Manages relocation information.
    - **Interaction**: Works independently but is part of the overall record management alongside `TextRecordManager`.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the assembly process.
    - **Interaction**: Utilizes `TextRecordManager` to collect and manage text records during object code generation.
- **`LocationCounter`**:
    - **Role**: Manages current address and program length.
    - **Interaction**: `TextRecordManager` uses `LocationCounter` to verify address consistency and manage address-related operations.
- **`ObjectProgramWriter`**:
    - **Role**: Assembles the final object program.
    - **Interaction**: Receives the finalized text records from `TextRecordManager` to compile the final object program.

### Pseudocode Examples

Below are detailed pseudocode examples for each method within the `TextRecordManager` class, illustrating how the class operates with the integration of the `LocationCounter`.

#### A. `__init__` Method

```python
class TextRecordManager:
    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter
```

#### B. `add_object_code` Method

```python
def add_object_code(self, address: int, object_code: str):
    """
    Adds an object code to the current text record, ensuring length and continuity constraints.

    :param address: The memory address of the object code.
    :param object_code: The hexadecimal string representing the machine code.
    """
    if not self.current_record:
        # Start a new text record
        self.current_start_address = address

    if self.current_record:
        # Get the last object's end address
        last_object_code = self.current_record[-1]
        last_address = address - (len(last_object_code) // 2)
        contiguous = self.is_contiguous(last_address, address)
    else:
        contiguous = True

    if not contiguous:
        # Finalize the current record and start a new one
        self.finalize_current_record()
        self.current_start_address = address

    # Calculate the length of the new object code in bytes
    object_length = self.calculate_length(object_code)

    if self.current_length + object_length > self.MAX_RECORD_LENGTH:
        # Finalize the current record and start a new one
        self.finalize_current_record()
        self.current_start_address = address

    # Add the object code to the current record
    self.current_record.append(object_code)
    self.current_length += object_length
```

#### C. `finalize_current_record` Method

```python
def finalize_current_record(self):
    """
    Finalizes the current text record by formatting and adding it to the list of text records.
    Resets the current record buffer and counters.
    """
    if self.current_record:
        # Calculate the total length of the current record in bytes
        record_length = self.current_length

        # Concatenate all object codes in the current record
        concatenated_object_code = ''.join(self.current_record)

        # Format the text record as per the specification
        formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

        # Add the formatted record to the list of text records
        self.text_records.append(formatted_record)

        # Reset the current record buffer and counters
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
```

#### D. `get_text_records` Method

```python
def get_text_records(self) -> List[str]:
    """
    Retrieves all finalized text records.

    :return: A list of formatted text record strings.
    """
    # Finalize any remaining object codes in the current record
    self.finalize_current_record()

    # Return the list of all finalized text records
    return self.text_records
```

#### E. `is_contiguous` Helper Method

```python
def is_contiguous(self, last_address: int, new_address: int) -> bool:
    """
    Checks if the new address is contiguous with the last address.

    :param last_address: The address where the last object code ended.
    :param new_address: The address of the incoming object code.
    :return: True if contiguous, False otherwise.
    """
    expected_address = last_address + (len(self.current_record[-1]) // 2)
    return new_address == expected_address
```

#### F. `calculate_length` Helper Method

```python
def calculate_length(self, object_code: str) -> int:
    """
    Calculates the length of the object code in bytes.

    :param object_code: The hexadecimal string representing the machine code.
    :return: The length of the object code in bytes.
    """
    return len(object_code) // 2  # Each pair of hex digits represents one byte
```

#### G. `verify_address_consistency` Method

```python
def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
    """
    Verifies that the actual address matches the expected address from the LocationCounter.

    :param expected_address: The address as per the LocationCounter.
    :param actual_address: The address from the SourceCodeLine.
    :param line_number: The line number in the source code for error reporting.
    """
    if actual_address != expected_address:
        self.log_error(
            f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
        )
        # Additional error handling if necessary
```

#### H. `log_error` Method

```python
def log_error(self, message: str):
    """
    Logs an error message using the integrated ErrorHandler from the LocationCounter.

    :param message: The error message to be logged.
    """
    self.location_counter.error_handler.log_error(message)
```

### Pseudocode Summary

To encapsulate the entire functionality, here's a summary of the `TextRecordManager` pseudocode with `LocationCounter` integration:

```python
class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.

    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter

    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address

        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True

        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)

        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length

    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()

        # Return the list of all finalized text records
        return self.text_records

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.

        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### 4. Detailed Method Descriptions

#### A. Initialization

1. **`__init__(self, location_counter: LocationCounter)`**
    
    ```python
    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.
    
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter
    ```
    
    - **Description**: Sets up the initial state of the `TextRecordManager` with empty records and default values. Integrates the `LocationCounter` for address management.

#### B. Core Functionality

2. **`add_object_code(self, address: int, object_code: str)`**
    
    ```python
    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.
    
        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address
    
        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True
    
        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address
    
        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)
    
        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address
    
        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length
    ```
    
    - **Parameters**:
        
        - `address`: The memory address of the object code.
        - `object_code`: The hexadecimal string representing the machine code.
    - **Purpose**: Adds an object code to the current text record while ensuring length constraints and address continuity. Utilizes the `LocationCounter` to verify address consistency.
        
    - **Details**:
        
        - **Starting a New Record**: If the `current_record` is empty, set the `current_start_address` to the address of the incoming object code.
        - **Contiguity Check**: Determines if the incoming object code is contiguous with the last one in the `current_record` using the `is_contiguous` helper method.
        - **Length Check**: Ensures that adding the new object code does not exceed `MAX_RECORD_LENGTH`. If it does, finalize the current record and start a new one.
        - **Adding to Record**: Appends the `object_code` to `current_record` and updates `current_length`.
3. **`finalize_current_record(self)`**
    
    ```python
    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length
    
            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)
    
            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"
    
            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)
    
            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0
    ```
    
    - **Purpose**: Finalizes the current text record by formatting it and adding it to the list of text records. Resets the buffer and counters for the next record.
        
    - **Details**:
        
        - **Record Formatting**: Follows the record format `T^StartAddress^Length^ObjectCodes`.
        - **Resetting State**: Clears the `current_record` buffer and resets `current_start_address` and `current_length` for the next record.
4. **`get_text_records(self) -> List[str]`**
    
    ```python
    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.
    
        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()
    
        # Return the list of all finalized text records
        return self.text_records
    ```
    
    - **Purpose**: Returns all finalized text records, ensuring that any remaining object codes are included.

#### C. Helper Functions

5. **`is_contiguous(self, last_address: int, new_address: int) -> bool`**
    
    ```python
    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.
    
        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address
    ```
    
    - **Parameters**:
        
        - `last_address`: The address where the last object code ended.
        - `new_address`: The address of the incoming object code.
    - **Purpose**: Determines if the new object code address is contiguous with the current record.
        
    - **Returns**: `True` if contiguous, `False` otherwise.
        
6. **`calculate_length(self, object_code: str) -> int`**
    
    ```python
    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.
    
        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte
    ```
    
    - **Parameters**:
        
        - `object_code`: The hexadecimal string representing the machine code.
    - **Purpose**: Calculates the length of the object code in bytes.
        
    - **Returns**: The length in bytes.
        
7. **`verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int)`**
    
    ```python
    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.
    
        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary
    ```
    
    - **Parameters**:
        - `expected_address`: The address as per the `LocationCounter`.
        - `actual_address`: The address from the `SourceCodeLine`.
        - `line_number`: The line number in the source code for error reporting.
    - **Purpose**: Verifies that the actual address matches the expected address from the `LocationCounter`. Logs an error if there is a mismatch.
8. **`log_error(self, message: str)`**
    
    ```python
    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.
    
        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
    ```
    
    - **Parameters**:
        - `message`: The error message to be logged.
    - **Purpose**: Logs an error message using the integrated `ErrorHandler` from the `LocationCounter`.

### Edge Case Handling

9. **Handling Non-Contiguous Addresses**
    
    - **Scenario**: When an object code is not contiguous with the previous one, a new text record should be started.
    - **Implementation**:  
        In the `add_object_code` method, use the `is_contiguous` helper to check continuity. If not contiguous, finalize the current record and start a new one.
10. **Handling Maximum Record Length Exceedance**
    
    - **Scenario**: Adding a new object code exceeds the maximum allowed length of a text record.
    - **Implementation**:  
        In the `add_object_code` method, check if the current length plus the new object code's length exceeds `MAX_RECORD_LENGTH`. If so, finalize the current record and start a new one with the new object code.
11. **Handling Empty Records**
    
    - **Scenario**: Ensuring that no empty records are added to the `text_records` list.
    - **Implementation**:  
        In the `finalize_current_record` method, check if `current_record` is not empty before formatting and adding it to `text_records`.

### Interactions with Other Classes

- **`ObjectCodeGenerator`**:
    - **Role**: Generates object codes for each instruction.
    - **Interaction**: Calls `text_record_manager.add_object_code(address, object_code)` to add generated codes to text records.
- **`ModificationRecordManager`**:
    - **Role**: Manages relocation information.
    - **Interaction**: Works independently but is part of the overall record management alongside `TextRecordManager`.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the assembly process.
    - **Interaction**: Utilizes `TextRecordManager` to collect and manage text records during object code generation.
- **`LocationCounter`**:
    - **Role**: Manages current address and program length.
    - **Interaction**: `TextRecordManager` uses `LocationCounter` to verify address consistency and manage address-related operations.
- **`ObjectProgramWriter`**:
    - **Role**: Assembles the final object program.
    - **Interaction**: Receives the finalized text records from `TextRecordManager` to compile the final object program.

### Implementation Details

#### Instruction Address Consistency

- **Purpose**: Ensures that each object code is placed at the correct memory address as tracked by the `LocationCounter`.
- **Implementation**:
    - Before adding an object code, verify that the provided `address` matches the expected address from the `LocationCounter`.
    - If there is a mismatch, log an error indicating the inconsistency.

#### Record Continuity and Length Management

- **Contiguity Check**:
    
    - Determines if the incoming object code is contiguous with the last one in the `current_record`.
    - Utilizes the `is_contiguous` helper method to perform this check.
- **Length Check**:
    
    - Ensures that adding the new object code does not exceed `MAX_RECORD_LENGTH`.
    - If it does, finalizes the current record and starts a new one.

#### Integration with `LocationCounter`

- **Address Verification**:
    
    - `TextRecordManager` uses `LocationCounter` to verify that the addresses of object codes are consistent.
    - This helps in detecting address mismatches and maintaining accurate address tracking.
- **Error Logging**:
    
    - Uses the `ErrorHandler` from `LocationCounter` to log any address-related errors.

### Pseudocode Example

Below is a detailed pseudocode example for the updated `TextRecordManager` class, incorporating the `LocationCounter`.

```python
class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.
    
    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter

    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address

        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True

        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)

        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length

    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()

        # Return the list of all finalized text records
        return self.text_records

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.

        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### 5. Integration with `LocationCounter`

Integrating the `LocationCounter` into the `TextRecordManager` ensures accurate address tracking and validation throughout the object code organization process. Here's how the integration impacts various parts of the `TextRecordManager`:

#### a. **Address Verification**

Before adding an object code to a text record, verify that the `address` in the `SourceCodeLine` matches the current address from `LocationCounter`. This ensures consistency between Pass 1 and Pass 2.

```python
def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
    if actual_address != expected_address:
        self.log_error(
            f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
        )
        # Additional error handling if necessary
```

#### b. **Error Logging**

Leverage the `ErrorHandler` from `LocationCounter` to log any address-related errors, ensuring that all discrepancies are appropriately recorded.

```python
def log_error(self, message: str):
    self.location_counter.error_handler.log_error(message)
```

### 6. Example Workflow Incorporating `LocationCounter`

1. **Initialization**:
    
    - `AssemblerPass2` initializes all components, including `LocationCounter`.
    - `TextRecordManager` is instantiated with a reference to the `LocationCounter`.
2. **Adding Object Codes**:
    
    - For each `SourceCodeLine`, `AssemblerPass2` generates the `object_code` using `ObjectCodeGenerator`.
    - Before adding the `object_code` to `TextRecordManager`, verify address consistency:
        
        ```python
        expected_address = location_counter.get_current_address_int()
        actual_address = source_line.address
        text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
        ```
        
    - If address consistency is verified, proceed to add the `object_code`:
        
        ```python
        text_record_manager.add_object_code(actual_address, object_code)
        ```
        
3. **Handling Directives Affecting Addresses**:
    
    - Directives like `LTORG` assign addresses to literals. When processing such directives, ensure that `LocationCounter` is updated accordingly before adding literal object codes to `TextRecordManager`.
4. **Finalization**:
    
    - After processing all lines, retrieve all text records:
        
        ```python
        text_records = text_record_manager.get_text_records()
        ```
        
    - Pass these records to `ObjectProgramWriter` for assembling the final object program.
5. **Writing Output**:
    
    - `ObjectProgramWriter` assembles the final object program using the header record, text records, modification records, and end record.

### 7. Testing the `TextRecordManager`

To ensure the `TextRecordManager` functions correctly with `LocationCounter`, implement the following test cases:

#### a. **Address Consistency**

- **Test Case**: Intermediate file has sequential addresses matching `LocationCounter`.
- **Expected Outcome**: Object codes are added to text records without address mismatch errors.

#### b. **Address Mismatch Detection**

- **Test Case**: Intermediate file contains a line with an address that does not match `LocationCounter`.
- **Expected Outcome**: Error is logged specifying the expected and found addresses, and the object code is not added to the current record.

#### c. **Displacement Calculation**

- **Test Case**: Operand displacement within range for PC-relative and base-relative addressing.
    
- **Expected Outcome**: Correct displacement is calculated, and appropriate flags are set in `ObjectCodeGenerator`.
    
- **Edge Case**: Operand displacement out of range.
    
- **Expected Outcome**: Error is logged indicating displacement out of range, and the object code is not added to the current record.
    

#### d. **Format Handling**

- **Test Case**: Instructions of all formats (1 to 4).
- **Expected Outcome**: Object codes are correctly generated for each format and appropriately grouped into text records.

#### e. **Addressing Modes**

- **Test Case**: Instructions using various addressing modes (immediate, indirect, indexed).
- **Expected Outcome**: Flags are correctly set in `ObjectCodeGenerator`, and object codes reflect addressing modes in the text records.

#### f. **Base Register Usage**

- **Test Case**: Instructions requiring base-relative addressing with `BASE` directive set.
    
- **Expected Outcome**: Displacement is calculated relative to the base register, and `b` flag is set in `ObjectCodeGenerator`.
    
- **Edge Case**: `BASE` register not set when required.
    
- **Expected Outcome**: Error is logged, and displacement calculation fails, preventing object code addition to text records.
    

#### g. **Literal Handling**

- **Test Case**: Instructions referencing literals.
- **Expected Outcome**: Object codes for literals are correctly generated, added to text records, and their addresses are verified against `LocationCounter`.

### 8. Documentation and Code Comments

Ensure that all methods within the `TextRecordManager` class are well-documented with clear docstrings and inline comments explaining their purpose, parameters, and logic. This practice facilitates maintenance and future enhancements.

```python
class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.
    
    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """
    
    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter

    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address

        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True

        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)

        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length

    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()

        # Return the list of all finalized text records
        return self.text_records

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.

        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### 9. Example Workflow Incorporating `LocationCounter`

Here’s how the `TextRecordManager` operates within the assembly process, leveraging the `LocationCounter`:

1. **Initialization**:
    
    - `AssemblerPass2` initializes all components, including `LocationCounter`.
    - `TextRecordManager` is instantiated with a reference to the `LocationCounter`.
2. **Generating Object Code**:
    
    - For each `SourceCodeLine`, `ObjectCodeGenerator` generates the `object_code`.
    - Before adding the `object_code` to `TextRecordManager`, verify address consistency:
        
        ```python
        expected_address = location_counter.get_current_address_int()
        actual_address = source_line.address
        text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
        ```
        
    - If address consistency is verified, proceed to add the `object_code`:
        
        ```python
        text_record_manager.add_object_code(actual_address, object_code)
        ```
        
    - After adding, `LocationCounter` is updated based on the instruction length within `ObjectCodeGenerator`.
3. **Handling Directives Affecting Addresses**:
    
    - Directives like `LTORG` assign addresses to literals. When processing such directives, ensure that `LocationCounter` is updated accordingly before adding literal object codes to `TextRecordManager`.
4. **Finalization**:
    
    - After processing all lines, retrieve all text records:
        
        ```python
        text_records = text_record_manager.get_text_records()
        ```
        
    - Pass these records to `ObjectProgramWriter` for assembling the final object program.
5. **Writing Output**:
    
    - `ObjectProgramWriter` assembles the final object program using the header record, text records, modification records, and end record.

### 10. Comprehensive Pseudocode Example

Below is an example implementation snippet showcasing the integration of `LocationCounter` within the `TextRecordManager` class.

```python
class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.
    
    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter

    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address

        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True

        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)

        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length

    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()

        # Return the list of all finalized text records
        return self.text_records

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.

        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### 11. Finalization and Output

After processing all lines, the `TextRecordManager` finalizes any remaining object codes and provides the complete list of text records to the `ObjectProgramWriter` for assembling the final object program.

1. **Generating the Header Record**:
    
    - `AssemblerPass2` creates the header record using the program name, starting address, and program length from `LocationCounter`.
2. **Generating the End Record**:
    
    - The end record references the address of the first executable instruction, as determined by `LocationCounter`.
3. **Assembling the Final Object Program**:
    
    - `ObjectProgramWriter` receives the header record, text records from `TextRecordManager`, modification records from `ModificationRecordManager`, and the end record.
    - It assembles these components into the final object program and writes them to the output file.

### 12. Comprehensive Example

Here's an illustrative example of how the `TextRecordManager` interacts with other classes during the assembly process:

```python
class AssemblerPass2:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        self.opcode_handler = OpcodeHandler()
        self.error_handler = ErrorLogHandler()
        self.location_counter = LocationCounter()
        self.text_record_manager = TextRecordManager(self.location_counter)
        self.modification_record_manager = ModificationRecordManager()
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler,
            location_counter=self.location_counter
        )
        self.object_program_writer = ObjectProgramWriter()

    def process_source_lines(self, source_lines: List[SourceCodeLine]):
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue
            # Verify address consistency
            expected_address = self.location_counter.get_current_address_int()
            actual_address = source_line.address
            self.text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
            # Generate object code
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)
            if object_code:
                self.text_record_manager.add_object_code(actual_address, object_code)
                # Handle modification records if necessary
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    self.modification_record_manager.add_modification(
                        address=actual_address + modification_offset,
                        length=modification_length
                    )
            else:
                self.error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
        # Finalize text records and prepare object program
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        header_record = self.create_header_record()
        end_record = self.create_end_record()
        self.object_program_writer.write_object_program(header_record, text_records, modification_records, end_record)

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Handles assembly directives such as BYTE, WORD, RESB, RESW, BASE, NOBASE, LTORG.

        :param source_line: The current SourceCodeLine being processed.
        """
        # Implementation of directive handling, including updating LocationCounter
        pass

    def create_header_record(self) -> str:
        """
        Creates the header record for the object program.

        :return: Formatted header record string.
        """
        program_name = self.location_counter.program_name
        starting_address = self.location_counter.starting_address
        program_length = self.location_counter.program_length
        return f"H{program_name:<6}{starting_address:06X}{program_length:06X}"

    def create_end_record(self) -> str:
        """
        Creates the end record for the object program.

        :return: Formatted end record string.
        """
        first_executable_address = self.location_counter.first_executable_address
        return f"E{first_executable_address:06X}"
```

- **Explanation**:
    - **Initialization**: Sets up all necessary components, including `LocationCounter` and `TextRecordManager`.
    - **Processing Source Lines**: Iterates over each source line, handling directives and generating object codes.
    - **Address Verification**: Ensures that each object code is placed at the correct address.
    - **Adding Object Codes**: Adds generated object codes to `TextRecordManager`, managing text records accordingly.
    - **Modification Records**: Adds modification records when necessary for relocatable addresses.
    - **Finalization**: Retrieves all text records and passes them to `ObjectProgramWriter` along with header and end records.

### 13. Additional Design Enhancements

#### a. **Handling Base and PC Relative Addressing**

- **Purpose**: Ensure that object codes are correctly grouped based on addressing modes.
- **Implementation**:
    - Use `LocationCounter` to determine the current address and manage displacement calculations in `ObjectCodeGenerator`.
    - `TextRecordManager` relies on accurate addresses from `LocationCounter` to maintain continuity.

#### b. **Managing Extended Instructions (Format 4)**

- **Purpose**: Properly handle object codes that require extended addressing and relocation.
- **Implementation**:
    - When a format 4 instruction is encountered, ensure that `ObjectCodeGenerator` marks it for modification.
    - `TextRecordManager` manages the addition of such object codes into text records without violating length constraints.

#### c. **Supporting Multiple Control Sections**

- **Purpose**: If the assembler supports multiple control sections, manage object codes across different sections.
- **Implementation**:
    - `TextRecordManager` can reset its state when a new control section starts.
    - Ensure that addresses are correctly managed across sections using `LocationCounter`.

#### d. **Listing File Generation (Optional)**

- **Purpose**: Create a human-readable listing file that combines source lines with their corresponding object codes and addresses for debugging purposes.
- **Implementation**:
    - Integrate a `ListingFileWriter` class that formats and writes the listing file based on processed `SourceCodeLine` objects.

### 14. Code Example

Below is an example implementation snippet showcasing the integration of `LocationCounter` within the `TextRecordManager` class.

```python
class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.
    
    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the TextRecordManager with empty records and default values.

        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.text_records = []
        self.current_record = []
        self.current_start_address = None
        self.current_length = 0
        self.MAX_RECORD_LENGTH = 30
        self.location_counter = location_counter

    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address

        if self.current_record:
            # Get the last object's end address
            last_object_code = self.current_record[-1]
            last_address = address - (len(last_object_code) // 2)
            contiguous = self.is_contiguous(last_address, address)
        else:
            contiguous = True

        if not contiguous:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Calculate the length of the new object code in bytes
        object_length = self.calculate_length(object_code)

        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.finalize_current_record()
            self.current_start_address = address

        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length

    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        if self.current_record:
            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()

        # Return the list of all finalized text records
        return self.text_records

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (len(self.current_record[-1]) // 2)
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            self.log_error(
                f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            )
            # Additional error handling if necessary

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.

        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### 13. Comprehensive Testing Strategies

To ensure the `TextRecordManager` functions correctly with `LocationCounter`, implement the following test cases:

#### a. **Address Consistency**

- **Test Case**: Intermediate file has sequential addresses matching `LocationCounter`.
- **Expected Outcome**: Object codes are added to text records without address mismatch errors.

#### b. **Address Mismatch Detection**

- **Test Case**: Intermediate file contains a line with an address that does not match `LocationCounter`.
- **Expected Outcome**: Error is logged specifying the expected and found addresses, and the object code is not added to the current record.

#### c. **Displacement Calculation**

- **Test Case**: Operand displacement within range for PC-relative and base-relative addressing.
    
- **Expected Outcome**: Correct displacement is calculated, and appropriate flags are set in `ObjectCodeGenerator`.
    
- **Edge Case**: Operand displacement out of range.
    
- **Expected Outcome**: Error is logged indicating displacement out of range, and the object code is not added to the current record.
    

#### d. **Format Handling**

- **Test Case**: Instructions of all formats (1 to 4).
- **Expected Outcome**: Object codes are correctly generated for each format and appropriately grouped into text records.

#### e. **Addressing Modes**

- **Test Case**: Instructions using various addressing modes (immediate, indirect, indexed).
- **Expected Outcome**: Flags are correctly set in `ObjectCodeGenerator`, and object codes reflect addressing modes in the text records.

#### f. **Base Register Usage**

- **Test Case**: Instructions requiring base-relative addressing with `BASE` directive set.
    
- **Expected Outcome**: Displacement is calculated relative to the base register, and `b` flag is set in `ObjectCodeGenerator`.
    
- **Edge Case**: `BASE` register not set when required.
    
- **Expected Outcome**: Error is logged, and displacement calculation fails, preventing object code addition to text records.
    

#### g. **Literal Handling**

- **Test Case**: Instructions referencing literals.
- **Expected Outcome**: Object codes for literals are correctly generated, added to text records, and their addresses are verified against `LocationCounter`.

### 14. Conclusion

The updated `TextRecordManager` design seamlessly integrates the `LocationCounter`, enhancing the assembler's ability to manage and verify addresses accurately during object code organization. By following this comprehensive plan, you ensure that your assembler is robust, maintainable, and capable of handling complex assembly instructions and addressing modes effectively.

- **Scalability**: Designed to handle large assembly programs efficiently by leveraging modular methods and clear interactions with supporting classes.
- **Modularity**: Each method within `TextRecordManager` has a single responsibility, enhancing maintainability and readability.
- **Error Handling**: Comprehensive error checking ensures that all potential issues during text record organization are detected and logged appropriately.
- **Integration with `LocationCounter`**: Ensures that address management is consistent and accurate, reducing the likelihood of address-related errors.
- **Testing**: Implement thorough unit and integration tests to validate each method's functionality, especially the interactions with `LocationCounter` and `ObjectCodeGenerator`.

---

## 4. `ModificationRecordManager`

### Overview
The `ModificationRecordManager` is responsible for tracking and managing modification records essential for the relocation of symbols during the linking and loading phases. Modification records indicate parts of the object code that require adjustments based on the final memory addresses assigned during linking/loading. By integrating the `LocationCounter`, the `ModificationRecordManager` ensures precise tracking of addresses needing modification, thereby facilitating accurate relocation.

### Responsibilities
- **Track Modification Records**: Maintain a list of addresses and lengths that require modification for relocation.
- **Generate Modification Records**: Create formatted modification records that adhere to the assembler's output specifications.
- **Handle Relocatable Symbols**: Identify and record symbols that are relocatable and require adjustments.
- **Integrate with LocationCounter**: Use the `LocationCounter` to verify and manage addresses needing modification.
- **Provide Records for Output**: Supply all finalized modification records to the `ObjectProgramWriter`.

### Attributes
- **`modification_records`**:
    - **Type**: `List[str]`
    - **Description**: Stores all finalized modification records in the order they are created.
- **`location_counter`**:
    - **Type**: `LocationCounter`
    - **Description**: Reference to the `LocationCounter` instance for address verification and management.
- **`MAX_RECORDS_PER_LINE`** (Optional):
    - **Type**: `int`
    - **Description**: (If needed) Maximum number of modification records per output line.
    - **Value**: Implementation-specific; could be based on output format constraints.

### Methods
#### A. Initialization
1. **`__init__(self, location_counter: LocationCounter)`**
    
    ```python
    def __init__(self, location_counter: LocationCounter):
        self.modification_records = []         # List to store finalized modification records
        self.location_counter = location_counter  # Reference to the LocationCounter
    ```
    
    - **Purpose**: Sets up the initial state of the `ModificationRecordManager` with an empty list of modification records and integrates the `LocationCounter` for address management.
#### B. Core Functionality
2. **`add_modification(self, address: int, length: int)`**
    ```python
    def add_modification(self, address: int, length: int):
        """
        Records a modification at the specified address with the given length.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        """
        # Validate address and length
        if not self.validate_modification(address, length):
            return  # Validation failed; error already logged
        
        # Format the modification record
        formatted_record = f"M^{address:06X}^{length:02X}"
        
        # Add to the list of modification records
        self.modification_records.append(formatted_record)
        
        # Optional: Log the action
        self.location_counter.error_handler.log_action(
            f"Added modification record: {formatted_record}"
        )
    ```
    - **Parameters**:
        - `address`: The memory address that requires modification.
        - `length`: The length in half-bytes (nibbles) that need to be modified.
    - **Purpose**: Adds a new modification record ensuring that the address and length are valid. Formats the record according to the specified output format and appends it to the `modification_records` list.
    - **Details**:
        - **Validation**: Ensures that the `address` and `length` are within acceptable ranges.
        - **Formatting**: Adheres to the `M^Address^Length` format.
3. **`finalize_modification_records(self)`**
    
    ```python
    def finalize_modification_records(self):
        """
        Finalizes all modification records, if any final processing is required.
        Currently, modification records are stored as formatted strings.
        """
        # Implementation can include grouping records if necessary
        pass
    ```
    
    - **Purpose**: Finalizes the modification records. Currently, since modification records are stored as formatted strings upon addition, no additional processing is required. This method is a placeholder for future enhancements, such as grouping multiple modifications into a single output line if needed.
4. **`get_modification_records(self) -> List[str]`**
    
    ```python
    def get_modification_records(self) -> List[str]:
        """
        Retrieves all finalized modification records.
        
        :return: A list of formatted modification record strings.
        """
        # Finalize any remaining modification records
        self.finalize_modification_records()
        
        return self.modification_records
    ```
    
    - **Purpose**: Returns all finalized modification records, ensuring that any final processing is completed before retrieval.

#### C. Helper Functions

1. **`validate_modification(self, address: int, length: int) -> bool`**
    
    ```python
    def validate_modification(self, address: int, length: int) -> bool:
        """
        Validates the modification parameters.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        :return: True if valid, False otherwise.
        """
        # Example validation: address should be within program range
        program_length = self.location_counter.program_length
        if address < 0 or address + (length // 2) > program_length:
            self.log_error(
                f"Invalid modification address or length: Address={address:06X}, Length={length}"
            )
            return False
        
        # Additional validations can be added here
        
        return True
    ```
    
    - **Parameters**:
        - `address`: The memory address that requires modification.
        - `length`: The length in half-bytes (nibbles) that need to be modified.
    - **Purpose**: Ensures that the modification parameters are within acceptable ranges and do not exceed program boundaries.
    - **Returns**: `True` if the parameters are valid, `False` otherwise.

2. **`log_error(self, message: str)`**
    
    ```python
    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.
        
        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
    ```
    - **Parameters**:
        - `message`: The error message to be logged.
    - **Purpose**: Logs an error message using the integrated `ErrorHandler` from the `LocationCounter`.

#### D. Edge Case Handling
7. **Handling Duplicate Modifications**
    - **Scenario**: Multiple modification records targeting the same address.
    - **Implementation**:
        - Before adding a modification, check if a record for the same address already exists.
        - Decide whether to allow duplicates, merge lengths, or log a warning/error.
        - Example implementation
            ```python
            def add_modification(self, address: int, length: int):
                if any(record.startswith(f"M^{address:06X}") for record in self.modification_records):
                    self.log_error(
                        f"Duplicate modification record for address {address:06X}."
                    )
                    return
                # Proceed to add as usual
            ```
            
8. **Handling Invalid Modification Parameters**
    - **Scenario**: Negative addresses, zero-length modifications, or lengths exceeding limits.
    - **Implementation**:
        - Utilize the `validate_modification` helper method to detect and handle such cases.
        - Log appropriate error messages and prevent adding invalid records.
9. **Handling Maximum Modification Records**
    - **Scenario**: Exceeding any predefined limits on the number of modification records.
    - **Implementation**:
        - Implement checks within `add_modification` to ensure limits are not breached.
        - Log errors or warnings if limits are exceeded.
        - Example:
            
            ```python
            def add_modification(self, address: int, length: int):
                if len(self.modification_records) >= self.MAX_MODIFICATION_RECORDS:
                    self.log_error(
                        f"Maximum number of modification records ({self.MAX_MODIFICATION_RECORDS}) exceeded."
                    )
                    return
                # Proceed to add as usual
            ```
            

### Interactions with Other Classes
- **`ObjectCodeGenerator`**
    - **Role**: Identifies symbols and instructions that require relocation.
    - **Interaction**: Calls `modification_record_manager.add_modification(address, length)` to record necessary modifications when generating object codes for relocatable symbols or format 4 instructions.
- **`LocationCounter`**:
    - **Role**: Manages current address, program length, and other address-related operations.
    - **Interaction**: Provides information for validating modification records and logging errors.
- **`ErrorLogHandler`**:
    - **Role**: Manages logging of errors and actions.
    - **Interaction**: `ModificationRecordManager` utilizes it through `LocationCounter` to log any errors encountered during modification record handling.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the second pass of the assembly process, generating object codes, text records, and modification records.
    - **Interaction**: Utilizes `ModificationRecordManager` to track and manage all modification records during object code generation.
- **`ObjectProgramWriter`**:
    - **Role**: Assembles the final object program.
    - **Interaction**: Receives the finalized modification records from `ModificationRecordManager` to include them in the final object program.

### Pseudocode Examples
Below are detailed pseudocode examples for each method within the `ModificationRecordManager` class to illustrate how the class operates, especially with the integration of the `LocationCounter`.
#### A. `__init__` Method
```python
class ModificationRecordManager:
    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the ModificationRecordManager with an empty list of modification records.
        
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.modification_records = []             # List to store finalized modification records
        self.location_counter = location_counter   # Reference to the LocationCounter
```
#### B. `add_modification` Method
```python
def add_modification(self, address: int, length: int):
    """
    Records a modification at the specified address with the given length.
    
    :param address: The memory address that requires modification.
    :param length: The length in half-bytes (nibbles) that need to be modified.
    """
    # Validate modification parameters
    if not self.validate_modification(address, length):
        return  # Validation failed; error already logged
    
    # Check for duplicate modification records
    if any(record.startswith(f"M^{address:06X}") for record in self.modification_records):
        self.log_error(
            f"Duplicate modification record for address {address:06X}."
        )
        return
    
    # Format the modification record as per the specification
    formatted_record = f"M^{address:06X}^{length:02X}"
    
    # Add the formatted record to the list of modification records
    self.modification_records.append(formatted_record)
    
    # Optional: Log the action
    self.location_counter.error_handler.log_action(
        f"Added modification record: {formatted_record}"
    )
```
- **Explanation**:
    - **Validation**: Ensures that the `address` and `length` are within valid ranges.
    - **Duplication Check**: Prevents adding multiple modification records for the same address.
    - **Formatting**: Adheres to the `M^Address^Length` format.
    - **Logging**: Optionally logs the addition of a new modification record.

#### C. `finalize_modification_records` Method
```python
def finalize_modification_records(self):
    """
    Finalizes all modification records, performing any necessary final processing.
    Currently, no additional processing is required as records are stored as formatted strings.
    """
    # Placeholder for future enhancements, such as grouping records or additional formatting
    pass
```
- **Explanation**:
    - Currently, modification records are stored as formatted strings upon addition. This method serves as a placeholder for any future processing needs.

#### D. `get_modification_records` Method
```python
def get_modification_records(self) -> List[str]:
    """
    Retrieves all finalized modification records.
    
    :return: A list of formatted modification record strings.
    """
    # Finalize any remaining modification records
    self.finalize_modification_records()
    
    # Return the list of all finalized modification records
    return self.modification_records
```
- **Explanation**:
    - Ensures that any final processing is completed before retrieving the modification records.
#### E. `validate_modification` Helper Method
```python
def validate_modification(self, address: int, length: int) -> bool:
    """
    Validates the modification parameters.
    
    :param address: The memory address that requires modification.
    :param length: The length in half-bytes (nibbles) that need to be modified.
    :return: True if valid, False otherwise.
    """
    # Example validation: address should be within program range
    program_length = self.location_counter.program_length
    if address < 0 or address + (length // 2) > program_length:
        self.log_error(
            f"Invalid modification address or length: Address={address:06X}, Length={length}"
        )
        return False
    
    # Additional validations can be implemented here
    
    return True
```
- **Explanation**:
    - Ensures that the modification does not exceed the program's memory bounds.
    - Prevents negative addresses and zero-length modifications.
    - Logs an error message if validation fails.
#### F. `log_error` Method
```python
def log_error(self, message: str):
    """
    Logs an error message using the integrated ErrorHandler from the LocationCounter.
    
    :param message: The error message to be logged.
    """
    self.location_counter.error_handler.log_error(message)
```

- **Explanation**:
    - Utilizes the `ErrorHandler` from `LocationCounter` to log error messages related to modification records.

### Example Workflow Incorporating `LocationCounter`

Here's how the `ModificationRecordManager` operates within the assembly process, leveraging the `LocationCounter`:

1. **Initialization**:
    
    - `AssemblerPass2` initializes all components, including `LocationCounter` and `ModificationRecordManager`.
    - `ModificationRecordManager` is instantiated with a reference to the `LocationCounter`.
2. **Generating Object Code**:
    
    - For each `SourceCodeLine`, `ObjectCodeGenerator` generates the `object_code`.
    - If the instruction requires relocation (e.g., format 4 instructions or relocatable symbols), `ObjectCodeGenerator` determines the `address` and `length` that need modification.
    - `ObjectCodeGenerator` calls `modification_record_manager.add_modification(address, length)` to record the necessary modifications.
    - `LocationCounter` ensures that the `address` is valid and within the program's memory range.
3. **Handling Directives Affecting Addresses**:
    
    - Directives like `BASE` may affect how modifications are calculated.
    - Ensure that `LocationCounter` is updated accordingly before any modifications are recorded.
4. **Finalization**:
    
    - After processing all lines, retrieve all modification records:
        
        ```python
        modification_records = modification_record_manager.get_modification_records()
        ```
        
    - Pass these records to `ObjectProgramWriter` for assembling the final object program.
5. **Writing Output**:
    
    - `ObjectProgramWriter` assembles the final object program using the header record, text records from `TextRecordManager`, modification records from `ModificationRecordManager`, and the end record.
    - Writes the assembled object program to the output file.

### Comprehensive Pseudocode Example

Below is an example implementation snippet showcasing the integration of `LocationCounter` within the `ModificationRecordManager` class.

```python
class ModificationRecordManager:
    """
    Manages the creation and organization of modification records in the object program.
    
    Responsibilities:
        - Tracks addresses that require modification for relocation.
        - Generates formatted modification records.
        - Validates modification parameters.
        - Integrates with LocationCounter for address management and error logging.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the ModificationRecordManager with an empty list of modification records.
        
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.modification_records = []             # List to store finalized modification records
        self.location_counter = location_counter   # Reference to the LocationCounter

    def add_modification(self, address: int, length: int):
        """
        Records a modification at the specified address with the given length.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        """
        # Validate modification parameters
        if not self.validate_modification(address, length):
            return  # Validation failed; error already logged
        
        # Check for duplicate modification records
        if any(record.startswith(f"M^{address:06X}") for record in self.modification_records):
            self.log_error(
                f"Duplicate modification record for address {address:06X}."
            )
            return
        
        # Format the modification record
        formatted_record = f"M^{address:06X}^{length:02X}"
        
        # Add the formatted record to the list of modification records
        self.modification_records.append(formatted_record)
        
        # Optional: Log the action
        self.location_counter.error_handler.log_action(
            f"Added modification record: {formatted_record}"
        )

    def finalize_modification_records(self):
        """
        Finalizes all modification records, performing any necessary final processing.
        Currently, modification records are stored as formatted strings.
        """
        # Placeholder for future enhancements, such as grouping records or additional formatting
        pass

    def get_modification_records(self) -> List[str]:
        """
        Retrieves all finalized modification records.
        
        :return: A list of formatted modification record strings.
        """
        # Finalize any remaining modification records
        self.finalize_modification_records()
        
        return self.modification_records

    def validate_modification(self, address: int, length: int) -> bool:
        """
        Validates the modification parameters.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        :return: True if valid, False otherwise.
        """
        # Example validation: address should be within program range
        program_length = self.location_counter.program_length
        if address < 0 or address + (length // 2) > program_length:
            self.log_error(
                f"Invalid modification address or length: Address={address:06X}, Length={length}"
            )
            return False
        
        # Additional validations can be implemented here
        
        return True

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.
        
        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

- **Explanation**:
    - **Initialization**: Sets up the manager with an empty list and integrates `LocationCounter`.
    - **Adding Modifications**: Validates, checks for duplicates, formats, and records modifications.
    - **Finalization**: Placeholder for any future processing needs.
    - **Retrieving Records**: Ensures all records are finalized before retrieval.
    - **Validation**: Ensures modifications are within program bounds.
    - **Error Logging**: Uses `LocationCounter`'s `ErrorHandler` to log errors.

### Integration with `AssemblerPass2`

Below is an example of how the `ModificationRecordManager` integrates within the `AssemblerPass2` class during the assembly process.

```python
class AssemblerPass2:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        self.opcode_handler = OpcodeHandler()
        self.error_handler = ErrorLogHandler()
        self.location_counter = LocationCounter()
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler,
            location_counter=self.location_counter
        )
        self.text_record_manager = TextRecordManager(self.location_counter)
        self.modification_record_manager = ModificationRecordManager(self.location_counter)
        self.object_program_writer = ObjectProgramWriter()

    def process_source_lines(self, source_lines: List[SourceCodeLine]):
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue
            # Verify address consistency
            expected_address = self.location_counter.get_current_address_int()
            actual_address = source_line.address
            self.text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
            # Generate object code
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)
            if object_code:
                self.text_record_manager.add_object_code(actual_address, object_code)
                # Handle modification records if necessary
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    modification_address = actual_address + modification_offset
                    self.modification_record_manager.add_modification(modification_address, modification_length)
            else:
                self.error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
        # Finalize text records and prepare object program
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        header_record = self.create_header_record()
        end_record = self.create_end_record()
        self.object_program_writer.write_object_program(header_record, text_records, modification_records, end_record)

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Handles assembly directives such as BYTE, WORD, RESB, RESW, BASE, NOBASE, LTORG.
        
        :param source_line: The current SourceCodeLine being processed.
        """
        # Implementation of directive handling, including updating LocationCounter and possibly modification records
        pass

    def create_header_record(self) -> str:
        """
        Creates the header record for the object program.
        
        :return: Formatted header record string.
        """
        program_name = self.location_counter.program_name
        starting_address = self.location_counter.starting_address
        program_length = self.location_counter.program_length
        return f"H{program_name:<6}{starting_address:06X}{program_length:06X}"

    def create_end_record(self) -> str:
        """
        Creates the end record for the object program.
        
        :return: Formatted end record string.
        """
        first_executable_address = self.location_counter.first_executable_address
        return f"E{first_executable_address:06X}"
```

- **Explanation**:
    - **Initialization**: Sets up all necessary components, including `LocationCounter` and `ModificationRecordManager`.
    - **Processing Source Lines**:
        - Skips comments and lines with existing errors.
        - Handles directives appropriately.
        - Verifies address consistency using `TextRecordManager`.
        - Generates object codes using `ObjectCodeGenerator`.
        - Adds object codes to `TextRecordManager`.
        - If modifications are required (e.g., format 4 instructions), records them using `ModificationRecordManager`.
        - Logs errors if object code generation fails.
    - **Finalization**:
        - Retrieves all text and modification records.
        - Creates header and end records using `LocationCounter`.
        - Passes all records to `ObjectProgramWriter` to assemble the final object program.

### Testing the `ModificationRecordManager`

To ensure the `ModificationRecordManager` functions correctly with `LocationCounter`, implement the following test cases:

#### a. **Valid Modification Recording**

- **Test Case**: Adding a modification record with a valid address and length.
- **Expected Outcome**: Modification record is added successfully without errors.

#### b. **Invalid Modification Parameters**

- **Test Case**: Adding a modification record with an address outside the program range or an invalid length.
- **Expected Outcome**: Error is logged, and the modification record is not added.

#### c. **Duplicate Modification Records**

- **Test Case**: Adding multiple modification records for the same address.
- **Expected Outcome**: Error is logged for duplicate records, and subsequent duplicates are not added.

#### d. **Maximum Modification Records**

- **Test Case**: Adding modification records up to and exceeding any predefined maximum limit (if implemented).
- **Expected Outcome**: Records are added up to the limit; attempts to exceed the limit result in errors.

#### e. **Edge Cases**

- **Test Case**: Adding a modification record with zero length.
- **Expected Outcome**: Error is logged, and the modification record is not added.
- **Test Case**: Adding a modification record with maximum possible length.
- **Expected Outcome**: Record is added successfully, ensuring boundary conditions are handled.

### Documentation and Code Comments

Ensure that all methods within the `ModificationRecordManager` class are well-documented with clear docstrings and inline comments explaining their purpose, parameters, and logic. This practice facilitates maintenance and future enhancements.

```python
class ModificationRecordManager:
    """
    Manages the creation and organization of modification records in the object program.
    
    Responsibilities:
        - Tracks addresses that require modification for relocation.
        - Generates formatted modification records.
        - Validates modification parameters.
        - Integrates with LocationCounter for address management and error logging.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the ModificationRecordManager with an empty list of modification records.
        
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.modification_records = []             # List to store finalized modification records
        self.location_counter = location_counter   # Reference to the LocationCounter

    def add_modification(self, address: int, length: int):
        """
        Records a modification at the specified address with the given length.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        """
        # Validate modification parameters
        if not self.validate_modification(address, length):
            return  # Validation failed; error already logged
        
        # Check for duplicate modification records
        if any(record.startswith(f"M^{address:06X}") for record in self.modification_records):
            self.log_error(
                f"Duplicate modification record for address {address:06X}."
            )
            return
        
        # Format the modification record
        formatted_record = f"M^{address:06X}^{length:02X}"
        
        # Add the formatted record to the list of modification records
        self.modification_records.append(formatted_record)
        
        # Optional: Log the action
        self.location_counter.error_handler.log_action(
            f"Added modification record: {formatted_record}"
        )

    def finalize_modification_records(self):
        """
        Finalizes all modification records, performing any necessary final processing.
        Currently, modification records are stored as formatted strings.
        """
        # Placeholder for future enhancements, such as grouping records or additional formatting
        pass

    def get_modification_records(self) -> List[str]:
        """
        Retrieves all finalized modification records.
        
        :return: A list of formatted modification record strings.
        """
        # Finalize any remaining modification records
        self.finalize_modification_records()
        
        return self.modification_records

    def validate_modification(self, address: int, length: int) -> bool:
        """
        Validates the modification parameters.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        :return: True if valid, False otherwise.
        """
        # Example validation: address should be within program range
        program_length = self.location_counter.program_length
        if address < 0 or address + (length // 2) > program_length:
            self.log_error(
                f"Invalid modification address or length: Address={address:06X}, Length={length}"
            )
            return False
        
        # Additional validations can be implemented here
        
        return True

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.
        
        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### Example Usage

Here's how the `ModificationRecordManager` might be used within the `AssemblerPass2` class during the assembly process.

```python
class AssemblerPass2:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        self.opcode_handler = OpcodeHandler()
        self.error_handler = ErrorLogHandler()
        self.location_counter = LocationCounter()
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler,
            location_counter=self.location_counter
        )
        self.text_record_manager = TextRecordManager(self.location_counter)
        self.modification_record_manager = ModificationRecordManager(self.location_counter)
        self.object_program_writer = ObjectProgramWriter()

    def process_source_lines(self, source_lines: List[SourceCodeLine]):
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue
            # Verify address consistency
            expected_address = self.location_counter.get_current_address_int()
            actual_address = source_line.address
            self.text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
            # Generate object code
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)
            if object_code:
                self.text_record_manager.add_object_code(actual_address, object_code)
                # Handle modification records if necessary
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    modification_address = actual_address + modification_offset
                    self.modification_record_manager.add_modification(modification_address, modification_length)
            else:
                self.error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
        # Finalize text records and prepare object program
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        header_record = self.create_header_record()
        end_record = self.create_end_record()
        self.object_program_writer.write_object_program(header_record, text_records, modification_records, end_record)

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Handles assembly directives such as BYTE, WORD, RESB, RESW, BASE, NOBASE, LTORG.
        
        :param source_line: The current SourceCodeLine being processed.
        """
        # Implementation of directive handling, including updating LocationCounter and possibly modification records
        pass

    def create_header_record(self) -> str:
        """
        Creates the header record for the object program.
        
        :return: Formatted header record string.
        """
        program_name = self.location_counter.program_name
        starting_address = self.location_counter.starting_address
        program_length = self.location_counter.program_length
        return f"H{program_name:<6}{starting_address:06X}{program_length:06X}"

    def create_end_record(self) -> str:
        """
        Creates the end record for the object program.
        
        :return: Formatted end record string.
        """
        first_executable_address = self.location_counter.first_executable_address
        return f"E{first_executable_address:06X}"
```

- **Explanation**:
    - **Adding Modifications**: When `ObjectCodeGenerator` identifies that a `SourceCodeLine` requires modification (e.g., a format 4 instruction), it calculates the `modification_offset` and `modification_length` and records the modification using `ModificationRecordManager`.
    - **Finalization**: After processing all source lines, retrieves both text and modification records to assemble the final object program.


### Additional Design Enhancements

#### a. **Handling Relocatable Symbols**

- **Purpose**: Ensure that symbols requiring relocation are accurately tracked and recorded for modification.
- **Implementation**:
    - `ObjectCodeGenerator` identifies relocatable symbols during object code generation.
    - Upon identifying a relocatable symbol, `ObjectCodeGenerator` calculates the necessary `address` and `length` and records the modification using `ModificationRecordManager`.

#### b. **Supporting Multiple Control Sections**

- **Purpose**: If the assembler supports multiple control sections, manage modification records across different sections.
- **Implementation**:
    - Reset or appropriately manage `modification_records` when a new control section starts.
    - Ensure that addresses are correctly scoped within each control section using `LocationCounter`.

#### c. **Optimizing Modification Records**

- **Purpose**: Reduce the number of modification records by merging overlapping or adjacent modifications.
- **Implementation**:
    - Before adding a new modification record, check if it can be merged with an existing one.
    - If overlapping or adjacent, adjust the existing record's `length` accordingly.

#### d. **Listing File Integration (Optional)**

- **Purpose**: Include modification records in the listing file for debugging purposes.
- **Implementation**:
    - Integrate with a `ListingFileWriter` class to append modification record information alongside source lines and object codes.

### Interaction Diagram

```plaintext
ModificationRecordManager
    |
    |-- LocationCounter
    |
    |-- ErrorLogHandler <-- ModificationRecordManager
    |
    |-- ObjectCodeGenerator <-- ModificationRecordManager
    |
    |-- AssemblerPass2 <-- ModificationRecordManager
    |
    |-- ObjectProgramWriter <-- ModificationRecordManager
```

- **Flow**:
    1. **Modification Identification**: `ObjectCodeGenerator` identifies that an object code requires relocation.
    2. **Recording Modifications**: Calls `ModificationRecordManager.add_modification(address, length)` to record the necessary modification.
    3. **Validation and Logging**: `ModificationRecordManager` uses `LocationCounter` to validate the address and logs any errors via `ErrorLogHandler`.
    4. **Finalization**: `AssemblerPass2` retrieves all modification records using `ModificationRecordManager.get_modification_records()` and passes them to `ObjectProgramWriter`.
    5. **Output Assembly**: `ObjectProgramWriter` assembles the final object program, incorporating modification records for relocation.

### Comprehensive Pseudocode Example

To encapsulate the entire functionality, here's a summary of the `ModificationRecordManager` pseudocode with `LocationCounter` integration:

```python
class ModificationRecordManager:
    """
    Manages the creation and organization of modification records in the object program.
    
    Responsibilities:
        - Tracks addresses that require modification for relocation.
        - Generates formatted modification records.
        - Validates modification parameters.
        - Integrates with LocationCounter for address management and error logging.
    """

    def __init__(self, location_counter: LocationCounter):
        """
        Initializes the ModificationRecordManager with an empty list of modification records.
        
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.modification_records = []             # List to store finalized modification records
        self.location_counter = location_counter   # Reference to the LocationCounter

    def add_modification(self, address: int, length: int):
        """
        Records a modification at the specified address with the given length.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        """
        # Validate modification parameters
        if not self.validate_modification(address, length):
            return  # Validation failed; error already logged
        
        # Check for duplicate modification records
        if any(record.startswith(f"M^{address:06X}") for record in self.modification_records):
            self.log_error(
                f"Duplicate modification record for address {address:06X}."
            )
            return
        
        # Format the modification record
        formatted_record = f"M^{address:06X}^{length:02X}"
        
        # Add the formatted record to the list of modification records
        self.modification_records.append(formatted_record)
        
        # Optional: Log the action
        self.location_counter.error_handler.log_action(
            f"Added modification record: {formatted_record}"
        )

    def finalize_modification_records(self):
        """
        Finalizes all modification records, performing any necessary final processing.
        Currently, modification records are stored as formatted strings.
        """
        # Placeholder for future enhancements, such as grouping records or additional formatting
        pass

    def get_modification_records(self) -> List[str]:
        """
        Retrieves all finalized modification records.
        
        :return: A list of formatted modification record strings.
        """
        # Finalize any remaining modification records
        self.finalize_modification_records()
        
        return self.modification_records

    def validate_modification(self, address: int, length: int) -> bool:
        """
        Validates the modification parameters.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        :return: True if valid, False otherwise.
        """
        # Example validation: address should be within program range
        program_length = self.location_counter.program_length
        if address < 0 or address + (length // 2) > program_length:
            self.log_error(
                f"Invalid modification address or length: Address={address:06X}, Length={length}"
            )
            return False
        
        # Additional validations can be implemented here
        
        return True

    def log_error(self, message: str):
        """
        Logs an error message using the integrated ErrorHandler from the LocationCounter.
        
        :param message: The error message to be logged.
        """
        self.location_counter.error_handler.log_error(message)
```

### Final Considerations
- **Scalability**: The `ModificationRecordManager` is designed to handle a large number of modification records efficiently by using simple list operations and checks.
- **Modularity**: Each method within `ModificationRecordManager` has a single responsibility, enhancing maintainability and readability.
- **Error Handling**: Comprehensive error checking ensures that all potential issues during modification record handling are detected and logged appropriately.
- **Integration with `LocationCounter`**: Ensures that address management is consistent and accurate, reducing the likelihood of address-related errors.
- **Testing**: Implement thorough unit and integration tests to validate each method's functionality, especially the interactions with `LocationCounter` and `ObjectCodeGenerator`.
- **Future Enhancements**:
    - **Grouping Modifications**: Implement logic to group multiple modifications into a single record if the output format allows.
    - **Dynamic Lengths**: Adjust the `length` field dynamically based on the requirements of the relocation process.
    - **Optimization**: Optimize storage and retrieval of modification records for faster access during the linking/loading phases.

---
## 5. `ObjectProgramWriter`

### Overview

The `ObjectProgramWriter` is responsible for assembling all the records generated during the assembly process into the final object program. It consolidates the header, text, modification, and end records into a structured format and writes the assembled program to an output file. By integrating with other components like `TextRecordManager` and `ModificationRecordManager`, it ensures that all necessary records are accurately compiled and formatted according to the assembler's specifications.

### Responsibilities

- **Assemble Object Program**: Combine the header, text, modification, and end records into the final object program.
- **Format Records**: Ensure that all records adhere to the specified formats.
- **Write to Output File**: Output the assembled object program to a designated file.
- **Handle Multiple Control Sections** (If applicable): Manage and assemble records from multiple control sections seamlessly.
- **Error Handling**: Ensure that all necessary records are present and correctly formatted before writing to the file.

### Attributes

- **`header_record`**:
    - **Type**: `str`
    - **Description**: The formatted header record string, adhering to the `H^ProgramName^StartAddress^ProgramLength` format.
- **`text_records`**:
    - **Type**: `List[str]`
    - **Description**: A list of formatted text record strings, each adhering to the `T^StartAddress^Length^ObjectCodes` format.
- **`modification_records`**:
    - **Type**: `List[str]`
    - **Description**: A list of formatted modification record strings, each adhering to the `M^Address^Length` format.
- **`end_record`**:
    - **Type**: `str`
    - **Description**: The formatted end record string, adhering to the `E^FirstExecutableInstructionAddress` format.
- **`error_handler`**:
    - **Type**: `ErrorLogHandler`
    - **Description**: Reference to the `ErrorLogHandler` instance for logging any errors encountered during the writing process.

### Methods

#### A. Initialization

1. **`__init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler)`**
    
    ```python
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        self.header_record = header_record                    # The header record string
        self.text_records = text_records                      # List of text record strings
        self.modification_records = modification_records      # List of modification record strings
        self.end_record = end_record                          # The end record string
        self.error_handler = error_handler                    # Reference to the ErrorLogHandler
    ```
    
    - **Purpose**: Initializes the `ObjectProgramWriter` with all necessary records and a reference to the `ErrorLogHandler`. Sets up the initial state for assembling and writing the object program.

#### B. Core Functionality

2. **`assemble_object_program(self) -> str`**
    
    ```python
    def assemble_object_program(self) -> str:
        """
        Assembles all records into the final object program string.
        
        :return: The complete object program as a single string.
        """
        object_program = ""
        
        # Append header record
        if self.header_record:
            object_program += f"{self.header_record}\n"
        else:
            self.error_handler.log_error("Header record is missing.")
        
        # Append text records
        for text_record in self.text_records:
            object_program += f"{text_record}\n"
        
        # Append modification records
        for modification_record in self.modification_records:
            object_program += f"{modification_record}\n"
        
        # Append end record
        if self.end_record:
            object_program += f"{self.end_record}\n"
        else:
            self.error_handler.log_error("End record is missing.")
        
        return object_program
    ```
    
    - **Purpose**: Combines all individual records into the final object program string, ensuring each record is correctly formatted and ordered.
    - **Details**:
        - Validates the presence of mandatory records (`header_record` and `end_record`).
        - Logs errors if any essential records are missing.
        - Concatenates all records, separated by newline characters.
3. **`write_to_file(self, file_name: str)`**
    
    ```python
    def write_to_file(self, file_name: str):
        """
        Writes the assembled object program to the specified output file.
        
        :param file_name: The name/path of the output file.
        """
        object_program = self.assemble_object_program()
        
        try:
            with open(file_name, 'w') as file:
                file.write(object_program)
            self.error_handler.log_action(f"Object program successfully written to {file_name}.")
        except IOError as e:
            self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
    ```
    
    - **Parameters**:
        - `file_name`: The name or path of the output file where the object program will be written.
    - **Purpose**: Outputs the assembled object program to a specified file, handling any I/O errors gracefully.
    - **Details**:
        - Utilizes the `assemble_object_program` method to get the complete object program.
        - Handles file opening and writing within a `try-except` block to catch and log any I/O-related errors.

#### C. Helper Functions

4. **`validate_records(self)`**
    
    ```python
    def validate_records(self) -> bool:
        """
        Validates that all necessary records are present and correctly formatted.
        
        :return: True if all records are valid, False otherwise.
        """
        is_valid = True
        
        # Validate header record
        if not self.header_record:
            self.error_handler.log_error("Header record is missing.")
            is_valid = False
        elif not self.header_record.startswith("H"):
            self.error_handler.log_error("Header record format is incorrect.")
            is_valid = False
        
        # Validate end record
        if not self.end_record:
            self.error_handler.log_error("End record is missing.")
            is_valid = False
        elif not self.end_record.startswith("E"):
            self.error_handler.log_error("End record format is incorrect.")
            is_valid = False
        
        # Additional validations can be added here (e.g., text and modification records)
        
        return is_valid
    ```
    
    - **Purpose**: Ensures that all necessary records are present and adhere to the required formats before assembling the object program.
    - **Details**:
        - Checks the presence and correct starting character of the header and end records.
        - Can be extended to include format checks for text and modification records.
5. **`format_header_record(self, program_name: str, start_address: int, program_length: int) -> str`**
    
    ```python
    def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
        """
        Formats the header record according to the specification.
        
        :param program_name: The name of the program.
        :param start_address: The starting memory address of the program.
        :param program_length: The total length of the program.
        :return: The formatted header record string.
        """
        # Ensure program name is exactly 6 characters, padded with spaces if necessary
        program_name_formatted = f"{program_name:<6}"[:6]
        return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"
    ```
    
    - **Parameters**:
        - `program_name`: The name of the program being assembled.
        - `start_address`: The starting address of the program in memory.
        - `program_length`: The total length of the program.
    - **Purpose**: Generates a correctly formatted header record string based on the provided program details.
    - **Details**:
        - Ensures the program name is exactly 6 characters long, padding with spaces if necessary.
        - Formats the start address and program length as 6-digit hexadecimal numbers.
6. **`format_end_record(self, first_executable_address: int) -> str`**
    
    ```python
    def format_end_record(self, first_executable_address: int) -> str:
        """
        Formats the end record according to the specification.
        
        :param first_executable_address: The address of the first executable instruction.
        :return: The formatted end record string.
        """
        return f"E^{first_executable_address:06X}"
    ```
    
    - **Parameters**:
        - `first_executable_address`: The memory address where execution begins.
    - **Purpose**: Generates a correctly formatted end record string based on the provided address.
    - **Details**:
        - Formats the first executable address as a 6-digit hexadecimal number.

#### D. Edge Case Handling

7. **Handling Missing Records**
    - **Scenario**: Essential records like header or end records are missing.
    - **Implementation**:
        - The `validate_records` method checks for the presence and correct formatting of these records.
        - Logs appropriate error messages if any essential records are missing or malformed.
8. **Handling Multiple Control Sections** (If applicable)
    - **Scenario**: Assembler supports multiple control sections, each requiring separate header and end records.
    - **Implementation**:
        - Modify `ObjectProgramWriter` to handle lists of records for each control section.
        - Iterate through each control section's records, assembling them accordingly.
        - Ensure that each control section's header and end records are correctly formatted and separated.
9. **Handling Large Object Programs**
    - **Scenario**: Assembling very large programs with numerous records.
    - **Implementation**:
        - Optimize the `assemble_object_program` method to handle large lists efficiently.
        - Consider writing records incrementally to the file to manage memory usage.

### Interactions with Other Classes

- **`TextRecordManager`**:
    - **Role**: Manages the creation and organization of text records.
    - **Interaction**: Provides a list of formatted text records to `ObjectProgramWriter` for assembly.
- **`ModificationRecordManager`**:
    - **Role**: Manages relocation information by tracking addresses needing modification.
    - **Interaction**: Provides a list of formatted modification records to `ObjectProgramWriter` for assembly.
- **`LocationCounter`**:
    - **Role**: Manages current address, program length, and other address-related operations.
    - **Interaction**: Supplies program metadata (name, start address, length) and assists in formatting records.
- **`ErrorLogHandler`**:
    - **Role**: Manages logging of errors and actions throughout the assembly process.
    - **Interaction**: `ObjectProgramWriter` utilizes it to log any errors encountered during record assembly and file writing.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the second pass of the assembly process, generating object codes, text records, and modification records.
    - **Interaction**: Collects records from `TextRecordManager` and `ModificationRecordManager` and passes them to `ObjectProgramWriter` for final assembly and output.
- **`ObjectCodeGenerator`**:
    - **Role**: Generates object codes for each instruction.
    - **Interaction**: Identifies symbols and instructions requiring modifications and coordinates with `ModificationRecordManager`.

### Pseudocode Examples

Below are detailed pseudocode examples for each method within the `ObjectProgramWriter` class, illustrating how the class operates and integrates with other components.

#### A. `__init__` Method

```python
class ObjectProgramWriter:
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param error_handler: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record
        self.text_records = text_records
        self.modification_records = modification_records
        self.end_record = end_record
        self.error_handler = error_handler
```

#### B. `assemble_object_program` Method

```python
def assemble_object_program(self) -> str:
    """
    Assembles all records into the final object program string.
    
    :return: The complete object program as a single string.
    """
    object_program = ""
    
    # Append header record
    if self.header_record:
        object_program += f"{self.header_record}\n"
    else:
        self.error_handler.log_error("Header record is missing.")
    
    # Append text records
    for text_record in self.text_records:
        object_program += f"{text_record}\n"
    
    # Append modification records
    for modification_record in self.modification_records:
        object_program += f"{modification_record}\n"
    
    # Append end record
    if self.end_record:
        object_program += f"{self.end_record}\n"
    else:
        self.error_handler.log_error("End record is missing.")
    
    return object_program
```

- **Explanation**:
    - **Header Record**: Checks for the presence of the header record and appends it. Logs an error if missing.
    - **Text Records**: Iterates through all text records and appends each one.
    - **Modification Records**: Iterates through all modification records and appends each one.
    - **End Record**: Checks for the presence of the end record and appends it. Logs an error if missing.
    - **Final Output**: Returns the concatenated string representing the complete object program.

#### C. `write_to_file` Method

```python
def write_to_file(self, file_name: str):
    """
    Writes the assembled object program to the specified output file.
    
    :param file_name: The name/path of the output file.
    """
    object_program = self.assemble_object_program()
    
    try:
        with open(file_name, 'w') as file:
            file.write(object_program)
        self.error_handler.log_action(f"Object program successfully written to {file_name}.")
    except IOError as e:
        self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
```

- **Explanation**:
    - **Assembly**: Calls `assemble_object_program` to get the complete object program.
    - **File Writing**: Attempts to open the specified file in write mode and writes the object program.
    - **Logging**: Logs a success message upon successful writing or an error message if an I/O error occurs.

#### D. `validate_records` Method

```python
def validate_records(self) -> bool:
    """
    Validates that all necessary records are present and correctly formatted.
    
    :return: True if all records are valid, False otherwise.
    """
    is_valid = True
    
    # Validate header record
    if not self.header_record:
        self.error_handler.log_error("Header record is missing.")
        is_valid = False
    elif not self.header_record.startswith("H"):
        self.error_handler.log_error("Header record format is incorrect.")
        is_valid = False
    
    # Validate end record
    if not self.end_record:
        self.error_handler.log_error("End record is missing.")
        is_valid = False
    elif not self.end_record.startswith("E"):
        self.error_handler.log_error("End record format is incorrect.")
        is_valid = False
    
    # Validate text records
    for text_record in self.text_records:
        if not text_record.startswith("T"):
            self.error_handler.log_error(f"Invalid text record format: {text_record}")
            is_valid = False
            break  # Stop further validation on first error
    
    # Validate modification records
    for modification_record in self.modification_records:
        if not modification_record.startswith("M"):
            self.error_handler.log_error(f"Invalid modification record format: {modification_record}")
            is_valid = False
            break  # Stop further validation on first error
    
    return is_valid
```

- **Explanation**:
    - **Header and End Records**: Ensures that both are present and start with the correct characters (`H` and `E` respectively).
    - **Text Records**: Validates that each text record starts with `T`.
    - **Modification Records**: Validates that each modification record starts with `M`.
    - **Error Logging**: Logs specific error messages for any malformed or missing records.
    - **Return Value**: Indicates whether all records are valid (`True`) or if any validation failed (`False`).

#### E. `format_header_record` and `format_end_record` Methods

While these methods are primarily handled by other components (`TextRecordManager` and `AssemblerPass2`), including them here can provide flexibility for re-formatting or regenerating records if needed.

```python
def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
    """
    Formats the header record according to the specification.
    
    :param program_name: The name of the program.
    :param start_address: The starting memory address of the program.
    :param program_length: The total length of the program.
    :return: The formatted header record string.
    """
    # Ensure program name is exactly 6 characters, padded with spaces if necessary
    program_name_formatted = f"{program_name:<6}"[:6]
    return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"

def format_end_record(self, first_executable_address: int) -> str:
    """
    Formats the end record according to the specification.
    
    :param first_executable_address: The address of the first executable instruction.
    :return: The formatted end record string.
    """
    return f"E^{first_executable_address:06X}"
```

- **Purpose**:
    - **Header Record Formatting**: Ensures the program name is exactly 6 characters and formats the header record accordingly.
    - **End Record Formatting**: Formats the end record based on the first executable instruction's address.
- **Note**: Depending on design preferences, these formatting methods can be managed by `AssemblerPass2` or other related classes instead of `ObjectProgramWriter`.

### Interactions with Other Classes

- **`TextRecordManager`**:
    - **Role**: Manages the creation and organization of text records.
    - **Interaction**: Provides a list of formatted text records to `ObjectProgramWriter` for assembly.
- **`ModificationRecordManager`**:
    - **Role**: Manages relocation information by tracking addresses needing modification.
    - **Interaction**: Provides a list of formatted modification records to `ObjectProgramWriter` for assembly.
- **`LocationCounter`**:
    - **Role**: Manages current address, program length, and other address-related operations.
    - **Interaction**: Supplies program metadata (name, start address, length) and assists in formatting records.
- **`ErrorLogHandler`**:
    - **Role**: Manages logging of errors and actions throughout the assembly process.
    - **Interaction**: `ObjectProgramWriter` utilizes it to log any errors encountered during record assembly and file writing.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the second pass of the assembly process, generating object codes, text records, and modification records.
    - **Interaction**: Collects records from `TextRecordManager` and `ModificationRecordManager` and passes them to `ObjectProgramWriter` for final assembly and output.

### Pseudocode Examples

Below are detailed pseudocode examples for each method within the `ObjectProgramWriter` class to illustrate how the class operates and integrates with other components.

#### A. `__init__` Method

```python
class ObjectProgramWriter:
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param error_handler: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record                    # The header record string
        self.text_records = text_records                      # List of text record strings
        self.modification_records = modification_records      # List of modification record strings
        self.end_record = end_record                          # The end record string
        self.error_handler = error_handler                    # Reference to the ErrorLogHandler
```

#### B. `assemble_object_program` Method

```python
def assemble_object_program(self) -> str:
    """
    Assembles all records into the final object program string.
    
    :return: The complete object program as a single string.
    """
    object_program = ""
    
    # Append header record
    if self.header_record:
        object_program += f"{self.header_record}\n"
    else:
        self.error_handler.log_error("Header record is missing.")
    
    # Append text records
    for text_record in self.text_records:
        object_program += f"{text_record}\n"
    
    # Append modification records
    for modification_record in self.modification_records:
        object_program += f"{modification_record}\n"
    
    # Append end record
    if self.end_record:
        object_program += f"{self.end_record}\n"
    else:
        self.error_handler.log_error("End record is missing.")
    
    return object_program
```

- **Explanation**:
    - **Header Record**: Validates and appends the header record.
    - **Text Records**: Iterates through all text records and appends them.
    - **Modification Records**: Iterates through all modification records and appends them.
    - **End Record**: Validates and appends the end record.
    - **Error Logging**: Logs errors if essential records are missing.
    - **Final Output**: Returns the complete object program as a single string, with each record separated by a newline.

#### C. `write_to_file` Method

```python
def write_to_file(self, file_name: str):
    """
    Writes the assembled object program to the specified output file.
    
    :param file_name: The name/path of the output file.
    """
    object_program = self.assemble_object_program()
    
    try:
        with open(file_name, 'w') as file:
            file.write(object_program)
        self.error_handler.log_action(f"Object program successfully written to {file_name}.")
    except IOError as e:
        self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
```

- **Explanation**:
    - **Assembly**: Calls `assemble_object_program` to get the complete object program.
    - **File Writing**: Attempts to open the specified file in write mode and writes the object program.
    - **Logging**: Logs a success message upon successful writing or an error message if an I/O error occurs.

#### D. `validate_records` Method

```python
def validate_records(self) -> bool:
    """
    Validates that all necessary records are present and correctly formatted.
    
    :return: True if all records are valid, False otherwise.
    """
    is_valid = True
    
    # Validate header record
    if not self.header_record:
        self.error_handler.log_error("Header record is missing.")
        is_valid = False
    elif not self.header_record.startswith("H"):
        self.error_handler.log_error("Header record format is incorrect.")
        is_valid = False
    
    # Validate end record
    if not self.end_record:
        self.error_handler.log_error("End record is missing.")
        is_valid = False
    elif not self.end_record.startswith("E"):
        self.error_handler.log_error("End record format is incorrect.")
        is_valid = False
    
    # Validate text records
    for text_record in self.text_records:
        if not text_record.startswith("T"):
            self.error_handler.log_error(f"Invalid text record format: {text_record}")
            is_valid = False
            break  # Stop further validation on first error
    
    # Validate modification records
    for modification_record in self.modification_records:
        if not modification_record.startswith("M"):
            self.error_handler.log_error(f"Invalid modification record format: {modification_record}")
            is_valid = False
            break  # Stop further validation on first error
    
    return is_valid
```

- **Explanation**:
    - **Header and End Records**: Ensures that both are present and start with the correct characters (`H` and `E` respectively).
    - **Text Records**: Validates that each text record starts with `T`.
    - **Modification Records**: Validates that each modification record starts with `M`.
    - **Error Logging**: Logs specific error messages for any malformed or missing records.
    - **Return Value**: Indicates whether all records are valid (`True`) or if any validation failed (`False`).

#### E. `format_header_record` and `format_end_record` Methods

While these methods are primarily handled by other components (`TextRecordManager` and `AssemblerPass2`), including them here can provide flexibility for re-formatting or regenerating records if needed.

```python
def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
    """
    Formats the header record according to the specification.
    
    :param program_name: The name of the program.
    :param start_address: The starting memory address of the program.
    :param program_length: The total length of the program.
    :return: The formatted header record string.
    """
    # Ensure program name is exactly 6 characters, padded with spaces if necessary
    program_name_formatted = f"{program_name:<6}"[:6]
    return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"

def format_end_record(self, first_executable_address: int) -> str:
    """
    Formats the end record according to the specification.
    
    :param first_executable_address: The address of the first executable instruction.
    :return: The formatted end record string.
    """
    return f"E^{first_executable_address:06X}"
```

- **Purpose**:
    - **Header Record Formatting**: Ensures the program name is exactly 6 characters and formats the header record accordingly.
    - **End Record Formatting**: Formats the end record based on the first executable instruction's address.
- **Note**: Depending on design preferences, these formatting methods can be managed by `AssemblerPass2` or other related classes instead of `ObjectProgramWriter`.

### Integration with Other Classes
- **`TextRecordManager`**:
    - **Role**: Manages the creation and organization of text records.
    - **Interaction**: Provides a list of formatted text records to `ObjectProgramWriter` for assembly.
- **`ModificationRecordManager`**:
    - **Role**: Manages relocation information by tracking addresses needing modification.
    - **Interaction**: Provides a list of formatted modification records to `ObjectProgramWriter` for assembly.
- **`LocationCounter`**:
    - **Role**: Manages current address, program length, and other address-related operations.
    - **Interaction**: Supplies program metadata (name, start address, length) and assists in formatting records.
- **`ErrorLogHandler`**:
    - **Role**: Manages logging of errors and actions throughout the assembly process.
    - **Interaction**: `ObjectProgramWriter` utilizes it to log any errors encountered during record assembly and file writing.
- **`AssemblerPass2`**:
    - **Role**: Orchestrates the second pass of the assembly process, generating object codes, text records, and modification records.
    - **Interaction**: Collects records from `TextRecordManager` and `ModificationRecordManager` and passes them to `ObjectProgramWriter` for final assembly and output.
- **`ObjectCodeGenerator`**:
    - **Role**: Generates object codes for each instruction.
    - **Interaction**: Identifies symbols and instructions requiring modifications and coordinates with `ModificationRecordManager`.
### Example Workflow Incorporating `ObjectProgramWriter`
Here's how the `ObjectProgramWriter` operates within the assembly process, leveraging other components for comprehensive functionality:

1. **Initialization**:
    - `AssemblerPass2` initializes all components, including `LocationCounter`, `TextRecordManager`, `ModificationRecordManager`, and `ErrorLogHandler`.
    - `ObjectProgramWriter` is instantiated with the header record, text records, modification records, end record, and a reference to the `ErrorLogHandler`.
2. **Processing Source Lines**:
    - For each `SourceCodeLine`, `AssemblerPass2` performs the following:
        - **Directive Handling**: Processes directives like `BASE`, `NOBASE`, `LTORG`, etc., updating `LocationCounter` as needed.
        - **Address Verification**: Ensures that the address from `SourceCodeLine` matches the expected address from `LocationCounter`.
        - **Object Code Generation**: Uses `ObjectCodeGenerator` to generate the `object_code`.
        - **Adding to Text Records**: Adds the generated `object_code` to `TextRecordManager`.
        - **Recording Modifications**: If the instruction requires relocation (e.g., format 4), calculates the necessary `address` and `length` and records the modification using `ModificationRecordManager`.
        - **Error Logging**: Logs any errors encountered during processing.
3. **Finalizing Records**:
    - After processing all source lines, retrieves all text and modification records:
        ```python
        text_records = text_record_manager.get_text_records()
        modification_records = modification_record_manager.get_modification_records()
        ```
    - Creates the header and end records using information from `LocationCounter`:
        ```python
        header_record = object_program_writer.format_header_record(program_name, start_address, program_length)
        end_record = object_program_writer.format_end_record(first_executable_address)
        ```
    - Initializes `ObjectProgramWriter` with all records:
        ```python
        object_program_writer = ObjectProgramWriter(header_record, text_records, modification_records, end_record, error_handler)
        ```
        
4. **Writing Output**:
    - Calls `write_to_file` to generate the final object program file:
        ```python
        object_program_writer.write_to_file("output.obj")
        ```
    - `ObjectProgramWriter` assembles all records and writes them to the specified file, logging success or any errors encountered.

### Comprehensive Pseudocode Example
Below is an example implementation snippet showcasing the `ObjectProgramWriter` class and its integration within the `AssemblerPass2` class.

```python
class ObjectProgramWriter:
    """
    Manages the assembly of all records into the final object program and writes it to an output file.
    
    Responsibilities:
        - Assembles header, text, modification, and end records into the final object program.
        - Formats records according to the specified output format.
        - Writes the assembled object program to a designated output file.
        - Logs any errors encountered during the writing process.
    """
    
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param error_handler: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record
        self.text_records = text_records
        self.modification_records = modification_records
        self.end_record = end_record
        self.error_handler = error_handler
    
    def assemble_object_program(self) -> str:
        """
        Assembles all records into the final object program string.
        
        :return: The complete object program as a single string.
        """
        object_program = ""
        
        # Append header record
        if self.header_record:
            object_program += f"{self.header_record}\n"
        else:
            self.error_handler.log_error("Header record is missing.")
        
        # Append text records
        for text_record in self.text_records:
            object_program += f"{text_record}\n"
        
        # Append modification records
        for modification_record in self.modification_records:
            object_program += f"{modification_record}\n"
        
        # Append end record
        if self.end_record:
            object_program += f"{self.end_record}\n"
        else:
            self.error_handler.log_error("End record is missing.")
        
        return object_program
    
    def write_to_file(self, file_name: str):
        """
        Writes the assembled object program to the specified output file.
        
        :param file_name: The name/path of the output file.
        """
        object_program = self.assemble_object_program()
        
        try:
            with open(file_name, 'w') as file:
                file.write(object_program)
            self.error_handler.log_action(f"Object program successfully written to {file_name}.")
        except IOError as e:
            self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
    
    def validate_records(self) -> bool:
        """
        Validates that all necessary records are present and correctly formatted.
        
        :return: True if all records are valid, False otherwise.
        """
        is_valid = True
        
        # Validate header record
        if not self.header_record:
            self.error_handler.log_error("Header record is missing.")
            is_valid = False
        elif not self.header_record.startswith("H"):
            self.error_handler.log_error("Header record format is incorrect.")
            is_valid = False
        
        # Validate end record
        if not self.end_record:
            self.error_handler.log_error("End record is missing.")
            is_valid = False
        elif not self.end_record.startswith("E"):
            self.error_handler.log_error("End record format is incorrect.")
            is_valid = False
        
        # Validate text records
        for text_record in self.text_records:
            if not text_record.startswith("T"):
                self.error_handler.log_error(f"Invalid text record format: {text_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        # Validate modification records
        for modification_record in self.modification_records:
            if not modification_record.startswith("M"):
                self.error_handler.log_error(f"Invalid modification record format: {modification_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        return is_valid
    
    def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
        """
        Formats the header record according to the specification.
        
        :param program_name: The name of the program.
        :param start_address: The starting memory address of the program.
        :param program_length: The total length of the program.
        :return: The formatted header record string.
        """
        # Ensure program name is exactly 6 characters, padded with spaces if necessary
        program_name_formatted = f"{program_name:<6}"[:6]
        return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"
    
    def format_end_record(self, first_executable_address: int) -> str:
        """
        Formats the end record according to the specification.
        
        :param first_executable_address: The address of the first executable instruction.
        :return: The formatted end record string.
        """
        return f"E^{first_executable_address:06X}"
```

- **Explanation**:
    - **Initialization**: Sets up the writer with all necessary records and a reference to the `ErrorLogHandler`.
    - **Assemble Object Program**: Concatenates all records into a single string, ensuring proper formatting and order.
    - **Write to File**: Handles writing the assembled object program to a specified file, with error handling for I/O operations.
    - **Validate Records**: Checks the presence and correct formatting of all essential records before assembly.
    - **Format Records**: Provides methods to format header and end records if needed.

#### D. Integration with `AssemblerPass2` Class

Below is an example of how the `ObjectProgramWriter` integrates within the `AssemblerPass2` class during the assembly process.

```python
class AssemblerPass2:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        self.opcode_handler = OpcodeHandler()
        self.error_handler = ErrorLogHandler()
        self.location_counter = LocationCounter()
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler,
            location_counter=self.location_counter
        )
        self.text_record_manager = TextRecordManager(self.location_counter)
        self.modification_record_manager = ModificationRecordManager(self.location_counter)
        self.object_program_writer = None  # Will be initialized after all records are ready
    
    def process_source_lines(self, source_lines: List[SourceCodeLine]):
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue
            # Verify address consistency
            expected_address = self.location_counter.get_current_address_int()
            actual_address = source_line.address
            self.text_record_manager.verify_address_consistency(expected_address, actual_address, source_line.line_number)
            # Generate object code
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)
            if object_code:
                self.text_record_manager.add_object_code(actual_address, object_code)
                # Handle modification records if necessary
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    modification_address = actual_address + modification_offset
                    self.modification_record_manager.add_modification(modification_address, modification_length)
            else:
                self.error_handler.log_error(f"Error at line {source_line.line_number}: {source_line.errors}")
        
        # Finalize text and modification records
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        
        # Create header and end records
        program_name = self.location_counter.program_name
        start_address = self.location_counter.starting_address
        program_length = self.location_counter.program_length
        first_executable_address = self.location_counter.first_executable_address
        
        header_record = self.object_code_generator.format_header_record(program_name, start_address, program_length)
        end_record = self.object_code_generator.format_end_record(first_executable_address)
        
        # Initialize ObjectProgramWriter
        self.object_program_writer = ObjectProgramWriter(
            header_record=header_record,
            text_records=text_records,
            modification_records=modification_records,
            end_record=end_record,
            error_handler=self.error_handler
        )
        
        # Validate all records before writing
        if self.object_program_writer.validate_records():
            # Write to output file
            self.object_program_writer.write_to_file("output.obj")
        else:
            self.error_handler.log_error("Object program assembly failed due to record validation errors.")
    
    def handle_directive(self, source_line: SourceCodeLine):
        """
        Handles assembly directives such as BYTE, WORD, RESB, RESW, BASE, NOBASE, LTORG.
        
        :param source_line: The current SourceCodeLine being processed.
        """
        # Implementation of directive handling, including updating LocationCounter and possibly modification records
        pass
```

- **Explanation**:
    - **Initialization**: Sets up all necessary components, including `LocationCounter`, `TextRecordManager`, `ModificationRecordManager`, and `ErrorLogHandler`.
    - **Processing Source Lines**:
        - **Comments and Errors**: Skips lines that are comments or have pre-existing errors.
        - **Directives**: Processes directives appropriately via `handle_directive`.
        - **Address Verification**: Ensures that each object code is placed at the correct address.
        - **Object Code Generation**: Generates object codes using `ObjectCodeGenerator`.
        - **Adding to Text Records**: Adds generated object codes to `TextRecordManager`.
        - **Recording Modifications**: If required, records necessary modifications using `ModificationRecordManager`.
        - **Error Logging**: Logs any errors encountered during processing.
    - **Finalizing Records**:
        - Retrieves all text and modification records from their respective managers.
        - Creates the header and end records using information from `LocationCounter`.
        - Initializes `ObjectProgramWriter` with all records and the error handler.
    - **Validation and Writing**:
        - Validates all records using `ObjectProgramWriter`.
        - Writes the assembled object program to the output file if validation passes.
        - Logs an error if validation fails, preventing incomplete or malformed object programs.

### Testing the `ObjectProgramWriter`

To ensure the `ObjectProgramWriter` functions correctly and integrates seamlessly with other components, implement the following test cases:
#### a. **Valid Assembly and Writing**
- **Test Case**: Assembling and writing a complete object program with valid header, text, modification, and end records.
- **Input**: Properly formatted records generated by `TextRecordManager` and `ModificationRecordManager`.
- **Expected Outcome**: The object program is correctly assembled and written to the specified output file without errors.
#### b. **Missing Header Record**
- **Test Case**: Attempting to assemble an object program without a header record.
- **Input**: `header_record` is `None` or empty.
- **Expected Outcome**: An error is logged indicating that the header record is missing, and the assembly fails.
#### c. **Missing End Record**
- **Test Case**: Attempting to assemble an object program without an end record.
- **Input**: `end_record` is `None` or empty.
- **Expected Outcome**: An error is logged indicating that the end record is missing, and the assembly fails.
#### d. **Malformed Header Record**
- **Test Case**: Providing a header record that does not start with `H` or does not adhere to the required format.
- **Input**: `header_record` = `"X^Prog^001000^0010"`.
- **Expected Outcome**: An error is logged indicating an incorrect header record format, and the assembly fails.
#### e. **Malformed End Record**
- **Test Case**: Providing an end record that does not start with `E` or does not adhere to the required format.
- **Input**: `end_record` = `"X^0010"`.
- **Expected Outcome**: An error is logged indicating an incorrect end record format, and the assembly fails.
#### f. **Malformed Text Record**
- **Test Case**: Including a text record that does not start with `T`.
- **Input**: `text_records` contains `"X^001000^0A^1F4B"`.
- **Expected Outcome**: An error is logged indicating an invalid text record format, and the assembly fails.
#### g. **Malformed Modification Record**
- **Test Case**: Including a modification record that does not start with `M`.
- **Input**: `modification_records` contains `"X^001010^05"`.
- **Expected Outcome**: An error is logged indicating an invalid modification record format, and the assembly fails.
#### h. **File Writing Errors**
- **Test Case**: Attempting to write to a read-only file or a location without write permissions.
- **Input**: `file_name` points to a read-only file or restricted directory.
- **Expected Outcome**: An I/O error is caught, an error is logged indicating the failure to write, and the assembly process handles the exception gracefully.
#### i. **Multiple Control Sections** (If applicable)
- **Test Case**: Assembling multiple control sections, each with their own header and end records.
- **Input**: Multiple sets of records corresponding to different control sections.
- **Expected Outcome**: Each control section's records are correctly assembled and written, maintaining separation and correct formatting.
#### j. **Large Object Programs**

- **Test Case**: Assembling a very large program with numerous text and modification records.
- **Input**: A large list of text and modification records.
- **Expected Outcome**: The object program is correctly assembled without performance degradation, and all records are accurately written to the output file.

### Documentation and Code Comments

Ensure that the `ObjectProgramWriter` class and its methods are well-documented with clear docstrings and inline comments explaining their purpose, parameters, and logic. This practice facilitates maintenance, debugging, and future enhancements.

```python
class ObjectProgramWriter:
    """
    Manages the assembly of all records into the final object program and writes it to an output file.
    
    Responsibilities:
        - Assembles header, text, modification, and end records into the final object program.
        - Formats records according to the specified output format.
        - Writes the assembled object program to a designated output file.
        - Logs any errors encountered during the writing process.
    """
    
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param error_handler: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record
        self.text_records = text_records
        self.modification_records = modification_records
        self.end_record = end_record
        self.error_handler = error_handler
    
    def assemble_object_program(self) -> str:
        """
        Assembles all records into the final object program string.
        
        :return: The complete object program as a single string.
        """
        object_program = ""
        
        # Append header record
        if self.header_record:
            object_program += f"{self.header_record}\n"
        else:
            self.error_handler.log_error("Header record is missing.")
        
        # Append text records
        for text_record in self.text_records:
            object_program += f"{text_record}\n"
        
        # Append modification records
        for modification_record in self.modification_records:
            object_program += f"{modification_record}\n"
        
        # Append end record
        if self.end_record:
            object_program += f"{self.end_record}\n"
        else:
            self.error_handler.log_error("End record is missing.")
        
        return object_program
    
    def write_to_file(self, file_name: str):
        """
        Writes the assembled object program to the specified output file.
        
        :param file_name: The name/path of the output file.
        """
        object_program = self.assemble_object_program()
        
        try:
            with open(file_name, 'w') as file:
                file.write(object_program)
            self.error_handler.log_action(f"Object program successfully written to {file_name}.")
        except IOError as e:
            self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
    
    def validate_records(self) -> bool:
        """
        Validates that all necessary records are present and correctly formatted.
        
        :return: True if all records are valid, False otherwise.
        """
        is_valid = True
        
        # Validate header record
        if not self.header_record:
            self.error_handler.log_error("Header record is missing.")
            is_valid = False
        elif not self.header_record.startswith("H"):
            self.error_handler.log_error("Header record format is incorrect.")
            is_valid = False
        
        # Validate end record
        if not self.end_record:
            self.error_handler.log_error("End record is missing.")
            is_valid = False
        elif not self.end_record.startswith("E"):
            self.error_handler.log_error("End record format is incorrect.")
            is_valid = False
        
        # Validate text records
        for text_record in self.text_records:
            if not text_record.startswith("T"):
                self.error_handler.log_error(f"Invalid text record format: {text_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        # Validate modification records
        for modification_record in self.modification_records:
            if not modification_record.startswith("M"):
                self.error_handler.log_error(f"Invalid modification record format: {modification_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        return is_valid
    
    def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
        """
        Formats the header record according to the specification.
        
        :param program_name: The name of the program.
        :param start_address: The starting memory address of the program.
        :param program_length: The total length of the program.
        :return: The formatted header record string.
        """
        # Ensure program name is exactly 6 characters, padded with spaces if necessary
        program_name_formatted = f"{program_name:<6}"[:6]
        return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"
    
    def format_end_record(self, first_executable_address: int) -> str:
        """
        Formats the end record according to the specification.
        
        :param first_executable_address: The address of the first executable instruction.
        :return: The formatted end record string.
        """
        return f"E^{first_executable_address:06X}"
```

- **Explanation**:
    - **Docstrings**: Each method includes a clear docstring explaining its purpose, parameters, and return values.
    - **Inline Comments**: Comments within methods clarify specific steps and logic.
    - **Error Handling**: Ensures that all essential records are present and correctly formatted before writing to the output file, logging errors as necessary.

### Implementation Details

#### a. **Header Record Format**

- **Specification**: `H^ProgramName^StartAddress^ProgramLength`
- **Components**:
    - `ProgramName`: Exactly 6 characters, padded with spaces if shorter.
    - `StartAddress`: 6-digit hexadecimal address where the program starts.
    - `ProgramLength`: 6-digit hexadecimal representing the total length of the program.
- **Implementation**:
    - The `format_header_record` method ensures that the program name is correctly formatted and that the start address and program length are represented as 6-digit hexadecimal numbers.

#### b. **End Record Format**

- **Specification**: `E^FirstExecutableInstructionAddress`
- **Components**:
    - `FirstExecutableInstructionAddress`: 6-digit hexadecimal address where execution begins.
- **Implementation**:
    - The `format_end_record` method formats the end record based on the first executable instruction's address.

#### c. **Text Record Format**

- **Specification**: `T^StartAddress^Length^ObjectCodes`
- **Components**:
    - `StartAddress`: 6-digit hexadecimal address where the text record begins.
    - `Length`: 2-digit hexadecimal number representing the length of the object codes in bytes.
    - `ObjectCodes`: Concatenated hexadecimal object codes.
- **Implementation**:
    - Managed by the `TextRecordManager`, which ensures that each text record adheres to the `T` format and length constraints.

#### d. **Modification Record Format**

- **Specification**: `M^Address^Length`
- **Components**:
    - `Address`: 6-digit hexadecimal address requiring modification.
    - `Length`: 2-digit hexadecimal number representing the length in half-bytes (nibbles) that need modification.
- **Implementation**:
    - Managed by the `ModificationRecordManager`, which formats each modification record accordingly.

### Final Considerations

- **Scalability**: Designed to handle large assembly programs efficiently by managing records through dedicated managers and optimizing the assembly process.
    
- **Modularity**: Maintains a clear separation of concerns, with each class handling specific aspects of the assembly process. This enhances maintainability and readability.
    
- **Error Handling**: Ensures that all potential issues during the assembly and writing process are detected and logged appropriately, preventing the creation of malformed object programs.
    
- **Integration with Other Components**: Seamlessly interacts with `TextRecordManager`, `ModificationRecordManager`, `LocationCounter`, and `ErrorLogHandler` to ensure accurate and efficient assembly.
    
- **Testing**: Implement comprehensive unit and integration tests to validate each method's functionality, ensuring correct assembly and writing of object programs.
    

### Comprehensive Testing Strategies

To ensure the `ObjectProgramWriter` functions correctly and integrates seamlessly with other components, implement the following test cases:

#### a. **Valid Assembly and Writing**

- **Test Case**: Assemble and write a complete object program with valid header, text, modification, and end records.
- **Input**:
    - `header_record`: `"H^PROG ^001000^000015"`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `"E^001000"`
- **Expected Outcome**: The object program is correctly assembled and written to the specified output file without errors.

#### b. **Missing Header Record**

- **Test Case**: Attempt to assemble an object program without a header record.
- **Input**:
    - `header_record`: `""`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `"E^001000"`
- **Expected Outcome**: An error is logged indicating that the header record is missing, and the object program is not written to the file.

#### c. **Missing End Record**

- **Test Case**: Attempt to assemble an object program without an end record.
- **Input**:
    - `header_record`: `"H^PROG ^001000^000015"`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `""`
- **Expected Outcome**: An error is logged indicating that the end record is missing, and the object program is not written to the file.

#### d. **Malformed Header Record**

- **Test Case**: Provide a header record that does not start with `H` or has incorrect formatting.
- **Input**:
    - `header_record`: `"X^PROG ^001000^000015"`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `"E^001000"`
- **Expected Outcome**: An error is logged indicating an incorrect header record format, and the object program is not written to the file.

#### e. **Malformed End Record**

- **Test Case**: Provide an end record that does not start with `E` or has incorrect formatting.
- **Input**:
    - `header_record`: `"H^PROG ^001000^000015"`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `"X^001000"`
- **Expected Outcome**: An error is logged indicating an incorrect end record format, and the object program is not written to the file.

#### f. **Malformed Text Record**

- **Test Case**: Include a text record that does not start with `T`.
- **Input**:
    - `header_record`: `"H^PROG ^001000^000015"`
    - `text_records`: `["X^001000^0A^141033281030"]`
    - `modification_records`: `["M^00100A^05"]`
    - `end_record`: `"E^001000"`
- **Expected Outcome**: An error is logged indicating an invalid text record format, and the object program is not written to the file.

#### g. **Malformed Modification Record**

- **Test Case**: Include a modification record that does not start with `M`.
- **Input**:
    - `header_record`: `"H^PROG ^001000^000015"`
    - `text_records`: `["T^001000^0A^141033281030"]`
    - `modification_records`: `["X^00100A^05"]`
    - `end_record`: `"E^001000"`
- **Expected Outcome**: An error is logged indicating an invalid modification record format, and the object program is not written to the file.

#### h. **File Writing Errors**

- **Test Case**: Attempt to write to a read-only file or a location without write permissions.
- **Input**:
    - `file_name`: Points to a read-only file or restricted directory.
    - Valid records as in previous test cases.
- **Expected Outcome**: An I/O error is caught, an error is logged indicating the failure to write, and the assembly process handles the exception gracefully without crashing.

#### i. **Multiple Control Sections** (If applicable)

- **Test Case**: Assemble multiple control sections, each with their own header and end records.
- **Input**:
    - Multiple sets of header, text, modification, and end records corresponding to different control sections.
- **Expected Outcome**: Each control section's records are correctly assembled and written to the output file, maintaining proper separation and formatting.

#### j. **Large Object Programs**

- **Test Case**: Assemble a very large program with numerous text and modification records.
- **Input**:
    - A large list of text and modification records.
- **Expected Outcome**: The object program is correctly assembled without performance degradation, and all records are accurately written to the output file.

### Documentation and Code Comments

Ensure that the `ObjectProgramWriter` class and its methods are well-documented with clear docstrings and inline comments explaining their purpose, parameters, and logic. This practice facilitates maintenance, debugging, and future enhancements.

```python
class ObjectProgramWriter:
    """
    Manages the assembly of all records into the final object program and writes it to an output file.
    
    Responsibilities:
        - Assembles header, text, modification, and end records into the final object program.
        - Formats records according to the specified output format.
        - Writes the assembled object program to a designated output file.
        - Logs any errors encountered during the writing process.
    """
    
    def __init__(self, header_record: str, text_records: List[str], modification_records: List[str], end_record: str, error_handler: ErrorLogHandler):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param error_handler: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record
        self.text_records = text_records
        self.modification_records = modification_records
        self.end_record = end_record
        self.error_handler = error_handler
    
    def assemble_object_program(self) -> str:
        """
        Assembles all records into the final object program string.
        
        :return: The complete object program as a single string.
        """
        object_program = ""
        
        # Append header record
        if self.header_record:
            object_program += f"{self.header_record}\n"
        else:
            self.error_handler.log_error("Header record is missing.")
        
        # Append text records
        for text_record in self.text_records:
            object_program += f"{text_record}\n"
        
        # Append modification records
        for modification_record in self.modification_records:
            object_program += f"{modification_record}\n"
        
        # Append end record
        if self.end_record:
            object_program += f"{self.end_record}\n"
        else:
            self.error_handler.log_error("End record is missing.")
        
        return object_program
    
    def write_to_file(self, file_name: str):
        """
        Writes the assembled object program to the specified output file.
        
        :param file_name: The name/path of the output file.
        """
        object_program = self.assemble_object_program()
        
        try:
            with open(file_name, 'w') as file:
                file.write(object_program)
            self.error_handler.log_action(f"Object program successfully written to {file_name}.")
        except IOError as e:
            self.error_handler.log_error(f"Failed to write object program to {file_name}: {e}")
    
    def validate_records(self) -> bool:
        """
        Validates that all necessary records are present and correctly formatted.
        
        :return: True if all records are valid, False otherwise.
        """
        is_valid = True
        
        # Validate header record
        if not self.header_record:
            self.error_handler.log_error("Header record is missing.")
            is_valid = False
        elif not self.header_record.startswith("H"):
            self.error_handler.log_error("Header record format is incorrect.")
            is_valid = False
        
        # Validate end record
        if not self.end_record:
            self.error_handler.log_error("End record is missing.")
            is_valid = False
        elif not self.end_record.startswith("E"):
            self.error_handler.log_error("End record format is incorrect.")
            is_valid = False
        
        # Validate text records
        for text_record in self.text_records:
            if not text_record.startswith("T"):
                self.error_handler.log_error(f"Invalid text record format: {text_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        # Validate modification records
        for modification_record in self.modification_records:
            if not modification_record.startswith("M"):
                self.error_handler.log_error(f"Invalid modification record format: {modification_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        return is_valid
    
    def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
        """
        Formats the header record according to the specification.
        
        :param program_name: The name of the program.
        :param start_address: The starting memory address of the program.
        :param program_length: The total length of the program.
        :return: The formatted header record string.
        """
        # Ensure program name is exactly 6 characters, padded with spaces if necessary
        program_name_formatted = f"{program_name:<6}"[:6]
        return f"H^{program_name_formatted}^{start_address:06X}^{program_length:06X}"
    
    def format_end_record(self, first_executable_address: int) -> str:
        """
        Formats the end record according to the specification.
        
        :param first_executable_address: The address of the first executable instruction.
        :return: The formatted end record string.
        """
        return f"E^{first_executable_address:06X}"
```

- **Explanation**:
    - **Docstrings**: Each method includes a clear docstring explaining its purpose, parameters, and return values.
    - **Inline Comments**: Comments within methods clarify specific steps and logic.
    - **Error Handling**: Ensures that all essential records are present and correctly formatted before writing to the output file, logging errors as necessary.

### Final Considerations

- **Scalability**: The `ObjectProgramWriter` is designed to handle large object programs efficiently by managing records through dedicated managers and optimizing the assembly process.
    
- **Modularity**: Maintains a clear separation of concerns, with each class handling specific aspects of the assembly process. This enhances maintainability and readability.
    
- **Error Handling**: Ensures that all potential issues during the assembly and writing process are detected and logged appropriately, preventing the creation of malformed object programs.
    
- **Integration with Other Components**: Seamlessly interacts with `TextRecordManager`, `ModificationRecordManager`, `LocationCounter`, and `ErrorLogHandler` to ensure accurate and efficient assembly.
    
- **Testing**: Implement comprehensive unit and integration tests to validate each method's functionality, ensuring correct assembly and writing of object programs.

---

---

## 6. `AssemblerPass2` Class Overview

### 1. **Class Overview**
The `AssemblerPass2` class orchestrates the second pass of the assembly process. It coordinates interactions between various helper classes, manages the flow from parsing the intermediate file to generating object codes, organizing records, and producing the final object program. The class emphasizes robustness, maintainability, and scalability, ensuring accurate assembly even for complex programs.

---

### 2. **Enhanced Responsibilities**

- **Initialize and Load Tables:** Set up and manage symbol tables, literal tables, and other necessary data structures.
- **Read and Parse Intermediate File:** Utilize `IntermediateFileParser` to parse the intermediate file and create structured `SourceCodeLine` objects.
- **Generate Object Code:** Use `ObjectCodeGenerator` to translate assembly instructions into machine code, handling various instruction formats and addressing modes.
- **Manage Records:** Coordinate with `TextRecordManager` and `ModificationRecordManager` to organize object codes, manage text records, and track relocations.
- **Assemble Object Program:** Utilize `ObjectProgramWriter` to compile all records into the final object program, ensuring proper formatting and order.
- **Error Handling and Logging:** Collect, manage, and report errors throughout the assembly process, ensuring that critical errors halt the process gracefully.
- **Support Additional Features:** Optionally manage multiple control sections, handle listing file generation, and support extended assembly directives.

---

### 3. Attributes

To streamline the class and adhere to the Single Responsibility Principle, attributes are categorized based on their roles and dependencies.

#### **Core Attributes:**

- **File Management:**
    
    - `intermediate_file_name`: `str` — Path to the intermediate file.
    - `object_program_file_name`: `str` — Path to the output object program file.
- **Data Structures:**
    
    - `symbol_table`: `SymbolTable` — Stores symbol definitions and addresses.
    - `literal_table`: `LiteralTableList` — Manages literals and their assigned addresses.
- **Handlers and Managers:**
    
    - `error_handler`: `ErrorLogHandler` — Manages error logging and reporting.
    - `file_explorer`: `FileExplorer` — Handles file operations (reading and writing).
    - `opcode_handler`: `OpcodeHandler` — Provides opcode information.
    - `object_code_generator`: `ObjectCodeGenerator` — Generates object codes from source lines.
    - `text_record_manager`: `TextRecordManager` — Manages text records for the object program.
    - `modification_record_manager`: `ModificationRecordManager` — Tracks modifications for relocation.
    - `object_program_writer`: `ObjectProgramWriter` — Assembles and writes the final object program.
- **Program Metadata:**
    
    - `program_name`: `str` — Name of the program being assembled.
    - `program_start_address`: `int` — Starting memory address of the program.
    - `program_length`: `int` — Total length of the program.
    - `first_executable_address`: `int` — Address where execution begins.
- **Control Flags and Prefixes:**
    
    - `allow_error_lines_in_generated_document`: `bool` — Flag to allow or halt on errors.
    - `base_register`: `int` — Current value of the base register for base-relative addressing.

---

### 4. **Detailed Methods and Their Responsibilities**

#### A. Initialization and Setup

1. **`__init__` Method**
    
    ```python
    def __init__(self, intermediate_file_name: str,
                 object_program_file_name: str = "output.obj",
                 file_explorer: FileExplorer = None,
                 error_handler: ErrorLogHandler = None):
        """
        Initializes the AssemblerPass2 with necessary configurations and dependencies.
        
        :param intermediate_file_name: Path to the intermediate file.
        :param object_program_file_name: Path to the output object program file.
        :param file_explorer: Instance of FileExplorer for file operations.
        :param error_handler: Instance of ErrorLogHandler for logging.
        """
        self.intermediate_file_name = intermediate_file_name
        self.object_program_file_name = object_program_file_name
        
        # Initialize handlers and managers
        self.file_explorer = file_explorer or FileExplorer()
        self.error_handler = error_handler or ErrorLogHandler()
        
        # Initialize symbol and literal tables
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        
        # Initialize opcode handler
        self.opcode_handler = OpcodeHandler()
        
        # Initialize object code generator
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler
        )
        
        # Initialize record managers
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        
        # Initialize object program writer
        self.object_program_writer = ObjectProgramWriter(
            header_record="",
            text_records=[],
            modification_records=[],
            end_record="",
            error_handler=self.error_handler
        )
        
        # Initialize program metadata
        self.program_name = ""
        self.program_start_address = 0
        self.program_length = 0
        self.first_executable_address = 0
        
        # Initialize control flags
        self.allow_error_lines_in_generated_document = True
        self.base_register = None  # To handle BASE and NOBASE directives
    ```
    
    - **Purpose:** Sets up the assembler with all necessary dependencies, initializing symbol and literal tables, handlers, and managers. It ensures that all components are ready before the assembly process begins.
    - **Enhancements:**
        - **Dependency Injection:** Allows external injection of `FileExplorer` and `ErrorLogHandler` instances, facilitating testing and flexibility.
        - **Default Parameters:** Provides default values for optional parameters, ensuring ease of use.
        - **Initialization Order:** Ensures that dependent components (e.g., `ObjectCodeGenerator` depends on `SymbolTable`, `LiteralTableList`, etc.) are initialized in the correct order.

#### B. Running the Assembly Process
2. **`run` Method**
    ```python
    def run(self):
        """
        Orchestrates the entire Pass 2 assembly process.
        """
        self.load_intermediate_file()
        self.parse_intermediate_lines()
        self.initialize_generators_and_managers()
        self.process_source_lines()
        self.finalize_records()
        self.assemble_object_program()
        self.write_output_files()
        self.report_errors()
    ```
    - **Purpose:** Acts as the main driver, sequentially invoking methods to perform each step of the assembly process.
    - **Enhancements:**
        - **Sequential Flow:** Ensures a logical and orderly execution of the assembly steps.
        - **Error Checks Between Steps:** Could include checks after each step to decide whether to continue based on critical errors.
#### C. Loading and Parsing Intermediate File
3. **`load_intermediate_file` Method**
    ```python
    def load_intermediate_file(self):
        """
        Loads the intermediate file content into memory.
        """
        try:
            self.int_file_content = self.file_explorer.read_file_raw(self.intermediate_file_name)
            if not self.int_file_content:
                self.error_handler.log_error("Intermediate file is empty.")
                return
            self.error_handler.log_action(f"Read {len(self.int_file_content)} lines from {self.intermediate_file_name}.")
        except FileNotFoundError:
            self.error_handler.log_error(f"Intermediate file '{self.intermediate_file_name}' not found.")
        except IOError as e:
            self.error_handler.log_error(f"Error reading intermediate file '{self.intermediate_file_name}': {e}")
    ```
    - **Purpose:** Reads the intermediate file's content, handling file-related errors gracefully.
    - **Enhancements:**
        - **Exception Handling:** Catches specific exceptions like `FileNotFoundError` and general `IOError` to provide detailed error messages.
        - **Logging:** Logs successful reads and errors appropriately.
4. **`parse_intermediate_lines` Method**
    ```python
    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.
        """
        if not hasattr(self, 'int_file_content') or not self.int_file_content:
            self.error_handler.log_error("No content to parse in intermediate file.")
            return
        
        intermediate_parser = IntermediateFileParser(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            error_handler=self.error_handler,
            intermediate_content=self.int_file_content
        )
        
        self.int_source_code_lines = intermediate_parser.parse()
        self.error_handler.log_action(f"Parsed {len(self.int_source_code_lines)} source lines.")
    ```
    - **Purpose:** Converts raw intermediate file content into structured `SourceCodeLine` objects using `IntermediateFileParser`.
    - **Enhancements:**
        - **Pre-condition Check:** Ensures that there is content to parse before proceeding.
        - **Encapsulation:** Delegates parsing responsibilities to `IntermediateFileParser`, maintaining modularity.
        - **Logging:** Records the number of parsed lines for traceability.

#### **D. Initializing Generators and Managers**
5. **`initialize_generators_and_managers` Method**
    ```python
    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.
        """
        # Re-initialize in case of multiple runs
        self.object_code_generator.reset()
        self.text_record_manager.reset()
        self.modification_record_manager.reset()
        self.object_program_writer.reset()
        
        # Initialize object program writer with empty records
        self.object_program_writer = ObjectProgramWriter(
            header_record="",
            text_records=[],
            modification_records=[],
            end_record="",
            error_handler=self.error_handler
        )
    ```
    - **Purpose:** Prepares the generators and managers for a fresh assembly run, resetting their states to avoid residual data from previous runs.
    - **Enhancements:**
        - **Reset Functionality:** Assumes that helper classes have `reset` methods to clear previous states.
        - **Re-initialization:** Ensures that managers and writers are in a clean state before starting processing.
        - **Modular Reset:** If helper classes lack `reset` methods, consider implementing them for better state management.
#### E. Processing Source Lines
6. **`process_source_lines` Method**
    ```python
    def process_source_lines(self):
        """
        Processes each SourceCodeLine to generate object codes and manage records.
        """
        if not hasattr(self, 'int_source_code_lines') or not self.int_source_code_lines:
            self.error_handler.log_error("No source lines to process.")
            return
        
        for source_line in self.int_source_code_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue  # Skip comments and erroneous lines
            
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue  # Directives are handled separately
            
            # Generate object code for the instruction
            object_code, requires_modification, modification_details = self.object_code_generator.generate_object_code(source_line)
            
            if object_code:
                # Add object code to text records
                self.text_record_manager.add_object_code(source_line.address, object_code)
                
                # If modification is required, add to modification records
                if requires_modification:
                    address, length = modification_details
                    self.modification_record_manager.add_modification(address, length)
            else:
                # Object code generation failed; error already logged
                continue
    ```
    - **Purpose:** Iterates through each parsed source line, generating object codes, managing text and modification records, and handling directives.
    - **Enhancements:**
        - **Enhanced Object Code Generation:** Assumes `generate_object_code` returns a tuple with object code, a boolean flag for modification, and modification details.
        - **Separation of Concerns:** Clearly separates the handling of directives, comments, and instructions.
        - **Error Propagation:** Relies on `ObjectCodeGenerator` to handle and log errors, maintaining clean control flow.
        - **Modification Handling:** Encapsulates modification record details, ensuring flexibility in handling various modification scenarios.
7. **`handle_directive` Method**
    ```python
    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.
        
        :param source_line: The SourceCodeLine object representing the directive.
        """
        directive = source_line.opcode_mnemonic.upper()
        operands = source_line.operands
        
        if directive == "START":
            self.handle_start_directive(source_line)
        elif directive == "END":
            self.handle_end_directive(source_line)
        elif directive == "LTORG":
            self.handle_ltorg_directive()
        elif directive == "EQU":
            self.handle_equ_directive(source_line)
        elif directive == "BASE":
            self.handle_base_directive(operands)
        elif directive == "NOBASE":
            self.handle_nobase_directive()
        else:
            self.error_handler.log_error(f"Unknown directive '{directive}' at line {source_line.line_number}.")
    ```
    - **Purpose:** Delegates the handling of specific directives to dedicated methods, enhancing readability and maintainability.
    - **Enhancements:**
        - **Dedicated Handler Methods:** Each directive has its own method, adhering to the Single Responsibility Principle.
        - **Error Logging:** Logs errors for unknown directives, preventing silent failures.
          
8. **Dedicated Directive Handling Methods**
    - **`handle_start_directive` Method**
        ```python
        def handle_start_directive(self, source_line: SourceCodeLine):
            """
            Handles the START directive to initialize program metadata.
            
            :param source_line: The SourceCodeLine object representing the START directive.
            """
            operand = source_line.operands
            if operand:
                try:
                    self.program_start_address = int(operand, 16)
                    self.program_name = source_line.label.strip()
                    self.location_counter.set_current_address(self.program_start_address)
                    self.error_handler.log_action(f"Program '{self.program_name}' starting at address {self.program_start_address:X}.")
                except ValueError:
                    self.error_handler.log_error(f"Invalid start address '{operand}' at line {source_line.line_number}.")
            else:
                self.error_handler.log_error(f"Missing start address in START directive at line {source_line.line_number}.")
        ```
        
    - **`handle_end_directive` Method**
        ```python
        def handle_end_directive(self, source_line: SourceCodeLine):
            """
            Handles the END directive to finalize the assembly process.
            
            :param source_line: The SourceCodeLine object representing the END directive.
            """
            operand = source_line.operands
            if operand:
                symbol = operand.strip()
                executable_address = self.symbol_table.get_symbol_address(symbol)
                if executable_address is not None:
                    self.first_executable_address = executable_address
                    self.error_handler.log_action(f"Execution begins at address {self.first_executable_address:X}.")
                else:
                    self.error_handler.log_error(f"Undefined symbol '{symbol}' in END directive at line {source_line.line_number}.")
            else:
                # If no operand, default to program start address
                self.first_executable_address = self.program_start_address
                self.error_handler.log_action(f"Execution begins at program start address {self.first_executable_address:X}.")
        ```
        
    - **`handle_ltorg_directive` Method**
        ```python
        def handle_ltorg_directive(self):
            """
            Handles the LTORG directive by assigning addresses to literals and generating their object codes.
            """
            self.literal_table.assign_addresses(self.text_record_manager.get_next_available_address())
            for literal in self.literal_table.get_unassigned_literals():
                self.text_record_manager.add_object_code(literal.address, self.object_code_generator.generate_object_code_for_literal(literal))
                self.error_handler.log_action(f"Assigned address {literal.address:X} to literal '{literal.value}'.")
        ```
        
    - **`handle_equ_directive` Method**
        ```python
        def handle_equ_directive(self, source_line: SourceCodeLine):
            """
            Handles the EQU directive to define symbols with constant values.
            
            :param source_line: The SourceCodeLine object representing the EQU directive.
            """
            symbol = source_line.label.strip()
            expression = source_line.operands.strip()
            value = self.evaluate_expression(expression)
            if value is not None:
                self.symbol_table.define(symbol, value, relocatable=False)
                self.error_handler.log_action(f"Defined symbol '{symbol}' with value {value:X} using EQU directive.")
            else:
                self.error_handler.log_error(f"Invalid expression '{expression}' in EQU directive at line {source_line.line_number}.")
        ```
        
    - **`handle_base_directive` Method**
        ```python
        def handle_base_directive(self, operand: str):
            """
            Handles the BASE directive to set the base register for base-relative addressing.
            
            :param operand: The operand specifying the base symbol or address.
            """
            symbol = operand.strip()
            base_address = self.symbol_table.get_symbol_address(symbol)
            if base_address is not None:
                self.base_register = base_address
                self.object_code_generator.set_base_register(base_address)
                self.error_handler.log_action(f"Base register set to symbol '{symbol}' with address {base_address:X}.")
            else:
                self.error_handler.log_error(f"Undefined symbol '{symbol}' in BASE directive.")
        ```
        
    - **`handle_nobase_directive` Method**
        ```python
        def handle_nobase_directive(self):
            """
            Handles the NOBASE directive to unset the base register.
            """
            self.base_register = None
            self.object_code_generator.unset_base_register()
            self.error_handler.log_action("Base register unset using NOBASE directive.")
        ```
        
    - **Purpose:** Each method encapsulates the logic for handling a specific directive, improving code readability, maintainability, and adherence to the Single Responsibility Principle.
    - **Enhancements:**
        - **Error Handling:** Each method validates operands and handles errors gracefully, ensuring that invalid directives do not disrupt the assembly process.
        - **Program Metadata Management:** Updates program metadata (e.g., start address, executable address) based on directives.
        - **Integration with Other Components:** Coordinates with `SymbolTable`, `ObjectCodeGenerator`, and `TextRecordManager` to manage symbols, generate object codes for literals, and assign addresses.

#### F. Finalizing Records
9. **`finalize_records` Method**
    ```python
    def finalize_records(self):
        """
        Finalizes text and modification records, creates header and end records, and prepares them for assembly.
        """
        # Finalize any pending text records
        self.text_record_manager.finalize_current_record()
        
        # Retrieve text and modification records
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        
        # Create header and end records
        header_record = self.create_header_record()
        end_record = self.create_end_record()
        
        # Assign records to ObjectProgramWriter
        self.object_program_writer.header_record = header_record
        self.object_program_writer.text_records = text_records
        self.object_program_writer.modification_records = modification_records
        self.object_program_writer.end_record = end_record
        
        self.error_handler.log_action("Finalized all records for object program assembly.")
    ```
    - **Purpose:** Ensures that all text and modification records are finalized, creates the necessary header and end records, and assigns them to the `ObjectProgramWriter`.
    - **Enhancements:**
        - **Record Finalization:** Ensures that any pending object codes are correctly grouped into text records.
        - **Integration with `ObjectProgramWriter`:** Directly assigns records to the writer for assembly.
        - **Logging:** Provides confirmation that records have been finalized.
          
10. **`create_header_record` Method**
    ```python
    def create_header_record(self) -> str:
        """
        Constructs the header record based on program metadata.
        
        :return: The formatted header record string.
        """
        program_name_formatted = f"{self.program_name:<6}"[:6]  # Ensure 6 characters
        header_record = f"H^{program_name_formatted}^{self.program_start_address:06X}^{self.program_length:06X}"
        self.error_handler.log_action(f"Created header record: {header_record}")
        return header_record
    ```
    - **Purpose:** Generates a correctly formatted header record using program metadata.
    - **Enhancements:**
        - **Formatting:** Ensures program name is exactly 6 characters, padding with spaces if necessary.
        - **Logging:** Records the creation of the header record for traceability.
          
11. **`create_end_record` Method**
    ```python
    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.
        
        :return: The formatted end record string.
        """
        end_record = f"E^{self.first_executable_address:06X}"
        self.error_handler.log_action(f"Created end record: {end_record}")
        return end_record
    ```
    - **Purpose:** Generates a correctly formatted end record indicating where execution begins.
    - **Enhancements:**
        - **Formatting:** Ensures the address is represented as a 6-digit hexadecimal number.
        - **Logging:** Records the creation of the end record for traceability.

#### G. Assembling and Writing Output

12. **`assemble_object_program` Method**
    ```python
    def assemble_object_program(self):
        """
        Assembles all records into the final object program using ObjectProgramWriter.
        """
        object_program = self.object_program_writer.assemble_object_program()
        self.error_handler.log_action("Assembled the complete object program.")
    ```
    - **Purpose:** Utilizes `ObjectProgramWriter` to compile all records into the final object program string.
    - **Enhancements:**
        - **Logging:** Confirms the successful assembly of the object program.
          
13. **`write_output_files` Method**
    ```python
    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.
        """
        try:
            self.object_program_writer.write_to_file(self.object_program_file_name)
            self.error_handler.log_action(f"Object program successfully written to '{self.object_program_file_name}'.")
        except Exception as e:
            self.error_handler.log_error(f"Failed to write object program to '{self.object_program_file_name}': {e}")
    ```
    - **Purpose:** Outputs the assembled object program to the specified file, handling any I/O errors gracefully.
    - **Enhancements:**
        - **Exception Handling:** Catches all exceptions during file writing to prevent crashes.
        - **Logging:** Logs successful writes and detailed error messages if failures occur.

#### H. Error Reporting
14. **`report_errors` Method**
    ```python
    def report_errors(self):
        """
        Reports all errors collected during the assembly process.
        """
        if self.error_handler.has_errors():
            self.error_handler.display_errors()
            self.error_handler.log_action("Assembly completed with errors.")
            if not self.allow_error_lines_in_generated_document:
                raise AssemblyError("Assembly terminated due to errors.")
        else:
            self.error_handler.log_action("Assembly completed successfully without errors.")
    ```
    - **Purpose:** Summarizes and reports all errors encountered during the assembly process.
    - **Enhancements:**
        - **Conditional Termination:** Raises an exception to halt the assembly if critical errors are present and the flag `allow_error_lines_in_generated_document` is `False`.
        - **Comprehensive Reporting:** Ensures that all errors are displayed to the user for debugging.

#### I. Utility and Helper Methods

15. **`evaluate_expression` Method**
    ```python
    def evaluate_expression(self, expression: str) -> Optional[int]:
        """
        Evaluates arithmetic expressions used in directives like EQU.
        
        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated integer value, or None if evaluation fails.
        """
        try:
            # For simplicity, use Python's eval with restricted globals
            # In practice, implement a safe parser for assembly expressions
            value = eval(expression, {"__builtins__": None}, {})
            if isinstance(value, int):
                return value
            else:
                return None
        except Exception:
            return None
    ```
    - **Purpose:** Safely evaluates arithmetic expressions in directives like `EQU` to assign constant values to symbols.
    - **Enhancements:**
        - **Security Considerations:** Uses restricted `eval` to prevent execution of arbitrary code. However, for production, consider implementing a proper expression parser.
        - **Error Handling:** Returns `None` if evaluation fails, allowing the calling method to handle the error appropriately.
16. **`reset` Method (Optional)**
    
    ```python
    def reset(self):
        """
        Resets the AssemblerPass2 instance to its initial state.
        Useful for multiple assembly runs within the same instance.
        """
        self.symbol_table.reset()
        self.literal_table.reset()
        self.object_code_generator.reset()
        self.text_record_manager.reset()
        self.modification_record_manager.reset()
        self.object_program_writer.reset()
        self.program_name = ""
        self.program_start_address = 0
        self.program_length = 0
        self.first_executable_address = 0
        self.base_register = None
        self.error_handler.reset()
    ```
    
    - **Purpose:** Resets all components and metadata, preparing the assembler for a new assembly run.
    - **Enhancements:**
        - **Comprehensive Reset:** Ensures that no residual data affects subsequent assembly processes.
        - **Helper Methods:** Assumes that each manager and handler class has a `reset` method implemented.

---

### 5. Integration with Supporting Classes
Understanding how `AssemblerPass2` interacts with other classes is essential for a seamless assembly process.
- **`IntermediateFileParser`:**
    - **Role:** Parses raw intermediate file content into structured `SourceCodeLine` objects.
    - **Interaction:** Invoked by `AssemblerPass2.parse_intermediate_lines()` to convert file content into manageable objects.
- **`ObjectCodeGenerator`:**
    - **Role:** Translates `SourceCodeLine` objects into machine-readable object codes, handling different instruction formats and addressing modes.
    - **Interaction:** Called within `AssemblerPass2.process_source_lines()` to generate object codes and determine if modifications are necessary.
- **`TextRecordManager`:**
    
    - **Role:** Groups object codes into text records, ensuring each record adheres to length constraints and manages the current text record state.
    - **Interaction:** Receives object codes from `ObjectCodeGenerator` and organizes them appropriately.
- **`ModificationRecordManager`:**
    
    - **Role:** Tracks relocatable addresses and generates modification records necessary for linking and loading phases.
    - **Interaction:** Receives modification details from `ObjectCodeGenerator` when relocations are required.
- **`ObjectProgramWriter`:**
    
    - **Role:** Assembles all records (header, text, modification, end) into the final object program and writes it to an output file.
    - **Interaction:** Receives finalized records from `AssemblerPass2.finalize_records()` and manages the writing process.
- **`ErrorLogHandler`:**
    
    - **Role:** Collects, manages, and reports errors encountered during the assembly process.
    - **Interaction:** Utilized by `AssemblerPass2` and other components to log and display errors.
- **`FileExplorer`:**
    
    - **Role:** Handles file operations such as reading and writing files.
    - **Interaction:** Used by `AssemblerPass2` to read the intermediate file and by `ObjectProgramWriter` to write the object program.
- **`SymbolTable` and `LiteralTableList`:**
    
    - **Role:** Manage symbols and literals, respectively, storing their definitions and assigned addresses.
    - **Interaction:** Accessed and updated by various components, including `IntermediateFileParser`, `ObjectCodeGenerator`, and directive handlers within `AssemblerPass2`.

---

### 6. **Comprehensive Pseudocode Example**

Below is an enhanced pseudocode representation of the `AssemblerPass2` class, incorporating all the discussed improvements and ensuring a robust, maintainable, and efficient assembly process.

```python
class AssemblerPass2:
    """
    Orchestrates the second pass of the assembly process, handling object code generation,
    record management, and final object program assembly.
    """

    def __init__(self, intermediate_file_name: str,
                 object_program_file_name: str = "output.obj",
                 file_explorer: FileExplorer = None,
                 error_handler: ErrorLogHandler = None):
        """
        Initializes the AssemblerPass2 with necessary configurations and dependencies.
        
        :param intermediate_file_name: Path to the intermediate file.
        :param object_program_file_name: Path to the output object program file.
        :param file_explorer: Instance of FileExplorer for file operations.
        :param error_handler: Instance of ErrorLogHandler for logging.
        """
        self.intermediate_file_name = intermediate_file_name
        self.object_program_file_name = object_program_file_name
        
        # Initialize handlers and managers
        self.file_explorer = file_explorer or FileExplorer()
        self.error_handler = error_handler or ErrorLogHandler()
        
        # Initialize symbol and literal tables
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTableList()
        
        # Initialize opcode handler
        self.opcode_handler = OpcodeHandler()
        
        # Initialize object code generator
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            error_handler=self.error_handler
        )
        
        # Initialize record managers
        self.text_record_manager = TextRecordManager()
        self.modification_record_manager = ModificationRecordManager()
        
        # Initialize object program writer
        self.object_program_writer = ObjectProgramWriter(
            header_record="",
            text_records=[],
            modification_records=[],
            end_record="",
            error_handler=self.error_handler
        )
        
        # Initialize program metadata
        self.program_name = ""
        self.program_start_address = 0
        self.program_length = 0
        self.first_executable_address = 0
        
        # Initialize control flags
        self.allow_error_lines_in_generated_document = True
        self.base_register = None  # To handle BASE and NOBASE directives

    def run(self):
        """
        Orchestrates the entire Pass 2 assembly process.
        """
        self.load_intermediate_file()
        self.parse_intermediate_lines()
        self.initialize_generators_and_managers()
        self.process_source_lines()
        self.finalize_records()
        self.assemble_object_program()
        self.write_output_files()
        self.report_errors()

    def load_intermediate_file(self):
        """
        Loads the intermediate file content into memory.
        """
        try:
            self.int_file_content = self.file_explorer.read_file_raw(self.intermediate_file_name)
            if not self.int_file_content:
                self.error_handler.log_error("Intermediate file is empty.")
                return
            self.error_handler.log_action(f"Read {len(self.int_file_content)} lines from '{self.intermediate_file_name}'.")
        except FileNotFoundError:
            self.error_handler.log_error(f"Intermediate file '{self.intermediate_file_name}' not found.")
        except IOError as e:
            self.error_handler.log_error(f"Error reading intermediate file '{self.intermediate_file_name}': {e}")

    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.
        """
        if not hasattr(self, 'int_file_content') or not self.int_file_content:
            self.error_handler.log_error("No content to parse in intermediate file.")
            return
        
        intermediate_parser = IntermediateFileParser(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            error_handler=self.error_handler,
            intermediate_content=self.int_file_content
        )
        
        self.int_source_code_lines = intermediate_parser.parse()
        self.error_handler.log_action(f"Parsed {len(self.int_source_code_lines)} source lines.")

    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.
        """
        # Re-initialize in case of multiple runs
        self.object_code_generator.reset()
        self.text_record_manager.reset()
        self.modification_record_manager.reset()
        self.object_program_writer.reset()
        
        # Re-initialize object program writer with empty records
        self.object_program_writer = ObjectProgramWriter(
            header_record="",
            text_records=[],
            modification_records=[],
            end_record="",
            error_handler=self.error_handler
        )
        self.error_handler.log_action("Initialized object code generators and record managers.")

    def process_source_lines(self):
        """
        Iterates through each source line to generate object codes and manage records.
        """
        if not hasattr(self, 'int_source_code_lines') or not self.int_source_code_lines:
            self.error_handler.log_error("No source lines to process.")
            return
        
        for source_line in self.int_source_code_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue  # Skip comments and erroneous lines
            
            if source_line.is_directive():
                self.handle_directive(source_line)
                continue  # Directives are handled separately
            
            # Generate object code for the instruction
            object_code, requires_modification, modification_details = self.object_code_generator.generate_object_code(source_line)
            
            if object_code:
                # Add object code to text records
                self.text_record_manager.add_object_code(source_line.address, object_code)
                self.error_handler.log_action(f"Added object code '{object_code}' at address {source_line.address:X}.")
                
                # If modification is required, add to modification records
                if requires_modification:
                    address, length = modification_details
                    self.modification_record_manager.add_modification(address, length)
                    self.error_handler.log_action(f"Added modification record for address {address:X} with length {length}.")
            else:
                # Object code generation failed; error already logged
                continue

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.
        
        :param source_line: The SourceCodeLine object representing the directive.
        """
        directive = source_line.opcode_mnemonic.upper()
        operands = source_line.operands
        
        if directive == "START":
            self.handle_start_directive(source_line)
        elif directive == "END":
            self.handle_end_directive(source_line)
        elif directive == "LTORG":
            self.handle_ltorg_directive()
        elif directive == "EQU":
            self.handle_equ_directive(source_line)
        elif directive == "BASE":
            self.handle_base_directive(operands)
        elif directive == "NOBASE":
            self.handle_nobase_directive()
        else:
            self.error_handler.log_error(f"Unknown directive '{directive}' at line {source_line.line_number}.")

    def handle_start_directive(self, source_line: SourceCodeLine):
        """
        Handles the START directive to initialize program metadata.
        
        :param source_line: The SourceCodeLine object representing the START directive.
        """
        operand = source_line.operands
        if operand:
            try:
                self.program_start_address = int(operand, 16)
                self.program_name = source_line.label.strip()
                self.text_record_manager.set_current_address(self.program_start_address)
                self.location_counter.set_current_address(self.program_start_address)
                self.error_handler.log_action(f"Program '{self.program_name}' starting at address {self.program_start_address:X}.")
            except ValueError:
                self.error_handler.log_error(f"Invalid start address '{operand}' in START directive at line {source_line.line_number}.")
        else:
            self.error_handler.log_error(f"Missing start address in START directive at line {source_line.line_number}.")

    def handle_end_directive(self, source_line: SourceCodeLine):
        """
        Handles the END directive to finalize the assembly process.
        
        :param source_line: The SourceCodeLine object representing the END directive.
        """
        operand = source_line.operands
        if operand:
            symbol = operand.strip()
            executable_address = self.symbol_table.get_symbol_address(symbol)
            if executable_address is not None:
                self.first_executable_address = executable_address
                self.error_handler.log_action(f"Execution begins at address {self.first_executable_address:X}.")
            else:
                self.error_handler.log_error(f"Undefined symbol '{symbol}' in END directive at line {source_line.line_number}.")
        else:
            # If no operand, default to program start address
            self.first_executable_address = self.program_start_address
            self.error_handler.log_action(f"Execution begins at program start address {self.first_executable_address:X}.")

    def handle_ltorg_directive(self):
        """
        Handles the LTORG directive by assigning addresses to literals and generating their object codes.
        """
        self.literal_table.assign_addresses(self.text_record_manager.get_next_available_address())
        for literal in self.literal_table.get_unassigned_literals():
            object_code = self.object_code_generator.generate_object_code_for_literal(literal)
            if object_code:
                self.text_record_manager.add_object_code(literal.address, object_code)
                self.error_handler.log_action(f"Assigned address {literal.address:X} to literal '{literal.value}' with object code '{object_code}'.")
            else:
                self.error_handler.log_error(f"Failed to generate object code for literal '{literal.value}'.")

    def handle_equ_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive to define symbols with constant values.
        
        :param source_line: The SourceCodeLine object representing the EQU directive.
        """
        symbol = source_line.label.strip()
        expression = source_line.operands.strip()
        value = self.evaluate_expression(expression)
        if value is not None:
            self.symbol_table.define(symbol, value, relocatable=False)
            self.error_handler.log_action(f"Defined symbol '{symbol}' with value {value:X} using EQU directive.")
        else:
            self.error_handler.log_error(f"Invalid expression '{expression}' in EQU directive at line {source_line.line_number}.")

    def handle_base_directive(self, operand: str):
        """
        Handles the BASE directive to set the base register for base-relative addressing.
        
        :param operand: The operand specifying the base symbol or address.
        """
        symbol = operand.strip()
        base_address = self.symbol_table.get_symbol_address(symbol)
        if base_address is not None:
            self.base_register = base_address
            self.object_code_generator.set_base_register(base_address)
            self.error_handler.log_action(f"Base register set to symbol '{symbol}' with address {base_address:X}.")
        else:
            self.error_handler.log_error(f"Undefined symbol '{symbol}' in BASE directive.")

    def handle_nobase_directive(self):
        """
        Handles the NOBASE directive to unset the base register.
        """
        self.base_register = None
        self.object_code_generator.unset_base_register()
        self.error_handler.log_action("Base register unset using NOBASE directive.")

    def finalize_records(self):
        """
        Finalizes text and modification records, creates header and end records, and prepares them for assembly.
        """
        # Finalize any pending text records
        self.text_record_manager.finalize_current_record()
        
        # Retrieve text and modification records
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        
        # Create header and end records
        header_record = self.create_header_record()
        end_record = self.create_end_record()
        
        # Assign records to ObjectProgramWriter
        self.object_program_writer.header_record = header_record
        self.object_program_writer.text_records = text_records
        self.object_program_writer.modification_records = modification_records
        self.object_program_writer.end_record = end_record
        
        self.error_handler.log_action("Finalized all records for object program assembly.")

    def create_header_record(self) -> str:
        """
        Constructs the header record based on program metadata.
        
        :return: The formatted header record string.
        """
        program_name_formatted = f"{self.program_name:<6}"[:6]  # Ensure 6 characters
        header_record = f"H^{program_name_formatted}^{self.program_start_address:06X}^{self.program_length:06X}"
        self.error_handler.log_action(f"Created header record: {header_record}")
        return header_record

    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.
        
        :return: The formatted end record string.
        """
        end_record = f"E^{self.first_executable_address:06X}"
        self.error_handler.log_action(f"Created end record: {end_record}")
        return end_record

    def assemble_object_program(self):
        """
        Assembles all records into the final object program using ObjectProgramWriter.
        """
        object_program = self.object_program_writer.assemble_object_program()
        self.error_handler.log_action("Assembled the complete object program.")

    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.
        """
        try:
            self.object_program_writer.write_to_file(self.object_program_file_name)
            self.error_handler.log_action(f"Object program successfully written to '{self.object_program_file_name}'.")
        except Exception as e:
            self.error_handler.log_error(f"Failed to write object program to '{self.object_program_file_name}': {e}")

    def report_errors(self):
        """
        Reports all errors collected during the assembly process.
        """
        if self.error_handler.has_errors():
            self.error_handler.display_errors()
            self.error_handler.log_action("Assembly completed with errors.")
            if not self.allow_error_lines_in_generated_document:
                raise AssemblyError("Assembly terminated due to errors.")
        else:
            self.error_handler.log_action("Assembly completed successfully without errors.")

    def evaluate_expression(self, expression: str) -> Optional[int]:
        """
        Safely evaluates arithmetic expressions used in directives like EQU.
        
        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated integer value, or None if evaluation fails.
        """
        try:
            # Implement a safe parser or use a restricted eval
            # For the purpose of this example, we'll use a safe eval approach
            allowed_chars = "0123456789ABCDEFabcdef+-*/() "
            if any(char not in allowed_chars for char in expression):
                self.error_handler.log_error(f"Invalid characters in expression '{expression}'.")
                return None
            value = eval(expression, {"__builtins__": None}, {})
            if isinstance(value, int):
                return value
            else:
                self.error_handler.log_error(f"Expression '{expression}' did not evaluate to an integer.")
                return None
        except Exception as e:
            self.error_handler.log_error(f"Failed to evaluate expression '{expression}': {e}")
            return None

    def reset(self):
        """
        Resets the AssemblerPass2 instance to its initial state.
        Useful for multiple assembly runs within the same instance.
        """
        self.symbol_table.reset()
        self.literal_table.reset()
        self.object_code_generator.reset()
        self.text_record_manager.reset()
        self.modification_record_manager.reset()
        self.object_program_writer.reset()
        self.program_name = ""
        self.program_start_address = 0
        self.program_length = 0
        self.first_executable_address = 0
        self.base_register = None
        self.error_handler.reset()
        self.error_handler.log_action("AssemblerPass2 instance has been reset.")
```

---

### 7. **Key Enhancements and Design Improvements**

#### **A. Enhanced Error Handling**

- **Comprehensive Logging:** All methods include logging actions and errors, ensuring that every significant step and issue is recorded.
- **Graceful Termination:** The `report_errors` method can halt the assembly process by raising an `AssemblyError` if critical errors are present and the flag `allow_error_lines_in_generated_document` is set to `False`.
- **Detailed Error Messages:** Error logs include contextual information like line numbers and specific issues, facilitating easier debugging.

#### B. Modular Directive Handling
- **Dedicated Methods for Each Directive:** Each assembly directive has its own handling method, improving readability and maintainability.
- **Validation and Error Checks:** Each directive handler validates operands and handles errors, ensuring that directives are processed correctly.

#### C. Safe Expression Evaluation
- **Security Considerations:** The `evaluate_expression` method restricts allowed characters and prevents execution of arbitrary code by controlling the evaluation environment.
- **Fallback Mechanism:** Returns `None` and logs errors if evaluation fails, allowing the calling method to handle the issue appropriately.

#### **D. Record Finalization and Assembly**

- **Finalization Steps:** Ensures that all text and modification records are correctly finalized before assembling the object program.
- **Header and End Record Creation:** Creates header and end records based on program metadata, ensuring proper formatting and inclusion in the final object program.

#### **E. Reset Functionality**

- **State Management:** The `reset` method allows the assembler to be reused for multiple assembly runs without residual data affecting subsequent operations.
- **Comprehensive Reset:** Clears all tables, managers, writers, and metadata, preparing the assembler for a fresh run.

#### **F. Integration with Supporting Classes**

- **Seamless Interactions:** The assembler coordinates effectively with classes like `IntermediateFileParser`, `ObjectCodeGenerator`, `TextRecordManager`, `ModificationRecordManager`, and `ObjectProgramWriter`.
- **Dependency Management:** Ensures that all dependencies are initialized and reset appropriately, maintaining consistency and preventing data leakage between runs.

#### **G. Scalability and Extensibility**

- **Multiple Control Sections:** The design can be extended to support multiple control sections by managing separate symbol and literal tables or adjusting the `ObjectProgramWriter` accordingly.
- **Listing File Generation:** While optional, the assembler can integrate a `ListingFileWriter` to produce listing files that aid in debugging and verification.
- **Handling Large Programs:** Efficient record management and object code generation ensure that the assembler can handle large assembly programs without performance degradation.

---

### 9. Documentation and Code Comments
Ensure that the `AssemblerPass2` class and all its methods are thoroughly documented with clear docstrings and inline comments. This practice enhances understandability, facilitates maintenance, and aids future developers in comprehending the assembly process.
```python
class AssemblerPass2:
    """
    Orchestrates the second pass of the assembly process, handling object code generation,
    record management, and final object program assembly.

    Responsibilities:
        - Initialize and manage symbol and literal tables.
        - Load and parse the intermediate file into structured source lines.
        - Generate object codes from source lines.
        - Manage text and modification records.
        - Assemble the final object program.
        - Handle and report errors throughout the process.
    """

    def __init__(self, intermediate_file_name: str,
                 object_program_file_name: str = "output.obj",
                 file_explorer: FileExplorer = None,
                 error_handler: ErrorLogHandler = None):
        """
        Initializes the AssemblerPass2 with necessary configurations and dependencies.

        :param intermediate_file_name: Path to the intermediate file.
        :param object_program_file_name: Path to the output object program file.
        :param file_explorer: Instance of FileExplorer for file operations.
        :param error_handler: Instance of ErrorLogHandler for logging.
        """
        # [Initialization code as shown above]

    def run(self):
        """
        Orchestrates the entire Pass 2 assembly process by sequentially executing all necessary steps.
        """
        self.load_intermediate_file()
        self.parse_intermediate_lines()
        self.initialize_generators_and_managers()
        self.process_source_lines()
        self.finalize_records()
        self.assemble_object_program()
        self.write_output_files()
        self.report_errors()

    def load_intermediate_file(self):
        """
        Loads the intermediate file content into memory.

        Reads the intermediate file using FileExplorer and stores the content.
        Logs the number of lines read or any errors encountered during reading.
        """
        # [Method implementation as shown above]

    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.

        Utilizes IntermediateFileParser to convert raw lines into SourceCodeLine objects.
        Logs the number of parsed lines or any errors encountered during parsing.
        """
        # [Method implementation as shown above]

    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.

        Resets any existing states and prepares the object code generator and record managers for a new assembly run.
        """
        # [Method implementation as shown above]

    def process_source_lines(self):
        """
        Iterates through each SourceCodeLine to generate object codes and manage records.

        For each instruction:
            - Skips comments and erroneous lines.
            - Handles directives appropriately.
            - Generates object code using ObjectCodeGenerator.
            - Adds object code to TextRecordManager.
            - Records modifications if necessary using ModificationRecordManager.
            - Logs actions and errors.
        """
        # [Method implementation as shown above]

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.

        Delegates handling to specific methods based on the directive type.

        :param source_line: The SourceCodeLine object representing the directive.
        """
        # [Method implementation as shown above]

    def handle_start_directive(self, source_line: SourceCodeLine):
        """
        Handles the START directive to initialize program metadata.

        Sets the program start address and name based on the directive's operands and label.

        :param source_line: The SourceCodeLine object representing the START directive.
        """
        # [Method implementation as shown above]

    def handle_end_directive(self, source_line: SourceCodeLine):
        """
        Handles the END directive to finalize the assembly process.

        Sets the first executable address based on the directive's operand or defaults to the program start address.

        :param source_line: The SourceCodeLine object representing the END directive.
        """
        # [Method implementation as shown above]

    def handle_ltorg_directive(self):
        """
        Handles the LTORG directive by assigning addresses to literals and generating their object codes.

        Iterates through unassigned literals, assigns addresses, generates object codes, and logs actions.
        """
        # [Method implementation as shown above]

    def handle_equ_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive to define symbols with constant values.

        Evaluates the expression in the directive and updates the symbol table accordingly.

        :param source_line: The SourceCodeLine object representing the EQU directive.
        """
        # [Method implementation as shown above]

    def handle_base_directive(self, operand: str):
        """
        Handles the BASE directive to set the base register for base-relative addressing.

        Updates the base register value in ObjectCodeGenerator and logs the action.

        :param operand: The operand specifying the base symbol or address.
        """
        # [Method implementation as shown above]

    def handle_nobase_directive(self):
        """
        Handles the NOBASE directive to unset the base register.

        Clears the base register value in ObjectCodeGenerator and logs the action.
        """
        # [Method implementation as shown above]

    def finalize_records(self):
        """
        Finalizes text and modification records, creates header and end records, and prepares them for assembly.

        Finalizes current text records, retrieves all text and modification records, creates header and end records,
        assigns them to ObjectProgramWriter, and logs the finalization.
        """
        # [Method implementation as shown above]

    def create_header_record(self) -> str:
        """
        Constructs the header record based on program metadata.

        Ensures proper formatting and logs the creation of the header record.

        :return: The formatted header record string.
        """
        # [Method implementation as shown above]

    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.

        Ensures proper formatting and logs the creation of the end record.

        :return: The formatted end record string.
        """
        # [Method implementation as shown above]

    def assemble_object_program(self):
        """
        Assembles all records into the final object program using ObjectProgramWriter.

        Logs the successful assembly of the object program.
        """
        # [Method implementation as shown above]

    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.

        Handles any exceptions during file writing and logs the outcome.
        """
        # [Method implementation as shown above]

    def report_errors(self):
        """
        Reports all errors collected during the assembly process.

        Displays errors if any exist and logs the final assembly status.
        Optionally raises an exception to halt the assembly process if critical errors are present.
        """
        # [Method implementation as shown above]

    def evaluate_expression(self, expression: str) -> Optional[int]:
        """
        Safely evaluates arithmetic expressions used in directives like EQU.

        Restricts allowed characters and prevents execution of arbitrary code.

        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated integer value, or None if evaluation fails.
        """
        # [Method implementation as shown above]

    def reset(self):
        """
        Resets the AssemblerPass2 instance to its initial state.

        Clears all tables, managers, writers, and metadata, preparing for a new assembly run.
        """
        # [Method implementation as shown above]
```

- **Docstrings and Inline Comments:** Each method includes detailed docstrings explaining its purpose, parameters, and behavior. Inline comments clarify specific logic and steps within methods.
- **Error Logging and Actions:** All significant actions and errors are logged, providing a comprehensive trail for debugging and verification.
---
### 10. **Additional Design Enhancements**
#### A. Handling Base and PC Relative Addressing
- **Base Register Management:**
    - **Set and Unset:** Implement methods within `ObjectCodeGenerator` to set and unset the base register based on `BASE` and `NOBASE` directives.
    - **Usage in Address Calculation:** Ensure that displacement calculations consider whether base-relative or PC-relative addressing is in effect.
- **Displacement Calculation:**
    - **Accuracy:** Validate that displacement values fall within the allowable range for each addressing mode.
    - **Fallback Mechanism:** If PC-relative displacement is out of range, attempt base-relative displacement, and log errors if both fail.

#### B. Managing Extended Instructions (Format 4)
- **Modification Records:**
    - **Generation:** For format 4 instructions, automatically create modification records to handle relocations.
    - **Tracking:** Ensure that the address and length specified in modification records accurately reflect the parts of the object code that require relocation.
- **End Record Address:**
    - **Execution Start Point:** The end record should reference the starting address of the first executable instruction, which could be a format 4 instruction.
#### C. Supporting Multiple Control Sections
- **External Definitions and References:**
    - **Management:** Handle `EXTDEF` and `EXTREF` directives to manage symbols across multiple control sections.
    - **Record Management:** Ensure that symbols defined in external control sections are correctly tracked and referenced in modification records.
- **Linking Considerations:**
    - **Scope Management:** Maintain symbol and literal tables with scope awareness to prevent symbol conflicts across control sections.
    - **Separate Record Sets:** Manage separate sets of text and modification records for each control section, ensuring correct assembly and linking.
#### D. Listing File Generation (Optional)
- **Purpose:** Generate a listing file that combines source lines with their corresponding object codes and addresses, aiding in debugging and verification.
- **Implementation:**
    - **ListingFileWriter Class:** Implement a dedicated class to handle the creation and formatting of listing files.
    - **Integration:** Have `AssemblerPass2` coordinate with `ListingFileWriter` to append listing information during the assembly process.
#### E. Enhancing the Location Counter
- **Address Management:**
    - **Accuracy:** Ensure that the `LocationCounter` accurately tracks the current address, considering instruction lengths and directives that affect address allocation.
    - **Integration:** Seamlessly integrate `LocationCounter` with other components like `ObjectCodeGenerator` and `TextRecordManager` to synchronize address tracking.
- **Program Length Calculation:**
    - **Dynamic Updates:** Continuously update the program length as instructions and data declarations are processed.
    - **Final Calculation:** Calculate the total program length during the finalization phase based on the highest address used.

---

### 11. **Comprehensive Testing Plan**
To ensure the updated `AssemblerPass2` class functions correctly and integrates seamlessly with other components, implement the following comprehensive testing strategies:
#### A. Unit Tests
- **Initialization Tests:**
    - **Objective:** Verify that the assembler initializes all attributes and dependencies correctly.
    - **Test Cases:**
        - Initialization with default parameters.
        - Initialization with custom `FileExplorer` and `ErrorLogHandler` instances.
- **Directive Handling Tests:**
    - **Objective:** Ensure that each directive (`START`, `END`, `LTORG`, `EQU`, `BASE`, `NOBASE`) is handled correctly.
    - **Test Cases:**
        - Valid and invalid operands for each directive.
        - Handling of unknown directives.
- **Object Code Generation Tests:**
    - **Objective:** Validate that object codes are correctly generated for various instruction formats and addressing modes.
    - **Test Cases:**
        - Format 1, 2, 3, and 4 instructions with different addressing modes (immediate, indirect, indexed).
        - Instructions requiring base-relative and PC-relative addressing.
- **Record Management Tests:**
    - **Objective:** Verify that text and modification records are correctly managed, finalized, and retrieved.
    - **Test Cases:**
        - Adding object codes and ensuring correct grouping into text records.
        - Adding modification records and verifying their correctness.
- **Error Handling Tests:**
    - **Objective:** Ensure that errors are correctly logged and handled.
    - **Test Cases:**
        - Undefined symbols or literals.
        - Invalid directives or operands.
        - Displacement out of range.
- **Expression Evaluation Tests:**
    - **Objective:** Confirm that arithmetic expressions in directives like `EQU` are safely and correctly evaluated.
    - **Test Cases:**
        - Valid arithmetic expressions.
        - Expressions with invalid characters or syntax.
#### B. Integration Tests
- **End-to-End Assembly:**
    - **Objective:** Test the entire assembly process from loading the intermediate file to writing the final object program.
    - **Test Cases:**
        - Simple assembly programs with a few instructions.
        - Complex programs with multiple directives, symbols, and literals.
- **Multiple Control Sections:**
    - **Objective:** Validate the assembler's ability to handle multiple control sections, ensuring correct symbol management and record handling.
    - **Test Cases:**
        - Programs with multiple `CSECT` directives.
        - External symbol definitions and references across control sections.
- **Error Propagation:**
    - **Objective:** Ensure that errors in one component (e.g., undefined symbols) correctly propagate and affect the assembly process as intended.
    - **Test Cases:**
        - Programs with deliberate errors to test error handling and termination.
#### C. Edge Case Tests
- **Maximum Displacement:**
    - **Objective:** Test instructions with displacement values at the upper and lower bounds of allowed ranges.
    - **Test Cases:**
        - Displacements of +2047 and -2048 for format 3 instructions.
        - Displacements requiring base-relative addressing when PC-relative is insufficient.
- **Undefined Symbols and Literals:**
    - **Objective:** Confirm that references to undefined symbols or literals are handled gracefully with appropriate error logging.
    - **Test Cases:**
        - Instructions referencing symbols not present in the symbol table.
        - Literals used before definition.
- **Empty and Malformed Intermediate Files:**
    - **Objective:** Verify assembler behavior when dealing with empty or incorrectly formatted intermediate files.
    - **Test Cases:**
        - Completely empty intermediate files.
        - Intermediate files with malformed lines or unexpected content.
#### D. Performance Tests
- **Large Programs:**
    - **Objective:** Assess the assembler's performance and correctness with large assembly programs containing numerous instructions and records.
    - **Test Cases:**
        - Programs with thousands of instructions.
        - High number of literals and symbols.
- **Memory Management:**
    - **Objective:** Ensure that the assembler manages memory efficiently, avoiding leaks or excessive usage.
    - **Test Cases:**
        - Repeated assembly runs to test the `reset` functionality.
        - Programs with extensive use of data declarations.

#### E. Security Tests
- **Expression Evaluation Security:**
    - **Objective:** Ensure that the expression evaluation method does not allow execution of arbitrary or malicious code.
    - **Test Cases:**
        - Expressions containing restricted characters or attempts to execute functions.
- **Input Validation:**
    - **Objective:** Verify that all inputs from the intermediate file are correctly validated to prevent injection attacks or unexpected behavior.
    - **Test Cases:**
        - Instructions with maliciously crafted operands.
        - Directives with unexpected formats.

---

### 12. **Documentation and Code Comments**

Comprehensive documentation is essential for maintainability and ease of understanding. Ensure that all classes and methods within the assembler are well-documented with clear docstrings and inline comments.

**Example:**

```python
class AssemblerPass2:
    """
    Orchestrates the second pass of the assembly process, handling object code generation,
    record management, and final object program assembly.

    Responsibilities:
        - Initialize and manage symbol and literal tables.
        - Load and parse the intermediate file into structured source lines.
        - Generate object codes from source lines.
        - Manage text and modification records.
        - Assemble the final object program.
        - Handle and report errors throughout the process.
    """

    def __init__(self, intermediate_file_name: str,
                 object_program_file_name: str = "output.obj",
                 file_explorer: FileExplorer = None,
                 error_handler: ErrorLogHandler = None):
        """
        Initializes the AssemblerPass2 with necessary configurations and dependencies.
        
        :param intermediate_file_name: Path to the intermediate file.
        :param object_program_file_name: Path to the output object program file.
        :param file_explorer: Instance of FileExplorer for file operations.
        :param error_handler: Instance of ErrorLogHandler for logging.
        """
        # [Initialization code as shown above]

    def run(self):
        """
        Orchestrates the entire Pass 2 assembly process by sequentially executing all necessary steps.
        """
        # [Method implementation as shown above]

    def load_intermediate_file(self):
        """
        Loads the intermediate file content into memory.

        Reads the intermediate file using FileExplorer and stores the content.
        Logs the number of lines read or any errors encountered during reading.
        """
        # [Method implementation as shown above]

    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.

        Utilizes IntermediateFileParser to convert raw lines into SourceCodeLine objects.
        Logs the number of parsed lines or any errors encountered during parsing.
        """
        # [Method implementation as shown above]

    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.

        Resets any existing states and prepares the object code generator and record managers for a new assembly run.
        """
        # [Method implementation as shown above]

    def process_source_lines(self):
        """
        Iterates through each SourceCodeLine to generate object codes and manage records.

        For each instruction:
            - Skips comments and erroneous lines.
            - Handles directives appropriately.
            - Generates object code using ObjectCodeGenerator.
            - Adds object code to TextRecordManager.
            - Records modifications if necessary using ModificationRecordManager.
            - Logs actions and errors.
        """
        # [Method implementation as shown above]

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.

        Delegates handling to specific methods based on the directive type.

        :param source_line: The SourceCodeLine object representing the directive.
        """
        # [Method implementation as shown above]

    def handle_start_directive(self, source_line: SourceCodeLine):
        """
        Handles the START directive to initialize program metadata.

        Sets the program start address and name based on the directive's operands and label.

        :param source_line: The SourceCodeLine object representing the START directive.
        """
        # [Method implementation as shown above]

    def handle_end_directive(self, source_line: SourceCodeLine):
        """
        Handles the END directive to finalize the assembly process.

        Sets the first executable address based on the directive's operand or defaults to the program start address.

        :param source_line: The SourceCodeLine object representing the END directive.
        """
        # [Method implementation as shown above]

    def handle_ltorg_directive(self):
        """
        Handles the LTORG directive by assigning addresses to literals and generating their object codes.

        Iterates through unassigned literals, assigns addresses, generates object codes, and logs actions.
        """
        # [Method implementation as shown above]

    def handle_equ_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive to define symbols with constant values.

        Evaluates the expression in the directive and updates the symbol table accordingly.

        :param source_line: The SourceCodeLine object representing the EQU directive.
        """
        # [Method implementation as shown above]

    def handle_base_directive(self, operand: str):
        """
        Handles the BASE directive to set the base register for base-relative addressing.

        Updates the base register value in ObjectCodeGenerator and logs the action.

        :param operand: The operand specifying the base symbol or address.
        """
        # [Method implementation as shown above]

    def handle_nobase_directive(self):
        """
        Handles the NOBASE directive to unset the base register.

        Clears the base register value in ObjectCodeGenerator and logs the action.
        """
        # [Method implementation as shown above]

    def finalize_records(self):
        """
        Finalizes text and modification records, creates header and end records, and prepares them for assembly.

        Finalizes current text records, retrieves all text and modification records, creates header and end records,
        assigns them to ObjectProgramWriter, and logs the finalization.
        """
        # [Method implementation as shown above]

    def create_header_record(self) -> str:
        """
        Constructs the header record based on program metadata.

        Ensures proper formatting and logs the creation of the header record.

        :return: The formatted header record string.
        """
        # [Method implementation as shown above]

    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.

        Ensures proper formatting and logs the creation of the end record.

        :return: The formatted end record string.
        """
        # [Method implementation as shown above]

    def assemble_object_program(self):
        """
        Assembles all records into the final object program using ObjectProgramWriter.

        Logs the successful assembly of the object program.
        """
        # [Method implementation as shown above]

    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.

        Handles any exceptions during file writing and logs the outcome.
        """
        # [Method implementation as shown above]

    def report_errors(self):
        """
        Reports all errors collected during the assembly process.

        Displays errors if any exist and logs the final assembly status.
        Optionally raises an exception to halt the assembly process if critical errors are present.
        """
        # [Method implementation as shown above]

    def evaluate_expression(self, expression: str) -> Optional[int]:
        """
        Safely evaluates arithmetic expressions used in directives like EQU.

        Restricts allowed characters and prevents execution of arbitrary code.

        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated integer value, or None if evaluation fails.
        """
        # [Method implementation as shown above]

    def reset(self):
        """
        Resets the AssemblerPass2 instance to its initial state.

        Clears all tables, managers, writers, and metadata, preparing for a new assembly run.
        """
        # [Method implementation as shown above]
```

- **Docstrings:** Provide clear explanations of each class and method, detailing their purpose, parameters, and behaviors.
- **Inline Comments:** Explain complex logic and steps within methods, enhancing readability and comprehension.
- **Logging:** Consistently log significant actions and errors, ensuring traceability and ease of debugging.

---


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