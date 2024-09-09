import sys

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
    Takes care of anything to do with files
     - Opens, Reads files
     - Checks for default locations, prompt for paths, or use a system file explorer.
    """
    
    # ------------------- SYMS File Operations -------------------
    def find_syms_file(self):
        """
        Checks if SYMS.DAT exists in the current working directory.
        If not found, prompts the user for input or to use file explorer.
        Returns the valid file path to SYMS.DAT.
        """
        default_path = os.path.join(os.getcwd(), "SYMS.DAT")  # Default directory (same as script)
        
        # Check if SYMS.DAT exists in the current directory
        if os.path.isfile(default_path):
            print(f"Found SYMS.DAT in current directory: {default_path}")
            return default_path

        # If not found, present a menu to the user
        print("SYMS.DAT file not found in the current directory.")
        return self.prompt_for_file()

    def prompt_for_file(self):
        """
        Prompt the user for either typing the file path or using the system file explorer.
        Validates the input and returns a valid file path.
        """
        while True:
            print("\nFinding Menu:")
            print("1. Type the SYMS file path manually.")
            print("2. Use the system file explorer to locate the SYMS file.")
            choice = input("Choose an option (1 or 2): ").strip()

            if choice == "1":
                # Ask the user to type the path manually
                file_path = input("Enter the full path to SYMS.DAT: ").strip()
                if self.validate_file(file_path):
                    return file_path
                else:
                    print("Error: Invalid file path. Please try again.")
            
            elif choice == "2":
                # Use the system file explorer (mock function for now)
                try:
                    file_path = self.get_file_from_system()
                    if os.path.isfile(file_path):
                        return file_path
                    else:
                        print("Error: Invalid file path. Please try again.")
                except Exception as e:
                    print(f"Unexpected Error: Prompt_for_file {e} @ prompt_for_file")
            else:
                print("Invalid choice. Please select 1 or 2.")
                
        def open_SYSM_file(self, file_path):
        """
        Attempts to open SYMS.DAT for reading and returns the content.
        """
        try:
            with open(file_path, "r") as file:
                return file.readlines()  # Read all lines at once
        except FileNotFoundError:
            print("Error: File not found. @ open_SYSM_file")
        except PermissionError:
            print("Error: Permission denied. @ open_SYSM_file")
        except Exception as e:
            print(f"An unexpected error occurred: {e} @ open_SYSM_file")
        return None
    
    def read_SYSM(self, file):
        """
        Read SYMS.DAT line by line, clean the lines, and return the list.
        """
        lines = [] # List to store cleaned lines
        for line in file:
            cleaned_line = self.read_line_from_file(line)
            if cleaned_line:
                lines.append(cleaned_line)
        return lines

    # def validate_file(self, file_path):
    #     """
    #     Validates if the file path exists and points to a valid file.
    #     """
    #     return os.path.isfile(file_path)

    def get_file_from_system(self):
        """
        This uses the system file explorer to get the file path.
        """
        return input("Enter the full path to SYMS.DAT using file explorer: ").strip()


    # ------------------- Search File Operations -------------------


    def read_search_file(self, file):
        """
        Read the search file line by line, clean the lines, and return the list.
        """
        lines = []
        for line in file:
            cleaned_line = self.read_line_from_file(line)
            if cleaned_line:
                lines.append(cleaned_line)
        return lines


class Validator:
    """
    Contains methods to validate symbols, values, and RFlag.
    """
    def validate_symbol(self, symbol):
        """
        Validate the symbol based on project requirements.
        """
        if len(symbol) > 10:
            return "Error: Symbol length exceeds 10 characters."
        if not symbol[0].isalpha():
            return "Error: Symbol must start with a letter."
        if not symbol.replace("_", "").isalnum():
            return "Error: Symbol contains invalid characters."
        return "Success"

    def validate_value(self, value):
        """
        Validate the value (integer between -5000 and 5000).
        """
        if isinstance(value, int) and -5000 <= value <= 5000:
            return "Success"
        else:
            return "Error: Value must be an integer between -5000 and 5000."
    
    def validate_rflag(self, rflag):
        """
        Validate the RFlag, ensuring it's a boolean or convertable to boolean.
        """
        if isinstance(rflag, bool):
            return "Success"
        if isinstance(rflag, str):
            rflag = rflag.lower()
            if rflag == "true":
                return "Success"
            elif rflag == "false":
                return "Success"
        return "Error: RFlag must be 'true' or 'false'."
    
    def validate_syms_line(self, line):
        """
        Validate a line from the SYMS.DAT file.
        """
        parts = line.split()
        if len(parts) != 3:
            return "Error: SYMS.DAT line must contain symbol, value, and rflag."
        symbol, value, rflag = parts
        symbol_validation = self.validate_symbol(symbol)
        value_validation = self.validate_value(int(value))
        rflag_validation = self.validate_rflag(rflag)
        if symbol_validation == "Success" and value_validation == "Success" and rflag_validation == "Success":
            return SymbolData(symbol, int(value), rflag.lower() == "true")
        return "Error in line validation"

    def validate_search_line(self, line):
        """
        Validate a line from the search file (only a symbol).
        """
        parts = line.split()
        if len(parts) != 1:
            return "Error: Search file line must contain only a symbol."
        symbol = parts[0]
        return self.validate_symbol(symbol)


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
        lines = self.file_explorer.open_SYSM_file(file_path)
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
        lines = self.file_explorer.open_SYSM_file(file_path)
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
