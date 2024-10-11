## CSC 354 - Systems Programming
# Project: Literal table Builder
# File: johnA2.py

# Author: John Akujobi
# Date: 10/3/2024
# Description: 

"""
/**************************************************************************************
*** NAME : John Akujobi                                                             ***
*** CLASS : CSc 354 - Systems Programming                                           ***
*** ASSIGNMENT : Assignment 2                                                       ***
*** DUE DATE : Oct, 2024                                                            ***
*** INSTRUCTOR : GEORGE HAMER                                                       ***
***************************************************************************************
*** DESCRIPTION :                                                                   ***
***                                                                                 ***
**************************************************************************************/
"""

from symbol_table_builder import SymbolTableDriver, SymbolData, SymbolTable


class LiteralData:
    """
    Class to represent a literal with its name, value, length, and address.
    """
    def __init__(self, name, value, length):
        """
        Initialize a literal with its name, value, length, and address.

        :param name: Name of the literal (e.g., '=X'05A'').
        :param value: Hexadecimal value of the literal.
        :param length: Length of the literal in bytes.
        :raises ValueError: If name, value, or length is invalid.
        """
        if not name or not value or length <= 0:
            raise ValueError(f"Literal data is invalid. "
                             f"Make sure the name is provided, value is not empty, and length is a positive integer.")
        
        self.name = name
        self.value = value
        self.length = length
        self.address = None  # Address will be assigned later


class LiteralNode:
    """
    Class to represent a node in the linked list of literals.
    Each node contains LiteralData and a reference to the next node.
    """
    def __init__(self, literal_data):
        """
        Initialize the node with literal data.

        :param literal_data: Instance of LiteralData.
        :raises TypeError: If literal_data is not an instance of LiteralData.
        """
        if not isinstance(literal_data, LiteralData):
            raise TypeError("Expected an instance of LiteralData. Please ensure you are passing a valid LiteralData object.")
        
        self.literal_data = literal_data
        self.next = None


class LiteralTableList:
    """
    Class to represent the literal table, which is stored as a linked list.
    This class provides methods to insert literals, update their addresses, 
    and display the literal table.
    """
    def __init__(self):
        """
        Initialize the literal table with an empty linked list.
        """
        self.head = None  # Head of the linked list (first node)
        self.log_entries = []  # Log of actions performed on the literal table
        self.errors = []  # Log of errors encountered during processing

    def insert(self, literal_data):
        """
        Insert a new literal into the linked list.

        :param literal_data: An instance of LiteralData to be inserted.
        :raises TypeError: If literal_data is not an instance of LiteralData.
        :raises ValueError: If the literal_data has invalid fields.
        """
        if not isinstance(literal_data, LiteralData):
            self._log_error(f"Cannot insert: Invalid LiteralData object. Please ensure the data passed is a LiteralData object.")
            return
        
        # Validate the literal data before inserting
        if not literal_data.name or not literal_data.value or literal_data.length <= 0:
            self._log_error(f"Cannot insert literal. Invalid data: "
                            f"Literal name: '{literal_data.name}', "
                            f"value: '{literal_data.value}', "
                            f"length: {literal_data.length}. "
                            "Ensure the name and value are not empty, and length is a positive integer.")
            return
        
        # If the table is empty, insert the first literal as the head
        if self.head is None:
            self.head = LiteralNode(literal_data)
            self._log_action(f"Inserted literal '{literal_data.name}' as head.")
        else:
            # Traverse the list to insert the new literal at the end
            current = self.head
            while current.next is not None:
                # Check for duplicates
                if current.literal_data.name == literal_data.name:
                    self._log_error(f"Duplicate literal insertion error: "
                                    f"The literal '{literal_data.name}' already exists in the table. "
                                    "Duplicate entries are not allowed.")
                    return
                current = current.next
            
            # Insert at the end of the list
            if current.literal_data.name == literal_data.name:
                self._log_error(f"Duplicate literal insertion error: "
                                f"The literal '{literal_data.name}' already exists in the table.")
            else:
                current.next = LiteralNode(literal_data)
                self._log_action(f"Inserted literal '{literal_data.name}' into the table.")

    def update_addresses(self, start_address=0):
        """
        Assign addresses to literals sequentially. If the table is empty, log an error.

        :param start_address: The starting address for the first literal.
        :raises ValueError: If start_address is negative.
        """
        if start_address < 0:
            self._log_error("Invalid starting address. Addresses cannot be negative. "
                            "Please provide a valid non-negative integer as the starting address.")
            return
        
        if self.head is None:
            self._log_error("Update failed: The literal table is currently empty. "
                            "Please add literals before attempting to update addresses.")
            return

        current = self.head
        current_address = start_address
        
        # Traverse the list and assign addresses to each literal
        while current is not None:
            current.literal_data.address = current_address
            self._log_action(f"Assigned address {current_address} to literal '{current.literal_data.name}'.")
            current_address += current.literal_data.length
            current = current.next
        
        self._log_action(f"Successfully updated all addresses starting from {start_address}.")

    def display_literals(self):
        """
        Display all the literals in the table in a formatted manner.
        """
        if self.head is None:
            print("Literal table is empty. No literals to display.")
            return
        
        # Print header for the table
        print("LITERAL TABLE:")
        print(f"{'Literal':<15} {'Value':<15} {'Length':<10} {'Address':<10}")
        print("="*50)
        
        # Traverse the list and display each literal
        current = self.head
        while current is not None:
            literal = current.literal_data
            print(f"{literal.name:<15} {literal.value:<15} {literal.length:<10} {literal.address:<10}")
            current = current.next

    def display_log(self):
        """
        Display the log of actions performed on the literal table.
        """
        if not self.log_entries:
            print("No actions have been logged yet.")
        else:
            print("Literal Table Log:")
            for entry in self.log_entries:
                print(entry)

    def display_errors(self):
        """
        Display any errors encountered during literal table processing.
        """
        if not self.errors:
            print("No errors encountered during literal table processing.")
        else:
            print("Literal Table Errors:")
            for error in self.errors:
                print(f"[ERROR]: {error}")

    def _log_action(self, message):
        """
        Log an action performed on the literal table.
        
        :param message: The action message to be logged.
        """
        self.log_entries.append(f"[ACTION]: {message}")

    def _log_error(self, error_message):
        """
        Log an error encountered during literal table processing.
        
        :param error_message: The error message to be logged.
        """
        self.errors.append(error_message)
        self._log_action(f"Error encountered: {error_message}")



def main():
    """
    /********************************************************************
    ***  FUNCTION : main                                              ***
    ***  CLASS  :                                                     ***
    *********************************************************************
    ***  DESCRIPTION: Main function that initializes and runs the app ***
    ***  with optional command-line arguments. If a search file is     ***
    ***  provided as a command-line argument, it is used; otherwise,   ***
    ***  the program asks for the search file name interactively.      ***
    ********************************************************************/
    """
    try:
        driver = SymbolTableDriver()
        driver.build_symbol_table()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()