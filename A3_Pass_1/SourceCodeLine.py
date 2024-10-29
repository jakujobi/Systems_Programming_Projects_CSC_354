class SourceCodeLine:
    """
    Represents a single line of assembly code.

    This class serves as a data container for all the components of an assembly instruction.
    It does not perform any parsing or validation; instead, it allows its attributes to be
    set and retrieved, facilitating manipulation and viewing within the assembler.

    Attributes:
        line_number (int): The line number in the source file.
        address (int): The memory address assigned to the instruction (set by LOCCTR).
        label (str): The label of the instruction, if present.
        opcode (str): The operation code or assembler directive.
        instr_format (int): The final format of the instruction (e.g., 1, 2, 3/4).
        operands (list): The operands of the instruction.
        object_code (str): The object code generated (if any).
        comment (str): The comment associated with the line, if any.
        is_comment (bool): True if the line is a comment.
        errors (list): A list to store any errors associated with the line.
    """
    
    directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'EQU', 'ORG', 'EXTDEF', 'EXTREF']


    def __init__(self, line_number):
        """
        Initializes a SourceCodeLine instance.

        :param line_number: The line number in the source file.
        """
        self.line_number = line_number    # The line number in the source file
        self.address = None               # Memory address assigned to the instruction
        self.label = None                 # Label of the instruction, if present
        self.opcode = None                # Operation code or assembler directive
        self.instr_format = None          # Format of the instruction (e.g., 1, 2, 3/4)
        self.operands = []                # List of operands
        self.object_code = None           # Object code generated (if any)
        self.comment = ''                 # Comment associated with the line
        self.is_comment = False           # True if the line is a comment
        self.errors = []                  # List of errors for this line
        self.instruction_length = 0     # Length of the instruction in bytes

    def has_label(self):
        """
        Checks if the line contains a label.

        :return: True if label exists, False otherwise.
        """
        return self.label is not None

    def add_error(self, error_message):
        """
        Adds an error message to the list of errors for this line.

        :param error_message: The error message to add.
        """
        self.errors.append(error_message)

    def has_errors(self):
        """
        Checks if there are any errors associated with this line.

        :return: True if there are errors, False otherwise.
        """
        return len(self.errors) > 0
    
    @property
    def is_directive(self):
        """
        Checks if the line contains an assembler directive.

        :return: True if the opcode is a directive, False otherwise.
        """
        return self.opcode and self.opcode.upper() in {'START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'EQU', 'EXTDEF', 'EXTREF'}

    @property
    def is_instruction(self):
        """
        Checks if the line contains an instruction mnemonic.

        :return: True if the opcode is an instruction, False otherwise.
        """
        return not self.is_directive and self.opcode is not None


    def __str__(self):
        """
        Provides a string representation of the line for debugging.

        :return: A formatted string with details of the source line.
        """
        label_str = f"{self.label}:" if self.label else ""
        operands_str = ', '.join(self.operands) if self.operands else ""
        errors_str = '; '.join(self.errors) if self.errors else "None"
        comment_str = f"; {self.comment}" if self.comment else ""
        return (f"Line {self.line_number}: {label_str} {self.opcode or ''} {operands_str} "
                f"(Address: {hex(self.address) if self.address is not None else 'N/A'}, "
                f"Object Code: {self.object_code or 'N/A'}, Errors: {errors_str}){comment_str}")

    # Additional helper methods can be added as needed

# Example usage
if __name__ == "__main__":
    # Create an instance of SourceCodeLine
    line = SourceCodeLine(line_number=1)

    # Manually set attributes (parsing is done elsewhere)
    line.label = "START"
    line.opcode = "LDA"
    line.operands = ["BUFFER,X"]
    line.address = 0x1000
    line.instr_format = 3
    line.object_code = "00AF"
    line.comment = "Load accumulator"
    line.is_comment = False

    # Check if the line has a label
    print(f"Has label: {line.has_label()}")

    # Print the line's string representation
    print(line)

    # Add an error
    line.add_error("Undefined symbol 'BUFFER'")
    print(f"Has errors: {line.has_errors()}")
    print(line)
