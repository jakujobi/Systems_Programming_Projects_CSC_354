## CSC 354 - Systems Programming
# Project: Symbol Table Manager
# File: SYMBOL_TABLE.py

# Author: John Akujobi
# Date: 9/8/2024
# Description: This program is a symbol table manager that reads symbols from a SYMS.DAT file, inserts them into a binary search tree, and searches for symbols in the tree using a SEARCH.TXT file. The program uses a FileExplorer class to handle file operations, a Validator class to validate symbols, values, and RFlag, and a SymbolTable class to manage the binary search tree. The SymbolData class represents a symbol entry, and the SymbolNode class represents a node in the binary search tree. The SymbolTableDriver class manages the high-level logic for file processing and symbol table management. The program also includes a GUI file explorer using Tkinter for selecting files. The main function initializes and runs the SymbolTableDriver.

import sys
import os

# Try to import Tkinter for GUI file explorer. If not available, fallback to manual entry.
try:
    import tkinter as tk
    from tkinter import filedialog
    tkinter_available = True
except ImportError:
    tkinter_available = False

class SymbolData:
    """
    Represents a single symbol entry in the table.
    Attributes:
        symbol: string of the symbol (first 4 chars, uppercase).
        value: Signed integer between -5000 and 5000.
        rflag: Boolean for the relocation flag.
        iflag: Always true.
        mflag: Bboolean indicating if the symbol was duplicated.
    """
    def __init__(self, symbol, value, rflag, iflag=True, mflag=False):
        self.symbol = symbol.upper()[:4]  # Only first 4 characters, uppercase
        self.value = value
        self.rflag = rflag
        self.iflag = iflag
        self.mflag = mflag


class SymbolNode:
    """
    Represents a node in the Binary Search Tree, storing a SymbolData object.
    """
    def __init__(self, symbol_data):
        self.symbol_data = symbol_data  # SymbolData object containing symbol info
        self.left = None  # Left child node
        self.right = None  # Right child node


class SymbolTable:
    """
    Binary Search Tree implementation for managing symbols.
    Methods include insert, search, view, remove, and destroy.
    """
    def __init__(self):
        self.root = None
    
    def insert(self, symbol_data):
        """
        Insert symbol into the binary search tree, calls internal _insert.
        """
        if not isinstance(symbol_data, SymbolData):
            raise TypeError("Expected a SymbolData object.")
            
        if self.root is None:
            self.root = SymbolNode(symbol_data)
            print("New Symbol Table Created, Symbol Inserted")
        else:
            self._insert(self.root, symbol_data)

    
    def _insert(self, current_node, symbol_data):
        """
        Recursively inserts the symbol_data into the BST.
        """
        # Set MFlag to true if there's a duplicate
        if symbol_data.symbol == current_node.symbol_data.symbol:
            current_node.symbol_data.mflag = True
            print("Duplicate symbol found. MFlag set to True.")
        # Insert into left subtree
        elif symbol_data.symbol < current_node.symbol_data.symbol:
            if current_node.left is None:
                current_node.left = SymbolNode(symbol_data)
                print ("Symbol Inserted")
            else:
                self._insert(current_node.left, symbol_data)
        # Insert into right subtree
        else:
            if current_node.right is None:
                current_node.right = SymbolNode(symbol_data)
                print ("Symbol Inserted")
            else:
                self._insert(current_node.right, symbol_data)

    def search(self, symbol):
        """
        Search for a symbol in the binary search tree and return it.
        """
        result = self._search(self.root, symbol.upper()[:4])
        if result is None:
            print(f"Symbol '{symbol.upper()[:4]}' not found.")
        return result

    
    def _search(self, current_node, symbol):
        """
        Recursive search for the symbol.
        """
        if current_node is None:
            return None  # Symbol not found
        if symbol == current_node.symbol_data.symbol:
            print ("Symbol Found")
            return current_node.symbol_data
        elif symbol < current_node.symbol_data.symbol:
            return self._search(current_node.left, symbol)
        else:
            return self._search(current_node.right, symbol)

    def view(self):
        """
        Perform an in-order traversal to display symbols.
        Pauses every 20 lines.
        """
        if self.root is None:
            print("No symbols in the table.")
            return
        
        print(f"{'Symbol':<10} {'Value':<5} {'RFlag':<5} {'IFlag':<5} {'MFlag':<5}")
        print("-" * 35)
        self.inorder_traversal(self.root, counter=0)


    def inorder_traversal(self, node, counter):
        """
        Recursive in-order traversal to print symbols in sorted order.
        Pauses every 20 lines to prevent scrolling.
        """
        if node is not None:
            counter = self.inorder_traversal(node.left, counter)
            print(f"{node.symbol_data.symbol:<10} {node.symbol_data.value:<5} "
                  f"{int(node.symbol_data.rflag):<5} {int(node.symbol_data.iflag):<5} "
                  f"{int(node.symbol_data.mflag):<5}")
            counter += 1
            if counter % 20 == 0:
                input("Press Enter to continue...")
            counter = self.inorder_traversal(node.right, counter)
        return counter
    
    def remove_symbol(self, symbol):
        """
        Remove a symbol from the BST and notify if it doesn't exist.
        """
        if self.root is None:
            print("Symbol table is empty.")
            return
        
        self.root, removed = self._remove(self.root, symbol.upper()[:4])
        if removed:
            print(f"Symbol '{symbol.upper()[:4]}' removed.")
        else:
            print(f"Symbol '{symbol.upper()[:4]}' not found.")


    def _remove(self, node, symbol):
        """
        Recursive removal of a symbol from the BST.
        Returns the updated node and whether the symbol was removed.
        """
        if node is None:
            return None, False
        if symbol < node.symbol_data.symbol:
            node.left, removed = self._remove(node.left, symbol)
        elif symbol > node.symbol_data.symbol:
            node.right, removed = self._remove(node.right, symbol)
        else:
            # Node to be removed found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                # Node with two children
                temp_node = self.find_min(node.right)
                node.symbol_data = temp_node.symbol_data
                node.right, _ = self._remove(node.right, temp_node.symbol_data.symbol)
            return node, True
        return node, removed
        
    def destroy(self):
        """
        Destroy the symbol table by setting the root to None.
        """
        if self.root is None:
            print("Symbol table is already empty.")
        else:
            self._destroy()
            print("Symbol Table Destroyed")
            
    def _destroy(self):
        """
        Recursive destruction of the symbol table.
        """
        if self.root is not None:
            self._destroy_nodes(self.root)
            self.root = None
            
    def _destroy_nodes(self, node):
        """
        Recursive destruction of nodes.
        """
        if node is not None:
            self._destroy_nodes(node.left)
            self._destroy_nodes(node.right)
            del node


class FileExplorer:
    """
    Takes care of anything to do with files:
     - Opens, reads files line by line.
     - Checks for default locations, prompts for paths, or uses a system file explorer.
    """
    
    def process_file(self, file_name):
        """
        Process the file by finding it, opening it, and reading it line by line.
        Returns a list of cleaned lines from the file or None if errors occur.
        """
        file_path = self.find_file(file_name)
        if file_path is None:
            print(f"Error: Could not find the file '{file_name}'.")
            return None

        file_generator = self.open_file(file_path)  # Get generator from open_file
        if file_generator is None:
            print(f"Error: Could not open the file '{file_name}'.")
            return None
        
        return self.read_file(file_generator)

    
    def find_file(self, file_name):
        """
        Checks if the specified file exists in the same directory as the script.
        Prompts the user to use the file found, or proceed to manually input the file path or use the system file explorer.
        Returns the valid file path to the file.
        """
        # Get the directory where the script is running from
        script_directory = os.path.dirname(os.path.realpath(__file__))
        default_path = os.path.join(script_directory, file_name)  # Search in the script's directory
        
        # Check if the file exists in the script's directory
        if os.path.isfile(default_path):
            print(f"\nFound {file_name} in the script directory ({script_directory}).")
            use_found_file = input(f"Do you want to use this {file_name}? (y/n): ").strip().lower()

            if use_found_file == "y" or use_found_file == "":
                print(f"Using {file_name} from script directory ({script_directory}).")
                return default_path  # Use the file found in the script directory

        # If the file is not found or user says 'no', proceed to manually find it
        return self.prompt_for_file(file_name)


    def prompt_for_file(self, file_name):
        """
        Prompt the user for either typing the file path or using the system file explorer.
        Validates the input and returns a valid file path.
        """
        while True:
            print("\nFinding Menu:")
            print(f"1. Type the {file_name} file path manually.")
            if tkinter_available:
                print(f"2. Use your system file explorer to locate the {file_name} file.")
            
            choice = input("Choose an option (1 or 2): ").strip()

            if choice == "1":
                # Manually type the file path
                file_path = input(f"Enter the full path to {file_name}: ").strip()
                if os.path.isfile(file_path):
                    return file_path
                else:
                    print(f"Error: Invalid typed file path for {file_name}. Please try again.")
            
            elif choice == "2" and tkinter_available:
                # Use the system file explorer
                try:
                    file_path = self.use_system_explorer()
                    if os.path.isfile(file_path):
                        return file_path
                    else:
                        print(f"Error: Invalid file path for {file_name} from system explorer. Please try again.")
                except Exception as e:
                    print(f"Unexpected Error: {e} @ prompt_for_file")
            else:
                print("Invalid choice. Please select 1 or 2.")

    
    def open_file(self, file_path):
        """
        Opens the file and reads line by line, using a generator to yield each line.
        This approach avoids reading all lines into memory at once.
        """
        try:
            # Specify UTF-8 encoding while opening the file
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    yield line  # Yield line to the caller (used in 'read_file')
        except FileNotFoundError:
            print(f"Error: {file_path} not found. @ open_file")
        except PermissionError:
            print(f"Error: Permission denied for {file_path}. @ open_file")
        except Exception as e:
            print(f"An unexpected error occurred while opening {file_path}: {e} @ open_file")

    def read_file(self, file):
        """
        Reads file line by line, cleans the lines, and returns the list of cleaned lines.
        Uses the open_file generator to process each line lazily.
        """
        lines = []  # List to store cleaned lines
        for line in file:  # The file here is a generator, so we can iterate over it
            cleaned_line = self.read_line_from_file(line)
            if cleaned_line:
                lines.append(cleaned_line)
        
        if not lines:
            print("Warning: No valid lines found in the file.")
        
        return lines


    def use_system_explorer(self):
        """
        Opens a system file explorer window for the user to select a file using Tkinter.
        Returns the selected file path as a string.
        """
        if not tkinter_available:
            return input("Enter the full path to the file: ").strip()

        # Create a Tkinter root window and hide it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.update()    # Keep the GUI up to date
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*"), ("DAT files", "*.dat"), ("Text files", "*.txt")]
        )
        
        # Destroy the hidden Tkinter window after use
        root.destroy()
        
        return file_path if file_path else None  # Return None if no file is selected

    def read_line_from_file(self, line):
        """
        Cleans and processes a single line from the file.
        - Removes leading/trailing spaces.
        - Removes anything after '//' (including the '//' itself).
        - Skips empty lines and comments.
        """
        # Remove everything after '//' if present
        line = line.split("//", 1)[0].strip()  # Split at '//' and take the first part, then strip spaces
        
        if not line:  # Skip empty lines
            return None
        
        return line


class Validator:
    """
    Contains methods to validate symbols, values, and RFlag.
    """
    
    def validate_symbol(self, symbol):
        """
        Validate the symbol based on project requirements.
        - Must be at most 10 characters.
        - Must start with a letter.
        - Must contain only letters, digits, and underscores.
        """
        # Strip colons (:) and spaces, and convert to uppercase for consistency
        symbol = symbol.strip().rstrip(":").upper()

        # Check if the symbol length exceeds 10 characters
        if len(symbol) > 10:
            return f"Error: Symbol '{symbol}' length exceeds 10 characters."
        
        # Check if the first character is a letter
        if not symbol[0].isalpha():
            return f"Error: Symbol '{symbol}' must start with a letter."

        # Check if the symbol contains only letters, digits, or underscores
        for char in symbol:
            if not (char.isalnum() or char == "_"):
                return f"Error: Symbol '{symbol}' contains invalid character '{char}'."
        
        return "Success"

    def validate_value(self, value):
        """
        Validate the value:
        - Must be an integer.
        - Must be between -5000 and 5000.
        """
        value = value.strip()  # Strip spaces
        try:
            # Allow values like +45 and -45 to be processed as integers
            value = int(value)  # Attempt to convert to integer
        except ValueError:
            return f"Error: Value '{value}' must be an integer."
        
        if -5000 <= value <= 5000:
            return "Success"
        else:
            return f"Error: Value '{value}' must be an integer between -5000 and 5000."
    
    def validate_rflag(self, rflag):
        """
        Validate the RFlag, ensuring it's a boolean or convertible to boolean.
        """
        rflag = rflag.strip().lower()  # Strip spaces and convert to lowercase
        if rflag in ["true", "false"]:
            return "Success"
        return f"Error: RFlag '{rflag}' must be 'true' or 'false'."
    
    def convert_symbol(self, symbol):
        """
        Convert the symbol to uppercase and truncate it to the first 4 characters.
        """
        return symbol.strip().rstrip(":").upper()[:4]  # Strip spaces and colons, convert to uppercase, truncate

    def validate_syms_line(self, line):
        """
        Validate a line from the SYMS.DAT file.
        Line must contain exactly three parts: symbol, value, and rflag.
        Returns a SymbolData object if valid, or an error message if invalid.
        """
        # Split line by spaces but ensure there are exactly 3 parts (symbol, value, rflag)
        parts = line.split(maxsplit=2)
        if len(parts) != 3:
            return f"Error: SYMS.DAT line '{line}' must contain symbol, value, and rflag."
        
        symbol, value, rflag = parts
        
        # Validate each part after stripping spaces
        symbol_validation = self.validate_symbol(symbol)
        value_validation = self.validate_value(value)
        rflag_validation = self.validate_rflag(rflag)
        
        # If all validations pass, convert the symbol and return a SymbolData object
        if symbol_validation == "Success" and value_validation == "Success" and rflag_validation == "Success":
            converted_symbol = self.convert_symbol(symbol)
            rflag_bool = rflag.lower() == "true"  # Convert rflag to boolean based on the string value
            return SymbolData(converted_symbol, int(value), rflag_bool)
        
        # Otherwise, return an error message indicating the first failure
        if symbol_validation != "Success":
            return f"{symbol_validation} in line: '{line}'"
        if value_validation != "Success":
            return f"{value_validation} in line: '{line}'"
        if rflag_validation != "Success":
            return f"{rflag_validation} in line: '{line}'"


    def validate_search_line(self, line):
        """
        Validate a line from the search file, which should contain only a symbol.
        Returns the processed symbol (converted, uppercase, truncated) if valid, 
        or an error message if invalid.
        """
        parts = line.split()

        if len(parts) != 1:
            return f"Error: Search file line '{line}' must contain only a symbol."
        
        symbol = parts[0].strip()  # Strip any surrounding spaces

        # Validate the symbol using the same logic as SYMS.DAT validation
        symbol_validation = self.validate_symbol(symbol)
        
        if symbol_validation == "Success":
            # If valid, convert the symbol to uppercase and truncate it
            converted_symbol = self.convert_symbol(symbol)
            return converted_symbol  # Return the processed symbol
        else:
            # Return the error message if the symbol is invalid
            return f"{symbol_validation} in line: '{line}'"


class SymbolTableDriver:
    """
    Manages the high-level logic for file processing and symbol table management.
    Handles inserting symbols from SYMS.DAT into a symbol table and searching for symbols.
    """
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.file_explorer = FileExplorer()
        self.validator = Validator()


    def process_syms_file(self, file_path):
        """
        Process SYMS.DAT file, validate symbols, and insert valid symbols into the symbol table.
        """
        try:
            print(f"\nProcessing SYMS.DAT for symbol insertion...\n")
            lines = self.file_explorer.process_file("SYMS.DAT")
            if lines is None:
                print(f"Error: Unable to read {file_path}.")
                return

            valid_count = 0 # Number of valid symbols inserted
            invalid_count = 0   # Number of invalid lines encountered

            # Process each line from the file
            for line_num, line in enumerate(lines, start=1):
                validation_result = self.validator.validate_syms_line(line)
                if isinstance(validation_result, SymbolData):
                    self.symbol_table.insert(validation_result)
                    valid_count += 1
                    print(f"- Symbol '{validation_result.symbol}' Inserted")
                else:
                    print(f"\nError in Line {line_num}: '{line}'")
                    print(f"  Reason: {validation_result}")
                    invalid_count += 1

            # Summary
            print(f"\nSummary:")
            print(f"- {valid_count} valid symbols inserted")
            print(f"- {invalid_count} invalid lines encountered")
        
        except Exception as e:
            print(f"An error occurred while processing the SYMS file: {e}")


    def process_search_file(self, file_path):
        """
        Process the search file and look for each symbol in the symbol table.
        Display found symbols in a paginated table format.
        """
        try:
            print(f"Processing {file_path} for symbol search...")
            lines = self.file_explorer.process_file(file_path)
            if lines is None:
                print(f"Error: Unable to read {file_path}.")
                return

            found_symbols = []
            not_found_symbols = []

            # Search for each symbol from the search file
            for line in lines:
                validation_result = self.validator.validate_search_line(line)
                if "Error" not in validation_result:
                    symbol = validation_result
                    result = self.symbol_table.search(symbol)
                    if result:
                        found_symbols.append(result)
                    else:
                        not_found_symbols.append(symbol)
                else:
                    print(f"Invalid search line: {validation_result}")

            # Display found symbols in a paginated table format
            if found_symbols:
                self.display_symbols_paginated(found_symbols)
            else:
                print("No symbols were found in the search.")

            # Display not found symbols
            if not_found_symbols:
                print(f"\nSymbols not found: {', '.join(not_found_symbols)}")
            
        except Exception as e:
            print(f"An error occurred while processing the search file: {e}")

            
    def display_symbols_paginated(self, symbols):
        """
        Display the given symbols in a table format with pagination.
        Pauses every 20 lines to prevent output scrolling.
        """
        print("\n\n")
        print("-" * 35)  # Table header
        print("Displaying found symbols:")
        print("-" * 35)  # Table header
        print(f"{'Symbol':<10} {'Value':<5} {'RFlag':<5} {'IFlag':<5} {'MFlag':<5}")
        print("-" * 35)
        
        counter = 0
        for sym in symbols:
            print(f"{sym.symbol:<10} {sym.value:<5} {int(sym.rflag):<5} {int(sym.iflag):<5} {int(sym.mflag):<5}")
            counter += 1
            if counter % 20 == 0:
                input("Press Enter to continue...")  # Pause after every 20 symbols

        print("-" * 35)  # End of the table

    def view(self):
        """
        Display the contents of the symbol table in-order.
        """
        try:
            if self.symbol_table.root is None:
                print("The symbol table is empty.")
            else:
                print("-" * 35)  # Table header
                print("\n\nDisplaying symbol table:")
                print("-" * 35)  # Table header
                self.symbol_table.view()
                print("-" * 35)  # Table header
        except Exception as e:
            print(f"An error occurred while displaying the symbol table: {e}")

    def run(self):
        """
        Main method to run the program. Asks the user to process SYMS.DAT and a search file.
        """
        try:
            # Step 1: Process SYMS.DAT file
            print("\nProcessing SYMS.DAT file...")
            print("_" * 50)                
            self.process_syms_file("SYMS.DAT")
                
            #Step 2: Display the contents of the symbol table
            self.view()
            print("\n")

            # Step 3: Process the search file
            print("\nProcessing SEARCH.TXT file...")
            print("_" * 50)
            self.process_search_file("SEARCH.TXT")
            print("\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        

def main():
    """
    The main function that initializes and runs the SymbolTableDriver.
    """
    print("Welcome to the Symbol Table Manager!\n")
    driver = SymbolTableDriver()
    driver.run()

if __name__ == "__main__":
    main()