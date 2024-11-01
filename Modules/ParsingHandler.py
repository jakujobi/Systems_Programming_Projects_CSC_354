import re
import os
import sys


repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import SourceCodeLine
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.OpcodeHandler import OpcodeHandler

class ParsingHandler:
    """
    Handles parsing of a single line of assembly code into components: label, opcode, operands, and comments.
    Includes validation if validate_parsing is set to True.
    """
    
    def __init__(self, source_line, validate_parsing=False, logger=None, opcode_handler=None):
        self.source_line = source_line
        self.validate_parsing = validate_parsing
        self.logger = logger or ErrorLogHandler()
        self.opcode_handler = opcode_handler

    def parse_line(self):
        """
        Parses the line into components: label, opcode, operands, and comments.
        Validates the components if validate_parsing is True.
        Updates the SourceCodeLine instance accordingly.
        """
        line = self.line_text.strip()

        # Handle empty or comment lines
        if not line or line.startswith(SourceCodeLine.comment_symbol):
            self.handle_comment_line(line)
            return

        try:
            # Handle inline comments
            if SourceCodeLine.comment_symbol in line:
                code_part, comment_part = line.split(SourceCodeLine.comment_symbol, 1)
                self.source_line.comment = SourceCodeLine.comment_symbol + ' ' + comment_part.strip()
            else:
                code_part = line

            tokens = code_part.strip().split()

            label = None
            opcode = None
            operands_str = ''

            # Extract label and opcode
            if tokens:
                # Check if first token is a label (ends with ':')
                if tokens[0].endswith(':'):
                    label = tokens.pop(0).rstrip(':')
                # Check if first token is a label (not an opcode)
                elif len(tokens) > 1 and not self.opcode_handler.is_opcode(tokens[0].lstrip('+').upper()):
                    label = tokens.pop(0)
                # Otherwise, first token is opcode
                if tokens:
                    opcode = tokens.pop(0)
                # Extract operands
                if tokens:
                    operands_str = ' '.join(tokens)

            # Update SourceCodeLine
            self.source_line.label = label
            self.source_line.opcode = opcode
            self.source_line.set_operands(operands_str)

            if self.validate_parsing:
                self.validate_line()

        except Exception as e:
            error_msg = f"Exception occurred while parsing line: {e}"
            self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
            self.source_line.add_error(error_msg)
            
    def print_full_opcodes(self):
        """
        Prints the full opcode information for the parsed line.
        """
        self.source_line.print_full_opcodes()


    def reset_source_line(self):
        """
        Clears the attributes of SourceCodeLine before parsing a new line.
        Ensures that previous data doesn't interfere with the new parsing process.
        """
        self.source_line.label = None
        self.source_line.opcode = None
        self.source_line.operands = ''
        self.source_line.operands_list = []
        self.source_line.comment = ''
        self.source_line.is_comment = False
        self.source_line.clear_errors()

    def check_if_empty_line(self):
        """
        Checks if the line is empty or contains only whitespace.
        """
        return not self.source_line.label and not self.source_line.opcode and not self.source_line.operands and not self.source_line.comment


    def handle_empty_line(self):
        """ Handles empty lines in the source code.
        Sets is_empty to True in SourceCodeLine.
        """

    def handle_comment_line(self, line):
        """
        Handles lines that are purely comments and sets is_comment to True in SourceCodeLine.
        """
        self.source_line.comment = line.strip()
        self.source_line.is_comment = True

    def validate_line(self):
        """
        Validates the parsed line components: label, opcode, operands.
        Adds errors to SourceCodeLine and logs them using ErrorLogHandler if validation fails.
        """
        self.validate_label()
        self.validate_opcode()
        self.validate_operands()

    def validate_label(self):
        """
        Validates the label for correctness according to assembly language rules.
        """
        label = self.source_line.label
        if label:
            if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', label):
                error_msg = f"Invalid label '{label}'. Labels must start with a letter and contain only alphanumeric characters."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)
            elif len(label) > 10:
                error_msg = f"Label '{label}' is too long. Maximum length is 10 characters."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)

    def validate_opcode(self):
        """
        Validates the opcode using OpcodeHandler.
        """
        opcode = self.source_line.opcode
        if opcode:
            opcode_clean = opcode.lstrip('+').upper()
            if self.opcode_handler:
                if not self.opcode_handler.is_opcode(opcode_clean):
                    error_msg = f"Invalid opcode '{opcode}'."
                    self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                    self.source_line.add_error(error_msg)
            else:
                error_msg = "OpcodeHandler not provided. Cannot validate opcode."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)

    # def validate_operands(self):
    #     """
    #     Validates the operands for correctness according to assembly language rules.
    #     """
    #     operands = self.source_line.operands
    #     if operands:
    #         # Check for balanced parentheses and quotes
    #         if operands.count('(') != operands.count(')'):
    #             error_msg = f"Unbalanced parentheses in operands '{operands}'."
    #             self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
    #             self.source_line.add_error(error_msg)
    #         if operands.count("'") % 2 != 0:
    #             error_msg = f"Unmatched quotes in operands '{operands}'."
    #             self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
    #             self.source_line.add_error(error_msg)
    #         # Additional operand validations can be added here

    @classmethod
    def test(cls):
        """
        Tests various parsing scenarios for ParsingHandler.
        """
        logger = ErrorLogHandler()
        opcode_handler = OpcodeHandler(logger=logger)  # Ensure the opcodes are loaded
        test_cases = [

        ]

        passed_tests = 0
        failed_tests = 0
        failed_test_details = []

        for i, (line_text, expected) in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i} ---")
            source_line = SourceCodeLine(line_number=i, line_text=line_text)
            parser = cls(source_line, line_text, validate_parsing=True, logger=logger, opcode_handler=opcode_handler)
            parser.parse_line()
            print(f"Parsed Line: {source_line}")
            parser.print_full_opcodes()
            print ("\n")

            # Verify results
            success = True
            for key, value in expected.items():
                actual_value = getattr(source_line, key)
                if key == 'errors':
                    actual_errors = actual_value
                    if sorted(actual_errors) != sorted(value):
                        success = False
                        print(f"Failed: {key} | Expected: {value} | Got: {actual_errors}")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: {value} | Got: {actual_errors}")
                elif key == 'is_comment':
                    if actual_value != value:
                        success = False
                        print(f"Failed: {key} | Expected: {value} | Got: {actual_value}")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: {value} | Got: {actual_value}")
                else:
                    if actual_value != value:
                        success = False
                        print(f"Failed: {key} | Expected: '{value}' | Got: '{actual_value}'")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: '{value}' | Got: '{actual_value}'")

            if success:
                print("Test passed.")
                passed_tests += 1
            else:
                print("Test failed.")
                failed_tests += 1

        # Summary of test results
        print("\n=== Test Results Summary ===")
        print(f"Total Tests Passed: {passed_tests}")
        print(f"Total Tests Failed: {failed_tests}")
        if failed_tests > 0:
            print("\nFailed Test Details:")
            for detail in failed_test_details:
                print(detail)

        print("\n=== All Tests Completed ===")

# Run the test if this script is executed directly
if __name__ == "__main__":
    ParsingHandler.test()