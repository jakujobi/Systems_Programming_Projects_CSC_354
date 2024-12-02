## CSC 354 - Systems Programming
# Project: Symbol Table Manager
# File: SYMBOL_TABLE.py
# Version 3.0
# Author: John Akujobi
# Date: 9/8/2024
# Description: 

#Symbol_Table_Builder.py

"""
/**************************************************************************************
*** NAME : John Akujobi                                                             ***
*** CLASS : CSc 354 - Systems Programming                                           ***
*** Program : Symbol_Table_Builder                                                  ***
***************************************************************************************
*** DESCRIPTION :                                                                   ***
*** This program is a symbol table manager that reads symbols from a SYMS.DAT file, ***
***    inserts them into a binary search tree,                                      ***
***     and searches for symbols in the tree using a SEARCH.TXT file.               ***
*** The program uses a FileExplorer class to handle file operations,                ***
***     a Validator class to validate symbols, values, and RFlag,                   ***
***     and a SymbolTable class to manage the binary search tree.                   ***
*** The SymbolData class represents a symbol entry,                                 ***
***     and the SymbolNode class represents a node in the binary search tree.       ***
***     The SymbolTableDriver class manages the high-level logic                    ***
***          for file processingsymbol table management.                            ***
*** The program also includes a GUI file explorer using Tkinter for selecting files.***
*** The main function initializes and runs the SymbolTableDriver.                   ***
**************************************************************************************/
"""



import sys
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.FileExplorer import FileExplorer
from Modules.ErrorLogHandler import ErrorLogHandler

# Try to import Tkinter for GUI file explorer. If not available, fallback to manual entry.
try:
    import tkinter as tk
    from tkinter import filedialog
    tkinter_available = True
except ImportError:
    tkinter_available = False


class SymbolData:
    """
    /********************************************************************
    ***  CLASS  : SymbolData                                            ***
    ***  INSTRUCTOR : George Hamer                                      ***
    ***  ASSIGNMENT : Assignment 1 - Symbol Table Manager               ***
    ***  DUE DATE : September 18, 2024                                  ***
    *********************************************************************
    ***  DESCRIPTION : This class represents a single symbol entry      ***
    ***  in the symbol table. It stores the symbol's name, value,       ***
    ***  relocation flag, and additional flags for duplication and      ***
    ***  immutability.                                                  ***
    ***                                                                 ***
    ***  Key attributes:                                                ***
    ***    - symbol (str): The symbol's name (max 4 chars, uppercase).  ***
    ***    - value (int): The value of the symbol (-5000 to 5000).      ***
    ***    - rflag (bool): Boolean indicating if relocation is allowed. ***
    ***    - iflag (bool): Always true, indicating immutability.        ***
    ***    - mflag (bool): Boolean indicating if the symbol is          ***
    ***      duplicated.                                                ***
    ********************************************************************/
    """
    
    def __init__(self, symbol, value, rflag, iflag=True, mflag=False, address=None):
        """
        /********************************************************************
        ***  FUNCTION : __init__                                            ***
        ***  CLASS  : SymbolData                                            ***
        *********************************************************************
        ***  DESCRIPTION : Constructor for the SymbolData class. It         ***
        ***  initializes the symbol, value, and various flags (rflag,       ***
        ***  iflag, mflag). The symbol is truncated to 4 uppercase          ***
        ***  characters. The iflag defaults to True and mflag to False.     ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol (str): The symbol's name.                           ***
        ***    - value (int): A signed integer between -5000 and 5000.      ***
        ***    - rflag (bool): A boolean indicating the relocation flag.    ***
        ***    - iflag (bool, optional): Defaults to True.                  ***
        ***    - mflag (bool, optional): Defaults to False.                 ***
        ********************************************************************/
        """
        self.symbol: str = symbol.upper()[:4]  # Only first 4 characters, uppercase
        self.value: int = value
        self.rflag: bool = rflag
        self.iflag: bool = iflag
        self.mflag: bool = mflag
        if address is not None:
            self.address = address
        else:
            self.address: int = None


class SymbolNode:
    """
    /********************************************************************
    ***  CLASS  : SymbolNode                                            ***
    ***  INSTRUCTOR : George Hamer                                      ***
    ***  ASSIGNMENT : Assignment 1 - Symbol Table Manager               ***
    ***  DUE DATE : September 18, 2024                                  ***
    *********************************************************************
    ***  DESCRIPTION : This class represents a node in a Binary         ***
    ***  Search Tree (BST), storing a SymbolData object. Each node      ***
    ***  also has references to its left and right child nodes,         ***
    ***  which will hold other SymbolNode objects in the tree.          ***
    ***                                                                 ***
    ***  Key attributes:                                                ***
    ***    - symbol_data (SymbolData): Contains the symbol's data.      ***
    ***    - left (SymbolNode): Left child node, initialized to None.   ***
    ***    - right (SymbolNode): Right child node, initialized to None. ***
    ********************************************************************/
    """
    # Represents a node in the Binary Search Tree, storing a SymbolData object.
    def __init__(self, symbol_data: SymbolData):
        """
        /********************************************************************
        ***  FUNCTION : __init__                                            ***
        ***  CLASS  : SymbolNode                                            ***
        *********************************************************************
        ***  DESCRIPTION : Constructor for the SymbolNode class. It         ***
        ***  initializes the node with a SymbolData object and sets the     ***
        ***  left and right child nodes to None, indicating that the node   ***
        ***  has no children when created.                                  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol_data (SymbolData): The symbol's data.               ***
        ********************************************************************/
        """
        if not isinstance(symbol_data, SymbolData):
            raise TypeError("symbol_data must be an instance of SymbolData")
        self.symbol_data: SymbolData = symbol_data  # SymbolData object containing symbol info
        self.left = None  # Left child node
        self.right = None  # Right child node


class SymbolTable:
    """
    /********************************************************************
    ***  CLASS  : SymbolTable                                           ***
    ***  INSTRUCTOR : George Hamer                                      ***
    ***  ASSIGNMENT : Assignment 1 - Symbol Table Manager               ***
    ***  DUE DATE : September 18, 2024                                  ***
    *********************************************************************
    ***  DESCRIPTION : This class implements a Binary Search Tree       ***
    ***  (BST) for managing symbols in a symbol table. It provides      ***
    ***  methods to insert, search, view, remove, and destroy symbols.  ***
    ********************************************************************/
    """

    def __init__(self, logger=None):
        """
        /********************************************************************
        ***  FUNCTION : __init__                                            ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Initializes the SymbolTable class by setting     ***
        ***  the root of the tree to None, representing an empty symbol     ***
        ***  table.                                                         ***
        ********************************************************************/
        """
        self.root = None
        self.logger = logger or ErrorLogHandler()
        self.str_header = (f"{'Symbol':<10} {'Value':<10} {'RFlag':<6} {'IFlag':<6} {'MFlag':<6}")
    
    def __str__(self):
        """
        /********************************************************************
        ***  FUNCTION : __str__                                             ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Returns a string representation of the symbol    ***
        ***  table, displaying all symbols in sorted order.                 ***
        ********************************************************************/
        """
        if self.root is None:
            return "Symbol table is empty."
        
        divider = "_" * 46
        symbols = []
        self._collect_symbols(self.root, symbols)
        result = [f"\n{divider}\nSymbol Table:\n{divider}"]
        result.append(self.str_header)
        result.append(f"{divider}")
    
        
        for sym in symbols:
            hex_address = format(sym.value, '05X') if sym.value is not None else "None"
            result.append(f"{sym.symbol:<10} {hex_address:<10} {int(sym.rflag):<6} {int(sym.iflag):<6} {int(sym.mflag):<6}")
        
        result.append(f"{divider}\n")
        return "\n".join(result)

    def _collect_symbols(self, node, symbols):
        """
        /********************************************************************
        ***  FUNCTION : _collect_symbols                                    ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Helper method to collect all symbols in the      ***
        ***  binary search tree using in-order traversal.                   ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - node (SymbolNode): Current node in the tree.               ***
        ***    - symbols (list): List to collect symbols.                   ***
        ********************************************************************/
        """
        if node is not None:
            self._collect_symbols(node.left, symbols)
            symbols.append(node.symbol_data)
            self._collect_symbols(node.right, symbols)
        

    def insert(self, symbol_data):
        """
        /********************************************************************
        ***  FUNCTION : insert                                              ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Inserts a new symbol into the binary search      ***
        ***  tree. If the tree is empty, the symbol becomes the root.       ***
        ***  Otherwise, the _insert method is called to place the symbol    ***
        ***  in the correct position.                                       ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol_data (SymbolData): The symbol to be inserted.       ***
        ********************************************************************/
        """
        if not isinstance(symbol_data, SymbolData):
            _error = "Expected a SymbolData object."
            self.logger.log_error(_error)
            raise TypeError(_error)

        if self.root is None:
            self.root = SymbolNode(symbol_data)
            self.logger.log_action(f"New symbol table created. Symbol '{symbol_data.symbol}' inserted.", False)
        else:
            self._insert(self.root, symbol_data)

    
    def _insert(self, current_node, symbol_data):
        """
        /********************************************************************
        ***  FUNCTION : _insert                                             ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Recursively inserts symbol_data into the BST.    ***
        ***  If the symbol already exists, sets the mflag to True,          ***
        ***  indicating a duplicate. Otherwise, places the symbol in the    ***
        ***  appropriate left or right subtree.                             ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - current_node (SymbolNode): Current node in the tree.       ***
        ***    - symbol_data (SymbolData): Symbol data to be inserted.      ***
        ********************************************************************/
        """
        # Set MFlag to true if there's a duplicate
        if symbol_data.symbol == current_node.symbol_data.symbol:
            current_node.symbol_data.mflag = True
            self.logger.log_action(f"Duplicate symbol '{symbol_data.symbol}' found. MFlag set to True.", False)
        # Insert into left subtree
        elif symbol_data.symbol < current_node.symbol_data.symbol:
            if current_node.left is None:
                current_node.left = SymbolNode(symbol_data)
                self.logger.log_action(f"Symbol '{symbol_data.symbol}' inserted.", False)
            else:
                self._insert(current_node.left, symbol_data)
        # Insert into right subtree
        else:
            if current_node.right is None:
                current_node.right = SymbolNode(symbol_data)
                self.logger.log_action(f"Symbol '{symbol_data.symbol}' inserted.", False)
            else:
                self._insert(current_node.right, symbol_data)
    
    def insert_or_update(self, symbol_data):
        """
        Inserts a new symbol or updates an existing symbol's value.
        """
        existing_symbol = self.search(symbol_data.symbol)
        if existing_symbol:
            existing_symbol.value = symbol_data.value
            existing_symbol.rflag = symbol_data.rflag
            existing_symbol.iflag = symbol_data.iflag
            existing_symbol.mflag = symbol_data.mflag
        else:
            self.insert(symbol_data)


    # def get(self, operand):
    #     # Symbol lookup from the symbol table
    #     symbol = self.search(operand)  # Search the table for the symbol
    #     if symbol:
    #         return symbol.value, symbol.rflag, None
    #     else:
    #         return None, None, f"Undefined symbol: {operand}"
        
    def get(self, operand):
        is_immediate = operand.startswith('#')
        is_indirect = operand.startswith('@')
        is_indexed = operand.endswith(',X')

        base_operand = operand.strip('#@,X')  # Remove addressing symbols
        symbol = self.search(base_operand)

        if symbol:
            value = symbol.value
            if is_indexed:
                value += 0x8000  # Example: Set indexed addressing flag in object code
            return value, symbol.rflag, None
        else:
            return None, None, f"Undefined symbol: {operand}"


    def search(self, symbol):
        """
        /********************************************************************
        ***  FUNCTION : search                                              ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Searches for a symbol in the BST by calling      ***
        ***  the _search method and returns the SymbolData if found.        ***
        ***  If not found, prints a message indicating the symbol's absence.***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol (str): The symbol to search for (4 chars max).      ***
        ***  RETURNS :                                                      ***
        ***    - (SymbolData or None): Returns the symbol data if found.    ***
        ********************************************************************/
        """
        result = self._search(self.root, symbol.upper()[:4])
        if result is None:
            self.logger.log_action(f"Symbol '{symbol.upper()[:4]}' not found.", False)
            return None
        return result
        # return {'value': result.value, 'rflag': result.rflag}

    
    def _search(self, current_node, symbol):
        """
        /********************************************************************
        ***  FUNCTION : _search                                             ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Recursively searches the binary search tree      ***
        ***  for a specific symbol. If found, returns the corresponding     ***
        ***  SymbolData object; otherwise, returns None.                    ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - current_node (SymbolNode): The current node in the tree.   ***
        ***    - symbol (str): The symbol to search for (4 chars max).      ***
        ***  RETURNS :                                                      ***
        ***    - (SymbolData or None): The symbol data if found, or None.   ***
        ********************************************************************/
        """
        if current_node is None:
            return None  # Symbol not found
        if symbol == current_node.symbol_data.symbol:
            self.logger.log_action(f"Symbol '{symbol}' found in symbol table.", False)
            return current_node.symbol_data
        elif symbol < current_node.symbol_data.symbol:
            return self._search(current_node.left, symbol)
        else:
            return self._search(current_node.right, symbol)

    def view(self):
        """
        /********************************************************************
        ***  FUNCTION : view                                                ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Displays all symbols in the BST in sorted order  ***
        ***  using an in-order traversal. The method pauses every 20 lines  ***
        ***  to prevent scrolling past entries.                             ***
        ********************************************************************/
        """
        if self.root is None:
            print("No symbols in the table.")
            return
        print("┏" + ("━" * 47) + "┓")
        print(f"┃ {'Symbols currently in symbol table':<46}┃")
        print("┣" + ("━" * 47) + "┫")
        # print("┏" + ("━" * 11) + "┯" + ("━" * 11) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┓")
        print("┣" + ("━" * 11) + "┯" + ("━" * 11) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┫")
        print(f"┃ {'Symbol':<10}│ {'Value':<10}│ {'RFlag':<6}│ {'IFlag':<6}│ {'MFlag':<6}┃")
        print("┣" + ("━" * 11) + "┿" + ("━" * 11) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┫")
        self.inorder_traversal(self.root, counter=0)
        print("┗" + ("━" * 11) + "┷" + ("━" * 11) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┛") # end of table

    def pressContinue(self):
        """
        /********************************************************************
        ***  FUNCTION : pressContinue                                       ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Pauses the program and waits for the user to     ***
        ***  press Enter before continuing execution. This is used to       ***
        ***  prevent the program from printing too many lines at once.      ***
        ********************************************************************/
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')

    def inorder_traversal(self, node, counter):
        """
        /********************************************************************
        ***  FUNCTION : inorder_traversal                                   ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Performs an in-order traversal of the BST,       ***
        ***  printing symbols in sorted order. Pauses after every 20 lines  ***
        ***  to prompt user input.                                          ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - node (SymbolNode): Current node in the tree.               ***
        ***    - counter (int): Line counter to track when to pause.        ***
        ********************************************************************/
        """
        if node is not None:
            counter = self.inorder_traversal(node.left, counter)
            print(f"┃ {node.symbol_data.symbol:<10}│ {node.symbol_data.value:<10}│ "
                  f"{int(node.symbol_data.rflag):<6}│ {int(node.symbol_data.iflag):<6}│ "
                  f"{int(node.symbol_data.mflag):<6}┃")
            counter += 1
            if counter % 20 == 0:
                self.pressContinue()  # Pause after every 20 symbols
            counter = self.inorder_traversal(node.right, counter)
        return counter
    
    def remove_symbol(self, symbol):
        """
        /********************************************************************
        ***  FUNCTION : remove_symbol                                       ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Removes a symbol from the binary search tree.    ***
        ***  If the symbol does not exist in the tree, a message is         ***
        ***  printed. Calls the _remove method internally.                  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol (str): The symbol to be removed.                    ***
        ********************************************************************/
        """
        if self.root is None:
            self.logger.log_error("Symbol table is empty.")
            return
        
        self.root, removed = self._remove(self.root, symbol.upper()[:4])
        if removed:
            self.logger.log_action(f"Symbol '{symbol.upper()[:4]}' removed.", False)
        else:
            print(f"Symbol '{symbol.upper()[:4]}' not found.")
            self.logger.log_error(f"Symbol '{symbol.upper()[:4]}' not found.")


    def _remove(self, node, symbol):
        """
        /********************************************************************
        ***  FUNCTION : _remove                                             ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Recursively removes a symbol from the BST.       ***
        ***  Handles cases with no children, one child, or two children,    ***
        ***  replacing nodes as necessary.                                  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - node (SymbolNode): Current node in the tree.               ***
        ***    - symbol (str): The symbol to remove (4 chars max).          ***
        ***  RETURNS :                                                      ***
        ***    - (SymbolNode, bool): Updated node and whether symbol        ***
        ***      was removed.                                               ***
        ********************************************************************/
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
        /********************************************************************
        ***  FUNCTION : destroy                                             ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Destroys the symbol table by setting the root    ***
        ***  to None, effectively removing all symbols from the tree.       ***
        ********************************************************************/
        """
        if self.root is None:
            self.logger.log_error("Symbol table is already empty.")
        else:
            self._destroy()
            self.logger.log_action("Symbol Table Destroyed.", False)
            
    def _destroy(self):
        """
        /********************************************************************
        ***  FUNCTION : _destroy                                            ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Recursively destroys the symbol table by         ***
        ***  traversing through all nodes and deleting them. Sets the       ***
        ***  root of the tree to None when completed.                       ***
        ********************************************************************/
        """
        if self.root is not None:
            self._destroy_nodes(self.root)
            self.root = None
            
    def _destroy_nodes(self, node):
        """
        /********************************************************************
        ***  FUNCTION : _destroy_nodes                                      ***
        ***  CLASS  : SymbolTable                                           ***
        *********************************************************************
        ***  DESCRIPTION : Recursively deletes all nodes in the tree.       ***
        ***  Used as part of the table destruction process.                 ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - node (SymbolNode): The current node being destroyed.       ***
        ********************************************************************/
        """
        if node is not None:
            self._destroy_nodes(node.left)
            self._destroy_nodes(node.right)
            del node



class Validator:
    """
    /********************************************************************
    ***  CLASS  : Validator                                             ***
    *********************************************************************
    ***  DESCRIPTION : This class contains methods to validate symbols, ***
    ***  values, and RFlag for different conditions according to the    ***
    ***  project's requirements.                                        ***
    ********************************************************************/
    """
    
    
    
    def validate_symbol(self, symbol):
        """
        /********************************************************************
        ***  FUNCTION : validate_symbol                                     ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a symbol based on the following rules: ***
        ***  - Must be at most 10 characters.                               ***
        ***  - Must start with a letter.                                    ***
        ***  - Cannot be just an underscore.                                ***
        ***  - Can contain only letters, digits, and underscores.           ***
        ********************************************************************/
        """
        symbol = symbol.strip().rstrip(":").upper()

        # Check if the symbol length exceeds 10 characters
        if len(symbol) > 10:
            # self.logger.log_error(f"Symbol '{symbol}' length exceeds 10 characters.")
            return f"Error: Symbol '{symbol}' length exceeds 10 characters."
        
        # Check if the symbol starts with a letter
        if not symbol[0].isalpha():
            # self.logger.log_error(f"Symbol '{symbol}' must start with a letter.")
            return f"Error: Symbol '{symbol}' must start with a letter."

        # Check if the entire symbol is "_"
        if symbol == "_":
            # self.logger.log_error("Symbol cannot be an underscore ('_') only.")
            return "Error: Symbol cannot be an underscore ('_') only."

        # Check for invalid characters
        for char in symbol:
            if not (char.isalnum() or char == "_"):
                # self.logger.log_error(f"Symbol '{symbol}' contains invalid character '{char}'.")
                return f"Error: Symbol '{symbol}' contains invalid character '{char}'."
        
        return "Success"
    

    def validate_value(self, value):
        """
        /********************************************************************
        ***  FUNCTION : validate_value                                      ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a value based on the following rules:  ***
        ***  - Must be an integer.                                          ***
        ***  - Must be between -5000 and 5000.                              ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - value (str): The value to be validated.                    ***
        ***  RETURNS :                                                      ***
        ***    - str: "Success" if valid, otherwise an error message.       ***
        ********************************************************************/
        """
        value = value.strip()
        try:
            value = int(value)
        except ValueError:
            return f"Error: Value '{value}' must be an integer."
        
        if -5000 <= value <= 5000:
            return "Success"
        else:
            return f"Error: Value '{value}' must be an integer between -5000 and 5000."
    
    def validate_rflag(self, rflag):
        """
        /********************************************************************
        ***  FUNCTION : validate_rflag                                      ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates the RFlag, ensuring it is either       ***
        ***  'true' or 'false'.                                             ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - rflag (str): The RFlag to be validated.                    ***
        ***  RETURNS :                                                      ***
        ***    - str: "Success" if valid, otherwise an error message.       ***
        ********************************************************************/
        """
        rflag = rflag.strip().lower()
        if rflag in ["true", "false"]:
            return "Success"
        return f"Error: RFlag '{rflag}' must be 'true' or 'false'."
    
    def convert_symbol(self, symbol):
        """
        /********************************************************************
        ***  FUNCTION : convert_symbol                                      ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Converts the symbol to uppercase and truncates   ***
        ***  it to the first 4 characters.                                  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol (str): The symbol to be converted.                  ***
        ***  RETURNS :                                                      ***
        ***    - str: The converted symbol.                                 ***
        ********************************************************************/
        """
        return symbol.strip().rstrip(":").upper()[:4]

    def validate_syms_line(self, line):
        """
        /********************************************************************
        ***  FUNCTION : validate_syms_line                                  ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a line from the SYMS.DAT file, which   ***
        ***  must contain exactly three parts: symbol, value, and rflag.    ***
        ***  Returns a SymbolData object if valid, or an error message if   ***
        ***  invalid.                                                       ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - line (str): The line from SYMS.DAT to be validated.        ***
        ***  RETURNS :                                                      ***
        ***    - SymbolData or str: The validated SymbolData object or an   ***
        ***      error message if invalid.                                  ***
        ********************************************************************/
        """
        parts = line.split(maxsplit=2)
        if len(parts) != 3:
            return f"Error: SYMS.DAT line '{line}' must contain symbol, value, and rflag."
        
        symbol, value, rflag = parts
        
        symbol_validation = self.validate_symbol(symbol)
        value_validation = self.validate_value(value)
        rflag_validation = self.validate_rflag(rflag)
        
        if symbol_validation == "Success" and value_validation == "Success" and rflag_validation == "Success":
            converted_symbol = self.convert_symbol(symbol)
            rflag_bool = rflag.lower() == "true"
            return SymbolData(converted_symbol, int(value), rflag_bool)
        
        if symbol_validation != "Success":
            return f"{symbol_validation} in line: '{line}'"
        if value_validation != "Success":
            return f"{value_validation} in line: '{line}'"
        if rflag_validation != "Success":
            return f"{rflag_validation} in line: '{line}'"

    def validate_search_line(self, line):
        """
        /********************************************************************
        ***  FUNCTION : validate_search_line                                ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a line from the search file, which     ***
        ***  should contain only a symbol. Returns the processed symbol     ***
        ***  (converted, uppercase, truncated) if valid, or an error        ***
        ***  message if invalid.                                            ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - line (str): The line from the search file to be validated. ***
        ***  RETURNS :                                                      ***
        ***    - str: The validated symbol or an error message.             ***
        ********************************************************************/
        """
        parts = line.split()

        if len(parts) != 1:
            return f"Error: Search file line '{line}' must contain only a symbol."
        
        symbol = parts[0].strip()

        symbol_validation = self.validate_symbol(symbol)
        
        if symbol_validation == "Success":
            converted_symbol = self.convert_symbol(symbol)
            return converted_symbol
        else:
            return f"{symbol_validation} in line: '{line}'"


class SymbolTableDriver:
    """
    /**********************************************************************
    ***  CLASS  : SymbolTableDriver                                     ***
    ***********************************************************************
    ***  DESCRIPTION : Manages the high-level logic for file processing ***
    ***  and symbol table management. Handles inserting symbols from    ***
    ***  SYMS.DAT into a symbol table and searching for symbols.        ***
    ********************************************************************/
    """
    def __init__(self, logger=None, file_explorer=None, validator=None, symbol_table=None):
        """
        /********************************************************************
        ***  FUNCTION : __init__                                            ***
        ***  CLASS  : SymbolTableDriver                                     ***
        *********************************************************************
        ***  DESCRIPTION : Initializes the SymbolTableDriver class,         ***
        ***  setting up the symbol table, file explorer, and validator      ***
        ***  components.                                                    ***
        ********************************************************************/
        """
        self.symbol_table = symbol_table or SymbolTable()
        self.file_explorer = file_explorer or FileExplorer()
        self.validator = validator or Validator()
        self.logger = logger or ErrorLogHandler()


    def process_syms_file(self, file_path):
        """
        /**********************************************************************
        ***  FUNCTION : process_syms_file                                   ***
        ***  CLASS  : SymbolTableDriver                                     ***
        ***********************************************************************
        ***  DESCRIPTION : Processes the SYMS.DAT file, validating symbols  ***
        ***  and inserting valid symbols into the symbol table. Prints      ***
        ***  a summary of valid and invalid lines processed.                ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - file_path (str): The path to the SYMS.DAT file.            ***
        **********************************************************************/
        """
        try:
            print(f"\nProcessing SYMS.DAT for symbol insertion...\n")
            lines = self.file_explorer.process_file("SYMS.DAT")
            if lines is None:
                print(f"Error: Unable to read {file_path}.")
                return

            valid_count = 0
            invalid_count = 0

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

            print(f"\nSummary:")
            print(f"- {valid_count} valid symbols inserted")
            print(f"- {invalid_count} invalid lines encountered")
        
        except Exception as e:
            print(f"An error occurred while processing the SYMS file: {e}")


    def process_search_file(self, file_path):
        """
        /********************************************************************
        ***  FUNCTION : process_search_file                                 ***
        ***  CLASS  : SymbolTableDriver                                     ***
        *********************************************************************
        ***  DESCRIPTION : Processes the search file and searches for each  ***
        ***  symbol in the symbol table. Displays found symbols in a        ***
        ***  paginated table format and lists symbols not found.            ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - file_path (str): The path to the search file.              ***
        ********************************************************************/
        """
        try:
            print(f"Processing {file_path} for symbol search...")
            lines = self.file_explorer.process_file(file_path)
            if lines is None:
                print(f"Error: Unable to read {file_path}.")
                return

            found_symbols = []
            not_found_symbols = []

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

            if found_symbols:
                self.display_symbols_paginated(found_symbols)
            else:
                print("No symbols were found in the search.")

            if not_found_symbols:
                print(f"\nSymbols not found: {', '.join(not_found_symbols)}")
        except FileNotFoundError as fnf_error:
            print(f"Error: {file_path} not found: {fnf_error}")
    
        except Exception as e:
            print(f"An error occurred while processing the search file: {e}")

            

    def display_symbols_paginated(self, symbols):
        """
        /********************************************************************
        ***  FUNCTION : display_symbols_paginated                           ***
        ***  CLASS  : SymbolTableDriver                                     ***
        *********************************************************************
        ***  DESCRIPTION : Displays the given symbols in a table format     ***
        ***  with pagination, pausing every 20 lines to prevent scrolling.  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbols (list): List of SymbolData objects to display.     ***
        ********************************************************************/
        """
        print("\n\n")
        print("┏" + ("━" * 47) + "┓")
        print(f"┃ {'Displaying found symbols':<46}┫")
        print("┣" + ("━" * 47) + "┫")
        # print("┏" + ("━" * 11) + "┯" + ("━" * 11) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┓")
        print("┣" + ("━" * 11) + "┯" + ("━" * 11) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┫")
        print(f"┃ {'Symbol':<10}│ {'Value':<10}│ {'RFlag':<6}│ {'IFlag':<6}│ {'MFlag':<6}┃")
        print("┣" + ("━" * 11) + "┿" + ("━" * 11) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┫")
        
        counter = 0
        for sym in symbols:
            print(f"┃ {sym.symbol:<10}│ {sym.value:<10}│ {int(sym.rflag):<6}│ {int(sym.iflag):<6}│ {int(sym.mflag):<6}┃")
            counter += 1
            if counter % 20 == 0:
                self.symbol_table.pressContinue()

        print("┗" + ("━" * 11) + "┷" + ("━" * 11) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┛") # end of table


    def view(self):
        """
        /********************************************************************
        ***  FUNCTION : view                                                ***
        ***  CLASS  : SymbolTableDriver                                     ***
        *********************************************************************
        ***  DESCRIPTION : Displays the contents of the symbol table in     ***
        ***  sorted order using an in-order traversal.                      ***
        ********************************************************************/
        """
        try:
            if self.symbol_table.root is None:
                print("The symbol table is empty.")
            else:
                print("-" * 35)
                print("\n\nDisplaying symbol table:")
                print("-" * 35)
                self.symbol_table.view()
                print("-" * 35)
        except Exception as e:
            print(f"An error occurred while displaying the symbol table: {e}")


    def run(self, search_file=None):
        """
        /*********************************************************************
        ***  FUNCTION : run                                                ***
        ***  CLASS  : SymbolTableDriver                                    ***
        **********************************************************************
        ***  DESCRIPTION : Main method to run the program, which processes ***
        ***  the SYMS.DAT file and optionally asks the user for the search  ***
        ***  file if not provided as an argument. Also asks if the user     ***
        ***  wants to view the symbol table after processing SYMS.DAT.      ***
        ********************************************************************/
        """
        try:
            print("\nProcessing SYMS.DAT file...")
            print("_" * 50)                
            self.process_syms_file("SYMS.DAT")
        except FileNotFoundError as fnf_error:
            print(f"Error: SYMS.DAT file not found: {fnf_error}")
            return
        except Exception as e:
            print(f"An unexpected error occurred while processing SYMS.DAT: {e}")
            return

        try:
            while True:
                print("\n")
                user_choice = input("Do you want to view the current symbol table? (y/n): ").strip().lower()
                if user_choice == 'y':
                    self.view()
                    print("\n")
                    break
                elif user_choice == 'n':
                    print("Continuing without viewing the symbol table.")
                    break
                else:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        except Exception as e:
            print(f"Error in user input: {e}")
            return

        try:
            # Check if search_file was provided as an argument
            if not search_file:
                print("\nPlease provide the search file name (e.g., SEARCH.TXT) if it is in the same directory as the script:")
                search_file = input("Search file name: ").strip()

            print(f"\nProcessing {search_file} file...")
            print("_" * 50)
            self.process_search_file(search_file)
            print("\n")
        except FileNotFoundError as fnf_error:
            print(f"Error: {search_file} not found: {fnf_error}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {search_file}: {e}")


    def build_symbol_table(self):
        """
        /*********************************************************************
        ***  FUNCTION : run                                                ***
        ***  CLASS  : SymbolTableDriver                                    ***
        **********************************************************************
        ***  DESCRIPTION : Main method to run the program, which processes ***
        ***  the SYMS.DAT file and optionally asks the user for the search  ***
        ***  file if not provided as an argument. Also asks if the user     ***
        ***  wants to view the symbol table after processing SYMS.DAT.      ***
        ********************************************************************/
        """
        self.symbol_table = SymbolTable()
        try:
            print("\nProcessing SYMS.DAT file...")
            print("_" * 50)                
            self.process_syms_file("SymbolTableTest.DAT")
        except FileNotFoundError as fnf_error:
            print(f"Error: SYMS.DAT file not found: {fnf_error}")
            return
        except Exception as e:
            print(f"An unexpected error occurred while processing SYMS.DAT: {e}")
            return

        try:
            while True:
                print("\n")
                user_choice = input("Do you want to view the current symbol table? (y/n): ").strip().lower()
                if user_choice == 'y' or user_choice == "":
                    self.view()
                    print("\n")
                    break
                elif user_choice == 'n':
                    print("Continuing without viewing the symbol table.")
                    break
                else:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        except Exception as e:
            print(f"Error in user input: {e}")
            return

# def main():
#     """
#     /********************************************************************
#     ***  FUNCTION : main                                              ***
#     ***  CLASS  :                                                     ***
#     *********************************************************************
#     ***  DESCRIPTION: Main function that initializes and runs the app ***
#     ***  with optional command-line arguments. If a search file is     ***
#     ***  provided as a command-line argument, it is used; otherwise,   ***
#     ***  the program asks for the search file name interactively.      ***
#     ********************************************************************/
#     """
#     try:
#         print("Welcome to the Symbol Table Manager!\n")
#         driver = SymbolTableDriver()

#         # Check if the user provided a command-line argument for the search file
#         if len(sys.argv) > 1:
#             search_file = sys.argv[1]  # First argument is the search file
#             driver.run(search_file)
#         else:
#             # If no argument provided, fallback to interactive file finding
#             driver.run()
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     main()