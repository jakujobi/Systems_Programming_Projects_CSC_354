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
        if self.root is None:
            self.root = SymbolNode(symbol_data)
            print ("New Symbol Table Created, Symbol Inserted")
        else:
            self._insert(self.root, symbol_data)
    
    def _insert(self, current_node, symbol_data):
        """
        Recursively inserts the symbol_data into the BST.
        """
        # Set MFlag to true if there's a duplicate
        if symbol_data.symbol == current_node.symbol_data.symbol:
            current_node.symbol_data.mflag = True
        elif symbol_data.symbol < current_node.symbol_data.symbol:
            # Insert into left subtree
            if current_node.left is None:
                current_node.left = SymbolNode(symbol_data)
                print ("Symbol Inserted")
            else:
                self._insert(current_node.left, symbol_data)
        else:
            # Insert into right subtree
            if current_node.right is None:
                current_node.right = SymbolNode(symbol_data)
                print ("Symbol Inserted")
            else:
                self._insert(current_node.right, symbol_data)

    def search(self, symbol):
        """
        Search for a symbol in the binary search tree.
        """
        return self._search(self.root, symbol.upper()[:4])
    
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
    
    # def remove_symbol(self, symbol):
    #     """
    #     Remove a symbol from the BST. Added this feature just in case
    #     """
    #     self.root = self._remove(self.root, symbol.upper()[:4])
    
    # def _remove(self, node, symbol):
    #     """
    #     Recursive removal of a symbol from the BST.
    #     """
    #     if node is None:
    #         return None
    #     if symbol < node.symbol_data.symbol:
    #         node.left = self._remove(node.left, symbol)
    #     elif symbol > node.symbol_data.symbol:
    #         node.right = self._remove(node.right, symbol)
    #     else:
    #         # Node to be removed found
    #         if node.left is None:
    #             return node.right
    #         elif node.right is None:
    #             return node.left
    #         else:
    #             # Node with two children
    #             temp_node = self.find_min(node.right)
    #             node.symbol_data = temp_node.symbol_data
    #             node.right = self._remove(node.right, temp_node.symbol_data.symbol)
    #     return node
    
    
    def destroy_symbol_table(self):
        """
        Set the root to None to destroy the tree.
        """
        self.root = None
        print ("Symbol Table Destroyed")


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
        Checks if the specified file exists in the current working directory.
        If not found, prompts the user for input or to use the system file explorer.
        Returns the valid file path to the file.
        """
        default_path = os.path.join(os.getcwd(), file_name)  # Default directory (same as script)
        
        # Check if the file exists in the current directory
        if os.path.isfile(default_path):
            print(f"Found {file_name} in the current directory: {default_path}")
            return default_path

        # If not found, prompt the user for a file path
        print(f"{file_name} file not found in the current directory.")
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



class SymbolTableLogic:
    """
    Manages the high-level logic for file processing and symbol table management.
    """
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.file_explorer = FileExplorer()
        self.validator = Validator()

    def process_syms_file(self, file_path):
        """
        Process SYMS.DAT file and insert valid symbols into the symbol table.
        """
        lines = self.file_explorer.open_file(file_path)
        for line in lines:
            validation_result = self.validator.validate_syms_line(line)
            if isinstance(validation_result, SymbolData):
                self.symbol_table.insert(validation_result)
            else:
                print(validation_result)  # Print error message

    def process_search_file(self, file_path):
        """
        Process search file and search symbols in the symbol table.
        """
        lines = self.file_explorer.open_file(file_path)
        for line in lines:
            symbol = line.strip().upper()[:4]
            result = self.symbol_table.search(symbol)
            if result:
                print(f"Found: {result.symbol}, Value: {result.value}, RFlag: {result.rflag}")
            else:
                print(f"Error: {symbol} not found")

    def display_symbol_table(self):
        """
        Display the symbol table in order.
        """
        self.symbol_table.view()

def main():
    """
    Main program logic to handle command-line arguments and process files.
    """
    manager = SymbolTableLogic()

    # Process SYMS.DAT file
    if len(sys.argv) < 2:
        syms_file = input("Enter the SYMS.DAT file path: ")
    else:
        syms_file = sys.argv[1]
    manager.process_syms_file(syms_file)

    # Process search file
    if len(sys.argv) < 3:
        search_file = input("Enter the search file path: ")
    else:
        search_file = sys.argv[2]
    manager.process_search_file(search_file)

    # Display the symbol table
    manager.display_symbol_table()

if __name__ == "__main__":
    main()
