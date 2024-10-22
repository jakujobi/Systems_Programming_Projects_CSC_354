# Modules

### **Overview of the Project**
The purpose of this project is to create an assembler-like system that parses, evaluates, and processes **symbols**, **literals**, and **expressions** for a simplified assembly language (SIC/XE assembler). The main components are the **Symbol Table**, **Literal Table**, **Expression Evaluator**, and several supporting utility functions/classes.

This assembler will:
1. **Process Symbols** to manage their addresses, values, and relocation.
2. **Handle Literals** to store and manage unique literals.
3. **Evaluate Expressions** involving symbols and literals.
4. **Interact with Files** to read input, display results, and manage errors.

The following sections outline the plan for each module, the necessary classes, and their specific purposes and interactions.

---

## 1. Symbol Table Builder Module

### 1.1 SymbolData
- **Purpose**: Represents a single symbol in the symbol table.
- **Attributes**:
	- `symbol (str)`: Name of the symbol.
	- `value (int)`: Value of the symbol.
	- `rflag (bool)`: Relocation flag (true if relocatable).
	- `iflag (bool)`: Immutability flag (always true).
	- `mflag (bool)`: Indicates if the symbol is a duplicate.
- **Methods**:
	- `__init__(self, symbol, value, rflag)`: Initializes the symbol data.
	- `get_rflag(self)`: Returns the `rflag` value.

### 1.2 SymbolNode
- **Purpose**: Represents a node in the binary search tree (BST).
- **Attributes**:
	- `symbol_data (SymbolData)`: Contains the symbol data.
	- `left (SymbolNode)`: Pointer to the left child in the BST.
	- `right (SymbolNode)`: Pointer to the right child in the BST.
- **Methods**:
	- `__init__(self, symbol_data)`: Initializes the node with symbol data.

### 1.3 SymbolTable
- **Purpose**: Implements the BST to store and manage symbols.
- **Attributes**:
    - `root` (SymbolNode): The root node of the BST.
    - `log_entries` (list): Logs actions performed on the symbol table.
    - `reference_counts` (dict): Tracks how many times each symbol is referenced.
- **Methods**:
    - **Symbol Management**:
        - `insert(self, symbol_data)`: Inserts a new symbol into the BST.
        - `_insert(self, current_node, symbol_data)`: Helper method for insertion.
        - `search(self, symbol)`: Searches for a symbol in the BST.
        - `_search(self, current_node, symbol)`: Helper method for searching.
        - `view(self)`: Displays all symbols in the BST in sorted order.
        - `remove_symbol(self, symbol)`: Removes a symbol from the BST.
        - `_remove(self, node, symbol)`: Helper method for removal.
        - `destroy(self)`: Clears the entire symbol table.
    - **Reference Counting**:
        - `increment_reference(self, symbol)`: Increments the reference count for a symbol.
        - `display_reference_counts(self)`: Displays reference counts.
    - **Logging**:
        - `log_action(self, message)`: Adds a log entry.
        - `display_log(self)`: Displays all log entries.
    - **User Interaction**:
        - `prompt_for_confirmation(self, message)`: Prompts the user for confirmation.
        - `press_continue(self)`: Pauses output for readability.
#### Pseudocode
```python
Class SymbolTable:
    Attributes:
        root: SymbolNode            // Root of the BST
        log_entries: List           // Logs of actions performed
        reference_counts: Dictionary // Counts of symbol references

    Methods:
        Constructor():
            Set self.root to None
            Initialize self.log_entries as empty list
            Initialize self.reference_counts as empty dictionary

        insert(symbol_data):
            If self.root is None:
                Set self.root to new SymbolNode(symbol_data)
                Log action "Symbol inserted as root: symbol_data.symbol"
            Else:
                Call _insert(self.root, symbol_data)

        _insert(current_node, symbol_data):
            If symbol_data.symbol == current_node.symbol_data.symbol:
                Set current_node.symbol_data.mflag to True
                Log action "Duplicate symbol found: symbol_data.symbol"
            Else if symbol_data.symbol < current_node.symbol_data.symbol:
                If current_node.left is None:
                    Set current_node.left to new SymbolNode(symbol_data)
                    Log action "Symbol inserted to left: symbol_data.symbol"
                Else:
                    Call _insert(current_node.left, symbol_data)
            Else:
                If current_node.right is None:
                    Set current_node.right to new SymbolNode(symbol_data)
                    Log action "Symbol inserted to right: symbol_data.symbol"
                Else:
                    Call _insert(current_node.right, symbol_data)

        search(symbol):
            Call _search(self.root, uppercase first 4 chars of symbol)

        _search(current_node, symbol):
            If current_node is None:
                Return None
            If symbol == current_node.symbol_data.symbol:
                Log action "Symbol found: symbol"
                Return current_node.symbol_data
            Else if symbol < current_node.symbol_data.symbol:
                Return _search(current_node.left, symbol)
            Else:
                Return _search(current_node.right, symbol)

        view():
            If self.root is None:
                Print "Symbol table is empty."
            Else:
                Call inorder_traversal(self.root)

        inorder_traversal(node):
            If node is not None:
                Call inorder_traversal(node.left)
                Print node.symbol_data details
                Call inorder_traversal(node.right)

        remove_symbol(symbol):
            Call _remove(self.root, symbol)

        _remove(node, symbol):
            If node is None:
                Return node
            If symbol < node.symbol_data.symbol:
                node.left = _remove(node.left, symbol)
            Else if symbol > node.symbol_data.symbol:
                node.right = _remove(node.right, symbol)
            Else:
                If node.left is None:
                    temp = node.right
                    node = None
                    Return temp
                Else if node.right is None:
                    temp = node.left
                    node = None
                    Return temp
                temp = find_min(node.right)
                node.symbol_data = temp.symbol_data
                node.right = _remove(node.right, temp.symbol_data.symbol)
            Return node

        destroy():
            Set self.root to None
            Log action "Symbol table destroyed"

        increment_reference(symbol):
            If symbol in self.reference_counts:
                Increment self.reference_counts[symbol] by 1
            Else:
                Set self.reference_counts[symbol] to 1

        display_reference_counts():
            For each symbol in self.reference_counts:
                Print symbol and its count

        log_action(message):
            Append message to self.log_entries

        display_log():
            For each entry in self.log_entries:
                Print entry

        prompt_for_confirmation(message):
            Prompt user with message and get input (Yes/No)
            Return user's response

        press_continue():
            Prompt user to press Enter to continue

```

### 1.4 Validator
- **Purpose**: Validates symbols and their attributes.
- **Methods**:
    - `validate_symbol(self, symbol)`: Validates the symbol's format.
    - `validate_value(self, value)`: Validates the symbol's value.
    - `validate_rflag(self, rflag)`: Validates the `rflag` value.
    - `validate_syms_line(self, line)`: Validates a line from `SYMS.DAT`.

### 1.5 SymbolTableDriver
- **Purpose**: Manages the high-level operations of the symbol table.
- **Attributes**:
    - `symbol_table` (SymbolTable): Instance of the symbol table.
    - `file_explorer` (FileExplorer): Handles file operations.
    - `validator` (Validator): Validates symbols and values.
- **Methods**:
    - `process_syms_file(self, file_path)`: Reads `SYMS.DAT` and populates the symbol table.
    - `view(self)`: Displays the symbol table.
    - `search(self, symbol)`: Searches for a symbol in the symbol table.

### 1.6 SymbolReferenceCounter (Integrated into SymbolTable)
- **Purpose**: Tracks references to symbols.
- **Attributes**:
  - `reference_count (dict)`: Tracks the number of references to each symbol.
- **Methods**:
  - `increment(symbol)`: Updates the reference count for the specified symbol.

## 2. Literal Table Module
**Purpose**: Manages literals used in assembly expressions, storing them in a linked list.
### 2.1 LiteralData
- **Purpose**: Represents a literal with its attributes.
- **Attributes**:
    - `name` (str): The literal's name (e.g., `=0X5A`).
    - `value` (str): The hexadecimal representation of the literal's value.
    - `length` (int): Length of the literal in bytes.
    - `address` (int): Address assigned to the literal.
- **Methods**:
    - `__init__(self, name, value, length)`: Initializes the literal data.
### 2.2 LiteralNode
- **Purpose**: Represents a node in the linked list.
- **Attributes**:
    - `literal_data` (LiteralData): The literal data.
    - `next` (LiteralNode): Reference to the next node in the list.
- **Methods**:
    - `__init__(self, literal_data)`: Initializes the node with literal data.
### 2.3 LiteralTableList
- **Purpose**: Implements a linked list to store literals.
- **Attributes**:
    - `head` (LiteralNode): The head of the linked list.
- **Methods**:
    - `insert(self, literal_data)`: Inserts a new literal into the list.
    - `search(self, name)`: Searches for a literal in the list.
    - `display_literals(self)`: Displays all literals in the list.
        - It displays them in a table in 20 line pagination
    - 

---
## 3. Expression Module
**Purpose**: Handles the parsing and evaluation of expressions.
### 3.1 `ExpressionParser` Class
- **Purpose**: Reads expressions from a file and parses them into structured data.
- **Attributes**:
    - `file_explorer`: `FileExplorer` instance
    - `validator`: `Validator` instance
    - `error_log`: List of error messages
    - `log_entries`: List of log messages
- **Methods**:
    - `parse_expressions(self, file_path)`
        - Reads expressions from a file.
        - Returns a list of parsed expressions (e.g., dictionaries or custom objects).
    - `parse_expression(self, expression_line)`
        - Parses a single expression line into operands and operators.
### 3.2 `ExpressionEvaluator` Class
- **Purpose**: Evaluates parsed expressions and determines their values and relocatability.
	- Evaluating parsed expressions.
	- Determining addressing modes
	- Storing and formatting the results of expression evaluations
- **Attributes**:
    - `symbol_table`: `SymbolTable` instance
    - `literal_table`: `LiteralTableList` instance
    - `validator`: `Validator` instance
    - `error_log`: List of error messages
    - `log_entries`: List of log messages
- **Methods**:
	- `evaluate_expressions(self, parsed_expressions)`
	- `evaluate_expression(self, parsed_expression)`
	- `evaluate_operand(self, operand)`
	- **Addressing Mode Determination** (Integrated Methods):
	    - `determine_addressing_mode(self, operand)`
	        - Determines the addressing mode based on operand syntax.
	        - Sets the appropriate bits (`n_bit`, `i_bit`, `x_bit`).
	- **Relocatability Determination**:
	    - `determine_relocatability(self, operand1_info, operator, operand2_info)`
	- **Result Formatting**:
	    - `format_result(self, expression, value, is_relocatable, addressing_mode_info)`
	        - Formats the evaluation result for output.
	        - Replaces the functionality of `ExpressionResult`.

---
## 4. Utility Classes
**Purpose**: Provides supporting functionalities such as file handling and validation.
### 4.1 FileExplorer
- **Purpose**: Handles file operations.
- **Methods**:
    - `process_file(self, file_name)`: Reads a file and returns its lines.
    - `find_file(self, file_name)`: Locates a file in the system.
    - `prompt_for_file(self, file_name)`: Prompts the user to input a file path.
    - `open_file(self, file_path)`: Opens a file and yields its lines.
    - `read_file(self, file_generator)`: Reads lines from a file generator.
    - `read_line_from_file(self, line)`: Processes a single line from the file.
#### FileExplorer Pseudocode
```pseudocode
```

### 4.2 Validator (Already defined in 1.4)
- **Purpose**: Validates symbols, values, and expressions.
---
##  5. LiteralTableDriver
### 2.4 LiteralTableDriver
- **Purpose**: Manages high-level operations of the literal table.
- **Attributes**:
    - `literal_table` (LiteralTableList): Instance of the literal table.
- **Methods**:
    - `add_literal(self, literal_data)`: Adds a new literal to the table.
    - `update_addresses(self)`: Assigns addresses to literals.
    - `display_literals(self)`: Displays the literal table.
### 5.1 AssemblerMain
**Purpose:**
The `AssemblerMain` class orchestrates the entire assembly process by coordinating with various modules:
1. Loads and processes the `SYMS.DAT` file for symbols.
2. Handles literal management through the literal table.
3. Evaluates expressions from the provided input file (e.g., `EXPRESS.DAT`).
4. Manages user interaction and file operations.
5. Logs key actions and errors during the process.
### Attributes:
- **`symbol_table_driver` (SymbolTableDriver)**: Manages the symbol table.
- **`literal_table_driver` (LiteralTableDriver)**: Manages the literal table.
- **`expression_evaluator` (ExpressionEvaluator)**: Evaluates expressions and determines relocatability.
- **`file_explorer` (FileExplorer)**: Handles file operations, including reading input files.
- **`error_handler` (ErrorHandler)**: Centralized error logging and handling.
- **`log_entries` (list)**: Stores a log of all actions taken during the assembler execution.
- **`syms_file` (str)**: Stores the path of the `SYMS.DAT` file.
- **`express_file` (str)**: Stores the path of the expression file (e.g., `EXPRESS.DAT`).
### Methods:
1. **`__init__(self)`**:
    - Initializes all required components (`symbol_table_driver`, `literal_table_driver`, etc.).
    - Prepares the system for the overall assembly process.
2. **`load_files(self)`**:
    - Interacts with the user to locate and load the necessary files (`SYMS.DAT`, expression file).
    - Utilizes the `FileExplorer` to find and open files.
    - Ensures that both `SYMS.DAT` and the expression file are loaded successfully.
    - Logs the file-loading actions.
3. **`process_symbol_table(self)`**:
    - Processes the `SYMS.DAT` file using the `SymbolTableDriver`.
    - Validates the symbol data through the `Validator` and inserts valid entries into the symbol table.
    - Logs successful insertions or reports errors if symbols are invalid.
4. **`process_literals(self)`**:
    - Manages literals encountered during the expression evaluation.
    - Uses `LiteralTableDriver` to store and update literal information.
    - After all literals are collected, assigns addresses to them.
    - Displays and logs all literals in the table.
5. **`evaluate_expressions(self)`**:
    - Reads the expression file (e.g., `EXPRESS.DAT`) using the `FileExplorer`.
    - For each expression:
        - Sends it to `ExpressionEvaluator` for parsing, evaluation, and relocatability determination.
        - Logs and outputs the evaluated results, including the final value, addressing mode, and relocatability.
    - Handles errors encountered during expression evaluation.
6. **`display_results(self)`**:
    - Displays the contents of the symbol table, literal table, and evaluated expressions.
    - Outputs the reference counts of symbols (tracked by `SymbolTable`).
    - Ensures all tables and logs are output in a readable, formatted manner.
    - Provides the user with the option to view logs and errors.
7. **`log_action(self, message)`**:
    - Logs any significant action taken during the program (e.g., file loaded, symbol inserted, expression evaluated).
    - Appends each log entry to the `log_entries` list for later display.
8. **`log_error(self, message)`**:
    - Logs any errors encountered during the assembly process.
    - Appends errors to the `error_handler` for centralized logging.
9. **`run(self)`**:
    - The main entry point of the program:
        - Loads the required files.
        - Processes the symbol table.
        - Evaluates expressions.
        - Manages literals.
        - Displays results.
    - This method ties everything together and coordinates the program flow.
10. **`exit_program(self)`**:
    - Allows the program to gracefully exit after processing is complete.
    - Provides the user with a summary of logs and errors before closing.
    - Ensures all components are properly finalized or destroyed if necessary.
### 
---
### Overview of the Workflow
1. **Initialization**:
   - The `AssemblerMain` class initializes the symbol table, literal table, expression evaluator, and file explorer.
   - It sets up the environment for managing symbols, literals, and expressions.

2. **File Loading**:
   - The user is prompted to locate the `SYMS.DAT` and `EXPRESS.DAT` files.
   - The program uses the `FileExplorer` to ensure that the files are loaded correctly.

3. **Symbol Table Processing**:
   - The `SYMS.DAT` file is processed, and valid symbols are inserted into the `SymbolTable`.
   - Any errors encountered are logged and displayed at the end.

4. **Expression Evaluation**:
   - The `EXPRESS.DAT` file is processed line by line.
   - Each expression is evaluated by the `ExpressionEvaluator`, and results are displayed and logged.

5. **Literal Management**:
   - The program manages any literals encountered in the expressions.
   - After processing all expressions, literals are assigned addresses and displayed.

6. **Displaying Results**:
   - The program outputs the symbol table, literal table, and expression results.
   - It also displays logs of actions taken and any errors encountered during the process.

7. **Exiting**:
   - The program provides the user with a summary of logs and errors before exiting gracefully.

---
### **Conclusion**
The `AssemblerMain` class serves as the central point for coordinating the assembler's workflow. It manages interactions between different modules (symbol table, literal table, expression evaluator) and ensures that the process flows smoothly from start to finish. It handles file operations, manages user input/output, logs actions and errors, and ties all the different components together into a cohesive system.

---
## Class Interactions and Workflow
### 1. Initialization
- Instantiate the following:
    - `SymbolTable`
    - `LiteralTableList`
    - `Validator`
    - `FileExplorer`
    - `ErrorHandler`
- Create drivers and handlers:
    - `SymbolTableDriver` with `SymbolTable`, `FileExplorer`, and `Validator`
    - `LiteralTableDriver` with `LiteralTableList`
    - `ExpressionParser` with `FileExplorer`, `Validator`, and `ErrorHandler`
    - `ExpressionEvaluator` with `SymbolTable`, `LiteralTableList`, `Validator`, and `ErrorHandler`
    - `AddressingModeHandler`

### 2. Processing Symbols
- Use `SymbolTableDriver.process_syms_file(file_path)` to read `SYMS.DAT`:
    - For each line:
        - Validate using `Validator`
        - Insert into `SymbolTable`
        - Log actions and handle errors

### 3. Parsing Expressions
- Use `ExpressionParser.parse_expressions(file_path)` to read and parse expressions:
    - For each expression line:
        - Parse into operands and operators
        - Handle addressing modes
        - Collect parsed expressions into a list
        - Log actions and handle errors

### 4. Evaluating Expressions
- Use `ExpressionEvaluator.evaluate_expressions(parsed_expressions)`:
    - For each parsed expression:
        - Evaluate operands:
            - Use `evaluate_operand` to handle symbols and literals
            - Use `SymbolTable` for symbols
            - Use `LiteralTableDriver` for literals
        - Determine addressing modes using `AddressingModeHandler`
        - Determine relocatability using `determine_relocatability`
        - Compute expression value
        - Create `ExpressionResult`
        - Log actions and handle errors

### 5. Managing Literals
- When literals are encountered:
    - Use `LiteralTableDriver.add_literal(literal_data)` to add to the literal table
- After all expressions are evaluated:
    - Use `LiteralTableDriver.update_addresses()` to assign addresses to literals

### 6. Outputting Results
- Display evaluated expressions using `ExpressionResult.to_string()`
- Use `SymbolTableDriver.view()` to display the symbol table
- Use `LiteralTableDriver.display_literals()` to display the literal table
- Display any errors encountered using `ErrorHandler.display_errors()`

### 7. Reference Counting
- Increment symbol reference counts in `SymbolTable` during operand evaluation
- Use `SymbolTable.display_reference_counts()` to output reference counts

---
## Error Handling and Logging
- **Error Handling**:
    - All errors encountered during processing are logged using `log_error`.
    - Errors include invalid symbols, undefined symbols, invalid expressions, etc.
    - Errors are displayed at the end of processing via `display_errors`.
- **Logging**:
    - Actions such as symbol insertion, literal addition, expression evaluation are logged using `log_action`.
    - Logs provide a trace of operations for debugging and auditing.
---
## Addressing Modes and Relocatability Rules
- **Addressing Modes**:
    - **Immediate (`#`)**: Operand is a constant value.
    - **Indirect (`@`)**: Operand is the address of a value.
    - **Direct**: Operand is a symbol's value.
    - **Indexed (`,X`)**: Operand's value is modified by the index register.
- **Relocatability Determination**:
    - Based on the relocatability of operands and the operator used.
    - **Rules**:
        - **Relocatable + Relocatable**: Error.
        - **Relocatable - Relocatable**: Result is Absolute.
        - **Relocatable + Absolute**: Result is Relocatable.
        - **Relocatable - Absolute**: Result is Relocatable.
        - **Absolute + Absolute**: Result is Absolute.
        - **Absolute - Absolute**: Result is Absolute.
        - **Immediate Operands**: Treated as Absolute.

---
## Sample Workflow
1. **Load Symbols**:
    - Read `SYMS.DAT`.
    - For each line, validate and insert into `SymbolTable`.
2. **Evaluate Expressions**:
    - Read expressions from input file.
    - For each expression:
        - Parse expression into operands and operator.
        - Evaluate operands (handle symbols and literals).
        - Determine addressing mode.
        - Compute value and relocatability.
        - Create `ExpressionResult`.
        - Log actions and errors.
3. **Manage Literals**:
    - Add any new literals encountered to `LiteralTableList`.
    - Update addresses after all literals are collected.
4. **Output Results**:
    - Display evaluated expressions with values and attributes.
    - Display the symbol table and literal table.
    - Display any errors encountered.
---