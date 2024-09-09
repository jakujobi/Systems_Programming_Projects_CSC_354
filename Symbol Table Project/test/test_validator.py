from SYMBOL_TABLE import FileExplorer, Validator, SymbolData

def display_valid_symbols(valid_symbols):
    """
    Display the valid symbols in a tabular format.
    """
    print("\nDisplaying valid symbols...")
    print(f"{'Symbol':<10}{'Value':<10}{'RFlag':<10}")
    print("-" * 30)
    for symbol_data in valid_symbols:
        print(f"{symbol_data.symbol:<10}{symbol_data.value:<10}{str(symbol_data.rflag):<10}")

def main():
    # Create instances of FileExplorer and Validator
    print("Initializing FileExplorer and Validator...")
    file_explorer = FileExplorer()
    validator = Validator()
    
    # Step 1: Process the SYMS.DAT file
    file_name = "SYMS.DAT"
    print(f"\nStep 1: Processing file '{file_name}'...")
    lines = file_explorer.process_file(file_name)
    
    if not lines:
        print(f"Error: Could not process {file_name}. Exiting program.")
        return
    else:
        print(f"Successfully processed file '{file_name}'. {len(lines)} lines found.")

    valid_symbols = []  # List to store valid SymbolData objects
    
    # Step 2: Validate each line from SYMS.DAT
    print(f"\nStep 2: Validating {len(lines)} lines...")
    for index, line in enumerate(lines, start=1):
        print(f"Validating line {index}: '{line}'")
        symbol_data = validator.validate_syms_line(line)
        if isinstance(symbol_data, SymbolData):
            print(f"Line {index} is valid. Adding to valid symbols.")
            valid_symbols.append(symbol_data)
        else:
            print(f"Line {index} is invalid. Error: {symbol_data}")
    
    # Step 3: Display valid symbols
    if valid_symbols:
        print(f"\nStep 3: Displaying {len(valid_symbols)} valid symbols from SYMS.DAT:")
        display_valid_symbols(valid_symbols)
    else:
        print("No valid symbols found.")

if __name__ == "__main__":
    main()
