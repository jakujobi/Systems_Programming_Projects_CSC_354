from SYMBOL_TABLE import FileExplorer, Validator, SymbolData

def display_valid_symbols(symbols_list, title):
    """
    Display the valid symbols in a tabular format.
    """
    print(f"\n{title}")
    if len(symbols_list) == 0:
        print("No valid symbols found.")
        return

    print(f"{'Symbol':<10}{'Value':<10}{'RFlag':<10}")
    print("-" * 30)
    for symbol_data in symbols_list:
        if isinstance(symbol_data, SymbolData):
            print(f"{symbol_data.symbol:<10}{symbol_data.value:<10}{str(symbol_data.rflag):<10}")
        else:  # If it's a plain symbol (search results)
            print(f"{symbol_data:<10}")

def main():
    # Create instances of FileExplorer and Validator
    print("Initializing FileExplorer and Validator...")
    file_explorer = FileExplorer()
    validator = Validator()
    
    # Step 1: Process the SYMS.DAT file
    file_name_syms = "SYMS.DAT"
    print(f"\nStep 1: Processing file '{file_name_syms}'...")
    lines_syms = file_explorer.process_file(file_name_syms)
    
    if not lines_syms:
        print(f"Error: Could not process {file_name_syms}. Exiting program.")
        return

    valid_syms = []  # List to store valid SymbolData objects
    
    # Validate each line from SYMS.DAT
    print(f"\nStep 2: Validating {len(lines_syms)} lines from SYMS.DAT...")
    for index, line in enumerate(lines_syms, start=1):
        symbol_data = validator.validate_syms_line(line)
        if isinstance(symbol_data, SymbolData):
            valid_syms.append(symbol_data)
        else:
            print(f"Line {index} is invalid. Error: {symbol_data}")
    
    # Display valid symbols from SYMS.DAT
    display_valid_symbols(valid_syms, "Valid Symbols from SYMS.DAT:")
    
    # Step 3: Process the search file
    file_name_search = "SEARCH.DAT"  # Assuming the search file is named SEARCH.DAT
    print(f"\nStep 3: Processing file '{file_name_search}'...")
    lines_search = file_explorer.process_file(file_name_search)
    
    if not lines_search:
        print(f"Error: Could not process {file_name_search}. Exiting program.")
        return
    
    search_symbols = []  # List to store validated symbols from the search file
    
    # Validate each line from the search file
    print(f"\nStep 4: Validating {len(lines_search)} lines from SEARCH.DAT...")
    for index, line in enumerate(lines_search, start=1):
        symbol = validator.validate_search_line(line)
        if "Error" not in symbol:
            search_symbols.append(symbol)  # Add cleaned and converted symbol
        else:
            print(f"Line {index} is invalid. Error: {symbol}")
    
    # Display valid symbols from the search file
    display_valid_symbols(search_symbols, "Valid Symbols from SEARCH.DAT:")
    
    # Step 5: Compare and display symbols found in both SYMS.DAT and SEARCH.DAT
    valid_syms_set = {sym.symbol for sym in valid_syms}  # Extract valid symbols from SYMS.DAT
    matched_symbols = [sym for sym in search_symbols if sym in valid_syms_set]
    
    if matched_symbols:
        print(f"\nStep 5: Symbols found in both SYMS.DAT and SEARCH.DAT:")
        display_valid_symbols(matched_symbols, "Matching Symbols:")
    else:
        print("\nNo matching symbols found between SYMS.DAT and SEARCH.DAT.")

if __name__ == "__main__":
    main()