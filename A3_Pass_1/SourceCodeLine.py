class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler after being tokenized.
    """

    def __init__(self, line_number, address=None, label=None, opcode=None, instr_format=None, operands=None, object_code=None):
        """
        Initializes a SourceCodeLine instance.
        
        :param line_number: The line number in the source file.
        :param address: The memory address assigned to the instruction (set by LOCCTR).
        :param label: The label of the instruction, if present.
        :param opcode: The operation code or assembler directive.
        :param instr_format: The final format of the instruction (e.g., 1, 2, 3/4).
        :param operands: The operands of the instruction.
        :param object_code: The object code generated (if any).
        """
        self.line_number = line_number
        self.address = address
        self.label = label
        self.opcode = opcode
        self.instr_format = instr_format
        self.operands = operands or []
        self.object_code = object_code

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, value):
        self._line_number = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, value):
        self._opcode = value

    @property
    def instr_format(self):
        return self._instr_format

    @instr_format.setter
    def instr_format(self, value):
        self._instr_format = value

    @property
    def operands(self):
        return self._operands

    @operands.setter
    def operands(self, value):
        if isinstance(value, list):
            self._operands = value
        else:
            raise TypeError("Operands must be a list.")

    @property
    def object_code(self):
        return self._object_code

    @object_code.setter
    def object_code(self, value):
        self._object_code = value

    def has_label(self):
        """
        Checks if the line contains a label.
        
        :return: True if label exists, False otherwise.
        """
        return bool(self.label)

    def __str__(self):
        """
        Provides a string representation of the line for debugging.
        
        :return: A formatted string with details of the source line.
        """
        return (f"Line {self.line_number}: {self.label or ''} {self.opcode or ''} {', '.join(self.operands)} "
                f"(Address: {self.address or 'N/A'}, Object Code: {self.object_code or 'N/A'})")


# Example usage
if __name__ == "__main__":
    # Create an instance
    line = SourceCodeLine(line_number=1, label="START", opcode="LDA", instr_format=3, operands=["BUFFER,X"])
    print(line)  # Before modifications

    # Modify attributes directly
    line.address = 0x1000
    line.opcode = "STA"
    line.operands = ["BUFFER"]

    print(line)  # After modifications