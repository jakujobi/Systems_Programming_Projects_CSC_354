# Assignment Document
CSc 354 – Assignment #2
**Instructor**: Hamer  
**Due Date**: 10-9-24

## Objective
Create a module for your SIC/XE assembler to evaluate the operand field of an assembly language statement. The module must be **separate** from the symbol table developed in Assignment #1.

---
## Basic Algorithm
1. **Read Symbols from SYMS.DAT**
   - **SYMS.DAT** is a text file containing symbols and their attributes.
   - Format:
     - `SYMBOL    VALUE    RFLAG`
   - The process used here is the same as **Step #1** of Assignment #1.
2. **Read Expressions**
   - Read expressions from a text file specified via the command line.
   - If no file name is provided, prompt the user for one.
   - **Evaluate each expression**:
     - Maximum of **two values/operands per expression**.
     - Supported arithmetic operations: **Addition (+)** and **Subtraction (-)**.
     - **Determine RFLAG** using the provided table.
     - If an expression begins with `=`, treat it as a **literal** and insert it into the **literal table** if unique.
3. **Display Expression Information**
   - Output format is provided and must be adhered to – order of attributes is required – see `Expressions evaluation results`.
   - Display **detailed error messages** for invalid expressions.

4. **Display Literal Table Contents**
   - The output format is provided, and the order of attributes is required -see `Literal table`.
---
## Expression File Format
Expressions are provided line-by-line, possibly with leading spaces. Examples include:

| **Expression**     | **Addressing Mode**     | **Details**                                                                                     |
|--------------------|-------------------------|-------------------------------------------------------------------------------------------------|
| `GREEN`            | Simple/Direct           | Directly references `GREEN`. Uses `RFLAG` value of `GREEN`.                                     |
| `@GREEN`           | Indirect                | Indirect reference to `GREEN`. Uses `RFLAG` value of `GREEN`.                                   |
| `#GREEN`           | Immediate               | Immediate value of `GREEN`. Uses `RFLAG` value of `GREEN`.                                      |
| `#9`               | Immediate               | Numeric literal value (`9`). Treated as **absolute**.                                           |
| `GREEN,X`          | Indexed                 | Accesses `GREEN` with an index (`X`). Uses `RFLAG` value of `GREEN`.                            |
| `GREEN + YELLOW`   | Combination (Addition)  | Adds values of `GREEN` and `YELLOW`. Combines **RFLAG** values of both symbols.                 |
| `GREEN - 15`       | Combination (Subtraction) | Subtracts an **absolute** value (`15`) from `GREEN`. Resulting `RFLAG` is based on `GREEN`.     |
| `=0cABC`           | Character Literal       | Represents characters (`ABC`) as literals. One character per byte.                              |
| `=0x5A`            | Hexadecimal Literal     | Represents hexadecimal value (`5A`). Two hexadecimal digits per byte.                           |
### Breakdown
Below is a detailed breakdown of the expression types and their addressing modes:
- **Direct Addressing**: 
	- **Expression**: `GREEN`
	- **Details**: Represents a direct memory reference to the symbol `GREEN`. The **RFLAG** value determines whether this symbol is relocatable or not.
- **Indirect Addressing**:
	- **Expression**: `@GREEN`
	- **Details**: This means the value of `GREEN` should be interpreted indirectly (the value of the address that `GREEN` points to). The **RFLAG** value of `GREEN` is used.
- **Immediate Addressing**:
	- **Expression**: `#GREEN`
		- **Details**: Uses the value of `GREEN` immediately. The **RFLAG** is based on `GREEN`.
	- **Expression**: `#9`
		- **Details**: A numeric value specified directly. Since it's a literal value, it is **absolute**.
- **Indexed Addressing**:
	- **Expression**: `GREEN,X`
	- **Details**: The symbol `GREEN` is accessed with an index (`X`). The **RFLAG** of `GREEN` is used.
- **Combining Symbols and Values**:
	- **Expression**: `GREEN + YELLOW`
		- **Details**: Represents the addition of the values of `GREEN` and `YELLOW`. Both symbols have **RFLAG** values that determine if the result is relocatable.
	- **Expression**: `GREEN - 15`
		- **Details**: Represents subtraction of the constant value `15` from `GREEN`. Since `15` is an **absolute** value, the resulting **RFLAG** is based on `GREEN`.
- **Character Literal**:
	- **Expression**: `=0cABC`
	- **Details**: This is a character literal where each character is represented by one byte. The prefix `=0c` indicates the use of a character literal.
- **Hexadecimal Literal**:
	- **Expression**: `=0x5A`
	- **Details**: Represents a hexadecimal literal where each two hexadecimal digits represent one byte. The prefix `=0x` is used to denote hexadecimal representation.

## Rules for Evaluating Relocatability
- **Absolute Value**: Not relative to the program’s starting address (**RFLAG = FALSE (0)**).
- **Relative Value**: Relative to the starting address of the program (**RFLAG = TRUE (1)**).
### RFLAG Evaluation Table

| **RFLAG #1** | **Operation** | **RFLAG #2** | **Adjusted RFLAG** |
|--------------|---------------|--------------|--------------------|
| ABSOLUTE     | -             | ABSOLUTE     | ABSOLUTE           |
| ABSOLUTE     | -             | RELATIVE     | ERROR              |
| ABSOLUTE     | +             | ABSOLUTE     | ABSOLUTE           |
| ABSOLUTE     | +             | RELATIVE     | RELATIVE           |
| RELATIVE     | -             | ABSOLUTE     | RELATIVE           |
| RELATIVE     | -             | RELATIVE     | ABSOLUTE           |
| RELATIVE     | +             | ABSOLUTE     | RELATIVE           |
| RELATIVE     | +             | RELATIVE     | ERROR              |

---
## Literal Table Details

| **Attribute**       | **Description**                                                                                                                                       | **Examples**                                                |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Literal Name**    | The actual literal expression, including `=` and quotes.                                                                                              | `=0CABC`, `=0Cabc`, `=0X0F`, `=0X123`                       |
|                     |                                                                                                                                                       | `=0cABC`, `=0cabc`, `=0x0f`, `=0x123`                       |
| **Operand Value**   | Object code equivalent in **hexadecimal**.                                                                                                            | `414243`, `616263`, `0F`, `ERROR`                           |
| **Length in Bytes** | The number of bytes used to represent the literal.                                                                                                    | `3`, `3`, `1`, `ERROR`                                      |
| **Address**         | Initially represents the occurrence of the literal in the expression file. Eventually, it will be updated to represent the actual **memory address**. | `0` — first literal encountered, `1` — second literal, etc. |
### Implementation
- The literal table is implemented using a **linked list** to store each literal and its associated attributes.
- The **literal table** is well-suited to be implemented as a **standalone module**, supporting a more modular code structure.
### Attributes Stored in the Literal Table
1. **Literal Name**
    - Represents the full literal expression, including the `=` sign and possible quotes.
    - **Examples**:
        - `=0CABC`, `=0Cabc`, `=0X0F`, `=0X123`
        - `=0cABC`, `=0cabc`, `=0x0f`, `=0x123`
2. **Operand Value**
    - This is the **object code equivalent** in hexadecimal form.
    - **Examples**:
        - `414243`, `616263`, `0F`, `ERROR`
3. **Length in Bytes**
    - Indicates the number of bytes used to represent the literal.
    - **Examples**:
        - `3`, `3`, `1`, `ERROR`
4. **Address**
    - Initially, this attribute represents the **occurrence position** of the literal in the expression file, which will eventually be updated to reflect the actual **memory address**.
    - **Examples**:
        - `0` — First literal encountered
        - `1` — Second literal encountered

---
## Module Responsibilities
- Each module should **only** contain operations directly related to it.
- **Required Modules**:
  - **Symbol Table** and **Expression Processing**.
- **Optional Modules**:
  - **Literal Table, String Processing, Error Handling**, etc.
- The **Symbol Table module** should **not** handle:
  - File processing, literal table management, string/character processing, or most error handling.
---
## Output Requirements
- All output should be **understandable**:
  - Follow the **example** provided at the end of the document.
  - Prevent the screen from **scrolling off**:
    - Temporarily pause the screen if necessary.
    - Temporary pause the screen after every 18 lines, then ask the user to press enter to continue
  - The **default screen size** for Tera Term Pro is approximately **20 lines and 80 columns**.
  - Adjust Visual Studio projects accordingly.
---
## Error Handling
- Provide **detailed** error messages:
  - Print error messages immediately upon encountering them.
  - Describe each error clearly and indicate the component that caused it.
  - **Continue processing** after encountering an error; handle each line of the data file.
---
## Expression Processing Example
### SYMS.DAT File

| **SYMBOL** | **VALUE** | **RFLAG** |
|------------|-----------|-----------|
| RED        | 13        | TRUE      |
| PURPLE     | 6         | FALSE     |
| BLACK      | -7        | TRUE      |
| PINK       | 9         | TRUE      |
| WHITE      | 5         | FALSE     |
```
RED:		13	TRUE
PURPLE:	6	FALSE
BLACK:	-7	TRUE
PINK:		9	TRUE
WHITE:	5	FALSE
```
### Expressions File
```
RED  
PURPLE + #17
@BLACK
#WHITE
WHITE,X
22
=0X5A
PINK + #3
=0X5A
PINK - #3
@#25 + RED
=0C5A
#7
```
When a symbol is found, its attribute values are fetched from the **symbol table**.

--
### Expression Evaluation Results

| **EXPRESSION** | **VALUE** | **RELOCATABLE** | **N-Bit** | **I-Bit** | **X-Bit** |
|----------------|-----------|-----------------|-----------|-----------|-----------|
| RED            | 13        | RELATIVE        | 1         | 1         | 0         |
| PURPLE + #17   | 23        | ABSOLUTE        | 1         | 1         | 0         |
| @BLACK         | -7        | RELATIVE        | 1         | 0         | 0         |
| # WHITE        | 5         | ABSOLUTE        | 0         | 1         | 0         |
| WHITE, X       | 5         | ABSOLUTE        | 1         | 1         | 1         |
| #22            | 22        | ABSOLUTE        | 0         | 1         | 0         |
| PINK + #3      | 12        | RELATIVE        | 1         | 1         | 0         |
| PINK - #3      | 6         | RELATIVE        | 1         | 1         | 0         |
| @#25 + RED     | 38        | RELATIVE        | 1         | 0         | 0         |
| #7             | 7         | ABSOLUTE        | 0         | 1         | 0         |

---
## Literal Table Example

| **NAME**  | **VALUE** | **LENGTH** | **ADDRESS** |
|-----------|-----------|-----------|-------------|
| =0CDEFG   | 44454647  | 4         | 1           |
| =0X5A     | 5A        | 1         | 2           |
| =0C5A     | 3541      | 2         | 3           |

---
## Notes
- The symbols `@`, `#`, and `,X` apply to the **entire expression**, not individual operands:
  - Examples: `@(OP1+OP2)`, `#(OP1-OP2)`, `(OP1+OP2),X`.
  - **Parentheses** are not part of statement syntax, except with **numeric literals** associated with `#` (e.g., `PURPLE + #17`).
- **Duplicate literals** are not errors:
  - Each unique literal is entered **only once**.
  - Think of literals as **constants**—declared once, used multiple times.
- Display the **symbol table contents** for debugging purposes.
- Leading spaces in the files should be ignored
- For invalid expressions (such as unsupported operators or undefined symbols), the module should generate an error and continue processing the rest.
- Errors should indicate the type of error, the location, reason

### Professor's Specific Allowances Explained
1. **`#one + two` (Immediate Addressing with Addition)**
    - **Interpretation**:
        - This expression means that the value of `one` (a symbol) is to be added to `two` (another symbol) with **immediate addressing** (`#`).
        - The presence of `#` indicates **immediate addressing**, meaning you are using the value directly rather than looking it up indirectly or using it as a memory reference.
        - The **RFLAG** of `one` and `two` will need to be combined using the rules for evaluating `RFLAG` in the **RFLAG Evaluation Table**.
    - **Specific Allowance**:
        - This seems to imply that the system will handle combinations like **symbol + symbol** in immediate mode without any issue, as long as both are present in the symbol table.
2. **`@one + two` (Indirect Addressing with Addition)**
    - **Interpretation**:
        - The `@` symbol means **indirect addressing**, where `one` is treated as a pointer and `two` is added to the value indirectly referenced by `one`.
        - `one` is treated as an address, and you are adding `two` to the value stored at the address `one` points to.
    - **Specific Allowance**:
        - This expression is allowed, which suggests that indirect addressing with addition is supported and must be implemented. The addition must follow the rules specified, with **RFLAG** being adjusted based on the table.
3. `one + #2` (Symbol Added to Immediate Literal)
    - **Interpretation**:
        - This expression has a **symbol (`one`)** being added to an **immediate value (`#2`)**.
        - The immediate value `#2` is **absolute**, and its `RFLAG` value is `FALSE`.
    - **Specific Allowance**:
        - It’s mentioned that this will **not** be allowed to "TR". Likely, "TR" could mean **transform** or **relocate**.
        - This means the result of the addition involving an **absolute immediate value** and a **symbol** will not result in a **relocatable** address. This suggests that the relocation flag (`RFLAG`) handling must indicate that the result is **absolute**.
        - Essentially, an expression like this will always have a **non-relocatable** (`RFLAG = FALSE`) result.
4. **`#5 + 4` (Addition of Immediate Values without Symbol Table Lookup)**
    - **Interpretation**:
        - This involves adding two **immediate values** directly (`#5` and `4`). Since both values are **immediate**, they are treated as **absolute**.
    - **Specific Allowance**:
        - The statement "will calculate the value but will not check the symbol table" implies:
            - Since both operands are **literal values** and not symbols, the system does not need to perform a **symbol table lookup**.
            - It means that for calculations involving only **numeric literals**, the evaluation is straightforward arithmetic without needing to verify against the **symbol table** for attributes like `RFLAG`.
        - This allows for simplification in processing, as there's no need to check attributes from the symbol table when literals are involved.
### **Summary of Professor's Allowances**
- **Expressions Allowed**:
    - **Immediate Addressing with Addition of Symbols** (`#one + two`): Evaluate normally, use **RFLAG** rules.
    - **Indirect Addressing with Addition** (`@one + two`): Allowed, must follow **RFLAG** rules for evaluating relocatability.
    - **Symbol with Immediate Value Addition** (`one + #2`): Will **not transform** to a relocatable value; result is always **absolute**.
    - **Addition of Immediate Literals** (`#5 + 4`): Allowed, but the **symbol table** is not involved, as both are literals. Simply calculate the value.
### **Professor's Specific Disallowance Explained**

#### **Expression: `one#+two`**
- **Format**: The given format involves `one`, a symbol, combined with `#+`, which represents an **immediate addressing mode** with an arithmetic operation.
- **Interpretation**:
    - `one#+two` suggests that `one` is being combined with a **literal value** (`#+`) followed by another symbol (`two`). This syntax appears non-standard and ambiguous, which is why it is **not allowed**.
- **Specific Disallowance**:
    - The professor explicitly states that this form is **invalid** and will not be allowed.
    - This means:
        - Your assembler module should treat such an expression as an **error**.
        - When encountering an expression like `one#+two`, the module should flag it as **invalid** and produce an appropriate **error message**.
### **Summary of Handling `one#+two`**
- **Invalid Expression**: The expression format `one#+two` is **invalid**.
- **Action**: Your program must **detect** this syntax and **not allow** it, meaning:
    - Generate a **detailed error message** indicating that the format is incorrect or unsupported.
    - Do **not proceed** with evaluating or attempting to calculate such expressions.

### **Possible Implementation Considerations**

- **Error Handling**:
    - When parsing the expression file, include logic that can identify unsupported syntax, such as `one#+two`.
    - Ensure that detailed feedback is provided to the user, explaining why this format is not valid. For example, you could say: "Error: The expression `one#+two` contains an invalid immediate addressing operation. The `#+` syntax is not allowed."
- **Expression Parsing**:
    - As part of the expression parsing logic, include conditions that verify:
        - **Valid combinations** of addressing modes and operands.
        - **Proper use** of symbols and literals together.
    - Specifically, the parser should reject any expression where an **immediate addressing operator (`#`)** is improperly combined with another symbol in a non-standard format, like `#+`.
### **Professor's Additional Instructions**
1. **Handling the `+` Operator**
    - **"Tear into Two Operands"**:
        - If an expression includes `+`, split it into **two operands**.
        - For example, `GREEN + YELLOW` becomes **operand 1** (`GREEN`) and **operand 2** (`YELLOW`).
        - This split makes it easier to evaluate each part separately (e.g., look up values in the symbol table).
		```
		def evaluate_expression(expression):
    if '+' in expression:
        # Split the expression at the '+' operator
        operand1, operand2 = expression.split('+')
        operand1 = operand1.strip()  # Remove extra spaces
        operand2 = operand2.strip()
        
        # Fetch values for operand1 and operand2 from the symbol table
        value1 = get_value_from_symbol_table(operand1)  # Assume decimal value returned
        value2 = get_value_from_symbol_table(operand2)

        # Calculate the result in decimal
        result_decimal = value1 + value2
        
        # Convert to hexadecimal for output
        result_hex = hex(result_decimal)  # Convert to hexadecimal
        
        # Display result
        print(f"Result of {expression}: {result_hex.upper()}")
        # Example Usage
        evaluate_expression("GREEN + YELLOW")
		```
1. **Use Decimal for Calculations, Display Hexadecimal**
    
    - **Internal Calculations in Decimal**:
        - Perform arithmetic operations in **decimal** for simplicity.
        - Example: If `GREEN = 10` and `YELLOW = 15`, then `GREEN + YELLOW = 25` (in decimal).
    - **Output as Hexadecimal**:
        - Convert results to **hexadecimal** for output.
        - Example: The decimal value `25` should be displayed as `0x19`.
---

# Project Plan

### Plan Overview

The project can be divided into multiple modules/classes for better separation of concerns. The main components will include:

1. **Symbol Table Module** (existing from Assignment #1).
2. **Expression Evaluator Module**.
3. **Literal Table Module**.
4. **Main Driver Module**.
5. **Error Handling Module**.


---

### 1. Symbol Table Module

**Purpose**: Maintain the list of symbols and their attributes, which includes fetching symbol values when needed during expression evaluation.

**Class**: `SymbolTable`

**Attributes**:
- `symbols` (dictionary): Holds the symbol, value, and RFLAG.

**Methods**:
1. **`load_symbols(file_path)`**:
   - **Input**: `file_path` - the path to `SYMS.DAT`.
   - **Action**: Loads symbols from the `SYMS.DAT` file into the dictionary.
2. **`get_symbol(symbol_name)`**:
   - **Input**: `symbol_name` - the name of the symbol.
   - **Output**: Returns a tuple `(value, RFLAG)` for a given symbol.
3. **`display_symbols()`**:
   - **Action**: Prints out all the symbols and their attributes for debugging purposes.

---

### 2. Expression Evaluator Module

**Purpose**: Evaluate the expressions read from a file, supporting basic operations (`+`, `-`) and different addressing modes.

**Class**: `ExpressionEvaluator`

**Attributes**:
- `symbol_table` (instance of `SymbolTable`): Reference to the symbol table for resolving values.
- `literal_table` (instance of `LiteralTable`): Reference to the literal table for managing literals.

**Methods**:
1. **`evaluate_expressions(file_path)`**:
   - **Input**: `file_path` - path to the file containing the expressions.
   - **Action**: Reads expressions line by line and evaluates them.
2. **`parse_expression(expression)`**:
   - **Input**: `expression` - a single line of an expression.
   - **Output**: Parses the expression into components (e.g., `operand1`, `operator`, `operand2`).
3. **`evaluate(expression)`**:
   - **Input**: `expression` - parsed expression details.
   - **Output**: Returns the evaluated value and addressing mode flags.
   - **Details**: 
     - Split by `+` or `-` if needed.
     - Check the RFLAG and perform the appropriate calculations based on the type of operands.

**Functions for Addressing Modes**:
- **`evaluate_direct(operand)`**:
  - Evaluates direct operand (`GREEN`).
- **`evaluate_indirect(operand)`**:
  - Evaluates indirect operand (`@GREEN`).
- **`evaluate_immediate(operand)`**:
  - Evaluates immediate operand (`#9`).
- **`evaluate_indexed(operand)`**:
  - Evaluates indexed operand (`GREEN,X`).
- **`evaluate_literal(operand)`**:
  - Evaluates and adds literals to the literal table.

---

### 3. Literal Table Module

**Purpose**: Manage literals found in expressions and maintain their associated details.

**Class**: `LiteralTable`

**Attributes**:
- `literals` (linked list or list of dictionaries): Stores literals with their attributes (name, value, length, address).

**Methods**:
1. **`add_literal(literal)`**:
   - **Input**: `literal` - the literal expression (e.g., `=0x5A`).
   - **Action**: Adds a literal to the table if it doesn’t already exist.
2. **`get_literal(literal_name)`**:
   - **Input**: `literal_name` - name of the literal.
   - **Output**: Returns the literal's attributes.
3. **`display_literals()`**:
   - **Action**: Prints out the literal table.

---

### 4. Main Driver Module

**Purpose**: Serve as the entry point of the program, orchestrating interactions between different components.

**Class**: `AssemblerDriver`

**Attributes**:
- `symbol_table`: Instance of `SymbolTable`.
- `expression_evaluator`: Instance of `ExpressionEvaluator`.
- `literal_table`: Instance of `LiteralTable`.

**Methods**:
1. **`run()`**:
   - **Action**: Main function that loads the symbol table, reads and evaluates expressions, and manages the literal table.
   - **Steps**:
     1. Load symbols from `SYMS.DAT`.
     2. Prompt user for an expression file if not provided via command line.
     3. Evaluate each expression.
     4. Display results and handle output formatting requirements.

**Helper Methods**:
- **`prompt_for_file()`**: Prompts user for an expression file if none is provided.
- **`pause_screen()`**: Pauses screen after every 18 lines of output.

---

### 5. Error Handling Module

**Purpose**: Handle errors during parsing, evaluation, and literal processing.

**Class**: `ErrorHandler`

**Methods**:
1. **`handle_invalid_expression(expression, error_details)`**:
   - **Input**: `expression`, `error_details`.
   - **Action**: Prints detailed error message without stopping program execution.
2. **`validate_operand(operand)`**:
   - **Input**: `operand`.
   - **Output**: Checks if operand is valid and returns corresponding value or error.

---

### Class & Method Interactions

- **`AssemblerDriver`**:
  - Calls `SymbolTable.load_symbols()` to populate the symbols.
  - Creates instances of `ExpressionEvaluator` and `LiteralTable`.
  - Calls `ExpressionEvaluator.evaluate_expressions()` to evaluate input expressions.
  - Calls `LiteralTable.display_literals()` and `SymbolTable.display_symbols()` to show final tables.

- **`ExpressionEvaluator`**:
  - Uses `SymbolTable.get_symbol()` to fetch values during expression evaluation.
  - Uses `LiteralTable.add_literal()` for literals.

- **`ErrorHandler`**:
  - Is used throughout different classes whenever an error needs to be logged or an invalid input is detected.

---

### Example Workflow

1. **Initialization**:
   - **`AssemblerDriver`** starts, initializes `SymbolTable`, `ExpressionEvaluator`, and `LiteralTable`.
2. **Load Symbols**:
   - Symbols are loaded from `SYMS.DAT` by `SymbolTable`.
3. **Read and Evaluate Expressions**:
   - **`ExpressionEvaluator`** reads the expressions from the provided file.
   - For each line, **`ExpressionEvaluator`** splits it into operands and operators.
   - It fetches values using the **`SymbolTable`** and performs the arithmetic.
   - Literals are added to the **`LiteralTable`** if needed.
   - If an error occurs, **`ErrorHandler`** provides a message and continues.
4. **Display Results**:
   - **`AssemblerDriver`** manages output, displaying the evaluation results and the literal table.

---

### Sample Pseudo Code for the Modules

Here's some pseudo code to give a sense of how everything interacts:

```python
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def load_symbols(self, file_path):
        # Load symbols from SYMS.DAT file
        pass

    def get_symbol(self, symbol_name):
        # Return value and RFLAG of symbol
        pass


class ExpressionEvaluator:
    def __init__(self, symbol_table, literal_table):
        self.symbol_table = symbol_table
        self.literal_table = literal_table

    def evaluate_expressions(self, file_path):
        # Read and evaluate expressions from file
        pass

    def parse_expression(self, expression):
        # Parse a single expression into components
        pass

    def evaluate(self, expression):
        # Evaluate parsed expression
        pass


class LiteralTable:
    def __init__(self):
        self.literals = []

    def add_literal(self, literal):
        # Add a literal to the literal table
        pass


class ErrorHandler:
    @staticmethod
    def handle_invalid_expression(expression, error_details):
        # Print error details
        pass


class AssemblerDriver:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.literal_table = LiteralTable()
        self.expression_evaluator = ExpressionEvaluator(self.symbol_table, self.literal_table)

    def run(self):
        # Main driver code
        pass


if __name__ == "__main__":
    driver = AssemblerDriver()
    driver.run()
```

---

### Next Steps

- **Implementation**: You can start implementing these classes and methods incrementally. Begin by coding the `SymbolTable` and `LiteralTable`, as they provide necessary support for expression evaluation.
- **Testing**: Write unit tests for each module. Start with the `SymbolTable` and verify symbol retrieval, then move to expression parsing and evaluation.
- **Integration**: Once individual modules are tested, integrate them in `AssemblerDriver` and start testing with sample files.

Would you like to dive deeper into any specific part of the design, or is there a particular module you'd like more detailed help with first?