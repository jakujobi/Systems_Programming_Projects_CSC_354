# LocationCounter.py
import os
import sys


repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.Symbol_Table_Builder import SymbolTable
from Modules.OpcodeHandler import OpcodeHandler
from Modules.SourceCodeLine import SourceCodeLine
from Modules.FileExplorer import FileExplorer

class LocationCounter:
    """
    Manages the location counter (LOCCTR) during Pass 1 of the assembler.
    Keeps track of the current address and increments it based on instructions and directives.
    """

    def __init__(self, start_address=0, opcode_handler=None, logger=None):
        """
        Initializes the LocationCounter.

        :param start_address: The starting address of the program.
        :param opcode_handler: Instance of OpcodeHandler for instruction formats.
        :param symbol_table: Instance of SymbolTable for label management.
        :param logger: Instance of ErrorLogHandler for logging actions and errors.
        """
        self.start_address = start_address
        self.current_address = start_address
        self.program_length = 0
        self.opcode_handler = opcode_handler
        self.logger = logger or ErrorLogHandler()

    def set_start_address(self, address):
        """
        Sets the starting address for the program.

        :param address: The address specified in the START directive.
        """
        self.start_address = address
        self.current_address = address
        _action = f"Start address set to {self.start_address:X}"
        self.logger.log_action(_action, False)

    def get_current_address_int(self):
        """
        Returns the current location counter address.

        :return: Current address.
        """
        return self.current_address
    
    def get_current_address_hex(self):
        """
        Returns the current location counter address in hexadecimal.

        :return: Current address in hexadecimal.
        """
        # return hex(self.current_address)
        return format(self.current_address, '05X')
    
    def increment_by_decimal(self, increment_value: int):
        """
          Takes an integer value, increments the location counter by its hexadecimal equivalent.
        """
        try:
            hex_value = int(hex(increment_value), 16)
            self.current_address += hex_value
            _action = f"LOCCTR incremented by integer {increment_value} (hex {hex_value:X}) to {self.current_address:X}"
            self.logger.log_action(_action, False)
        except ValueError:
            Error = f"Invalid increment value '{increment_value}'"
            self.logger.log_error(Error)
            raise ValueError(Error)

        
    def increment_by_hexadecimal(self, increment_value: str):
        """
        Increments the location counter by a hexadecimal value.
        """
        try:
            increment_value = increment_value.strip()
            self.current_address += int(increment_value, 16)
            _action = f"LOCCTR incremented by hex '{increment_value}' to {self.current_address:X}"
            self.logger.log_action(_action, False)
        except ValueError:
            Error = f"Invalid increment value '{increment_value}'"
            self.logger.log_error(Error)
            raise ValueError(Error)

    def calculate_program_length(self):
        """
        Calculates the total length of the program.

        :return: The program length as an integer.
        """
        self.program_length = self.current_address - self.start_address
        return self.program_length

    def reset(self):
        """
        Resets the location counter to its initial state.
        """
        self.current_address = self.start_address
        self.program_length = 0
        self.logger.log_action("Location counter reset")

    @property
    def current_label(self):
        """
        Placeholder method to get the current label.
        This would be set in the context where the location counter is used.
        """
        # This property needs to be set appropriately in your assembler's context
        # For example, when processing an EQU directive, you need to know the label associated with it
        return getattr(self, '_current_label', None)

    @current_label.setter
    def current_label(self, value):
        self._current_label = value


if __name__ == "__main__":
    pass