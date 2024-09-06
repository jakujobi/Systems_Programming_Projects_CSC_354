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


