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

    def __init__(self, start_address=0, opcode_handler=None, symbol_table=None, logger=None):
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
        self.symbol_table = symbol_table
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

    def get_current_address(self):
        """
        Returns the current location counter address.

        :return: Current address as an integer.
        """
        return self.current_address
    
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
            self.logger.log_action(f"LOCCTR incremented by hex '{increment_value}' to {self.current_address:X}", False)
        except ValueError:
            Error = f"Invalid increment value '{increment_value}'"
            self.logger.log_error(Error)
            raise ValueError(Error)
        

    # def handle_directive(self, directive, operands):
    #     """
    #     Handles directives that affect the location counter differently.

    #     :param directive: The directive opcode (e.g., BYTE, WORD, RESB).
    #     :param operands: The operands associated with the directive.
    #     :return: The increment value as an integer.
    #     """
    #     elif directive == 'RESB':
    #         try:
    #             n = int(operands)
    #             return n
    #         except ValueError:
    #             raise ValueError(f"Invalid operand '{operands}' for RESB")
    #     elif directive == 'BYTE':
    #         return self.calculate_byte_size(operands)
    #     elif directive == 'EQU':
    #         # EQU may require expression evaluation
    #         self.handle_equ_directive(operands)
    #         return 0
    #     elif directive == 'ORG':
    #         self.handle_org_directive(operands)
    #         return 0
    #     else:
    #         raise ValueError(f"Unknown directive '{directive}'")


    # def update_symbol_table(self, label):
    #     """
    #     Updates the symbol table with the label and current address.

    #     :param label: The label to be added to the symbol table.
    #     """
    #     if self.symbol_table.search(label):
    #         error_msg = f"Duplicate label '{label}' found."
    #         self.logger.log_error(error_msg)
    #         raise ValueError(error_msg)
    #     else:
    #         self.symbol_table.insert_symbol(label, self.current_address)
    #         self.logger.log_action(f"Added label '{label}' with address {self.current_address:X}")

    # def handle_equ_directive(self, operands):
    #     """
    #     Handles the EQU directive by evaluating the expression and updating the symbol table.

    #     :param operands: The expression associated with the EQU directive.
    #     """
    #     # Extract label and expression
    #     # In this context, operands should be the expression
    #     expression = operands.strip()
    #     # Evaluate the expression (this is a simplified version)
    #     value = self.evaluate_expression(expression)
    #     # Insert or update the symbol in the symbol table
    #     # Since we don't have the label here, you might need to adjust how this method is called
    #     # For this example, we'll assume the label is available
    #     # You may need to pass the label as an additional parameter
    #     label = self.current_label  # Assume current_label is set appropriately
    #     self.symbol_table.insert_symbol(label, value, rflag=False)
    #     self.logger.log_action(f"Set symbol '{label}' to value {value} via EQU directive")

    # def handle_org_directive(self, operands):
    #     """
    #     Handles the ORG directive to set the current location counter.

    #     :param operands: The expression or value to set the LOCCTR.
    #     """
    #     expression = operands.strip()
    #     value = self.evaluate_expression(expression)
    #     self.current_address = value
    #     self.logger.log_action(f"LOCCTR set to {self.current_address:X} via ORG directive")

    # def evaluate_expression(self, expression):
    #     """
    #     Evaluates an expression to compute its value.

    #     :param expression: The expression to evaluate.
    #     :return: The computed value as an integer.
    #     """
    #     try:
    #         # Replace '*' with the current address
    #         expression = expression.replace('*', str(self.current_address))
    #         # Evaluate the expression
    #         # WARNING: Using eval can be dangerous; ensure that the expression is sanitized
    #         # For a real assembler, implement a proper expression evaluator
    #         value = eval(expression)
    #         return int(value)
    #     except Exception as e:
    #         raise ValueError(f"Invalid expression '{expression}': {e}")

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