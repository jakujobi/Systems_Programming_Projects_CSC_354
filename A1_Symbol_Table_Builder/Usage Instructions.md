# Usage Instructions

1. **Running the Program**:

   - Simply run `SYMBOL_TABLE.py` to start the program. It will prompt you to process `SYMS.DAT` and `SEARCH.TXT` files.
   - If files are found in the script's directory, the program will ask if you'd like to use them.
2. **Key Operations**:

   - **Insert**: Adds symbols from `SYMS.DAT` to the symbol table, while checking for duplicates and invalid data.
   - **Search**: Searches symbols from `SEARCH.TXT`, with feedback on found or not-found symbols.
   - **Display**: Shows the entire symbol table in a paginated format.
3. **Example File Formats**:

   - **SYMS.DAT**:
     ```
     ABCD_1: 100 true
     XYZ_12:  -45 false
     ```
   - **SEARCH.TXT**:
     ```
     ABCD
     XYZ
     ```
4. **Error Handling**:

   - Invalid lines from `SYMS.DAT` (e.g., invalid symbols or values) are skipped, and errors are logged for review.
   - Symbols not found in the search will be listed in the results.
