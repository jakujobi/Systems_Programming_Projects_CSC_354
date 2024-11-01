import re
import sys
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

# from Modules.OpcodeHandler import OpcodeHandler

class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """
    comment_symbol = '.'  # Default comment symbol
    label_suffix_symbol = ':'

    def __init__(self, line_number, line_text):
        try:
            self.line_number = int(line_number)
        except ValueError:
            raise ValueError(f"Invalid line number: {line_number}. It should be an integer.")

        self.line_text = line_text # Original line text

        # Core attributes: Gotten from the input after being parsed
        self.label = ''
        self.opcode_mnemonic = ''
        self.operands = ''          # Changed from list to string
        self.comment = ''
        
        self.opcode_hex = None   # Opcode in hexadecimal
        self.address = None
        self.object_code = None
        self.instr_format = None

        # Additional attributes
        self.errors = []
        self.instruction_length = 0
        
        self.initialize_line()
    
    def __str__(self) -> str:
        opcode_mnemonic = self.opcode_mnemonic if self.opcode_mnemonic else ''
        label = f"{self.label}{self.label_suffix_symbol}" if self.label else ''
        operands = self.operands if self.operands else ''
        comment = self.comment if self.comment else ''
        return f"{self.line_number}    {label}    {opcode_mnemonic}    {operands}    {comment}"

    def is_comment(self):
        return self.line_text.strip().startswith(self.comment_symbol)
    
    def is_empty_line(self):
        return not self.line_text.strip()
    
    def has_label(self):
        return bool(self.label)
    
    def has_opcode_mnemonic(self):
        return bool(self.opcode_mnemonic)
    
    def has_operands(self):
        return bool(self.operands)
    
    def has_comment(self):
        return bool(self.comment)

    def has_errors(self):
        return bool(self.errors)
    
    def add_error(self, error_message):
        self.errors.append(error_message)
        
    def clear_errors(self):
        self.errors = []
        
    def print_core_attributes(self, column_width=20):
        """
        Prints the core attributes of the SourceCodeLine object.
        """
        if self.has_errors():
            print(f"Error: {', '.join(self.errors)} on line {self.line_number}: {self.line_text}")
        else:
            label = f"{self.label}{self.label_suffix_symbol}" if self.label else ''
            operands = self.operands if self.operands else ''
            comment = self.comment if self.comment else ''
            print(f"{self.line_number:>{column_width}} {label:<{column_width}} {self.opcode_mnemonic:<{column_width}} {operands:<{column_width}} {comment:<{column_width}}")
    
    def remove_comment(self):
        self.comment = ''
        
    def set_label(self, label):
        self.label = label
    
    def set_opcode_mnemonic(self, opcode):
        self.opcode_mnemonic = opcode
        
    def set_opcode_hex(self, opcode):
        self.opcode_hex = opcode
    
    def set_operands(self, operands):
        self.operands = operands
    
    @staticmethod
    def test(self):
        """
        Tests the SourceCodeLine class.
        """
        #
        pass