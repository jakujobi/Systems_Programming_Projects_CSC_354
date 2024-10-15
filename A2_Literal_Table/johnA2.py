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

# run 
# cd .\Systems_Programming_Projects_CSC_354\A2_Literal_Table; python johnA2.py Express.DAT

import sys
import os
from symbol_table_builder import SymbolTableDriver, SymbolData, SymbolTable, Validator, FileExplorer



class LiteralData:
    """
    Class to represent a literal with its name, value, length, and address.
    """
    def __init__(self, name: str, value: str, length: int):
        """
        Initialize a literal with its name, value, length, and address.

        :param name: Name of the literal (e.g., '=X'05A'').
        :param value: Hexadecimal value of the literal.
        :param length: Length of the literal in bytes.
        :raises ValueError: If name, value, or length is invalid.
        """
        if not name or not value or length <= 0:
            raise ValueError("Invalid literal data: ensure the name is provided, value is not empty, and length is positive.")
        
        self.name: str = name
        self.value: str = value.upper()  # Normalize value
        self.length: int = length
        self.address: int = None  # Address will be assigned later



class LiteralNode:
    """
    Class to represent a node in the linked list of literals.
    Each node contains LiteralData and a reference to the next node.
    """
    def __init__(self, literal_data: LiteralData):
        """
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
    Class to represent the literal table, stored as a linked list.
    This class provides methods to insert literals, update their addresses,
    and display the literal table.
    """
    def __init__(self, log_handler):
        """
        Initialize the literal table with an empty linked list and a log handler.

        :param log_handler: An instance of ErrorLogHandler for logging actions and errors.
        """
        self.head: LiteralNode = None
        self.log_handler = log_handler

    def insert(self, literal_data: LiteralData):
        """
        Insert a new literal into the linked list.

        :param literal_data: An instance of LiteralData to be inserted.
        """
        if not isinstance(literal_data, LiteralData):
            self.log_handler.log_error("Cannot insert: Invalid LiteralData object.")
            return

        if self._find_literal(literal_data.name):
            self.log_handler.log_error(f"Duplicate literal insertion error: The literal '{literal_data.name}' already exists.")
            return

                    # Check if a literal with the same value already exists
        if self.exists_by_value(literal_data.value, literal_data.name):
            self.log_handler.log_action(f"Literal '{literal_data.name}' with value '{literal_data.value}' already exists. Skipping insertion.")
            return
    
        new_node = LiteralNode(literal_data)
        if self.head is None:
            self.head = new_node
            self.log_handler.log_action(f"Inserted literal '{literal_data.name}' as head.")
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            self.log_handler.log_action(f"Inserted literal '{literal_data.name}' into the table.")

    def exists_by_value(self, value: str, name: str) -> bool:
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


    def insert_sorted(self, literal_data: LiteralData):
        """
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
        Search for a literal by its name in the literal table.

        :param literal_name: The name of the literal to search for.
        :return: The LiteralData object if found, or None if not found.
        """
        current = self.head
        while current is not None:
            if current.literal_data.name == literal_name:
                self.log_handler.log_action(f"Found literal '{literal_name}' in the table.")
                return current.literal_data
            current = current.next
        self.log_handler.log_action(f"Literal '{literal_name}' not found in the table.")
        return None

    def update_addresses(self, start_address: int = 0):
        """
        Assign addresses to literals sequentially without sorting, retaining the order 
        in which they were encountered in the linked list.
        
        :param start_address: The starting address for the first literal (default is 0).
        """
        if start_address < 0:
            self.log_handler.log_error("Invalid starting address. Addresses cannot be negative.")
            return

        if self.head is None:
            self.log_handler.log_error("Update failed: The literal table is empty.")
            return

        current = self.head
        current_address = start_address

        while current:
            current.literal_data.address = current_address
            self.log_handler.log_action(f"Assigned address {current_address} to literal '{current.literal_data.name}'.")
            current_address += 1  # Increment address by 1 regardless of length
            current = current.next


    def display_literals(self):
        """
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
    
    def press_continue(self):
        """
        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')


class ErrorLogHandler:
    """
    Class to handle both logging actions and error messages throughout the program.
    Provides mechanisms to log actions, log errors, retrieve logs, and display all messages.
    """
    def __init__(self):
        """
        Initialize the ErrorLogHandler with empty logs for actions and errors.
        """
        self.log_entries: list[str] = []
        self.error_log: list[str] = []

    def log_action(self, message: str):
        """
        Log an action performed during the program's execution.

        :param message: The message describing the action.
        """
        self.log_entries.append(f"[ACTION]: {message}")
        print(f"[ACTION]: {message}")

        # Paginate after every 18 lines of actions
        if len(self.log_entries) % 18 == 0:
            self.paginate_output(self.log_entries, "Displaying Actions Log")

    def log_error(self, error_message: str, context_info: str = None):
        """
        Log an error message with optional context information for better clarity.

        :param error_message: The error message to be logged.
        :param context_info: Additional context about where the error occurred (optional).
        """
        full_message = f"[ERROR] {context_info}: {error_message}" if context_info else f"[ERROR]: {error_message}"
        self.error_log.append(full_message)
        print(full_message)  # Immediate feedback for critical errors

        # Paginate after every 18 lines of errors
        if len(self.error_log) % 18 == 0:
            self.paginate_output(self.error_log, "Displaying Error Log")
            
            
    def display_log(self):
        """
        Ask the user if they want to view the log entries. Paginate if they agree.
        """
        if not self.log_entries:
            print("No actions have been logged.")
        else:
            if self.ask_to_display("Do you want to view the log entries?"):
                print("\nLog of Actions:")
                print("=" * 50)
                self.paginate_output(self.log_entries, "Log of Actions")

    def display_errors(self):
        """
        Ask the user if they want to view the error logs. Paginate if they agree.
        """
        if not self.error_log:
            print("No errors have been logged.")
        else:
            if self.ask_to_display("Do you want to view the error log?"):
                print("\nError Log:")
                print("=" * 50)
                self.paginate_output(self.error_log, "Error Log")

    def ask_to_display(self, question: str) -> bool:
        """
        Ask the user if they want to display the logs/errors with retry logic for invalid inputs.

        :param question: The question to ask the user.
        :return: True if the user agrees to display, False otherwise.
        """
        valid_yes = {'y', 'yes', '', 'Y', 'YES', 'YeS'}
        valid_no = {'n', 'no', 'N', 'NO'}
        retry_limit = 5
        retries = 0

        while retries < retry_limit:
            user_input = input(f"{question} (y/n): ").strip()
            if user_input in valid_yes:
                return True
            elif user_input in valid_no:
                return False
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")
                retries += 1

        # If the user reaches the retry limit, display an "annoyed" message and skip the logs/errors
        print("Seriously? You can't just type 'y' or 'n'? Fine, I won't show it.")
        return False

    def paginate_output(self, log_entries, header: str):
        """
        Paginate the log/error output to prevent excessive scrolling.
        
        :param log_entries: The log or error entries to be displayed.
        :param header: The header for the log/error output.
        """
        counter = 0
        for entry in log_entries:
            print(entry)
            counter += 1
            if counter % 18 == 0:
                self.press_continue()

    def press_continue(self):
        """
        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')  # Clear the line after pressing enter to clean the screen

    def clear_logs(self):
        """
        Clear all logs of actions and errors.
        """
        self.log_entries.clear()
        self.error_log.clear()

    def has_errors(self) -> bool:
        """
        Check if there are any logged errors.

        :return: True if there are errors, False otherwise.
        """
        return bool(self.error_log)


class ExpressionParser:
    """
    Class responsible for parsing assembly expressions and literals.
    
    Attributes:
        expressions_lines (list): List of raw expression lines.
        parsed_expressions (list): List of dictionaries representing parsed expressions.
        literal_table (LiteralTableList): Reference to the literal table.
        log_handler (ErrorLogHandler): Reference to the error log handler.
    """
    
    def __init__(self, expressions_lines, literal_table, log_handler):
        """
        Initializes the parser with a list of expression lines, a literal table, and an error log handler.
        
        Args:
            expressions_lines (list): List of raw expression lines from the file.
            literal_table (LiteralTableList): Reference to the literal table.
            log_handler (ErrorLogHandler): Reference to the error log handler.
        """
        self.expressions_lines = expressions_lines
        self.parsed_expressions = []
        self.literal_table = literal_table
        self.log_handler = log_handler
        self.invalid_literals_set = set()  # Track invalid literals

    def parse_all(self):
        """
        Parses all expression lines and stores the parsed expressions in parsed_expressions.
        Logs actions and errors as necessary.
        """
        for line in self.expressions_lines:
            parsed_expr = self.parse_line(line)
            if parsed_expr:
                if parsed_expr.get('error'):
                    self.log_handler.log_error(parsed_expr['error'], context_info=parsed_expr['original_expression'])
                else:
                    self.log_handler.log_action(f"Parsed expression: {parsed_expr['original_expression']}")
                self.parsed_expressions.append(parsed_expr)

    def parse_line(self, line):
        """
        Parses a single line into a structured expression and handles literals.
        
        Args:
            line (str): A single line of expression.
        
        Returns:
            dict: A dictionary containing parsed expression details.
        """
        parsed_expr = {
            'original_expression': line.strip(),
            'addressing_mode': 'DIRECT',  # Default addressing mode
            'operator': None,
            'operand1': None,
            'operand2': None,
            'indexing': False,
            'error': None
        }

        # Trim leading and trailing whitespaces
        line = line.strip()

        # Ignore empty lines
        if not line:
            return None

        # Handle addressing modes
        if line.startswith('@'):
            parsed_expr['addressing_mode'] = 'INDIRECT'
            line = line[1:].strip()
        elif line.startswith('#'):
            parsed_expr['addressing_mode'] = 'IMMEDIATE'
            line = line[1:].strip()

        # Check for indexed addressing mode
        if line[-2:].upper() == ',X': 
            parsed_expr['indexing'] = True
            line = line[:-2].strip()
            
        # Error: Invalid combination of addressing mode and indexing
        if parsed_expr['indexing'] and parsed_expr['addressing_mode'] in ['IMMEDIATE', 'INDIRECT']:
            parsed_expr['error'] = f"{parsed_expr['addressing_mode'][0]} and x ERROR"
            return parsed_expr

        # Handle literals
        if line.startswith('='):
            literal_name = line
            literal = self.literal_table.search(literal_name)
            if not literal:
                try:
                    # Check for illegal character literal format =C'123'
                    if literal_name.upper().startswith("=C'"):
                        raise ValueError(f"Illegal literal format: {literal_name}")

                    
                    # Handle hexadecimal literals
                    if literal_name.upper().startswith("=0X"):
                        literal_value = literal_name[3:]  # Remove the "=0X" part
                        literal_value = literal_value.upper()  # Convert to uppercase

                        # Validate hexadecimal format
                        if not all(c in '0123456789ABCDEFabcdef' for c in literal_value):
                            raise ValueError(f"Invalid hexadecimal value: {literal_value}")

                        # Validate length (must be even to form complete bytes)
                        if len(literal_value) % 2 != 0:
                            raise ValueError(f"Hexadecimal value length is not valid (must be even): {literal_value}")

                        literal_length = len(literal_value) // 2  # Two characters per byte

                    # Handle character literals
                    elif literal_name.upper().startswith("=0C") or literal_name.upper().startswith("=C'"):
                        if literal_name.upper().startswith("=0C"):
                            char_sequence = literal_name[3:]  # Remove the "=0C" part
                        else:
                            if not (literal_name.endswith("'") and len(literal_name) > 4):
                                raise ValueError(f"Invalid character literal format: {literal_name}")
                            char_sequence = literal_name[3:-1]  # Extract characters inside C'...'

                        if len(char_sequence) == 0:
                            raise ValueError(f"Character literal is empty: {literal_name}")

                        literal_value = ''.join(f"{ord(c):02X}" for c in char_sequence)
                        literal_length = len(char_sequence)

                    else:
                        # Invalid literal format
                        raise ValueError(f"Invalid literal format: {literal_name}")

                    # Insert literal into the literal table
                    new_literal = LiteralData(name=literal_name, value=literal_value, length=literal_length)
                    self.literal_table.insert(new_literal)

                    parsed_expr['operand1'] = literal_name
                    self.log_handler.log_action(f"Inserted new literal '{literal_name}'")
                except ValueError as e:
                    # Capture any validation errors and mark them as "ERROR" in the expression table
                    parsed_expr['error'] = str(e)
                    #self.log_handler.log_error(parsed_expr['error'], context_info=literal_name)
                    
                    # Check if this invalid literal has already been processed
                    if literal_name in self.invalid_literals_set:
                        return None  # Skip duplicate invalid literals
                    else:
                        # Add to invalid literal set
                        self.invalid_literals_set.add(literal_name)
                        self.log_handler.log_error(parsed_expr['error'], context_info=literal_name)
                        return parsed_expr  # Return the invalid literal as an error

            else:
                parsed_expr['operand1'] = literal_name
                self.log_handler.log_action(f"Used existing literal '{literal_name}'")

            return parsed_expr

        # Continue with normal parsing for non-literal expressions
        # Split operands and operator
        if '+' in line:
            parsed_expr['operator'] = '+'
            operands = line.split('+')
        elif '-' in line:
            parsed_expr['operator'] = '-'
            operands = line.split('-')
        else:
            operands = [line]

        # Remove parentheses if present
        operands = [operand.strip('()').strip() for operand in operands]

        # Assign operands
        if len(operands) == 1:
            parsed_expr['operand1'] = operands[0]
        elif len(operands) == 2:
            parsed_expr['operand1'], parsed_expr['operand2'] = operands
        else:
            parsed_expr['error'] = f"Invalid expression format: {line}"
            return parsed_expr

        # Validate operands
        if not parsed_expr['operand1']:
            parsed_expr['error'] = "Missing first operand."
        elif parsed_expr['operator'] and not parsed_expr['operand2']:
            parsed_expr['error'] = "Missing second operand."

        return parsed_expr


    def get_parsed_expressions(self):
        """
        Returns the parsed expressions.
        
        Returns:
            list: List of parsed expressions.
        """
        return self.parsed_expressions



class ExpressionEvaluator:
    """
    Class responsible for evaluating parsed expressions.
    
    Attributes:
        parsed_expressions (list): List of parsed expressions from ExpressionParser.
        symbol_table (SymbolTable): Reference to the symbol table.
        literal_table (LiteralTableList): An object handling literal management.
        evaluated_expressions (list): List of evaluated expressions with their results.
        log_handler (ErrorLogHandler): Reference to the error log handler.
    """
    
    def __init__(self, parsed_expressions, symbol_table, literal_table, log_handler):
        """
        Initializes the evaluator with parsed expressions, symbol table, literal table, and log handler.
        
        Args:
            parsed_expressions (list): List of parsed expressions.
            symbol_table (SymbolTable): Reference to the symbol table.
            literal_table (LiteralTableList): Literal table for managing literals.
            log_handler (ErrorLogHandler): Reference to the error log handler.
        """
        self.parsed_expressions = parsed_expressions
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.evaluated_expressions = []
        self.log_handler = log_handler

    def evaluate_all(self):
        """
        Evaluates all parsed expressions and stores the results in evaluated_expressions.
        Logs actions and errors as necessary.
        """
        for parsed_expr in self.parsed_expressions:
            if parsed_expr:
                evaluated_expr = self.evaluate_expression(parsed_expr)
                if evaluated_expr.get('error'):
                    self.log_handler.log_error(evaluated_expr['error'], context_info=parsed_expr['original_expression'])
                else:
                    self.log_handler.log_action(f"Evaluated expression: {parsed_expr['original_expression']}")
                self.evaluated_expressions.append(evaluated_expr)

    def evaluate_expression(self, parsed_expr):
        """
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
        Returns the evaluated expressions.
        
        Returns:
            list: List of evaluated expressions with results.
        """
        return self.evaluated_expressions


class ExpressionResults:
    """
    Class responsible for formatting and outputting evaluated expression results.
    
    Attributes:
        evaluated_expressions (list): List of evaluated expressions.
        log_handler (ErrorLogHandler): Reference to the error log handler.
    """
    
    def __init__(self, evaluated_expressions, log_handler):
        """
        Initializes the result handler with evaluated expressions and log handler.
        
        Args:
            evaluated_expressions (list): List of evaluated expressions.
            log_handler (ErrorLogHandler): Reference to the error log handler.
        """
        self.evaluated_expressions = evaluated_expressions
        self.log_handler = log_handler

    def display_results(self, include_literals=True):
        """
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
        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')


class LiteralTableDriver:
    """
    Main driver class to handle the literal table operations and overall program flow.
    """
    def __init__(self):
        """
        Initialize the LiteralTableDriver with all necessary components.
        """
        self.log_handler = ErrorLogHandler()  # Combined error and action logging
        self.literal_table = LiteralTableList(self.log_handler)  # Pass log_handler to LiteralTableList
        self.symbol_table_driver = SymbolTableDriver()  # Use SymbolTableDriver to manage symbol table
        self.file_explorer = FileExplorer()  # File handling for locating files

    def run(self, expression_file: str = None):
        """
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
            self.log_handler.log_error(f"Unexpected error occurred: {e}")

    def build_symbol_table(self):
        """
        Build the symbol table using SymbolTableDriver.
        """
        try:
            self.log_handler.log_action("Building symbol table from SYMS.DAT")
            self.symbol_table_driver.build_symbol_table()
            self.symbol_table = self.symbol_table_driver.symbol_table
            self.log_handler.log_action("Symbol table building complete")
        except Exception as e:
            self.log_handler.log_error(f"Error while building symbol table: {e}")

    def get_expression_file(self) -> str:
        """
        Determine the expression file to use, either from the command line or default to 'EXPRESS.DAT'.
        
        :return: The name of the expression file.
        """
        return sys.argv[1] if len(sys.argv) > 1 else "EXPR.DAT"

    def load_expressions(self, file_name: str) -> list[str]:
        """
        Load expressions from the specified file.

        :param file_name: The name of the file containing expressions.
        :return: A list of expressions.
        """
        try:
            expressions = self.file_explorer.process_file(file_name)
            if not expressions:
                raise ValueError(f"The file '{file_name}' is empty. Please provide a valid file with expressions.")
            self.log_handler.log_action(f"Expressions loaded successfully from {file_name}.")
            return expressions
        except FileNotFoundError:
            self.log_handler.log_error(f"File '{file_name}' not found.")
            return []
        except Exception as e:
            self.log_handler.log_error(f"Error while loading expressions from {file_name}: {e}")
            return []

    def parse_expressions(self, expressions: list[str]) -> list[dict]:
        """
        Parse expressions into structured components.

        :param expressions: List of raw expression strings.
        :return: A list of parsed expression dictionaries.
        """
        parser = ExpressionParser(expressions, self.literal_table, self.log_handler)
        parser.parse_all()
        parsed_expressions = parser.get_parsed_expressions()
        self.log_handler.log_action(f"Parsed {len(parsed_expressions)} expressions.")
        return parsed_expressions

    def evaluate_expressions(self, parsed_expressions: list[dict]):
        """
        Evaluate parsed expressions and update the literal table with new literals.

        :param parsed_expressions: A list of parsed expression components.
        """
        evaluator = ExpressionEvaluator(
            parsed_expressions,
            self.symbol_table_driver.symbol_table,
            self.literal_table,
            self.log_handler
        )
        evaluator.evaluate_all()
        self.evaluated_expressions = evaluator.get_evaluated_expressions()

        # Update literal addresses
        self.literal_table.update_addresses(start_address=0)
        self.log_handler.log_action("Expressions evaluated and literal table updated.")

    def paginate_output(self, display_function, header: str):
        """
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
        Display all the results including literals, logs, and errors with paginated output.
        """
        # Display evaluated expressions
        results_display = ExpressionResults(self.evaluated_expressions, self.log_handler)
        self.paginate_output(lambda: results_display.display_results(include_literals=False), "Displaying Evaluated Expressions:")

        # Display the literal table
        self.paginate_output(self.literal_table.display_literals, "Displaying Literal Table:")

        # Display logs and errors
        self.paginate_output(self.log_handler.display_log, "Displaying Log Entries:")
        self.paginate_output(self.log_handler.display_errors, "Displaying Errors:")



def main():
    # Create an instance of LiteralTableDriver and run it
    expression_file = sys.argv[1] if len(sys.argv) > 1 else None
    driver = LiteralTableDriver()
    driver.run(expression_file)


if __name__ == "__main__":
    main()