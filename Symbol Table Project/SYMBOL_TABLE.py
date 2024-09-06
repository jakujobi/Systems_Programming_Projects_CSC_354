import sys

class SymbolData:
    """
    Represents a single symbol entry in the table.
    Attributes:
        symbol: A string representing the symbol (first 4 chars, uppercase).
        value: An integer value between -5000 and 5000.
        rflag: A boolean indicating the relocation flag.
        iflag: Always true, indicates the symbol was defined.
        mflag: A boolean indicating if the symbol was duplicated.
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
        else:
            self._insert(self.root, symbol_data)
    
    def _insert(self, current_node, symbol_data):
        """
        Recursively inserts the symbol_data into the BST.
        """
        if symbol_data.symbol == current_node.symbol_data.symbol:
            # Handle duplicate: Set MFlag to true
            current_node.symbol_data.mflag = True
        elif symbol_data.symbol < current_node.symbol_data.symbol:
            # Insert into left subtree
            if current_node.left is None:
                current_node.left = SymbolNode(symbol_data)
            else:
                self._insert(current_node.left, symbol_data)
        else:
            # Insert into right subtree
            if current_node.right is None:
                current_node.right = SymbolNode(symbol_data)
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
    
    def remove_symbol(self, symbol):
        """
        Remove a symbol from the BST.
        """
        self.root = self._remove(self.root, symbol.upper()[:4])
    
    def _remove(self, node, symbol):
        """
        Recursive removal of a symbol from the BST.
        """
        if node is None:
            return None
        if symbol < node.symbol_data.symbol:
            node.left = self._remove(node.left, symbol)
        elif symbol > node.symbol_data.symbol:
            node.right = self._remove(node.right, symbol)
        else:
            # Node to be removed found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Node with two children
                temp_node = self.find_min(node.right)
                node.symbol_data = temp_node.symbol_data
                node.right = self._remove(node.right, temp_node.symbol_data.symbol)
        return node
    
    def find_min(self, node):
        """
        Find the minimum value node in the subtree.
        """
        while node.left is not None:
            node = node.left
        return node
    
    def destroy_symbol_table(self):
        """
        Set the root to None to destroy the tree.
        """
        self.root = None


class FileExplorer:
    """
    Handles opening, reading, and processing files.
    """
    def open_SYSM_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                return file.readlines()  # Read all lines at once
        except FileNotFoundError:
            print("Error: File not found.")
        except PermissionError:
            print("Error: Permission denied.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None
    
    def read_SYSM(self, file):
        """
        Reads the SYMS.DAT file line by line.
        """
        lines = []
        for line in file:
            cleaned_line = self.read_line_from_file(line)
            if cleaned_line:
                lines.append(cleaned_line)
        return lines

    def read_search_file(self, file):
        """
        Reads the search file line by line.
        """
        lines = []
        for line in file:
            cleaned_line = self.read_line_from_file(line)
            if cleaned_line:
                lines.append(cleaned_line)
        return lines

    def get_search_file_from_command(self, args):
        """
        Get file name from command line or prompt the user.
        """
        if len(args) > 1:
            return args[1]
        else:
            return input("Enter the search file name: ")

    def get_search_file_from_system(self):
        """
        Mock function to open a system file explorer (not implemented).
        """
        file_path = input("Enter the file path: ")
        return file_path

    def read_line_from_file(self, line):
        """
        Cleans and processes a single line from the file.
        """
        line = line.strip()
        if not line or line.startswith("//"):
            return None
        return line


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
