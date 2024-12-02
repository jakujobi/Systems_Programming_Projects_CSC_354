import re
import sys
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """
    comment_symbol = '.'  # Default comment symbol
    label_suffix_symbol = ':'

    def __init__(self,
                 line_number: int,
                 line_text: str, label = '',
                 opcode_mnemonic = '',
                 operands = '',
                 comment = '',
                 errors = None,
                 opcode_hex = None,
                 address = 0x00000,
                 object_code = None,
                 instr_format = None,
                 instruction_length = 0,
                 original_line_number: int = None
                 ):
        """
        Initializes a SourceCodeLine object.

        :param line_number: The line number in the source file.
        :param line_text: The original line text.
        """
        try:
            self.line_number = int(line_number)
        except ValueError:
            raise ValueError(f"Invalid line number: {line_number}. It should be an integer.")

        self.line_text = line_text or ''  # Original line text

        # Core attributes: Gotten from the input after being parsed
        self.label = label or ''
        self.opcode_mnemonic = opcode_mnemonic or ''
        self.operands = operands or ''  # Changed from list to string
        self.comment = comment or ''

        self.opcode_hex = opcode_hex or None  # Opcode in hexadecimal
        self.address = address or 0x00000  # Address of the instruction
        self.object_code = object_code or None
        self.instr_format = instr_format or None

        # Additional attributes
        self.errors = errors or []
        self.instruction_length = instruction_length or 0
        
        self.original_line_number = original_line_number

    def __str__(self) -> str:
        """
        Provides a string representation of the SourceCodeLine object.
        """
        spacing = ' ' * 4
        column_size_line_number = 10
        line_number = f"{self.line_number:<{column_size_line_number}}"
        
        column_size_address = 6
        address = f"{self.address:<{column_size_address}}{spacing}" if self.address is not None else ' ' * (column_size_address)
        
        column_size_label = 11
        raw_label = f"{self.label}{self.label_suffix_symbol}" if self.label else ''
        label = f"{raw_label:<{column_size_label}}" if self.label else (' ' * column_size_label)
        
        column_size_opcode_mnemonic = 10
        opcode_mnemonic = f"{self.opcode_mnemonic:<{column_size_opcode_mnemonic}}" if self.opcode_mnemonic else (' ' * column_size_opcode_mnemonic)
        
        operands = f"{self.operands}{spacing}" if self.operands else ''
        comment = f"{self.comment}{spacing}" if self.comment else ''
        errors = f"[ERROR: {'; '.join(self.errors)}]{spacing}" if self.errors else ''
        return f"{line_number} {address}{errors}{label} {opcode_mnemonic} {operands}{comment}"

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
        if not re.fullmatch(r'[0-9A-Fa-f]+', opcode):
            raise ValueError(f"Opcode '{opcode}' is not a valid hexadecimal string.")
        self.opcode_hex = opcode.upper()

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