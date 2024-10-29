class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """

    # List of recognized assembler directives
    directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 
                  'EQU', 'ORG', 'EXTDEF', 'EXTREF']

    def __init__(self, line_number, line_text):
        """
        Initializes a SourceCodeLine instance.
        
        :param line_number: The line number in the source file.
        :param line_text: The original line text as read from the source file.
        """
        try:
            self.line_number = int(line_number)
        except ValueError:
            raise ValueError(f"Invalid line number: {line_number}. It should be an integer.")

        self.address = None
        self.label = None
        self.opcode = None
        self.instr_format = None
        self.operands = []
        self.object_code = None
        self.comment = ''
        self.is_comment = False
        self.errors = []
        self.line_text = line_text
        
        # Derived attributes
        self.instruction_length = 0

    # Basic Methods
    def __str__(self):
        """
        Provides a detailed string representation of the line for debugging or output.
        """
        line_info = f"Line {self.line_number}: "
        line_info += f"{self.label or ''} {self.opcode or ''} "
        line_info += f"{', '.join(self.operands)} "
        line_info += f"(Addr: {self.address or 'N/A'}, Obj Code: {self.object_code or 'N/A'})"
        if self.comment:
            line_info += f" ; {self.comment}"
        return line_info

    # Validation & Error Management Methods
    def add_error(self, error_message):
        """
        Adds an error message to the list of errors for the line.
        :param error_message: The error message to add.
        """
        if isinstance(error_message, str):
            self.errors.append(error_message)
        else:
            raise TypeError("Error message must be a string.")

    def has_errors(self):
        """
        Returns True if there are errors associated with this line.
        :return: True if errors are present, False otherwise.
        """
        return bool(self.errors)

    def clear_errors(self):
        """
        Clears all stored errors for the line.
        """
        self.errors.clear()

    # Line Attribute Checkers
    def has_label(self):
        """
        Returns True if a label is present.
        :return: True if the label is not None, False otherwise.
        """
        return self.label is not None

    def is_directive(self):
        """
        Returns True if the opcode is an assembler directive.
        :return: True if the opcode is a recognized directive, False otherwise.
        """
        return self.opcode in self.directives

    def is_instruction(self):
        """
        Returns True if the opcode is a machine instruction.
        :return: True if the opcode is not a directive and is defined, False otherwise.
        """
        return self.opcode is not None and not self.is_directive()

    def is_extended_format(self):
        """
        Returns True if the instruction is in extended format (format 4).
        :return: True if the opcode starts with '+', False otherwise.
        """
        return self.opcode is not None and self.opcode.startswith('+')

    def is_indexed_addressing(self):
        """
        Returns True if the addressing mode is indexed (e.g., BUFFER,X).
        :return: True if the last character of the operand is 'X', False otherwise.
        """
        return any(',' in operand and operand.split(',')[-1].strip() == 'X' for operand in self.operands)

    # Derived Attribute Methods
    def calculate_instruction_length(self):
        """
        Calculates the instruction length based on the format and sets the instruction_length attribute.
        """
        if self.instr_format is not None:
            # Standard instruction formats
            if self.instr_format == 1:
                self.instruction_length = 1
            elif self.instr_format == 2:
                self.instruction_length = 2
            elif self.instr_format in [3, 4]:
                self.instruction_length = 4 if self.is_extended_format() else 3
            else:
                self.add_error(f"Unknown instruction format: {self.instr_format}")
                self.instruction_length = 0  # Unknown format
        elif self.is_directive():
            # Directives can affect location counter, but typically have no instruction length
            self.instruction_length = 0
        else:
            self.add_error("Instruction length cannot be determined without a valid format or directive.")

    def get_operand_count(self):
        """
        Returns the number of operands present.
        :return: The number of operands in the operands list.
        """
        return len(self.operands)

    # Utility Methods
    def set_operands(self, operands):
        """
        Sets the operands for the line.
        :param operands: A list of operands to set.
        """
        if isinstance(operands, list):
            self.operands = operands
        else:
            error_msg = "Operands must be provided as a list."
            self.add_error(error_msg)
            raise TypeError(error_msg)

    def set_address(self, address):
        """
        Sets the address of the line.
        :param address: The address to set.
        """
        if isinstance(address, int) and address >= 0:
            self.address = address
        else:
            error_msg = f"Invalid address: {address}. Address must be a non-negative integer."
            self.add_error(error_msg)
            raise ValueError(error_msg)

    def update_object_code(self, code):
        """
        Updates the object code for the line.
        :param code: The object code to set.
        """
        if isinstance(code, str):
            self.object_code = code
        else:
            error_msg = "Object code must be a string."
            self.add_error(error_msg)
            raise TypeError(error_msg)