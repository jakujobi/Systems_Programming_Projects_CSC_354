# LocationCounter.py
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.Symbol_Table_Builder import SymbolTable
from OpcodeHandler import OpcodeHandler
from SourceCodeLine import SourceCodeLine
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
        self.log_action(f"Start address set to {self.start_address:X}")

    def get_current_address(self):
        """
        Returns the current location counter address.

        :return: Current address as an integer.
        """
        return self.current_address

    def increment(self, source_line):
        """
        Increments the location counter based on the instruction or directive in the source line.

        :param source_line: An instance of SourceCodeLine containing parsed line components.
        """
        if source_line.is_comment or source_line.has_errors():
            # Do not increment for comments or lines with errors
            return

        label = source_line.label
        opcode = source_line.opcode
        operands = source_line.operands

        # Update symbol table if there's a label
        if label:
            try:
                self.update_symbol_table(label)
            except ValueError as e:
                source_line.add_error(str(e))
                return

        # Calculate increment value
        try:
            increment_value = self.calculate_increment(opcode, operands)
            self.current_address += increment_value
            self.log_action(f"LOCCTR incremented by {increment_value} to {self.current_address:X}")
        except Exception as e:
            error_msg = f"Error incrementing LOCCTR: {e}"
            self.log_error(error_msg)
            source_line.add_error(error_msg)

    def calculate_increment(self, opcode, operands):
        """
        Calculates the increment value based on the opcode and operands.

        :param opcode: The opcode from the source line.
        :param operands: The operands from the source line.
        :return: The increment value as an integer.
        """
        if not opcode:
            return 0  # No opcode means no increment

        opcode_upper = opcode.upper()
        if opcode_upper in {'START', 'END'}:
            return 0  # START and END do not increment LOCCTR

        if self.opcode_handler.is_opcode(opcode_upper.lstrip('+')):
            # Instruction
            format_num = self.opcode_handler.get_format(opcode_upper.lstrip('+'))
            if opcode.startswith('+'):
                # Format 4 instruction
                return 4
            else:
                return format_num
        else:
            # Directive
            return self.handle_directive(opcode_upper, operands)

    def handle_directive(self, directive, operands):
        """
        Handles directives that affect the location counter differently.

        :param directive: The directive opcode (e.g., BYTE, WORD, RESB).
        :param operands: The operands associated with the directive.
        :return: The increment value as an integer.
        """
        if directive == 'WORD':
            return 3
        elif directive == 'RESW':
            try:
                n = int(operands)
                return 3 * n
            except ValueError:
                raise ValueError(f"Invalid operand '{operands}' for RESW")
        elif directive == 'RESB':
            try:
                n = int(operands)
                return n
            except ValueError:
                raise ValueError(f"Invalid operand '{operands}' for RESB")
        elif directive == 'BYTE':
            return self.calculate_byte_size(operands)
        elif directive == 'EQU':
            # EQU may require expression evaluation
            self.handle_equ_directive(operands)
            return 0
        elif directive == 'ORG':
            self.handle_org_directive(operands)
            return 0
        else:
            raise ValueError(f"Unknown directive '{directive}'")

    def calculate_byte_size(self, operand):
        """
        Calculates the size of the BYTE directive.

        :param operand: The operand for the BYTE directive.
        :return: The size in bytes as an integer.
        """
        operand = operand.strip()
        if operand.startswith('C\'') and operand.endswith('\''):
            value = operand[2:-1]
            return len(value)
        elif operand.startswith('X\'') and operand.endswith('\''):
            value = operand[2:-1]
            if len(value) % 2 != 0:
                raise ValueError("Hex string in BYTE directive must have even length")
            return len(value) // 2
        else:
            raise ValueError(f"Invalid operand '{operand}' for BYTE directive")

    def update_symbol_table(self, label):
        """
        Updates the symbol table with the label and current address.

        :param label: The label to be added to the symbol table.
        """
        if self.symbol_table.search(label):
            error_msg = f"Duplicate label '{label}' found."
            self.log_error(error_msg)
            raise ValueError(error_msg)
        else:
            self.symbol_table.insert_symbol(label, self.current_address)
            self.log_action(f"Added label '{label}' with address {self.current_address:X}")

    def handle_equ_directive(self, operands):
        """
        Handles the EQU directive by evaluating the expression and updating the symbol table.

        :param operands: The expression associated with the EQU directive.
        """
        # Extract label and expression
        # In this context, operands should be the expression
        expression = operands.strip()
        # Evaluate the expression (this is a simplified version)
        value = self.evaluate_expression(expression)
        # Insert or update the symbol in the symbol table
        # Since we don't have the label here, you might need to adjust how this method is called
        # For this example, we'll assume the label is available
        # You may need to pass the label as an additional parameter
        label = self.current_label  # Assume current_label is set appropriately
        self.symbol_table.insert_symbol(label, value, rflag=False)
        self.log_action(f"Set symbol '{label}' to value {value} via EQU directive")

    def handle_org_directive(self, operands):
        """
        Handles the ORG directive to set the current location counter.

        :param operands: The expression or value to set the LOCCTR.
        """
        expression = operands.strip()
        value = self.evaluate_expression(expression)
        self.current_address = value
        self.log_action(f"LOCCTR set to {self.current_address:X} via ORG directive")

    def evaluate_expression(self, expression):
        """
        Evaluates an expression to compute its value.

        :param expression: The expression to evaluate.
        :return: The computed value as an integer.
        """
        try:
            # Replace '*' with the current address
            expression = expression.replace('*', str(self.current_address))
            # Evaluate the expression
            # WARNING: Using eval can be dangerous; ensure that the expression is sanitized
            # For a real assembler, implement a proper expression evaluator
            value = eval(expression)
            return int(value)
        except Exception as e:
            raise ValueError(f"Invalid expression '{expression}': {e}")

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
        self.log_action("Location counter reset")

    def log_action(self, message):
        """
        Logs an action message.

        :param message: The message to log.
        """
        if self.logger:
            self.logger.log_action(message)

    def log_error(self, error_message):
        """
        Logs an error message.

        :param error_message: The error message to log.
        """
        if self.logger:
            self.logger.log_error(error_message)

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

def test_location_counter():
    opcode_handler = OpcodeHandler()
    symbol_table = SymbolTable()
    logger = ErrorLogHandler()
    loc_counter = LocationCounter(opcode_handler=opcode_handler, symbol_table=symbol_table, logger=logger)
    
    # Test starting at address 0
    loc_counter.set_start_address(0)
    assert loc_counter.get_current_address() == 0
    
    # Test incrementing with a Format 3 instruction
    source_line = SourceCodeLine(line_number=1, line_text="LDA BUFFER")
    source_line.label = None
    source_line.opcode = "LDA"
    source_line.operands = "BUFFER"
    loc_counter.increment(source_line)
    assert loc_counter.get_current_address() == 3
    
    # Test BYTE directive
    source_line = SourceCodeLine(line_number=2, line_text="BYTE C'EOF'")
    source_line.label = None
    source_line.opcode = "BYTE"
    source_line.operands = "C'EOF'"
    loc_counter.increment(source_line)
    assert loc_counter.get_current_address() == 6  # 'EOF' is 3 bytes
    
    # Test WORD directive
    source_line = SourceCodeLine(line_number=3, line_text="WORD 5")
    source_line.label = None
    source_line.opcode = "WORD"
    source_line.operands = "5"
    loc_counter.increment(source_line)
    assert loc_counter.get_current_address() == 9  # WORD is 3 bytes
    
    print("All tests passed.")

if __name__ == "__main__":
    test_location_counter()


# ### Testing
# # Assuming you have a list of SourceCodeLine instances called 'source_lines'
# for source_line in source_lines:
#     parser = ParsingHandler(source_line, source_line.line_text, validate_parsing=True, logger=logger, opcode_handler=opcode_handler)
#     parser.parse_line()
    
#     # Set the current label for directives like EQU
#     loc_counter.current_label = source_line.label
    
#     # Increment the location counter
#     loc_counter.increment(source_line)
    
#     # Optionally, you can print the current address for debugging
#     print(f"Line {source_line.line_number}: LOCCTR = {loc_counter.get_current_address():04X}")


# # Integration with the main assembler
# opcode_handler = OpcodeHandler()
# symbol_table = SymbolTable()
# logger = ErrorLogHandler()
# loc_counter = LocationCounter(opcode_handler=opcode_handler, symbol_table=symbol_table, logger=logger)

# # Processing each line
# for source_line in source_lines:
#     # Assume source_line is an instance of SourceCodeLine
#     parser = ParsingHandler(source_line, source_line.line_text, validate_parsing=True, logger=logger, opcode_handler=opcode_handler)
#     parser.parse_line()
    
#     # Before incrementing, set the current label if needed
#     loc_counter.current_label = source_line.label
    
#     # Increment the location counter
#     loc_counter.increment(source_line)
