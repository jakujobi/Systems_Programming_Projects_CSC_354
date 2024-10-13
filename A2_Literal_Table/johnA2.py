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
            print(f"┃ {literal.name:^13} │ {literal.value:^13} │ {literal.length:^6} │ {literal.address:^7} ┃")
            counter += 1
            if counter % 18 == 0:
                self.press_continue()
            current = current.next
        print("┗" + ("━" * 15) + "┷" + ("━" * 15) + "┷" + ("━" * 8) + "┷" + ("━" *9) + "┛")

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
    Class to parse expressions from a list of lines and break them down into operands and operators.
    Handles different addressing modes and logs actions or errors encountered during parsing.
    """
    def __init__(self, validator, log_handler):
        """
        Initialize the ExpressionParser with validation tools and a log handler.

        :param validator: An instance of Validator for validating expressions.
        :param log_handler: An instance of ErrorLogHandler for logging actions and errors.
        """
        self.validator = validator
        self.log_handler = log_handler

    def parse_expressions(self, lines):
        """
        Parse all expressions from a given list of lines and return structured expression data.

        :param lines: A list of strings, each representing an expression.
        :return: A list of dictionaries with parsed expression components.
        """
        if not lines:
            self.log_handler.log_error("The provided list of lines is empty. Please provide valid expressions.")
            return []

        parsed_expressions = []

        for line_number, line in enumerate(lines, start=1):
            result = self.parse_expression_line(line.strip(), line_number)
            if result:
                parsed_expressions.append(result)
                self.log_handler.log_action(f"Successfully parsed expression on line {line_number}: {line.strip()}")
            else:
                self.log_handler.log_error(f"Failed to parse expression on line {line_number}: '{line.strip()}'. Please check the syntax.")

        return parsed_expressions

    def parse_expression_line(self, expression_line, line_number):
        """
        Parse a single line of expression into operands and operators.

        :param expression_line: A single line containing an expression (e.g., 'A + B').
        :param line_number: The line number for reference in error handling.
        :return: A dictionary with the parsed components (e.g., {'operand1': 'A', 'operator': '+', 'operand2': 'B'}).
        """
        if not expression_line:
            self.log_handler.log_error(f"Empty expression line at line {line_number}. Skipping...")
            return None

        try:
            operand1, operator, operand2 = self.tokenize_expression(expression_line)

            # Validate operands and operator
            if not self.validator.validate_symbol(operand1):
                self.log_handler.log_error(f"Invalid operand1 '{operand1}' at line {line_number}.")
                return None

            if operand2 and not (self.validator.validate_symbol(operand2) or operand2.isnumeric()):
                self.log_handler.log_error(f"Invalid operand2 '{operand2}' at line {line_number}.")
                return None

            return {
                'original_expression': expression_line,
                'operand1': operand1,
                'operator': operator,
                'operand2': operand2
            }

        except ValueError as e:
            self.log_handler.log_error(f"Parsing error at line {line_number}: {str(e)}")
            return None

    def tokenize_expression(self, expression_line):
        """
        Tokenize an expression line into its components (operands and operator).
        Handles special cases for addressing modes (#, @, ,X).

        :param expression_line: The expression line to be tokenized.
        :return: Tuple (operand1, operator, operand2).
        """
        tokens = expression_line.replace(',', ' ,').split()

        if len(tokens) == 1:
            return tokens[0], None, None

        elif len(tokens) == 3:
            return tokens[0], tokens[1], tokens[2]

        elif len(tokens) == 2 and tokens[1] == ',X':
            return tokens[0] + tokens[1], None, None

        elif len(tokens) == 2:
            return tokens[0], None, tokens[1]

        else:
            raise ValueError("Unrecognized expression format. Ensure correct syntax with operands and operators.")




class ExpressionEvaluator:
    """
    Evaluates parsed expressions to determine their values, addressing modes, and relocatability.
    Utilizes the symbol table, literal table, and validator for comprehensive evaluation.
    """

    def __init__(self, symbol_table, literal_table, validator, log_handler):
        """
        Initialize the ExpressionEvaluator.

        :param symbol_table: An instance of SymbolTable for symbol lookup.
        :param literal_table: An instance of LiteralTableList for managing literals.
        :param validator: An instance of Validator for validating expressions.
        :param log_handler: An instance of ErrorLogHandler for logging actions and errors.
        """
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.validator = validator
        self.log_handler = log_handler

    def evaluate_expressions(self, parsed_expressions: list[dict]) -> list[dict]:
        """
        Evaluate a list of parsed expressions.

        :param parsed_expressions: A list of dictionaries with parsed expression components.
        :return: A list of evaluation results including value, addressing mode, and relocatability.
        """
        results = []
        for expression in parsed_expressions:
            try:
                result = self.evaluate_expression(expression)
                if result:
                    results.append(result)
                    self.log_handler.log_action(f"Successfully evaluated: {expression['original_expression']}")
                else:
                    self.log_handler.log_error(
                        f"Failed to evaluate expression: '{expression['original_expression']}'. Please check the expression format and referenced symbols.",
                        context_info="ExpressionEvaluator - evaluate_expressions"
                    )
            except Exception as e:
                self.log_handler.log_error(
                    f"Unexpected error while evaluating expression: {str(e)}",
                    context_info="ExpressionEvaluator - evaluate_expressions"
                )
        return results

    def evaluate_expression(self, parsed_expression: dict) -> dict | None:
        """
        Evaluate a single parsed expression.

        :param parsed_expression: A dictionary containing parsed components of an expression.
        :return: A dictionary with evaluation results or None if evaluation fails.
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
            return self.format_result(
                parsed_expression['original_expression'],
                operand1_info['value'],
                operand1_info['is_relocatable'],
                operand1_info['addressing_mode_info']
            )

        # Evaluate the second operand if an operator is present
        operand2_info = self.evaluate_operand(operand2)
        if not operand2_info:
            return None

        # Determine the result value and relocatability
        value = self.apply_operator(operand1_info['value'], operator, operand2_info['value'])
        if value is None:
            self.log_handler.log_error(
                f"Unsupported operator '{operator}' in expression: '{parsed_expression['original_expression']}'. Only '+' and '-' are supported.",
                context_info="ExpressionEvaluator - evaluate_expression"
            )
            return None

        is_relocatable = self.determine_relocatability(operand1_info, operator, operand2_info)
        if is_relocatable is None:
            return None

        # Format and return the final result
        return self.format_result(
            parsed_expression['original_expression'],
            value,
            is_relocatable,
            operand1_info['addressing_mode_info']
        )

    def evaluate_operand(self, operand: str) -> dict | None:
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
                return self.get_value_from_literal(operand_name, addressing_mode_info)

            # Otherwise, assume it's a symbol
            return self.get_value_from_symbol(operand_name, addressing_mode_info)

        except Exception as e:
            self.log_handler.log_error(
                f"Error evaluating operand '{operand}': {str(e)}",
                context_info="ExpressionEvaluator - evaluate_operand"
            )
            return None

    def determine_addressing_mode(self, operand: str) -> dict:
        """
        Determine the addressing mode of an operand.

        :param operand: The operand to analyze.
        :return: A dictionary with operand name, addressing mode, and relevant bits.
        """
        n_bit, i_bit, x_bit = 1, 1, 0
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

        addressing_mode = 'Immediate' if i_bit == 1 and n_bit == 0 else 'Indirect' if n_bit == 1 else 'Simple'
        return {
            'operand_name': operand_name,
            'addressing_mode': addressing_mode,
            'n_bit': n_bit,
            'i_bit': i_bit,
            'x_bit': x_bit
        }

    def get_value_from_literal(self, literal: str, addressing_mode_info: dict) -> dict | None:
        """
        Get the value of a literal.

        :param literal: The literal string.
        :param addressing_mode_info: Addressing mode information.
        :return: A dictionary with literal evaluation details or None if the literal is invalid.
        """
        literal_data = self.handle_literal(literal)
        if not literal_data:
            return None
        return {
            'value': int(literal_data.value, 16),
            'is_relocatable': False,
            'addressing_mode_info': addressing_mode_info
        }

    def get_value_from_symbol(self, symbol: str, addressing_mode_info: dict) -> dict | None:
        """
        Retrieve the value of a symbol from the symbol table.

        :param symbol: The symbol to evaluate.
        :param addressing_mode_info: Addressing mode information.
        :return: A dictionary with symbol evaluation details or None if the symbol is undefined.
        """
        symbol_data = self.symbol_table.search(symbol)
        if symbol_data:
            self.symbol_table.increment_reference(symbol)
            return {
                'value': symbol_data.value,
                'is_relocatable': symbol_data.rflag,
                'addressing_mode_info': addressing_mode_info
            }
        self.log_handler.log_error(
            f"Undefined symbol: '{symbol}'. Ensure it is defined before use.",
            context_info="ExpressionEvaluator - get_value_from_symbol"
        )
        return None

    def apply_operator(self, value1: int, operator: str, value2: int) -> int | None:
        """
        Apply an arithmetic operator to two values.

        :param value1: The first value.
        :param operator: The operator ('+' or '-').
        :param value2: The second value.
        :return: The result of the operation or None if the operator is unsupported.
        """
        if operator == '+':
            return value1 + value2
        elif operator == '-':
            return value1 - value2
        self.log_handler.log_error(
            f"Unsupported operator '{operator}' in expression evaluation.",
            context_info="ExpressionEvaluator - apply_operator"
        )
        return None

    def determine_relocatability(self, operand1_info: dict, operator: str, operand2_info: dict) -> bool | None:
        """
        Determine the relocatability of an expression based on its operands and operator.

        :param operand1_info: The information for the first operand.
        :param operator: The operator used in the expression.
        :param operand2_info: The information for the second operand.
        :return: True if the result is relocatable, False if absolute, or None if there's an error.
        """
        if operand1_info['is_relocatable'] and operand2_info['is_relocatable']:
            if operator == '+':
                self.log_handler.log_error(
                    "Cannot add two relocatable operands.",
                    context_info="ExpressionEvaluator - determine_relocatability"
                )
                return None
            return False  # Relocatable - Relocatable results in Absolute

        return operand1_info['is_relocatable']

    def format_result(self, expression: str, value: int, is_relocatable: bool, addressing_mode_info: dict) -> dict:
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

    def handle_literal(self, literal: str) -> LiteralData | None:
        """
        Handle a literal by either retrieving it from the literal table or adding it if it's new.

        :param literal: The literal to handle.
        :return: The LiteralData object for the literal or None if there's an error.
        """
        try:
            literal_data = self.literal_table.search(literal)
            if not literal_data:
                value, length = self.parse_literal(literal)
                if value is None or length is None:
                    self.log_handler.log_error(
                        f"Failed to parse literal '{literal}'",
                        context_info="ExpressionEvaluator - handle_literal"
                    )
                    return None
                literal_data = LiteralData(literal, value, length)
                self.literal_table.insert(literal_data)
            return literal_data
        except Exception as e:
            self.log_handler.log_error(
                f"Unexpected error while handling literal '{literal}': {str(e)}",
                context_info="ExpressionEvaluator - handle_literal"
            )
            return None

    def parse_literal(self, literal: str) -> tuple[int | None, int | None]:
        """
        Parse a literal to extract its value and length.

        :param literal: The literal to parse (e.g., '=0x5A').
        :return: A tuple containing the value and its length or (None, None) if parsing fails.
        """
        try:
            if literal.startswith('='):
                value_str = literal[1:]
                value = int(value_str, 16)
                length = len(value_str) // 2  # Length in bytes
                return value, length
            self.log_handler.log_error(
                f"Invalid literal format: '{literal}'",
                context_info="ExpressionEvaluator - parse_literal"
            )
            return None, None
        except ValueError:
            self.log_handler.log_error(
                f"Failed to parse literal value: '{literal}'. Ensure it is valid hexadecimal.",
                context_info="ExpressionEvaluator - parse_literal"
            )
            return None, None



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



# Main function
if __name__ == "__main__":
    # Create an instance of LiteralTableDriver and run it
    expression_file = sys.argv[1] if len(sys.argv) > 1 else None
    driver = LiteralTableDriver()
    driver.run(expression_file)
