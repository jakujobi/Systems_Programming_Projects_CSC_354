import re
import sys
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from OpcodeHandler import OpcodeHandler

class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """
    comment_symbol = '.'  # Default comment symbol
    label_suffix_symbol = ':'

    def __init__(self, line_number: int, line_text: str):
        """
        Initializes a SourceCodeLine object.

        :param line_number: The line number in the source file.
        :param line_text: The original line text.
        """
        try:
            self.line_number = int(line_number)
        except ValueError:
            raise ValueError(f"Invalid line number: {line_number}. It should be an integer.")

        self.line_text = line_text  # Original line text

        # Core attributes: Gotten from the input after being parsed
        self.label = ''
        self.opcode_mnemonic = ''
        self.operands = ''  # Changed from list to string
        self.comment = ''

        self.opcode_hex = None  # Opcode in hexadecimal
        self.address = None
        self.object_code = None
        self.instr_format = None

        # Additional attributes
        self.errors = []
        self.instruction_length = 0

        # Initialize line attributes
        self._initialize_line()

    def __str__(self) -> str:
        """
        Provides a string representation of the SourceCodeLine object.
        """
        label = f"{self.label}{self.label_suffix_symbol}" if self.label else ''
        operands = self.operands if self.operands else ''
        comment = self.comment if self.comment else ''
        return f"{self.line_number}    {label}    {self.opcode_mnemonic}    {operands}    {comment}"

    def is_comment(self) -> bool:
        """
        Checks if the line is a comment.
        """
        return self.line_text.strip().startswith(self.comment_symbol)

    def is_empty_line(self) -> bool:
        """
        Checks if the line is empty.
        """
        return not self.line_text.strip()

    def has_errors(self) -> bool:
        """
        Checks if there are any errors associated with the line.
        """
        return bool(self.errors)

    def add_error(self, error_message: str):
        """
        Adds an error message to the list of errors.

        :param error_message: The error message to add.
        """
        self.errors.append(error_message)

    def clear_errors(self):
        """
        Clears all errors associated with the line.
        """
        self.errors = []

    def print_core_attributes(self, column_width: int = 20):
        """
        Prints the core attributes of the SourceCodeLine object.

        :param column_width: The width of each column in the output.
        """
        if self.has_errors():
            print(f"Error: {', '.join(self.errors)} on line {self.line_number}: {self.line_text}")
        else:
            label = f"{self.label}{self.label_suffix_symbol}" if self.label else ''
            operands = self.operands if self.operands else ''
            comment = self.comment if self.comment else ''
            print(f"{self.line_number:>{column_width}} {label:<{column_width}} {self.opcode_mnemonic:<{column_width}} {operands:<{column_width}} {comment:<{column_width}}")

    def has_label(self) -> bool:
        """
        Checks if the line has a label.
        """
        return bool(self.label)

    def has_opcode_mnemonic(self) -> bool:
        """
        Checks if the line has an opcode mnemonic.
        """
        return bool(self.opcode_mnemonic)

    def has_operands(self) -> bool:
        """
        Checks if the line has operands.
        """
        return bool(self.operands)

    def has_comment(self) -> bool:
        """
        Checks if the line has a comment.
        """
        return bool(self.comment)

    def remove_comment(self):
        """
        Removes the comment from the line.
        """
        self.comment = ''

    def set_label(self, label: str):
        """
        Sets the label of the line.

        :param label: The label to set.
        """
        self.label = label

    def set_opcode_mnemonic(self, opcode: str):
        """
        Sets the opcode mnemonic of the line.

        :param opcode: The opcode mnemonic to set.
        """
        self.opcode_mnemonic = opcode

    def set_opcode_hex(self, opcode: str):
        """
        Sets the opcode in hexadecimal format.

        :param opcode: The opcode in hexadecimal format to set.
        """
        self.opcode_hex = opcode

    def set_operands(self, operands: str):
        """
        Sets the operands of the line.

        :param operands: The operands to set.
        """
        self.operands = operands

    @staticmethod
    def test():
        """
        Tests the SourceCodeLine class.
        """
        # Implement test cases here
        pass