import re
import sys
import os
from typing import List


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
                 line_text: str,
                 label: str = '',
                 opcode_mnemonic: str = '',
                 operands: str = '',
                 comment: str = '',
                 errors = None,
                 opcode_int: int = None,
                 opcode_hex = None,
                 address: int = None,
                 object_code_int: int = None,
                 instr_format: int = None,
                 instruction_length: int = None,
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


        self.opcode_int = opcode_int or None  # Opcode in int
        # self.address = address or 0x00000  # Address of the instruction
        self.address = address or None
        
        self.object_code_int = object_code_int or None
        self.instr_format = instr_format or None

        # Additional attributes
        self.errors = errors or []
        self.instruction_length = instruction_length or 0
        
        self.original_line_number = original_line_number
    
    @property
    def opcode_hex(self):
        """
        Returns the opcode in hexadecimal format.
        """
        return format(self.opcode_int, '02X') if self.opcode_int is not None else None
    
    @property
    def object_code_hex(self):
        """
        Returns the object code in hexadecimal format.
        """
        return format(self.object_code_int, '06X') if self.object_code_int is not None else None
    
    @property
    def address_hex(self):
        """
        Returns the address in hexadecimal format.
        """
        return format(self.address, '06X')


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
        
        column_size_object_code = 6
        object_code_in_hex = f"{self.object_code_hex}{spacing}" if self.object_code_hex else ''
        
        #comment = f"{self.comment}{spacing}" if self.comment else ''
        errors = f"[ERROR: {'; '.join(self.errors)}]{spacing}" if self.errors else ''
        return f"{line_number} {address}{errors}{label} {opcode_mnemonic} {operands} {object_code_in_hex}"
        # return f"{line_number} {address}{errors}{label} {opcode_mnemonic} {operands}{comment}"

#* region Setters
#region Setters
    def set_address_from_hex_string(self, hex_string: str):
        """
        Sets the address from a hexadecimal string.
        """
        try:
            self.address = int(hex_string, 16)
        except ValueError:
            raise ValueError(f"Invalid hexadecimal string: {hex_string}")
        
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
        # check if the label is a string
        if not isinstance(label, str):
            _error_message = f"Label '{label}' is not a string."
            self.logger.error(_error_message)
            raise ValueError(_error_message)
        try:
            # check if the label is a valid label
            self.label = label
        except ValueError:
            _error_message = f"Could not set Label '{label}'"
            self.logger.error(_error_message)
            raise ValueError(_error_message)

    def set_opcode_mnemonic(self, opcode: str):
        """
        Sets the opcode mnemonic of the line.

        :param opcode: The opcode mnemonic to set.
        """
        try:
            # check if the opcode is a string
            if not isinstance(opcode, str):
                _error_message = f"Opcode '{opcode}' is not a string."
                self.logger.error(_error_message)
                raise ValueError(_error_message)
            # check if the opcode is a valid opcode mnemonic
            self.opcode_mnemonic = opcode
        except ValueError:
            _error_message = f"Could not set Opcode '{opcode}'"
            self.logger.error(_error_message)
            raise ValueError(_error_message)

    def set_opcode_from_hex_string(self, hex_string: str):
        """
        Sets the opcode in hexadecimal format from a hexadecimal string.

        :param hex_string: The opcode in hexadecimal format to set.
        """
        hex_string = hex_string.strip().upper()
        if not re.fullmatch(r'[0-9A-Fa-f]+', hex_string):
            raise ValueError(f"Opcode '{hex_string}' is not a valid hexadecimal string.")
        self.opcode = int(hex_string, 16)


    def set_operands(self, operands: str):
        """
        Sets the operands of the line.

        :param operands: The operands to set.
        """
        try:
            # check if the operands is a string
            if not isinstance(operands, str):
                _error_message = f"Operands '{operands}' is not a string."
                self.logger.error(_error_message)
                raise ValueError(_error_message)
            # set the operands
            self.operands = operands
        except ValueError:
            _error_message = f"Could not set Operands '{operands}'"
            self.logger.error(_error_message)
            raise ValueError(_error_message)
        
    def set_object_code_int_from_hex_string(self, object_code: str):
        """
        Sets the object code of the line.

        :param object_code: The object code to set.
        """
        self.object_code_int = int(object_code, 16)
        
    def set_object_code_int_from_int(self, object_code: int):
        """
        Sets the object code of the line.
        """
        self.object_code_int = object_code

    def set_comment(self, comment: str):
        """
        Sets the comment of the line.

        :param comment: The comment to set.
        """
        self.comment = comment
        
    def set_instruction_length(self, length: int):
        """
        Sets the instruction length of the line.

        :param length: The instruction length to set.
        """
        try:
            # check if the length is an integer
            if not isinstance(length, int):
                _error_message = f"Length '{length}' is not an integer."
                self.logger.error(_error_message)
                raise ValueError(_error_message)
            # set the instruction length
            self.instruction_length = length
        except ValueError:
            _error_message = f"Could not set Length '{length}'"
            self.logger.error(_error_message)
            raise ValueError(_error_message)
#endregion Setters


#* region Getters
#region Getters
    def get_address(self):
        """
        Returns the address.
        """
        return self.address
    
    def get_label(self):
        """
        Returns the label.
        """
        return self.label
    
    
    def get_address_hex(self):
        """
        Returns the address in hexadecimal format.
        """
        return format(self.address, '06X')

    def get_opcode_mnemonic(self):
        """
        Returns the opcode mnemonic.
        """
        return self.opcode_mnemonic

    def get_operands(self):
        """
        Returns the operands.
        """
        return self.operands

    def get_object_code_int(self):
        """
        Returns the object code.
        """
        return self.object_code_int

    def get_object_code_hex(self):
        """
        Returns the object code in hexadecimal format.
        """
        return format(self.object_code_int, '02X')
    
    def get_opcode_hex(self):
        """
        Returns the opcode in hexadecimal format.
        """
        return format(self.opcode_hex, '02X')

    def get_comment(self):
        """
        Returns the comment.
        """
        return self.comment

    def get_instruction_length(self):
        """
        Returns the instruction length.
        """
        return self.instruction_length

    def get_line_text(self):
        """
        Returns the line text.
        """
        return self.line_text

    def get_line_number(self):
        """
        Returns the line number.
        """
        return self.line_number
#endregion Getters


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

    def clear_errors(self):
        """
        Clears all errors associated with the line.
        """
        self.errors = []

# * Has Attributes  
#region Has Attributes
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

    def has_object_code(self) -> bool:
        """
        Checks if the line has object code.
        """
        return bool(self.object_code)
    
    def has_errors(self) -> bool:
        """
        Checks if there are any errors associated with the line.
        """
        return bool(self.errors)
#endregion Has Attributes
    




    @staticmethod
    def test():
        """
        Tests the SourceCodeLine class.
        """
        # Implement test cases here
        pass