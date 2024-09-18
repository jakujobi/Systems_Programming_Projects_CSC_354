# Readme Symbol Table Manager

## Overview
This program manages a symbol table by reading symbols from a `SYMS.DAT` file and storing them in a Binary Search Tree (BST). It supports symbol insertion, searching, and validation. The program also reads a `SEARCH.TXT` file to look for symbols in the table. Symbols and their values can be displayed in a paginated table format.

## Features
- **Symbol Insertion**: Reads symbols from `SYMS.DAT` and inserts them into a binary search tree.
- **Symbol Search**: Reads symbols from `SEARCH.TXT` and searches for them in the symbol table.
- **Validation**: Ensures that each symbol, its value, and flags conform to specified rules.
- **Pagination**: Displays symbols in pages of 20 entries, with a pause between pages.
- **File Explorer**: Allows the user to manually select files via command line or system GUI (Tkinter).

## Files Used
- `SYMS.DAT`: Contains symbols to be inserted.
- `SEARCH.TXT`: Contains symbols to search for in the table.

## How to Run
1. Ensure you have Python 3 installed.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the program with the command:
   ```bash
   python SYMBOL_TABLE.py
   ```

## Program Flow
1. **Welcome Screen**: Upon starting, the program greets you with a welcome message.
2. **SYMS.DAT File Processing**: 
   - The program automatically looks for the `SYMS.DAT` file in the current directory.
   - If found, it will prompt: `Do you want to use this SYMS.DAT? (y/n)`. Press `Enter` or type `y` to confirm or type `n` to choose another file.
   - The program will validate and insert symbols from the file into the binary search tree.
3. **Viewing the Symbol Table**:
   - After processing, the program will ask: `Do you want to view the current symbol table? (y/n)`. You can choose to view the symbols in the table or skip this step.
   - If you view the table, it will be displayed in a paginated format, showing 20 entries at a time. You can press `Enter` to move to the next page.
4. **SEARCH.TXT File Processing**:
   - The program will then prompt to find the `SEARCH.TXT` file.
   - Similar to the previous step, it will check the current directory and ask if you want to use the file. You can press `Enter` to proceed or manually select another file.
   - It will search for each symbol listed in the file and display the results in a table format, showing whether each symbol was found or not.
5. **Exit**: After completing the search, the program will exit automatically.

## Dependencies
- Python 3.12
- Tkinter (for file browsing, fallback to manual entry if unavailable)


#### Disclaimer: This readme was reformatted using AI. I provided the first draft and then summarized and cleaned it up using AI.
---