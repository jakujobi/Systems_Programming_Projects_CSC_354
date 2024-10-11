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

from symbol_table_builder import SymbolTableDriver, SymbolData, SymbolTable, Validator, FileExplorer



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
            self._log_error("Cannot insert: Invalid LiteralData object. Please ensure the data passed is a LiteralData object.")
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
                    self._log_error(f"Error! I can't allow duplicate entries. "
                                    f"The literal '{literal_data.name}' already exists in the table. ")
                    return
                current = current.next
            
            # Insert at the end of the list
            if current.literal_data.name == literal_data.name:
                self._log_error(f"Duplicate literal insertion error: "
                                f"The literal '{literal_data.name}' already exists in the table.")
            else:
                current.next = LiteralNode(literal_data)
                self._log_action(f"Inserted literal '{literal_data.name}' into the table. Yay!")

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
        # Add an action entry for easier tracking in log history
        self._log_action(f"Error encountered: {error_message}")



class ErrorHandler:
    """
    Class to handle errors throughout the program, providing mechanisms to log, retrieve,
    and display error messages in a user-friendly manner.
    """
    def __init__(self):
        """
        Initialize the ErrorHandler with an empty list of error messages.
        """
        self.error_log = []  # Stores error messages

    def log_error(self, error_message, context_info=None):
        """
        Log an error message with optional context information for better clarity.

        :param error_message: The error message to be logged.
        :param context_info: Additional context about where the error occurred (optional).
        """
        if context_info:
            full_message = f"Error in {context_info}: {error_message}"
        else:
            full_message = f"Error: {error_message}"

        # Add the formatted error message to the log
        self.error_log.append(full_message)
        print(f"[ERROR] {full_message}")  # Immediate feedback to the user for critical errors

    def display_errors(self):
        """
        Display all logged error messages in a user-friendly format.
        """
        if not self.error_log:
            print("No errors have been logged.")
        else:
            print("\nError Log:")
            print("============")
            for index, error in enumerate(self.error_log, start=1):
                print(f"{index}. {error}")

    def clear_errors(self):
        """
        Clear all logged errors.
        """
        self.error_log = []

    def has_errors(self):
        """
        Check if there are any logged errors.

        :return: True if there are errors, False otherwise.
        """
        return len(self.error_log) > 0



class ExpressionParser:
    """
    Class to parse expressions from a file and break them down into operands and operators.
    Handles different addressing modes and logs actions or errors encountered during parsing.
    """
    def __init__(self, file_explorer, validator, error_handler):
        """
        Initialize the ExpressionParser with file handling and validation tools.

        :param file_explorer: An instance of FileExplorer to handle file operations.
        :param validator: An instance of Validator for validating expressions.
        :param error_handler: An instance of ErrorHandler for logging errors.
        """
        self.file_explorer = file_explorer
        self.validator = validator
        self.error_handler = error_handler
        self.log_entries = []  # Stores logs of parsing actions

    def parse_expressions(self, file_path):
        """
        Parse all expressions from a given file and return a list of structured expression data.

        :param file_path: The path to the file containing expressions (e.g., EXPRESS.DAT).
        :return: A list of dictionaries with parsed expression components.
        """
        try:
            # Read lines from the provided file path using FileExplorer
            lines = self.file_explorer.process_file(file_path)
            if not lines:
                self.log_error(f"The file '{file_path}' is empty. Please provide a valid file with expressions.")
                return []

            parsed_expressions = []

            for line_number, line in enumerate(lines, start=1):
                result = self.parse_expression(line, line_number)
                if result:
                    parsed_expressions.append(result)
                    self.log_action(f"Successfully parsed expression on line {line_number}: {line.strip()}")
                else:
                    self.log_error(f"Failed to parse expression on line {line_number}: '{line.strip()}'. Please check the syntax.")

            return parsed_expressions

        except FileNotFoundError:
            self.log_error(f"File '{file_path}' not found. Please provide a valid file path.")
            return []
        except PermissionError:
            self.log_error(f"Permission denied for file '{file_path}'. Please check your file permissions.")
            return []
        except Exception as e:
            self.log_error(f"An unexpected error occurred while parsing expressions: {str(e)}")
            return []

    def parse_expression(self, expression_line, line_number):
        """
        Parse a single line of expression into operands and operators.

        :param expression_line: A single line containing an expression (e.g., 'A + B').
        :param line_number: The line number in the file for reference in error handling.
        :return: A dictionary with the parsed components (e.g., {'operand1': 'A', 'operator': '+', 'operand2': 'B'}).
        """
        expression_line = expression_line.strip()

        if not expression_line:
            self.log_error(f"Empty expression line at line {line_number}. Skipping...")
            return None

        try:
            # Tokenize the expression into operands and operators
            operand1, operator, operand2 = self.tokenize_expression(expression_line, line_number)

            # Validate the parsed operands and operators
            if not self.validator.validate_symbol(operand1):
                self.log_error(f"Invalid operand1 '{operand1}' at line {line_number}. Check for correct syntax.")
                return None

            if operand2 and not (self.validator.validate_symbol(operand2) or operand2.isnumeric()):
                self.log_error(f"Invalid operand2 '{operand2}' at line {line_number}. Check for correct syntax.")
                return None

            return {
                'original_expression': expression_line,
                'operand1': operand1,
                'operator': operator,
                'operand2': operand2
            }

        except ValueError as e:
            self.log_error(f"Error while parsing expression on line {line_number}: {str(e)}")
            return None
        except Exception as e:
            self.log_error(f"Unexpected error while parsing line {line_number}: {str(e)}")
            return None

    def tokenize_expression(self, expression_line, line_number):
        """
        Tokenize an expression line into its components (operands and operator).
        Handles special cases for addressing modes (#, @, ,X).

        :param expression_line: The expression line to be tokenized.
        :param line_number: The line number in the file for reference in error handling.
        :return: Tuple (operand1, operator, operand2).
        """
        try:
            # Split the line into tokens based on whitespace and operator symbols
            tokens = expression_line.replace(',', ' ,').split()

            if len(tokens) == 1:
                # Single operand (e.g., '#5' or '@VAR')
                return tokens[0], None, None

            elif len(tokens) == 3:
                # Expression with an operator (e.g., 'A + B')
                return tokens[0], tokens[1], tokens[2]

            elif len(tokens) == 2 and tokens[1] == ',X':
                # Handle indexed addressing mode (e.g., 'VAR, X')
                return tokens[0] + tokens[1], None, None

            elif len(tokens) == 2:
                # Handle cases like '#NUM'
                return tokens[0], None, tokens[1]

            else:
                raise ValueError(f"Unrecognized expression format at line {line_number}. Ensure correct syntax with operands and operators.")

        except IndexError:
            raise ValueError(f"Malformed expression at line {line_number}. Missing operands or operator.")
        except Exception as e:
            raise ValueError(f"Unexpected error during tokenization at line {line_number}: {str(e)}")

    def log_action(self, message):
        """
        Log a successful parsing action.

        :param message: The message to be logged.
        """
        self.log_entries.append(f"[ACTION]: {message}")

    def log_error(self, error_message):
        """
        Log an error encountered during expression parsing.

        :param error_message: The error message to be logged.
        """
        self.error_handler.log_error(f"[ERROR]: {error_message}")
        self.log_entries.append(f"[ERROR]: {error_message}")

    def display_log(self):
        """
        Display the log of actions performed during parsing.
        """
        if not self.log_entries:
            print("No parsing actions have been logged.")
        else:
            print("\nExpression Parsing Log:")
            for entry in self.log_entries:
                print(entry)

    def display_errors(self):
        """
        Display any errors encountered during parsing.
        """
        self.error_handler.display_errors()


class ExpressionEvaluator:
    """
    Class to evaluate parsed expressions and determine their values, addressing modes, and relocatability.
    Utilizes the symbol table, literal table, and validator for comprehensive expression evaluation.
    """
    def __init__(self, symbol_table, literal_table, validator, error_handler):
        """
        Initialize the ExpressionEvaluator with symbol and literal tables, validation tools, and error handling.

        :param symbol_table: An instance of SymbolTable for symbol lookup.
        :param literal_table: An instance of LiteralTableList for managing literals.
        :param validator: An instance of Validator for validating expressions.
        :param error_handler: An instance of ErrorHandler for logging errors.
        """
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.validator = validator
        self.error_handler = error_handler
        self.log_entries = []  # Stores logs of evaluation actions

    def evaluate_expressions(self, parsed_expressions):
        """
        Evaluate a list of parsed expressions.

        :param parsed_expressions: A list of dictionaries with parsed expression components.
        :return: A list of evaluation results, including value, addressing mode, and relocatability.
        """
        evaluation_results = []

        for expression in parsed_expressions:
            try:
                result = self.evaluate_expression(expression)
                if result:
                    evaluation_results.append(result)
                    self.log_action(f"Successfully evaluated expression: {expression['original_expression']}")
                else:
                    self.error_handler.log_error(f"Failed to evaluate expression: '{expression['original_expression']}'. Please check the expression format and referenced symbols.", context_info="ExpressionEvaluator - evaluate_expressions")
            except Exception as e:
                self.error_handler.log_error(f"Unexpected error while evaluating expression: {str(e)}", context_info="ExpressionEvaluator - evaluate_expressions")

        return evaluation_results

    def evaluate_expression(self, parsed_expression):
        """
        Evaluate a single parsed expression.

        :param parsed_expression: A dictionary containing parsed components of an expression.
        :return: A dictionary with evaluated value, addressing mode, and relocatability information.
        """
        operand1 = parsed_expression['operand1']
        operator = parsed_expression.get('operator')
        operand2 = parsed_expression.get('operand2')

        # Evaluate the first operand
        operand1_info = self.evaluate_operand(operand1)
        if not operand1_info:
            return None

        # If there's no operator, return the value of operand1
        if not operator:
            return self.format_result(parsed_expression['original_expression'], operand1_info['value'], operand1_info['is_relocatable'], operand1_info['addressing_mode_info'])

        # Evaluate the second operand if an operator is present
        operand2_info = self.evaluate_operand(operand2)
        if not operand2_info:
            return None

        # Determine the result value and relocatability
        value = self.apply_operator(operand1_info['value'], operator, operand2_info['value'])
        if value is None:
            self.error_handler.log_error(f"Unsupported operator '{operator}' in expression: '{parsed_expression['original_expression']}'. Only '+' and '-' are supported.", context_info="ExpressionEvaluator - evaluate_expression")
            return None

        is_relocatable = self.determine_relocatability(operand1_info, operator, operand2_info)
        if is_relocatable is None:
            return None

        # Format and return the final result
        return self.format_result(parsed_expression['original_expression'], value, is_relocatable, operand1_info['addressing_mode_info'])

    def evaluate_operand(self, operand):
        """
        Evaluate a single operand, determining its value and addressing mode.

        :param operand: The operand to evaluate (e.g., symbol, literal, or constant).
        :return: A dictionary with value, relocatability, and addressing mode information.
        """
        try:
            # Determine the addressing mode
            addressing_mode_info = self.determine_addressing_mode(operand)
            operand_name = addressing_mode_info['operand_name']

            # Check if the operand is a numeric constant
            if operand_name.isdigit() or (operand_name.startswith('-') and operand_name[1:].isdigit()):
                return {
                    'value': int(operand_name),
                    'is_relocatable': False,
                    'addressing_mode_info': addressing_mode_info
                }

            # Check if the operand is a literal
            elif operand_name.startswith('='):
                literal_data = self.handle_literal(operand_name)
                if not literal_data:
                    return None
                return {
                    'value': int(literal_data.value, 16),
                    'is_relocatable': False,
                    'addressing_mode_info': addressing_mode_info
                }

            # Otherwise, assume it's a symbol and search the symbol table
            else:
                symbol_data = self.symbol_table.search(operand_name)
                if symbol_data is not None:
                    self.symbol_table.increment_reference(operand_name)
                    return {
                        'value': symbol_data.value,
                        'is_relocatable': symbol_data.rflag,
                        'addressing_mode_info': addressing_mode_info
                    }
                else:
                    self.error_handler.log_error(f"Undefined symbol: '{operand_name}'. Please ensure the symbol is defined before use.", context_info="ExpressionEvaluator - evaluate_operand")
                    return None

        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while evaluating operand '{operand}': {str(e)}", context_info="ExpressionEvaluator - evaluate_operand")
            return None

    def determine_addressing_mode(self, operand):
        """
        Determine the addressing mode of an operand.

        :param operand: The operand to analyze.
        :return: A dictionary with operand name, addressing mode, and relevant bits.
        """
        try:
            n_bit, i_bit, x_bit = 1, 1, 0  # Default bits for simple addressing
            operand_name = operand

            if operand.startswith('#'):
                i_bit, n_bit = 1, 0  # Immediate addressing
                operand_name = operand[1:]
            elif operand.startswith('@'):
                i_bit, n_bit = 0, 1  # Indirect addressing
                operand_name = operand[1:]
            if operand.endswith(',X'):
                x_bit = 1  # Indexed addressing
                operand_name = operand_name.replace(',X', '')

            return {
                'operand_name': operand_name,
                'addressing_mode': 'Immediate' if i_bit == 1 and n_bit == 0 else 'Indirect' if n_bit == 1 and i_bit == 0 else 'Simple',
                'n_bit': n_bit,
                'i_bit': i_bit,
                'x_bit': x_bit
            }
        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while determining addressing mode for operand '{operand}': {str(e)}", context_info="ExpressionEvaluator - determine_addressing_mode")
            return None

    def apply_operator(self, value1, operator, value2):
        """
        Apply an arithmetic operator to two values.

        :param value1: The first value.
        :param operator: The operator ('+' or '-').
        :param value2: The second value.
        :return: The result of the operation, or None if the operator is unsupported.
        """
        try:
            if operator == '+':
                return value1 + value2
            elif operator == '-':
                return value1 - value2
            else:
                self.error_handler.log_error(f"Unsupported operator '{operator}'. Please use either '+' or '-'.", context_info="ExpressionEvaluator - apply_operator")
                return None
        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while applying operator '{operator}': {str(e)}", context_info="ExpressionEvaluator - apply_operator")
            return None

    def determine_relocatability(self, operand1_info, operator, operand2_info):
        """
        Determine the relocatability of an expression based on its operands and operator.

        :param operand1_info: The information for the first operand.
        :param operator: The operator used in the expression.
        :param operand2_info: The information for the second operand.
        :return: True if the result is relocatable, False if absolute, or None if there's an error.
        """
        try:
            if operand1_info['is_relocatable'] and operand2_info['is_relocatable']:
                if operator == '+':
                    self.error_handler.log_error("Cannot add two relocatable operands. Please revise the expression.", context_info="ExpressionEvaluator - determine_relocatability")
                    return None
                elif operator == '-':
                    return False  # Relocatable - Relocatable results in Absolute
            elif operand1_info['is_relocatable']:
                return True  # Relocatable + Absolute or Relocatable - Absolute
            else:
                return False  # Absolute + Absolute or Absolute - Absolute
        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while determining relocatability: {str(e)}", context_info="ExpressionEvaluator - determine_relocatability")
            return None

    def handle_literal(self, literal):
        """
        Handle a literal by either retrieving it from the literal table or adding it if it's new.

        :param literal: The literal to handle.
        :return: The LiteralData object for the literal, or None if there's an error.
        """
        try:
            literal_data = self.literal_table.search(literal)
            if not literal_data:
                value, length = self.parse_literal(literal)
                if value is None or length is None:
                    self.error_handler.log_error(f"Failed to parse literal: '{literal}'. Please ensure it is in a valid format.", context_info="ExpressionEvaluator - handle_literal")
                    return None
                literal_data = LiteralData(literal, value, length)
                self.literal_table.insert(literal_data)
            return literal_data
        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while handling literal '{literal}': {str(e)}", context_info="ExpressionEvaluator - handle_literal")
            return None

    def parse_literal(self, literal):
        """
        Parse a literal to extract its value and length.

        :param literal: The literal to parse (e.g., '=5').
        :return: A tuple (value, length).
        """
        try:
            # For simplicity, assume literals are hexadecimal values prefixed with '='
            if literal.startswith('='):
                value_str = literal[1:]
                value = int(value_str, 16)  # Convert hexadecimal string to an integer
                length = len(value_str) // 2  # Assume length in bytes
                return value, length
            else:
                self.error_handler.log_error(f"Invalid literal format: '{literal}'. Expected format: '=hex_value'.", context_info="ExpressionEvaluator - parse_literal")
                return None, None
        except ValueError:
            self.error_handler.log_error(f"Failed to parse literal value: '{literal}'. Ensure the value is a valid hexadecimal.", context_info="ExpressionEvaluator - parse_literal")
            return None, None
        except Exception as e:
            self.error_handler.log_error(f"Unexpected error while parsing literal '{literal}': {str(e)}", context_info="ExpressionEvaluator - parse_literal")
            return None, None

    def format_result(self, expression, value, is_relocatable, addressing_mode_info):
        """
        Format the result of an expression evaluation for output.

        :param expression: The original expression.
        :param value: The evaluated value.
        :param is_relocatable: Boolean indicating if the result is relocatable.
        :param addressing_mode_info: Addressing mode details.
        :return: A dictionary containing the formatted result.
        """
        return {
            'expression': expression,
            'value': value,
            'is_relocatable': is_relocatable,
            'addressing_mode': addressing_mode_info['addressing_mode'],
            'n_bit': addressing_mode_info['n_bit'],
            'i_bit': addressing_mode_info['i_bit'],
            'x_bit': addressing_mode_info['x_bit']
        }

    def log_action(self, message):
        """
        Log a successful evaluation action.

        :param message: The message to be logged.
        """
        self.log_entries.append(f"[ACTION]: {message}")

    def log_error(self, error_message):
        """
        Log an error encountered during expression evaluation.

        :param error_message: The error message to be logged.
        """
        self.error_handler.log_error(f"[ERROR]: {error_message}")
        self.log_entries.append(f"[ERROR]: {error_message}")

    def display_log(self):
        """
        Display the log of actions performed during evaluation.
        """
        if not self.log_entries:
            print("No evaluation actions have been logged.")
        else:
            print("Expression Evaluation Log:")
            for entry in self.log_entries:
                print(entry)

    def display_errors(self):
        """
        Display any errors encountered during evaluation.
        """
        self.error_handler.display_errors()





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
    readfile = FileExplorer()
    expression_lines = readfile.process_file("Express.DAT")
    # print expression_lines
    for line in expression_lines:
        print(line)
        # Assuming FileExplorer, Validator, and ErrorHandler classes are implemented elsewhere
    
    file_explorer = FileExplorer()
    validator = Validator()
    error_handler = ErrorHandler()

    # Create the ExpressionParser instance
    expression_parser = ExpressionParser(file_explorer, validator, error_handler)

    # Parse expressions from EXPRESS.DAT
    parsed_expressions = expression_parser.parse_expressions("EXPRESS.DAT")

    # Display the parsed expressions
    for expr in parsed_expressions:
        print(expr)

    # Display logs and errors
    expression_parser.display_log()
    expression_parser.display_errors()
    
    

if __name__ == "__main__":
    main()