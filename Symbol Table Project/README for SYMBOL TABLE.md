# README for Symbol Table Project (GEN)

## Project Overview

The **Symbol Table Project** is a Python-based implementation of a symbol table using a **Binary Search Tree (BST)**. The project includes functionality for:

- Inserting symbols from a `SYMS.DAT` file into the symbol table.
- Searching for symbols in the table using a `SEARCH.TXT` file.
- Viewing and managing the symbol table, including duplication checking and pagination for displaying results.
- An additional generator (`generate_SYMS_SEARCH.py`) to create test `SYMS.DAT` and `SEARCH.TXT` files.

---

**Disclaimer**: I generated this specific README based on the directory & already implemented project content by OpenHermes 2.5 Mistral 7B, a small large language model hosted locally on my pc. The model was only used to generate this README

---

## Table of Contents

- [Symbol Table Project Documentation](#symbol-table-project-documentation)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [File Structure](#file-structure)
  - [Classes Overview](#classes-overview)
    - [SymbolData Class](#symboldata-class)
    - [SymbolNode Class](#symbolnode-class)
    - [SymbolTable Class](#symboltable-class)
    - [FileExplorer Class](#fileexplorer-class)
    - [Validator Class](#validator-class)
    - [SymbolTableDriver Class](#symboltabledriver-class)
  - [Usage](#usage)
    - [Running the Program](#running-the-program)
    - [Generating Test Files](#generating-test-files)
  - [SYMS.DAT File Format](#symsdat-file-format)
  - [SEARCH.TXT File Format](#searchtxt-file-format)
  - [Future Improvements](#future-improvements)
  - [Conclusion](#conclusion)
    - [Notes:](#notes)

---

## File Structure

The project is organized as follows:

```plaintext
Symbol Table Project/
├── test/
│   ├── generate_SYMS_SEARCH.py  # Generates test SYMS.DAT and SEARCH.TXT files
│   ├── test_SYMS.DAT            # Sample generated SYMS.DAT
│   ├── test_SEARCH.TXT          # Sample generated SEARCH.TXT
│   ├── test_FileExplorer.py           # Tests for FileExplorer class
│   ├── test_search_validator.py       # Tests for search functionality
│   ├── test_validator.py              # Tests for validation logic
├── Assignment 1.docx             # Documentation or assignment submission
├── Symbol Table Project.md       # Project documentation
├── SYMBOL_TABLE.py               # Main symbol table program
├── SYMS.DAT                      # Input file containing symbol data
├── SEARCH.txt                    # Input file containing search symbols
└── .gitattributes                 # Git configuration
```

---

## Classes Overview

### SymbolData Class

**Purpose**: Represents a single symbol entry in the symbol table.

- **Attributes**:

  - `symbol`: (str) The symbol's identifier (first 4 characters, uppercase).
  - `value`: (int) Signed integer between -5000 and 5000.
  - `rflag`: (bool) Relocation flag (True/False).
  - `iflag`: (bool) Always set to `True`.
  - `mflag`: (bool) Indicates if the symbol is a duplicate (True/False).
- **Usage**:
  A new instance of `SymbolData` is created when a valid symbol is inserted into the symbol table.

```python
def __init__(self, symbol, value, rflag, iflag=True, mflag=False):
    self.symbol = symbol.upper()[:4]
    self.value = value
    self.rflag = rflag
    self.iflag = iflag
    self.mflag = mflag
```

### SymbolNode Class

**Purpose**: Represents a node in the **Binary Search Tree (BST)**.

- **Attributes**:
  - `symbol_data`: Holds a `SymbolData` object.
  - `left`: Reference to the left child in the BST.
  - `right`: Reference to the right child in the BST.

```python
def __init__(self, symbol_data):
    self.symbol_data = symbol_data
    self.left = None
    self.right = None
```

### SymbolTable Class

**Purpose**: Implements the **Binary Search Tree** for managing symbols.

- **Methods**:
  - `insert(symbol_data)`: Inserts a `SymbolData` object into the BST.
  - `search(symbol)`: Searches for a symbol in the table.
  - `view()`: Displays the contents of the symbol table in sorted order (with pagination).
  - `remove_symbol(symbol)`: Removes a symbol from the BST.
  - `destroy()`: Destroys the BST.

```python
def insert(self, symbol_data):
    """Insert symbol into the binary search tree."""
```

### FileExplorer Class

**Purpose**: Handles file reading and file system navigation.

- **Methods**:
  - `process_file(file_name)`: Locates and opens a file, returning cleaned lines.
  - `find_file(file_name)`: Searches for the file in the script's directory or prompts the user.
  - `open_file(file_path)`: Reads the file line by line using a generator.
  - `read_file(file)`: Processes each line of the file.

```python
def process_file(self, file_name):
    """Process the file by finding it, opening it, and reading it line by line."""
```

### Validator Class

**Purpose**: Validates the symbols, values, and relocation flags from the `SYMS.DAT` and `SEARCH.TXT` files.

- **Methods**:
  - `validate_symbol(symbol)`: Ensures the symbol is valid according to project constraints.
  - `validate_value(value)`: Ensures the value is an integer between -5000 and 5000.
  - `validate_rflag(rflag)`: Ensures the relocation flag is `true` or `false`.
  - `validate_syms_line(line)`: Validates a full line from the `SYMS.DAT` file.
  - `validate_search_line(line)`: Validates a symbol from the `SEARCH.TXT` file.

```python
def validate_syms_line(self, line):
    """Validate a line from the SYMS.DAT file."""
```

### SymbolTableDriver Class

**Purpose**: Manages the high-level operations for symbol table management and file processing.

- **Methods**:
  - `process_syms_file(file_path)`: Processes the `SYMS.DAT` file.
  - `process_search_file(file_path)`: Processes the `SEARCH.TXT` file.
  - `display_symbols_paginated(symbols)`: Displays symbols in a paginated table.
  - `view()`: Displays the symbol table.
  - `run()`: Runs the main program.

```python
def run(self):
    """Main method to run the program."""
```

---

## Usage

### Running the Program

1. Place your `SYMS.DAT` and `SEARCH.TXT` files in the same directory as the script.
2. Run the main script:

```bash
python SYMBOL_TABLE.py
```

3. The program will prompt you to use the files from the directory or manually locate them.
4. The program will process and validate symbols, display the symbol table, and search for symbols.

### Generating Test Files

To generate test data, run:

```bash
python generate_SYMS_SEARCH.py
```

This will create `test_SYMS.DAT` and `test_SEARCH.TXT` files with randomized data for testing.

---

## SYMS.DAT File Format

Each line in `SYMS.DAT` must follow this format:

```
<SYMBOL>: <VALUE> <RFLAG>
```

- **SYMBOL**: Up to 10 characters, must start with a letter.
- **VALUE**: An integer between -5000 and 5000.
- **RFLAG**: Boolean (`true` or `false`).

Example:

```
ABC: 300 true
XYZ: -123 false
```

---

## SEARCH.TXT File Format

Each line in `SEARCH.TXT` contains a single symbol to search for in the symbol table:

```
<SYMBOL>
```

Example:

```
ABC
XYZ
```

---

## Future Improvements

- **Error Handling**: Improve error reporting and handling across the program.
- **GUI Interface**: Add a graphical interface for easier file selection and viewing.Kind of like in obscuRRRa

---
