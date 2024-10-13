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
        self.value: str = value
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
        Assign addresses to literals sequentially. If the table is empty, log an error.

        :param start_address: The starting address for the first literal.
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
            current_address += current.literal_data.length
            current = current.next

    def display_literals(self):
        """
        Display all the literals in the table in a formatted manner.
        """
        if self.head is None:
            print("Literal table is empty. No literals to display.")
            return
        print("┏" + ("━" * 50) + "┓")
        print(f"┃{' LITERAL TABLE':^50}┃")
        print("┣" + ("━" * 15) + "┯" + ("━" * 15) + "┯" + ("━" * 8) + "┯" + ("━" * 9) + "┫")
        print(f"┃ {'Literal':^13} │ {'Value':^13} │ {'Length':^6} │ {'Address':^7} ┃")
        print("┣" + ("━" * 15) + "┿" + ("━" * 15) + "┿" + ("━" * 8) + "┿" + ("━" * 9) + "┫")        
        current = self.head
        counter = 0
        while current:
            literal = current.literal_data
            address_display = literal.address if literal.address is not None else "N/A"  # Handle NoneType address
            print(f"┃ {literal.name:^13} │ {literal.value:^13} │ {literal.length:^6} │ {address_display:^7} ┃")
            counter += 1
            if counter % 18 == 0:
                self.press_continue()
            current = current.next
        print("┗" + ("━" * 15) + "┷" + ("━" * 15) + "┷" + ("━" * 8) + "┷" + ("━" * 9) + "┛")

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

    def log_error(self, error_message: str, context_info: str = None):
        """
        Log an error message with optional context information for better clarity.

        :param error_message: The error message to be logged.
        :param context_info: Additional context about where the error occurred (optional).
        """
        full_message = f"[ERROR] {context_info}: {error_message}" if context_info else f"[ERROR]: {error_message}"
        self.error_log.append(full_message)
        print(full_message)  # Immediate feedback for critical errors

    def display_log(self):
        """
        Display all logged actions in a user-friendly format.
        """
        if not self.log_entries:
            print("No actions have been logged.")
        else:
            print("\nLog of Actions:")
            print("=" * 50)
            print("\n".join(self.log_entries))

    def display_errors(self):
        """
        Display all logged error messages in a user-friendly format.
        """
        if not self.error_log:
            print("No errors have been logged.")
        else:
            print("\nError Log:")
            print("=" * 50)
            print("\n".join(f"{index + 1}. {error}" for index, error in enumerate(self.error_log)))

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

        # Check for indexed addressing mode (e.g., "GREEN,X")
        if ',X' in line:
            parsed_expr['indexing'] = True
            line = line.replace(',X', '').strip()

        # Handle literals (e.g., "=0X5A")
        if line.startswith('='):
            literal_name = line
            literal = self.literal_table.search(literal_name)
            if not literal:
                try:
                    # Extract the value part after '=0X' or '=0x'
                    if literal_name.upper().startswith("=0X"):
                        literal_value = literal_name[3:]  # Remove the "=0X" part
                    else:
                        literal_value = literal_name[1:]  # Handle other possible cases

                    # Assuming hexadecimal literal, length is two characters per byte
                    literal_length = len(literal_value) // 2  # Two characters per byte

                    # Insert literal into the literal table
                    new_literal = LiteralData(name=literal_name, value=literal_value, length=literal_length)
                    self.literal_table.insert(new_literal)

                    parsed_expr['operand1'] = literal_name
                    self.log_handler.log_action(f"Inserted new literal '{literal_name}'")
                except ValueError as e:
                    parsed_expr['error'] = f"Failed to insert literal '{literal_name}': {str(e)}"
            else:
                parsed_expr['operand1'] = literal_name
                self.log_handler.log_action(f"Used existing literal '{literal_name}'")

            return parsed_expr

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
                # Convert the hexadecimal literal value (stored as string) to an integer
                try:
                    return int(literal.value, 16), False, None  # Literal values are absolute
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
            rflag1 (bool): RFLAG of the first operand.
            operator (str): Operation ('+' or '-').
            rflag2 (bool): RFLAG of the second operand.
        
        Returns:
            tuple: (relocatable_flag, error_message) - returns error_message if an error occurs.
        """
        if operator == '+':
            if not rflag1 and not rflag2:
                return False, None
            elif not rflag1 and rflag2:
                return True, None
            elif rflag1 and not rflag2:
                return True, None
            else:
                return None, "Error: Cannot add two relocatable values."
        elif operator == '-':
            if not rflag1 and not rflag2:
                return False, None
            elif not rflag1 and rflag2:
                return None, "Error: Cannot subtract relocatable value from absolute."
            elif rflag1 and not rflag2:
                return True, None
            elif rflag1 and rflag2:
                return False, None
        return None, "Error: Invalid operation."

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

    def display_results(self):
        """
        Formats and outputs the expression evaluation results in a table-like format.
        Logs actions when results are displayed.
        """
        if not self.evaluated_expressions:
            print("No expressions to evaluate.")
            return
        
        # Table Header
        print("┏" + ("━" * 66) + "┓")
        print(f"┃{'EXPRESSION RESULTS':^66}┃")
        print("┣" + ("━" * 20) + "┯" + ("━" * 7) + "┯" + ("━" * 13) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┯" + ("━" * 7) + "┫")
        print(f"┃ {'Expression':^18} │ {'Value':^5} │ {'Relocatable':^10} │ {'N-Bit':^3} │ {'I-Bit':^3} │ {'X-Bit':^3} ┃")
        print("┣" + ("━" * 20) + "┿" + ("━" * 7) + "┿" + ("━" * 13) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┿" + ("━" * 7) + "┫")

        # Table Body
        for expr in self.evaluated_expressions:
            result_line = self.format_expression_result(expr)
            print(result_line)

        # Table Footer
        print("┗" + ("━" * 20) + "┷" + ("━" * 7) + "┷" + ("━" * 13) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┷" + ("━" * 7) + "┛")

    def format_expression_result(self, evaluated_expr):
        """
        Formats a single evaluated expression into a readable string.
        
        Args:
            evaluated_expr (dict): Evaluated expression with its results.
        
        Returns:
            str: Formatted string for display.
        """
        if evaluated_expr['error']:
            return f"┃ {evaluated_expr['original_expression']:^18} │ {'ERROR':^5} │ {'-':^11} │ {'-':^5} │ {'-':^5} │ {'-':^5} ┃"
        else:
            value = evaluated_expr['value']
            relocatable = 'RELATIVE' if evaluated_expr['relocatable'] else 'ABSOLUTE'
            return (f"┃ {evaluated_expr['original_expression']:^18} │ {value:^5} │ {relocatable:^11} │ "
                    f"{evaluated_expr['n_bit']:^5} │ {evaluated_expr['i_bit']:^5} │ {evaluated_expr['x_bit']:^5} ┃")





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
                self.evaluate_and_insert_literals(parsed_expressions)
                self.update_addresses()
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
            self.log_handler.log_action("Symbol table building complete")
        except Exception as e:
            self.log_handler.log_error(f"Error while building symbol table: {e}")

    def get_expression_file(self) -> str:
        """
        Determine the expression file to use, either from the command line or default to 'EXPRESS.DAT'.
        
        :return: The name of the expression file.
        """
        return sys.argv[1] if len(sys.argv) > 1 else "EXPRESS.DAT"

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
        parser = ExpressionParser(Validator(), self.log_handler)
        parsed_expressions = parser.parse_expressions(expressions)
        self.log_handler.log_action(f"Parsed {len(parsed_expressions)} expressions.")
        return parsed_expressions

    def evaluate_and_insert_literals(self, parsed_expressions: list[dict]):
        """
        Evaluate parsed expressions and update the literal table with new literals.

        :param parsed_expressions: A list of parsed expression components.
        """
        evaluator = ExpressionEvaluator(
            self.symbol_table_driver.symbol_table,
            self.literal_table,
            Validator(),
            self.log_handler
        )
        evaluation_results = evaluator.evaluate_expressions(parsed_expressions)

        for result in evaluation_results:
            if result['expression'].startswith('='):
                literal = LiteralData(result['expression'], result['value'], result['length'])
                self.literal_table.insert(literal)

        self.log_handler.log_action("Expressions evaluated and literal table updated.")

    def update_addresses(self):
        """
        Update the addresses of the literals in the table, starting from a base address.
        """
        try:
            start_address = 0
            self.literal_table.update_addresses(start_address)
            self.log_handler.log_action(f"Updated addresses starting from {start_address}.")
        except Exception as e:
            self.log_handler.log_error(f"Unexpected error while updating addresses: {e}")

    def display_results(self):
        """
        Display all the results including literals, logs, and errors with paginated output.
        """
        self.paginate_output(self.literal_table.display_literals, "Displaying Literal Table:")
        print ("\n\nLog Summary")
        self.paginate_output(self.log_handler.display_log, "Displaying Log Entries:")
        self.paginate_output(self.log_handler.display_errors, "Displaying Errors:")

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


# # Main function
# if __name__ == "__main__":
#     # Create an instance of LiteralTableDriver and run it
#     expression_file = sys.argv[1] if len(sys.argv) > 1 else None
#     driver = LiteralTableDriver()
#     driver.run(expression_file)



def main():
    # Initialize the error log handler
    log_handler = ErrorLogHandler()
    symbol_table_driver = SymbolTableDriver()  # Use SymbolTableDriver to manage symbol table

    symbol_table_driver.build_symbol_table()
    symbol_table = symbol_table_driver.symbol_table

    # Initialize the literal table
    literal_table = LiteralTableList(log_handler)

    file_explorer = FileExplorer()
    filename = sys.argv[1] if len(sys.argv) > 1 else "EXPRESS.DAT"
    expressions_lines = file_explorer.process_file(filename)

    # Step 1: Parse the expressions
    parser = ExpressionParser(expressions_lines, literal_table, log_handler)
    parser.parse_all()
    parsed_expressions = parser.get_parsed_expressions()

    # Step 2: Evaluate the parsed expressions
    evaluator = ExpressionEvaluator(parsed_expressions, symbol_table, literal_table, log_handler)
    evaluator.evaluate_all()
    evaluated_expressions = evaluator.get_evaluated_expressions()

    # Step 3: Display the evaluation results
    results_display = ExpressionResults(evaluated_expressions, log_handler)
    results_display.display_results()

    # Step 4: Display the literal table
    # Step 4: Update the literal table addresses (before displaying the table)
    literal_table.update_addresses(start_address=0)
    print("\nLiteral Table:")
    literal_table.display_literals()

    # Step 5: Display the logs (actions and errors)
    print("\nLogs:")
    log_handler.display_log()

    print("\nError Logs:")
    log_handler.display_errors()


if __name__ == "__main__":
    main()
