## CSC 354 - Systems Programming
# Project: Literal table Builder
# File: johnA2.py

# Author: John Akujobi
# Date: 10/3/2024
# Description: 

# Literal_Table_Builder.py

"""
/******************************************************************************************
***                                                                                     ***
***  CSc 354 - Systems Programming                                                      ***
***  ASSIGNMENT : A2 - Literal Table and Expression Evaluator                           ***
***  INSTRUCTOR : George Hamer                                                          ***
***  DUE DATE : October 9, 2024                                                         ***
***                                                                                     ***
*******************************************************************************************
***  PROGRAM NAME : Literal Table and Expression Evaluator                              ***
***                                                                                     ***
***  DESCRIPTION :                                                                      ***
***      This program is designed to build a literal table and evaluate assembly        ***
***      language expressions as part of a SIC/XE assembler. It processes assembly      ***
***      language expressions, evaluates their operands, and manages literals in a      ***
***      linked list-based literal table. The program supports various addressing       ***
***      modes (direct, indirect, and immediate) and arithmetic operations              ***
***      (addition and subtraction) for a maximum of two operands per expression.       ***
***                                                                                     ***
***      The program performs the following tasks:                                      ***
***         - Reads symbols from a symbol table (SYMS.DAT)                              ***
***         - Parses expressions from an input file (EXPR.DAT or provided via CLI)      ***
***         - Evaluates the parsed expressions                                          ***
***         - Manages the literal table with insertion and updates                      ***
***         - Outputs the evaluation results, including relocatability flags            ***
***         - Displays detailed error messages for invalid expressions                  ***
***         - Handles paginated display for both expression results and literal table   ***
***                                                                                     ***
*******************************************************************************************
***  MODULES INCLUDED :                                                                 ***
***                                                                                     ***
***      - LiteralData : Represents a literal with its name, value, length, and         ***
***                     address.                                                        ***
***      - LiteralNode : Represents a node in the linked list containing literal data.  ***
***      - LiteralTableList : Manages the literal table using a linked list. Supports   ***
***                          insertion, searching, address updates, and display.        ***
***      - ErrorLogHandler : Handles logging of actions and errors, with support for    ***
***                          pagination of logs and errors.                             ***
***      - ExpressionParser : Responsible for parsing assembly expressions,             ***
***                          identifying literals, and validating operands.             ***
***      - ExpressionEvaluator : Evaluates parsed expressions and handles operand       ***
***                              calculations and relocatability.                       ***
***      - ExpressionResults : Formats and outputs evaluated expression results,        ***
***                            including the N-bit, I-bit, and X-bit flags.             ***
***      - LiteralTableDriver : Coordinates the overall flow of the program,            ***
***                            including building the symbol table, parsing and         ***
***                            evaluating expressions, and displaying results.          ***
***                                                                                     ***
*******************************************************************************************
***  INPUTS :                                                                           ***
***      - SYMS.DAT : Contains symbols and their attributes (symbol, value, rflag).     ***
***      - EXPR.DAT : File containing assembly language expressions (can be provided    ***
***                   via command line as an argument or defaults to EXPR.DAT).         ***
***                                                                                     ***
*******************************************************************************************
***  OUTPUTS :                                                                          ***
***      - Evaluated expression results with value, relocatability, N-bit, I-bit,       ***
***        and X-bit information displayed.                                             ***
***      - Literal table displayed with literal name, value, length, and address.       ***
***      - Error logs and action logs displayed with detailed error information.        ***
***                                                                                     ***
*******************************************************************************************
***  ERROR HANDLING :                                                                   ***
***      The program provides detailed error messages for various invalid operations,   ***
***      including unsupported symbols, invalid literals, and undefined symbols. It     ***
***      continues processing despite errors, logging them for user reference.          ***
***                                                                                     ***
******************************************************************************************/

"""


# run 
# cd .\Systems_Programming_Projects_CSC_354\A2_Literal_Table; python johnA2.py Express.DAT

import sys
import os
from typing import List

# Add the parent directory to the Python path
repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.Symbol_Table_Builder import SymbolTableDriver, FileExplorer
from Modules.ErrorLogHandler import ErrorLogHandler



class LiteralData:
    """
    /***************************************************************************************
    ***  CLASS NAME : LiteralData                                                        ***
    ***  DESCRIPTION :                                                                   ***
    ***      This class represents a literal with attributes such as its name, value,    ***
    ***      length, and address. It stores hexadecimal literals and their associated    ***
    ***      data.                                                                       ***
    ***************************************************************************************/

    Class to represent a literal with its name, value, length, and address.
    """


    def __init__(self, name: str, value: str, length: int, address: int = None):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes a LiteralData object with its name, hexadecimal value, length   ***
        ***      in bytes, and sets the address to None initially.                           ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name   : str    : Name of the literal (e.g., '=X'05A'')                     ***
        ***      value  : str    : Hexadecimal value of the literal                          ***
        ***      length : int    : Length of the literal in bytes                            ***
        ***                                                                                  ***
        ***  EXCEPTIONS :                                                                    ***
        ***      Raises ValueError if the name is missing, value is empty, or length is      ***
        ***      invalid.                                                                    ***
        ***************************************************************************************/

        Initialize a literal with its name, value, length, and address.
        :param name: Name of the literal (e.g., '=X'05A'').
        :param value: Hexadecimal value of the literal.
        :param length: Length of the literal in bytes.
        :raises ValueError: If name, value, or length is invalid.
        """
        # if not name or not value or length <= 0:
        if not name or not value or not length:
            raise ValueError("Invalid literal data: ensure the name is provided, value is not empty, and length is positive.")
        
        self.name: str = name
        self.value: str = value.upper()  # Normalize value
        self.length: int = length
        self.address: int = address or None



class LiteralNode:
    """
    /***************************************************************************************
    ***  CLASS NAME : LiteralNode                                                        ***
    ***  DESCRIPTION :                                                                   ***
    ***      Represents a node in a linked list, containing literal data and a pointer   ***
    ***      to the next node in the list. Each node stores an instance of LiteralData.  ***
    ***************************************************************************************/

    Class to represent a node in the linked list of literals.
    Each node contains LiteralData and a reference to the next node.
    """

    def __init__(self, literal_data: LiteralData):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes a LiteralNode object with literal data and sets the next        ***
        ***      pointer to None.                                                            ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      literal_data : LiteralData  : An instance of LiteralData to store in the    ***
        ***                      node.                                                       ***
        ***                                                                                  ***
        ***  EXCEPTIONS :                                                                    ***
        ***      Raises TypeError if the literal_data is not an instance of LiteralData.     ***
        ***************************************************************************************/

        Initialize the node with literal data.

        :param literal_data: Instance of LiteralData.
        :raises TypeError: If literal_data is not an instance of LiteralData.
        """
        if not isinstance(literal_data, LiteralData):
            raise TypeError("Expected an instance of LiteralData.")
        
        self.literal_data: LiteralData = literal_data
        self.next: LiteralNode = None



class LiteralTableList:
    """
    /***************************************************************************************
    ***  CLASS NAME : LiteralTableList                                                   ***
    ***  DESCRIPTION :                                                                   ***
    ***      Represents a linked list that stores literal data. Provides methods for     ***
    ***      inserting literals, updating their addresses, and displaying the literal    ***
    ***      table.                                                                      ***
    ***************************************************************************************/

    Class to represent the literal table, stored as a linked list.
    This class provides methods to insert literals, update their addresses,
    and display the literal table.
    """


    def __init__(self, logger):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes the LiteralTableList with an empty linked list and a log        ***
        ***      handler to log actions and errors.                                          ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      logger : ErrorLogHandler  : Object used to handle logging of actions   ***
        ***                      and errors in the table.                                   ***
        ***************************************************************************************/

        Initialize the literal table with an empty linked list and a log handler.

        :param logger: An instance of ErrorLogHandler for logging actions and errors.
        """
        self.head: LiteralNode = None
        self.logger = logger
        self.str_header = (f"{'Literal':<10} {'Value':<10} {'Length':<6} {'Address':<8}")
        
    def __str__(self) -> str:
        """
        /***************************************************************************************
        ***  METHOD : __str__                                                                ***
        ***  DESCRIPTION :                                                                   ***
        ***      Returns a string representation of the literal table.                       ***
        ***                                                                                  ***
        ***  RETURN : str                                                                    ***
        ***      A string representation of the literal table.                               ***
        ***************************************************************************************/
        """

        if self.head is None:
            return "Literal table is empty."
        
        result = ["Literal Table:"]
        result.append(self.str_header)
        
        current = self.head
        while current is not None:
            literal_data = current.literal_data
            # address = f"{literal_data.address:05X}" if literal_data.address is not None else "None"
            address = f"{literal_data.address:05X}" if literal_data.address is not None else "None"
            result.append(f"{literal_data.name:<10} {literal_data.value:<10} {literal_data.length:<6} {address:<8}")
            current = current.next
        
        return "\n".join(result)


    def insert(self, literal_data: LiteralData):
        """
        /***************************************************************************************
        ***  METHOD : insert                                                                 ***
        ***  DESCRIPTION :                                                                   ***
        ***      Inserts a new literal into the linked list if it doesn't already exist.     ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      literal_data : LiteralData  : The LiteralData object to be inserted.        ***
        ***                                                                                  ***
        ***  EXCEPTIONS :                                                                    ***
        ***      Logs an error if the literal is a duplicate or the object is invalid.       ***
        ***************************************************************************************/

        Insert a new literal into the linked list.

        :param literal_data: An instance of LiteralData to be inserted.
        """
        if not isinstance(literal_data, LiteralData):
            self.logger.log_error("Cannot insert: Invalid LiteralData object.")
            return

        if self._find_literal(literal_data.name):
            self.logger.log_error(f"Duplicate literal insertion error: The literal '{literal_data.name}' already exists.")
            return

                    # Check if a literal with the same value already exists
        if self.exists_by_value(literal_data.value, literal_data.name):
            self.logger.log_action(f"Literal '{literal_data.name}' with value '{literal_data.value}' already exists. Skipping insertion.", False)
            return
    
        new_node = LiteralNode(literal_data)
        if self.head is None:
            self.head = new_node
            self.logger.log_action(f"Inserted literal '{literal_data.name}' as head.", False)
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            self.logger.log_action(f"Inserted literal '{literal_data.name}' into the table.", False)


    def exists_by_value(self, value: str, name: str) -> bool:
        """
        /***************************************************************************************
        ***  METHOD : exists_by_value                                                        ***
        ***  DESCRIPTION :                                                                   ***
        ***      Checks if a literal with a specific value and name exists in the list.      ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      value : str  : The hexadecimal value of the literal to check.               ***
        ***      name  : str  : The name of the literal.                                     ***
        ***                                                                                  ***
        ***  RETURN : bool                                                                   ***
        ***      Returns True if a literal with the same value and name exists, otherwise    ***
        ***      False.                                                                      ***
        ***************************************************************************************/
        """
        current = self.head
        while current is not None:
            if current.literal_data.value.upper() == value.upper():
                if current.literal_data.name.upper() == name.upper():
                    return True
            current = current.next
        return False


    def exists_by_value_alone(self, value: str) -> bool:
        current = self.head
        while current is not None:
            if current.literal_data.value.upper() == value.upper():
                return True
            current = current.next
        return False

    def get_literals(self) -> List[LiteralData]:
        """
        Returns a list of all literals in the literal table.

        :return: List of LiteralData objects.
        """
        literals = []
        current = self.head
        while current is not None:
            literals.append(current.literal_data)
            current = current.next
        return literals

    def get_address_for_literal_from_name(self, name: str) -> int | None:
        """
        /***************************************************************************************
        ***  METHOD : get_address_for_literal                                                ***
        ***  DESCRIPTION :                                                                   ***
        ***      Retrieves the address of a literal by its name.                             ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name : str  : The name of the literal to search for.                       ***
        ***                                                                                  ***
        ***  RETURN : int | None                                                             ***
        ***      Returns the address of the literal if found, otherwise None.                ***
        ***************************************************************************************/

        Retrieve the address of a literal by its name.

        :param name: The name of the literal to search for.
        :return: The address of the literal if found, or None if not found.
        """
        return self.search(name).address if self.search(name) else None
    
    def get_value_for_literal_from_name(self, name: str) -> str | None:
        """
        /***************************************************************************************
        ***  METHOD : get_value_for_literal                                                  ***
        ***  DESCRIPTION :                                                                   ***
        ***      Retrieves the value of a literal by its name.                               ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name : str  : The name of the literal to search for.                       ***
        ***                                                                                  ***
        ***  RETURN : str | None                                                             ***
        ***      Returns the value of the literal if found, otherwise None.                  ***
        ***************************************************************************************/

        Retrieve the value of a literal by its name.

        :param name: The name of the literal to search for.
        :return: The value of the literal if found, or None if not found.
        """
        return self.search(name).value if self.search(name) else None
        
    def get_length_for_literal_from_name(self, name: str) -> int | None:
        """
        /***************************************************************************************
        ***  METHOD : get_length_for_literal                                                 ***
        ***  DESCRIPTION :                                                                   ***
        ***      Retrieves the length of a literal by its name.                              ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name : str  : The name of the literal to search for.                       ***
        ***                                                                                  ***
        ***  RETURN : int | None                                                             ***
        ***      Returns the length of the literal if found, otherwise None.                 ***
        ***************************************************************************************/

        Retrieve the length of a literal by its name.

        :param name: The name of the literal to search for.
        :return: The length of the literal if found, or None if not found.
        """
        return self.search(name).length if self.search(name) else None
    
    def get_literal_data_from_name(self, name: str) -> LiteralData | None:
        """
        /***************************************************************************************
        ***  METHOD : get_literal_data_from_name                                             ***
        ***  DESCRIPTION :                                                                   ***
        ***      Retrieves the LiteralData object of a literal by its name.                  ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name : str  : The name of the literal to search for.                       ***
        ***                                                                                  ***
        ***  RETURN : LiteralData | None                                                    ***
        ***      Returns the LiteralData object if found, otherwise None.                    ***
        ***************************************************************************************/

        Retrieve the LiteralData object of a literal by its name.

        :param name: The name of the literal to search for.
        :return: The LiteralData object if found, or None if not found.
        """
        return self.search(name) if self.search(name) else None

    def insert_sorted(self, literal_data: LiteralData):
        """
        /***************************************************************************************
        ***  METHOD : insert_sorted                                                          ***
        ***  DESCRIPTION :                                                                   ***
        ***      Inserts a literal into the linked list in sorted order based on literal     ***
        ***      name.                                                                       ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      literal_data : LiteralData  : LiteralData object to insert into the list.   ***
        ***************************************************************************************/

        Insert a literal into the linked list in sorted order.
        
        :param literal_data: LiteralData object to insert.
        """
        new_node = LiteralNode(literal_data)
        if self.head is None or self.head.literal_data.name >= new_node.literal_data.name:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.literal_data.name < new_node.literal_data.name:
                current = current.next
            new_node.next = current.next
            current.next = new_node


    def _find_literal(self, name: str) -> bool:
        """
        /***************************************************************************************
        ***  METHOD : _find_literal                                                          ***
        ***  DESCRIPTION :                                                                   ***
        ***      Searches for a literal by name in the list.                                 ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      name : str  : The name of the literal to search for.                        ***
        ***                                                                                  ***
        ***  RETURN : bool                                                                   ***
        ***      Returns True if the literal is found, otherwise False.                      ***
        ***************************************************************************************/

        Check if a literal with the given name exists in the table.

        :param name: The name of the literal to search for.
        :return: True if the literal exists, False otherwise.
        """
        current = self.head
        while current is not None:
            if current.literal_data.name == name:
                return True
            current = current.next
        return False


    def search(self, literal_name: str) -> LiteralData | None:
        """
        /***************************************************************************************
        ***  METHOD : search                                                                 ***
        ***  DESCRIPTION :                                                                   ***
        ***      Searches for a literal by its name and returns the corresponding LiteralData***
        ***      object if found. Logs the action.                                           ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      literal_name : str  : The name of the literal to search for.                ***
        ***                                                                                  ***
        ***  RETURN : LiteralData | None                                                     ***
        ***      Returns the LiteralData object if found, otherwise None.                    ***
        ***************************************************************************************/

        Search for a literal by its name in the literal table.

        :param literal_name: The name of the literal to search for.
        :return: The LiteralData object if found, or None if not found.
        """
        current = self.head
        while current is not None:
            if current.literal_data.name == literal_name:
                self.logger.log_action(f"Found literal '{literal_name}' in the table.", False)
                return current.literal_data
            current = current.next
        self.logger.log_action(f"Literal '{literal_name}' not found in the table.", False)
        return None


    def update_addresses(self, start_address: int = 0):
        """
        /***************************************************************************************
        ***  METHOD : update_addresses                                                       ***
        ***  DESCRIPTION :                                                                   ***
        ***      Assigns addresses to literals in the order they were encountered in the     ***
        ***      list, starting from the specified start_address.                            ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      start_address : int  : The starting address for the first literal (default 0).***
        ***                                                                                  ***
        ***  EXCEPTIONS :                                                                    ***
        ***      Logs an error if the starting address is negative or the table is empty.    ***
        ***************************************************************************************/

        Assign addresses to literals sequentially without sorting, retaining the order 
        in which they were encountered in the linked list.
        
        :param start_address: The starting address for the first literal (default is 0).
        """
        if start_address < 0:
            self.logger.log_error("Invalid starting address. Addresses cannot be negative.")
            return

        if self.head is None:
            self.logger.log_error("Update failed: The literal table is empty.")
            return

        current = self.head
        current_address = start_address

        while current:
            current.literal_data.address = current_address
            self.logger.log_action(f"Assigned address {current_address} to literal '{current.literal_data.name}'.", False)
            current_address += 1  # Increment address by 1 regardless of length
            current = current.next


    def display_literals(self):
        """
        /***************************************************************************************
        ***  METHOD : display_literals                                                       ***
        ***  DESCRIPTION :                                                                   ***
        ***      Displays all literals stored in the table, formatted into columns.          ***
        ***************************************************************************************/

        Display all the literals in the table in a formatted manner.
        """
        if self.head is None:
            print("Literal table is empty. No literals to display.")
            return
    
        # Define column widths
        Lit = 15
        Val = 15
        Len = 8
        Addr = 9
    
        self.display_literals_header(Lit, Val, Len, Addr)
        self.display_literals_body(Lit, Val, Len, Addr)


    def display_literals_header(self, Lit, Val, Len, Addr):
        """
        /***************************************************************************************
        ***  METHOD : display_literals_header                                                ***
        ***  DESCRIPTION :                                                                   ***
        ***      Displays the header of the literal table with proper column titles.         ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      Lit  : int  : The width of the 'Literal' column.                            ***
        ***      Val  : int  : The width of the 'Value' column.                              ***
        ***      Len  : int  : The width of the 'Length' column.                             ***
        ***      Addr : int  : The width of the 'Address' column.                            ***
        ***************************************************************************************/

        Display the header for the literal table.
        """
        total_width = Lit + Val + Len + Addr + 3
        print("┏" + ("━" * total_width) + "┓")
        print(f"┃{' LITERAL TABLE':^{total_width}}┃")
        print("┣" + ("━" * Lit) + "┯" + ("━" * Val) + "┯" + ("━" * Len) + "┯" + ("━" * Addr) + "┫")
        print(f"┃ {'Literal':<{Lit - 2}} │ {'Value':^{Val - 2}} │ {'Length':^{Len - 2}} │ {'Address':^{Addr - 2}} ┃")
        print("┣" + ("━" * Lit) + "┿" + ("━" * Val) + "┿" + ("━" * Len) + "┿" + ("━" * Addr) + "┫")


    def display_literals_body(self, Lit, Val, Len, Addr):
        """
        /***************************************************************************************
        ***  METHOD : display_literals_body                                                  ***
        ***  DESCRIPTION :                                                                   ***
        ***      Displays the body of the literal table, pausing every 18 lines for          ***
        ***      pagination.                                                                 ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      Lit  : int  : The width of the 'Literal' column.                            ***
        ***      Val  : int  : The width of the 'Value' column.                              ***
        ***      Len  : int  : The width of the 'Length' column.                             ***
        ***      Addr : int  : The width of the 'Address' column.                            ***
        ***************************************************************************************/

        Display the body of the literal table, pausing every 18 lines.
        """
        current = self.head
        counter = 0
    
        while current:
            literal = current.literal_data
            address_display = literal.address if literal.address is not None else "N/A"  # Handle NoneType address
            print(f"┃ {literal.name:<{Lit - 2}} │ {literal.value:^{Val - 2}} │ {literal.length:^{Len - 2}} │ {address_display:^{Addr - 2}} ┃")
            counter += 1
            if counter % 18 == 0:
                self.press_continue()
            current = current.next
    
        total_width = Lit + Val + Len + Addr + 3
        print("┗" + ("━" * Lit) + "┷" + ("━" * Val) + "┷" + ("━" * Len) + "┷" + ("━" * Addr) + "┛")

    def get_total_size(self) -> int:
        """
        Calculates the total size of all literals in bytes.
        """
        total_size = 0
        current = self.head
        while current:
            total_size += current.literal_data.length
            current = current.next
        return total_size

    def press_continue(self):
        """
        /***************************************************************************************
        ***  METHOD : press_continue                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Pauses the program and waits for the user to press Enter before continuing. ***
        ***************************************************************************************/

        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')


class ExpressionParser:
    """
    /***************************************************************************************
    ***  CLASS NAME : ExpressionParser                                                   ***
    ***  DESCRIPTION :                                                                   ***
    ***      Responsible for parsing assembly expressions and literals. The class       ***
    ***      manages both expressions and literals, logging actions and errors.          ***
    ***************************************************************************************/

        Class responsible for parsing assembly expressions and literals.
    
    Attributes:
        expressions_lines (list): List of raw expression lines.
        parsed_expressions (list): List of dictionaries representing parsed expressions.
        literal_table (LiteralTableList): Reference to the literal table.
        logger (ErrorLogHandler): Reference to the error log handler.
    """


    def __init__(self, expressions_lines, literal_table, logger, hex_literal_prefix=None, character_literal_prefix='=0C'):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes the parser with raw expression lines, the literal table, and    ***
        ***      a log handler for managing errors and actions.                              ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      expressions_lines : list  : List of raw expression lines.                   ***
        ***      literal_table     : LiteralTableList  : Reference to the literal table.     ***
        ***      logger       : ErrorLogHandler  : Logs actions and errors.             ***
        ***************************************************************************************/

        Initializes the parser with a list of expression lines, a literal table, and an error log handler.
        
        Args:
            expressions_lines (list): List of raw expression lines from the file.
            literal_table (LiteralTableList): Reference to the literal table.
            logger (ErrorLogHandler): Reference to the error log handler.
        """
        self.expressions_lines = expressions_lines or []
        self.parsed_expressions = []
        self.literal_table = literal_table
        self.logger = logger
        self.invalid_literals_set = set()  # Track invalid literals
        self.hex_literal_prefix = hex_literal_prefix or '=0X'
        self.character_literal_prefix = character_literal_prefix or '=0C'


    def parse_all(self):
        """
        /***************************************************************************************
        ***  METHOD : parse_all                                                              ***
        ***  DESCRIPTION :                                                                   ***
        ***      Parses all expression lines and logs actions or errors as necessary.        ***
        ***************************************************************************************/

        Parses all expression lines and stores the parsed expressions in parsed_expressions.
        Logs actions and errors as necessary.
        """
        for line in self.expressions_lines:
            parsed_expr = self.parse_line(line)
            if parsed_expr:
                if parsed_expr.get('error'):
                    self.logger.log_error(parsed_expr['error'], context_info=parsed_expr['original_expression'])
                else:
                    self.logger.log_action(f"Parsed expression: {parsed_expr['original_expression']}", False)
                self.parsed_expressions.append(parsed_expr)

 
    def parse_line(self, line):
        """
        /***************************************************************************************
        ***  METHOD : parse_line                                                             ***
        ***  DESCRIPTION :                                                                   ***
        ***      Parses a single line into a structured expression, handling literals and    ***
        ***      addressing modes.                                                           ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      line : str  : A single line from the expression file to be parsed.          ***
        ***                                                                                  ***
        ***  RETURN : dict                                                                   ***
        ***      Returns a dictionary representing the parsed expression.                   ***
        ***************************************************************************************/

        Parses a single line into a structured expression and handles literals.
        """
        parsed_expr = {
            'original_expression': line.strip(),
            'addressing_mode': 'DIRECT',
            'operator': None,
            'operand1': None,
            'operand2': None,
            'indexing': False,
            'error': None
        }

        # Trim leading and trailing whitespaces
        line = line.strip()

        if not line:  # Ignore empty lines
            return None

        # Parse different parts of the expression
        line = self.parse_addressing_mode(line, parsed_expr)
        line = self.parse_indexing(line, parsed_expr)

        # Handle invalid combination of addressing mode and indexing
        if parsed_expr['indexing'] and parsed_expr['addressing_mode'] in ['IMMEDIATE', 'INDIRECT']:
            parsed_expr['error'] = f"{parsed_expr['addressing_mode'][0]} and x ERROR"
            return parsed_expr

        # Handle literals
        if line.startswith('='):
            result = self.parse_literals(line, parsed_expr)
            return result  # It either returns the expression or continues processing

        # Parse operands and operator
        self.parse_operands(line, parsed_expr)

        # Validate operands
        self.validate_operands(parsed_expr)

        return parsed_expr

    ### Sub-methods below ###

    def parse_addressing_mode(self, line, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : parse_addressing_mode                                                  ***
        ***  DESCRIPTION :                                                                   ***
        ***      Parses the addressing mode from the expression and modifies the parsed      ***
        ***      expression.                                                                 ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      line        : str   : The expression line being parsed.                     ***
        ***      parsed_expr : dict  : The dictionary representing the parsed expression.    ***
        ***                                                                                  ***
        ***  RETURN : str                                                                    ***
        ***      Returns the updated line after stripping the addressing mode.               ***
        ***************************************************************************************/

        Parse the addressing mode from the expression and modify the parsed expression.
        Returns the updated line (after stripping addressing mode).
        """
        if line.startswith('@'):
            parsed_expr['addressing_mode'] = 'INDIRECT'
            return line[1:].strip()
        elif line.startswith('#'):
            parsed_expr['addressing_mode'] = 'IMMEDIATE'
            return line[1:].strip()
        return line


    def parse_indexing(self, line, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : parse_indexing                                                        ***
        ***  DESCRIPTION :                                                                   ***
        ***      Parses the indexing mode from the expression and updates the parsed         ***
        ***      expression.                                                                 ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      line        : str   : The expression line being parsed.                     ***
        ***      parsed_expr : dict  : The dictionary representing the parsed expression.    ***
        ***                                                                                  ***
        ***  RETURN : str                                                                    ***
        ***      Returns the updated line after stripping the indexing mode.                 ***
        ***************************************************************************************/

        Parse the indexing mode from the expression (e.g., `,X`).
        Returns the updated line (after stripping indexing mode).
        """
        if line[-2:].upper() == ',X':
            parsed_expr['indexing'] = True
            return line[:-2].strip()
        return line


    def parse_literals(self, line, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : parse_literals                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Parses and validates literals from the expression, adding valid literals    ***
        ***      to the literal table and logging errors if encountered.                     ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      line        : str   : The expression line containing the literal.           ***
        ***      parsed_expr : dict  : The dictionary representing the parsed expression.    ***
        ***                                                                                  ***
        ***  RETURN : dict or None                                                           ***
        ***      Returns the parsed expression if invalid, otherwise None if the literal     ***
        ***      is valid.                                                                   ***
        ***************************************************************************************/

        Parse and validate literals from the expression. Handles errors and adds them to the literal table.
        Returns the parsed expression or None if it's valid and already inserted.
        """
        literal_name = line
        literal = self.literal_table.search(literal_name)

        if not literal:
            try:
                #check if the literal does not start with =0C or =0X or =0c or =0x
                if not literal_name.upper().startswith("=0C") and not literal_name.upper().startswith("=0X"):
                    _error_message = f"Invalid literal format: {literal_name}"
                    self.logger.log_error(_error_message)
                    raise ValueError(_error_message)
                # # Check for illegal character literal format =C'123'
                # if literal_name.upper().startswith("=C"):
                #     raise ValueError(f"Illegal literal format: {literal_name}")

                # Handle hexadecimal literals
                # Check if it starts with hex_literal_prefix
                if literal_name.upper().startswith(self.hex_literal_prefix):
                    literal_value = literal_name[3:].upper()
                    if not all(c in '0123456789ABCDEFabcdef' for c in literal_value):
                        _error_message = f"Invalid hexadecimal value: {literal_value}"
                        self.logger.log_error(_error_message)
                        raise ValueError(f"Invalid hexadecimal value: {literal_value}")
                    if len(literal_value) % 2 != 0:
                        _error_message = f"Hexadecimal value length is not valid (must be even): {literal_value}"
                        self.logger.log_error(_error_message)
                        raise ValueError(_error_message)
                    literal_length = len(literal_value) // 2  # Two characters per byte

                # Handle character literals
                # Check if it starts with character_literal_prefix
                elif literal_name.upper().startswith(self.character_literal_prefix):
                    char_sequence = literal_name[3:]
                    if len(char_sequence) == 0:
                        _error_message = f"Character literal is empty: {literal_name}"
                        self.logger.log_error(_error_message)
                        raise ValueError(_error_message)
                    literal_value = ''.join(f"{ord(c):02X}" for c in char_sequence)
                    literal_length = len(char_sequence)

                else:
                    raise ValueError(f"Invalid literal format: {literal_name}")

                # Insert literal into the literal table
                new_literal = LiteralData(name=literal_name, value=literal_value, length=literal_length)
                self.literal_table.insert(new_literal)

                parsed_expr['operand1'] = literal_name
                self.logger.log_action(f"Inserted new literal '{literal_name}'", False)
                return None  # Skip further processing for valid literals

            except ValueError as e:
                parsed_expr['error'] = str(e)
                if literal_name in self.invalid_literals_set:
                    return None  # Skip duplicate invalid literals
                else:
                    self.invalid_literals_set.add(literal_name)
                    self.logger.log_error(parsed_expr['error'], context_info=literal_name)
                    return parsed_expr  # Return the invalid literal as an error

        parsed_expr['operand1'] = literal_name
        self.logger.log_action(f"Used existing literal '{literal_name}'", False)
        return parsed_expr


    def parse_operands(self, line, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : parse_operands                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Splits the expression line and assigns operands, identifying the operator   ***
        ***      and handling parentheses.                                                   ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      line        : str   : The expression line containing operands.              ***
        ***      parsed_expr : dict  : The dictionary representing the parsed expression.    ***
        ***************************************************************************************/

        Split and assign operands to the parsed expression. Identifies the operator (`+`, `-`) and assigns operands.
        """
        self.logger.log_action(f"Parsing operands from line: {line}", False)
        if '+' in line:
            parsed_expr['operator'] = '+'
            operands = line.split('+')
        elif '-' in line:
            parsed_expr['operator'] = '-'
            operands = line.split('-')
        else:
            operands = [line]

        operands = [operand.strip('()').strip() for operand in operands]  # Clean parentheses

        if len(operands) == 1:
            parsed_expr['operand1'] = operands[0]
        elif len(operands) == 2:
            parsed_expr['operand1'], parsed_expr['operand2'] = operands


    def validate_operands(self, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : validate_operands                                                      ***
        ***  DESCRIPTION :                                                                   ***
        ***      Validates the parsed operands, checking for missing or invalid operands,    ***
        ***      and logs errors if found.                                                   ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      parsed_expr : dict  : The dictionary representing the parsed expression.    ***
        ***************************************************************************************/

        Validate the operands in the parsed expression. If missing operands or invalid combination, add errors.
        """
        if not parsed_expr['operand1']:
            parsed_expr['error'] = "Missing first operand."
        elif parsed_expr['operator'] and not parsed_expr['operand2']:
            parsed_expr['error'] = "Missing second operand."


    def get_parsed_expressions(self):
        """
        /***************************************************************************************
            ***  METHOD : get_parsed_expressions                                                 ***
            ***  DESCRIPTION :                                                                   ***
            ***      Returns the list of parsed expressions stored by the parser.                ***
            ***                                                                                  ***
            ***  RETURN : list                                                                   ***
            ***      A list of parsed expressions.                                               ***
            ***************************************************************************************/

        Returns the parsed expressions.
        
        Returns:
            list: List of parsed expressions.
        """
        return self.parsed_expressions



class ExpressionEvaluator:
    """
    /***************************************************************************************
    ***  CLASS NAME : ExpressionEvaluator                                                ***
    ***  DESCRIPTION :                                                                   ***
    ***      Evaluates parsed expressions by calculating their values and determining    ***
    ***      their relocatability.                                                       ***
    ***************************************************************************************/

    Class responsible for evaluating parsed expressions.
    
    Attributes:
        parsed_expressions (list): List of parsed expressions from ExpressionParser.
        symbol_table (SymbolTable): Reference to the symbol table.
        literal_table (LiteralTableList): An object handling literal management.
        evaluated_expressions (list): List of evaluated expressions with their results.
        logger (ErrorLogHandler): Reference to the error log handler.
    """


    def __init__(self, parsed_expressions, symbol_table, literal_table, logger):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes the evaluator with parsed expressions, a symbol table, literal  ***
        ***      table, and a log handler for managing errors and actions.                   ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      parsed_expressions : list  : List of parsed expressions.                    ***
        ***      symbol_table       : SymbolTable  : Reference to the symbol table.          ***
        ***      literal_table      : LiteralTableList  : Reference to the literal table.    ***
        ***      logger        : ErrorLogHandler  : Logs actions and errors.            ***
        ***************************************************************************************/

        Initializes the evaluator with parsed expressions, symbol table, literal table, and log handler.
        
        Args:
            parsed_expressions (list): List of parsed expressions.
            symbol_table (SymbolTable): Reference to the symbol table.
            literal_table (LiteralTableList): Literal table for managing literals.
            logger (ErrorLogHandler): Reference to the error log handler.
        """
        self.parsed_expressions = parsed_expressions
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.evaluated_expressions = [] 
        self.logger = logger or ErrorLogHandler()


    def evaluate_all(self):
        """
        /***************************************************************************************
        ***  METHOD : evaluate_all                                                           ***
        ***  DESCRIPTION :                                                                   ***
        ***      Evaluates all parsed expressions and logs actions or errors as necessary.   ***
        ***************************************************************************************/

        Evaluates all parsed expressions and stores the results in evaluated_expressions.
        Logs actions and errors as necessary.
        """
        for parsed_expr in self.parsed_expressions:
            if parsed_expr:
                evaluated_expr = self.evaluate_expression(parsed_expr)
                if evaluated_expr.get('error'):
                    self.logger.log_error(evaluated_expr['error'], context_info=parsed_expr['original_expression'])
                else:
                    self.logger.log_action(f"Evaluated expression: {parsed_expr['original_expression']}", False)
                self.evaluated_expressions.append(evaluated_expr)


    def evaluate_expression(self, parsed_expr):
        """
        /***************************************************************************************
        ***  METHOD : evaluate_expression                                                    ***
        ***  DESCRIPTION :                                                                   ***
        ***      Evaluates a single parsed expression and computes its value, relocatability,***
        ***      and various flags.                                                          ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      parsed_expr : dict   : A parsed expression dictionary.                      ***
        ***                                                                                  ***
        ***  RETURN : dict                                                                   ***
        ***      Returns a dictionary representing the evaluated expression, with its value  ***
        ***      and flags.                                                                  ***
        ***************************************************************************************/

        Evaluates a single parsed expression.
        
        Args:
            parsed_expr (dict): A parsed expression.
        
        Returns:
            dict: A dictionary representing the evaluated expression with value and flags.
        """
        evaluated_expr = {
            'original_expression': parsed_expr['original_expression'],
            'value': None,
            'relocatable': None,
            'n_bit': 1,
            'i_bit': 1,
            'x_bit': 1 if parsed_expr['indexing'] else 0,
            'error': parsed_expr.get('error')
        }

        if evaluated_expr['error']:
            return evaluated_expr

        # Determine N-Bit and I-Bit based on addressing mode
        if parsed_expr['addressing_mode'] == 'IMMEDIATE':
            evaluated_expr['n_bit'] = 0
            evaluated_expr['i_bit'] = 1
        elif parsed_expr['addressing_mode'] == 'INDIRECT':
            evaluated_expr['n_bit'] = 1
            evaluated_expr['i_bit'] = 0

        # Evaluate operands
        operand1_value, operand1_rflag, error1 = self.get_operand_value(parsed_expr['operand1'])
        if error1:
            evaluated_expr['error'] = error1
            return evaluated_expr

        if parsed_expr['operator']:
            operand2_value, operand2_rflag, error2 = self.get_operand_value(parsed_expr['operand2'])
            if error2:
                evaluated_expr['error'] = error2
                return evaluated_expr

            # Perform operation
            if parsed_expr['operator'] == '+':
                result_value = operand1_value + operand2_value
            elif parsed_expr['operator'] == '-':
                result_value = operand1_value - operand2_value
            else:
                evaluated_expr['error'] = f"Unsupported operator: {parsed_expr['operator']}"
                return evaluated_expr

            # Determine relocatability
            relocatable, error_rflag = self.evaluate_rflag(operand1_rflag, parsed_expr['operator'], operand2_rflag)
            if error_rflag:
                evaluated_expr['error'] = error_rflag
                return evaluated_expr

            evaluated_expr['value'] = result_value
            evaluated_expr['relocatable'] = relocatable

        else:
            # Single operand evaluation
            evaluated_expr['value'] = operand1_value
            evaluated_expr['relocatable'] = operand1_rflag

        return evaluated_expr


    def get_operand_value(self, operand):
        """
        /***************************************************************************************
        ***  METHOD : get_operand_value                                                      ***
        ***  DESCRIPTION :                                                                   ***
        ***      Retrieves the value and relocatability flag (RFLAG) for an operand,         ***
        ***      handling symbols, literals, and numeric values.                             ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      operand : str   : The operand to evaluate (symbol, literal, or numeric).    ***
        ***                                                                                  ***
        ***  RETURN : tuple                                                                  ***
        ***      Returns a tuple with (value, relocatability flag, error message).           ***
        ***************************************************************************************/

        Retrieves the value and RFLAG for an operand (symbol, literal, or numeric).
        
        Args:
            operand (str): The operand (symbol, literal, or immediate value).
        
        Returns:
            tuple: (value, relocatable_flag, error_message) - returns error_message if an error occurs.
        """
        # Check if operand is numeric
        if operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
            return int(operand), False, None  # Absolute value
        elif operand.startswith('#'):
            # Immediate literal value
            return int(operand[1:]), False, None
        elif operand.startswith('='):
            # Literal handling using the literal table
            literal = self.literal_table.search(operand)
            if literal:
                try:
                    return int(literal.value, 16), False, None  # Convert from hex to decimal
                except ValueError as e:
                    return None, None, f"Invalid literal value '{literal.value}': {str(e)}"
            else:
                return None, None, f"Literal '{operand}' not found in the literal table."
        else:
            # Symbol lookup using SymbolTable.get()
            value, rflag, error = self.symbol_table.get(operand)
            if error:
                return None, None, error
            return value, rflag, None


    def evaluate_rflag(self, rflag1, operator, rflag2):
        """
        /***************************************************************************************
        ***  METHOD : evaluate_rflag                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Evaluates the relocatability (RFLAG) of the result based on the operation   ***
        ***      performed between two operands.                                             ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      rflag1    : bool   : RFLAG of the first operand (True for relocatable).     ***
        ***      operator  : str    : The operation performed ('+' or '-').                  ***
        ***      rflag2    : bool   : RFLAG of the second operand (True for relocatable).    ***
        ***                                                                                  ***
        ***  RETURN : tuple                                                                  ***
        ***      Returns a tuple with (relocatable_flag, error_message) if applicable.       ***
        ***************************************************************************************/

        Evaluates the RFLAG (relocatability) based on the operation and RFLAGS of the operands.
        
        Args:
            rflag1 (bool): RFLAG of the first operand (True if relocatable, False if absolute).
            operator (str): The operation being performed ('+' or '-').
            rflag2 (bool): RFLAG of the second operand (True if relocatable, False if absolute).
            
        Returns:
            tuple: (relocatable_flag, error_message) 
                relocatable_flag (bool): The relocatability of the result.
                error_message (str): Error message if the operation is invalid.
        """
        if operator == '+':
            if not rflag1 and not rflag2:
                return False, None  # Absolute + Absolute = Absolute
            elif (rflag1 and not rflag2) or (not rflag1 and rflag2):
                return True, None  # Relocatable + Absolute or Absolute + Relocatable = Relocatable
            elif rflag1 and rflag2:
                return None, "T  +  T ERROR"  # Error: Cannot add two relocatable values

        elif operator == '-':
            if not rflag1 and not rflag2:
                return False, None  # Absolute - Absolute = Absolute
            elif rflag1 and not rflag2:
                return True, None  # Relocatable - Absolute = Relocatable
            elif not rflag1 and rflag2:
                return None, "F  -  T ERROR"  # Error: Cannot subtract relocatable value from absolute
            elif rflag1 and rflag2:
                return False, None  # Relocatable - Relocatable = Absolute

        return None, "Error: Invalid operation."  # Catch-all for invalid operations


    def get_evaluated_expressions(self):
        """
        /***************************************************************************************
        ***  METHOD : get_evaluated_expressions                                              ***
        ***  DESCRIPTION :                                                                   ***
        ***      Returns the list of evaluated expressions.                                  ***
        ***                                                                                  ***
        ***  RETURN : list                                                                   ***
        ***      A list of evaluated expressions with results.                               ***
        ***************************************************************************************/

        Returns the evaluated expressions.
        
        Returns:
            list: List of evaluated expressions with results.
        """
        return self.evaluated_expressions


class ExpressionResults:
    """
    /***************************************************************************************
    ***  CLASS NAME : ExpressionResults                                                   ***
    ***  DESCRIPTION :                                                                    ***
    ***      Responsible for formatting and outputting evaluated expression results.      ***
    ***      Manages display of expression evaluation results with pagination.            ***
    ***************************************************************************************/

    Class responsible for formatting and outputting evaluated expression results.
    
    Attributes:
        evaluated_expressions (list): List of evaluated expressions.
        logger (ErrorLogHandler): Reference to the error log handler.
    """


    def __init__(self, evaluated_expressions, logger):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                                ***
        ***  DESCRIPTION :                                                                    ***
        ***      Initializes the result handler with evaluated expressions and a log handler. ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      evaluated_expressions : list  : List of evaluated expressions.               ***
        ***      logger           : ErrorLogHandler  : Logs actions and errors.          ***
        ***************************************************************************************/

        Initializes the result handler with evaluated expressions and log handler.
        
        Args:
            evaluated_expressions (list): List of evaluated expressions.
            logger (ErrorLogHandler): Reference to the error log handler.
        """
        self.evaluated_expressions = evaluated_expressions
        self.logger = logger


    def display_results(self, include_literals=True):
        """
        /***************************************************************************************
        ***  METHOD : display_results                                                         ***
        ***  DESCRIPTION :                                                                    ***
        ***      Displays all the evaluated expression results with pagination. Excludes      ***
        ***      literals from the results if specified.                                      ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      include_literals : bool  : If False, excludes literals from the results.      ***
        ***************************************************************************************/

        Display all the evaluated expression results in a paginated format.
        
        Args:
            include_literals (bool): If False, literals are excluded from the results.
        """
        if not self.evaluated_expressions:
            print("No expressions to evaluate.")
            return

        # Define column widths
        Ex = 20
        Va = 14
        Re = 13
        Ns = 7
        Is = 7
        Xs = 7

        # Display the header first
        self.display_results_header(Ex, Va, Re, Ns, Is, Xs)

        # Display body with pagination
        self.display_results_body(Ex, Va, Re, Ns, Is, Xs, include_literals)


    def display_results_header(self, Ex, Va, Re, Ns, Is, Xs):
        """
        /***************************************************************************************
        ***  METHOD : display_results_header                                                  ***
        ***  DESCRIPTION :                                                                    ***
        ***      Displays the header for the evaluated expression results.                    ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      Ex  : int  : Width for the 'Expression' column.                              ***
        ***      Va  : int  : Width for the 'Value' column.                                   ***
        ***      Re  : int  : Width for the 'Relocatable' column.                             ***
        ***      Ns  : int  : Width for the 'N-Bit' column.                                   ***
        ***      Is  : int  : Width for the 'I-Bit' column.                                   ***
        ***      Xs  : int  : Width for the 'X-Bit' column.                                   ***
        ***************************************************************************************/

        Display the header for the expression results.
        """
        total_width = Ex + Va + Re + Ns + Is + Xs + 5
        print("┏" + ("━" * total_width) + "┓")
        print(f"┃{'EXPRESSION RESULTS':^{total_width}}┃")
        print("┣" + ("━" * Ex) + "┯" + ("━" * Va) + "┯" + ("━" * Re) + "┯" + ("━" * Ns) + "┯" + ("━" * Is) + "┯" + ("━" * Xs) + "┫")
        print(f"┃ {'Expression':<{Ex - 2}} │ {'Value':^{Va - 2}} │ {'Relocatable':^{Re - 2}} │ {'N-Bit':^{Ns - 2}} │ {'I-Bit':^{Is - 2}} │ {'X-Bit':^{Xs - 2}} ┃")
        print("┣" + ("━" * Ex) + "┿" + ("━" * Va) + "┿" + ("━" * Re) + "┿" + ("━" * Ns) + "┿" + ("━" * Is) + "┿" + ("━" * Xs) + "┫")


    def display_results_body(self, Ex, Va, Re, Ns, Is, Xs, include_literals):
        """
        /***************************************************************************************
        ***  METHOD : display_results_body                                                    ***
        ***  DESCRIPTION :                                                                    ***
        ***      Displays the body of the evaluated expression results in paginated format.    ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      Ex  : int  : Width for the 'Expression' column.                              ***
        ***      Va  : int  : Width for the 'Value' column.                                   ***
        ***      Re  : int  : Width for the 'Relocatable' column.                             ***
        ***      Ns  : int  : Width for the 'N-Bit' column.                                   ***
        ***      Is  : int  : Width for the 'I-Bit' column.                                   ***
        ***      Xs  : int  : Width for the 'X-Bit' column.                                   ***
        ***      include_literals : bool  : If False, excludes literals from the results.      ***
        ***************************************************************************************/

        Display the body of the results in paginated format.
        Pauses every 18 lines.
        """
        counter = 0
        
        for expr in self.evaluated_expressions:
            # Skip literals if include_literals is False
            if not include_literals and expr['original_expression'].startswith('=') and not expr.get('error'):
                continue  # Skip valid literals
            
            result_line = self.format_expression_result(expr, Ex, Va, Re, Ns, Is, Xs)
            print(result_line)
            counter += 1

            if counter % 18 == 0:
                self.press_continue()

        # Display footer
        total_width = Ex + Va + Re + Ns + Is + Xs + 5
        print("┗" + ("━" * Ex) + "┷" + ("━" * Va) + "┷" + ("━" * Re) + "┷" + ("━" * Ns) + "┷" + ("━" * Is) + "┷" + ("━" * Xs) + "┛")


    def format_expression_result(self, evaluated_expr, Ex, Va, Re, Ns, Is, Xs):
        """
        /***************************************************************************************
        ***  METHOD : format_expression_result                                                ***
        ***  DESCRIPTION :                                                                    ***
        ***      Formats a single evaluated expression into a readable string for display.     ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      evaluated_expr : dict  : The evaluated expression with its results.           ***
        ***      Ex  : int  : Width for the 'Expression' column.                              ***
        ***      Va  : int  : Width for the 'Value' column.                                   ***
        ***      Re  : int  : Width for the 'Relocatable' column.                             ***
        ***      Ns  : int  : Width for the 'N-Bit' column.                                   ***
        ***      Is  : int  : Width for the 'I-Bit' column.                                   ***
        ***      Xs  : int  : Width for the 'X-Bit' column.                                   ***
        ***                                                                                   ***
        ***  RETURN : str                                                                     ***
        ***      Returns a formatted string for the evaluated expression.                     ***
        ***************************************************************************************/

        Format a single evaluated expression into a readable string.
        
        Args:
            evaluated_expr (dict): Evaluated expression with its results.
            Ex (int): Width for the Expression column.
            Va (int): Width for the Value column.
            Re (int): Width for the Relocatable column.
            Ns (int): Width for the N-Bit column.
            Is (int): Width for the I-Bit column.
            Xs (int): Width for the X-Bit column.
        
        Returns:
            str: Formatted string for display.
        """
        if evaluated_expr['error']:
            return f"┃ {evaluated_expr['original_expression']:<{Ex - 2}} │ {'ERROR':^{Va - 2}} │ {'-':^{Re - 2}} │ {'-':^{Ns - 2}} │ {'-':^{Is - 2}} │ {'-':^{Xs - 2}} ┃"
        else:
            # Check if the expression is a literal to display value in hex
            if evaluated_expr['original_expression'].startswith('='):
                value = f"0x{evaluated_expr['value']:X}"
            else:
                value = evaluated_expr['value']
            relocatable = 'RELATIVE' if evaluated_expr['relocatable'] else 'ABSOLUTE'
            return (f"┃ {evaluated_expr['original_expression']:<{Ex - 2}} │ {value:^{Va - 2}} │ {relocatable:^{Re - 2}} │ "
                    f"{evaluated_expr['n_bit']:^{Ns - 2}} │ {evaluated_expr['i_bit']:^{Is - 2}} │ {evaluated_expr['x_bit']:^{Xs - 2}} ┃")


    def press_continue(self):
        """
        /***************************************************************************************
        ***  METHOD : press_continue                                                          ***
        ***  DESCRIPTION :                                                                    ***
        ***      Pauses the program and waits for the user to press Enter before continuing.   ***
        ***************************************************************************************/

        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')


class LiteralTableDriver:
    """
    /***************************************************************************************
    ***  CLASS NAME : LiteralTableDriver                                                  ***
    ***  DESCRIPTION :                                                                    ***
    ***      Main driver class for handling literal table operations and the overall      ***
    ***      program flow. Manages symbol tables, expression parsing, and evaluation.     ***
    ***************************************************************************************/

    Main driver class to handle the literal table operations and overall program flow.
    """


    def __init__(self, logger=None, symbol_table_driver=None, literal_table=None, file_explorer=None):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                                ***
        ***  DESCRIPTION :                                                                    ***
        ***      Initializes the LiteralTableDriver with all necessary components.            ***
        ***************************************************************************************/

        Initialize the LiteralTableDriver with all necessary components.
        """
        self.logger = logger or ErrorLogHandler()  # Error log handler
        self.literal_table = literal_table or LiteralTableList(self.logger)  # Pass logger to LiteralTableList
        self.symbol_table_driver = symbol_table_driver or SymbolTableDriver()  # Use SymbolTableDriver to manage symbol table
        self.file_explorer = file_explorer or FileExplorer()  # File handling for locating files
        


    def run(self, expression_file: str = None):
        """
        /***************************************************************************************
        ***  METHOD : run                                                                     ***
        ***  DESCRIPTION :                                                                    ***
        ***      Entry point for running the program. It builds the symbol table, loads and   ***
        ***      parses expressions, evaluates them, and displays the results.                ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      expression_file : str  : Optional. The file containing expressions to parse. ***
        ***************************************************************************************/

        The main entry point to drive the entire program.
        Coordinates the flow of building the symbol table, parsing, and evaluating expressions.
        """
        try:
            self.build_symbol_table()
            expression_file = expression_file or self.get_expression_file()
            expressions = self.load_expressions(expression_file)

            if expressions:
                parsed_expressions = self.parse_expressions(expressions)
                self.evaluate_expressions(parsed_expressions)
                self.display_results()
        except Exception as e:
            self.logger.log_error(f"Unexpected error occurred: {e}")


    def build_symbol_table(self):
        """
        /***************************************************************************************
        ***  METHOD : build_symbol_table                                                      ***
        ***  DESCRIPTION :                                                                    ***
        ***      Builds the symbol table using the SymbolTableDriver and logs the actions.    ***
        ***************************************************************************************/

        Build the symbol table using SymbolTableDriver.
        """
        try:
            self.logger.log_action("Building symbol table from SYMS.DAT")
            self.symbol_table_driver.build_symbol_table()
            self.symbol_table = self.symbol_table_driver.symbol_table
            self.logger.log_action("Symbol table building complete")
        except Exception as e:
            self.logger.log_error(f"Error while building symbol table: {e}")


    def get_expression_file(self) -> str:
        """
        /***************************************************************************************
        ***  METHOD : get_expression_file                                                     ***
        ***  DESCRIPTION :                                                                    ***
        ***      Determines the expression file to use, either from the command line or       ***
        ***      defaulting to 'EXPR.DAT'.                                                    ***
        ***                                                                                   ***
        ***  RETURN : str                                                                     ***
        ***      The name of the expression file.                                             ***
        ***************************************************************************************/

        Determine the expression file to use, either from the command line or default to 'EXPRESS.DAT'.
        
        :return: The name of the expression file.
        """
        return sys.argv[1] if len(sys.argv) > 1 else "EXPR.DAT"


    def load_expressions(self, file_name: str) -> list[str]:
        """
        /***************************************************************************************
        ***  METHOD : load_expressions                                                        ***
        ***  DESCRIPTION :                                                                    ***
        ***      Loads expressions from the specified file and logs any errors encountered.   ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      file_name : str  : The name of the file containing expressions.              ***
        ***                                                                                   ***
        ***  RETURN : list                                                                    ***
        ***      Returns a list of expressions loaded from the file.                          ***
        ***************************************************************************************/

        Load expressions from the specified file.

        :param file_name: The name of the file containing expressions.
        :return: A list of expressions.
        """
        try:
            expressions = self.file_explorer.process_file(file_name)
            if not expressions:
                raise ValueError(f"The file '{file_name}' is empty. Please provide a valid file with expressions.")
            self.logger.log_action(f"Expressions loaded successfully from {file_name}.")
            return expressions
        except FileNotFoundError:
            self.logger.log_error(f"File '{file_name}' not found.")
            return []
        except Exception as e:
            self.logger.log_error(f"Error while loading expressions from {file_name}: {e}")
            return []


    def parse_expressions(self, expressions: list[str]) -> list[dict]:
        """
        /***************************************************************************************
        ***  METHOD : parse_expressions                                                       ***
        ***  DESCRIPTION :                                                                    ***
        ***      Parses raw expression strings into structured components and logs actions.   ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      expressions : list  : A list of raw expression strings.                      ***
        ***                                                                                   ***
        ***  RETURN : list                                                                    ***
        ***      Returns a list of parsed expression dictionaries.                            ***
        ***************************************************************************************/

        Parse expressions into structured components.

        :param expressions: List of raw expression strings.
        :return: A list of parsed expression dictionaries.
        """
        parser = ExpressionParser(expressions, self.literal_table, self.logger)
        parser.parse_all()
        parsed_expressions = parser.get_parsed_expressions()
        self.logger.log_action(f"Parsed {len(parsed_expressions)} expressions.")
        return parsed_expressions


    def evaluate_expressions(self, parsed_expressions: list[dict]):
        """
        /***************************************************************************************
        ***  METHOD : evaluate_expressions                                                    ***
        ***  DESCRIPTION :                                                                    ***
        ***      Evaluates parsed expressions, updates the literal table, and assigns         ***
        ***      addresses to literals.                                                       ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      parsed_expressions : list  : List of parsed expression components.           ***
        ***************************************************************************************/

        Evaluate parsed expressions and update the literal table with new literals.

        :param parsed_expressions: A list of parsed expression components.
        """
        evaluator = ExpressionEvaluator(
            parsed_expressions,
            self.symbol_table_driver.symbol_table,
            self.literal_table,
            self.logger
        )
        evaluator.evaluate_all()
        self.evaluated_expressions = evaluator.get_evaluated_expressions()

        # Update literal addresses
        self.literal_table.update_addresses(start_address=0)
        self.logger.log_action("Expressions evaluated and literal table updated.")


    def paginate_output(self, display_function, header: str):
        """
        /***************************************************************************************
        ***  METHOD : paginate_output                                                         ***
        ***  DESCRIPTION :                                                                    ***
        ***      Paginates the output of a display function to prevent excessive scrolling.    ***
        ***                                                                                   ***
        ***  INPUT PARAMETERS :                                                               ***
        ***      display_function : function  : The function to display paginated output.      ***
        ***      header           : str       : Header text to display before the output.      ***
        ***************************************************************************************/

        Paginate the output of a display function to prevent excessive scrolling.

        :param display_function: The function to call to display the output.
        :param header: Header to display before the output.
        """
        print(header)
        print("=" * len(header))
        display_function()
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')
        

    def display_results(self):
        """
        /***************************************************************************************
        ***  METHOD : display_results                                                         ***
        ***  DESCRIPTION :                                                                    ***
        ***      Displays evaluated expressions, the literal table, and log entries/errors    ***
        ***      with pagination.                                                             ***
        ***************************************************************************************/

        Display all the results including literals, logs, and errors with paginated output.
        """
        # Display evaluated expressions
        results_display = ExpressionResults(self.evaluated_expressions, self.logger)
        self.paginate_output(lambda: results_display.display_results(include_literals=False), "Displaying Evaluated Expressions:")

        # Display the literal table
        self.paginate_output(self.literal_table.display_literals, "Displaying Literal Table:")

        # Display logs and errors
        self.paginate_output(self.logger.display_log, "Displaying Log Entries:")
        self.paginate_output(self.logger.display_errors, "Displaying Errors:")



def main():
    """
    /***************************************************************************************
    ***  FUNCTION : main                                                                  ***
    ***  DESCRIPTION :                                                                    ***
    ***      Creates an instance of LiteralTableDriver and runs the program with the      ***
    ***      expression file passed via command line or default.                          ***
    ***************************************************************************************/
    """
    # Create an instance of LiteralTableDriver and run it
    expression_file = sys.argv[1] if len(sys.argv) > 1 else None
    driver = LiteralTableDriver()
    driver.run(expression_file)


if __name__ == "__main__":
    main()