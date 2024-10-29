class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """

    directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 
                  'EQU', 'ORG', 'EXTDEF', 'EXTREF']

    def __init__(self, line_number, line_text):
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

        self.instruction_length = 0

    def __str__(self):
        line_info = f"Line {self.line_number}: "
        line_info += f"{self.label or ''} {self.opcode or ''} "
        line_info += f"{', '.join(self.operands)} "
        line_info += f"(Addr: {self.address or 'N/A'}, Obj Code: {self.object_code or 'N/A'})"
        if self.comment:
            line_info += f" ; {self.comment}"
        return line_info

    def add_error(self, error_message):
        if isinstance(error_message, str):
            self.errors.append(error_message)
        else:
            raise TypeError("Error message must be a string.")

    def has_errors(self):
        return bool(self.errors)

    def clear_errors(self):
        self.errors.clear()

    def has_label(self):
        return self.label is not None

    def is_directive(self):
        return self.opcode in self.directives

    def is_instruction(self):
        return self.opcode is not None and not self.is_directive()

    def is_extended_format(self):
        return self.opcode is not None and self.opcode.startswith('+')

    def is_indexed_addressing(self):
        return any(',' in operand and operand.split(',')[-1].strip() == 'X' for operand in self.operands)

    def calculate_instruction_length(self):
        if self.instr_format is not None:
            if self.instr_format == 1:
                self.instruction_length = 1
            elif self.instr_format == 2:
                self.instruction_length = 2
            elif self.instr_format in [3, 4]:
                self.instruction_length = 4 if self.is_extended_format() else 3
            else:
                self.add_error(f"Unknown instruction format: {self.instr_format}")
                self.instruction_length = 0
        elif self.is_directive():
            self.instruction_length = 0
        else:
            self.add_error("Instruction length cannot be determined without a valid format or directive.")

    def get_operand_count(self):
        return len(self.operands)

    def set_operands(self, operands):
        if isinstance(operands, list):
            self.operands = operands
        else:
            error_msg = "Operands must be provided as a list."
            self.add_error(error_msg)
            raise TypeError(error_msg)

    def set_address(self, address):
        if isinstance(address, int) and address >= 0:
            self.address = address
        else:
            error_msg = f"Invalid address: {address}. Address must be a non-negative integer."
            self.add_error(error_msg)
            raise ValueError(error_msg)

    def update_object_code(self, code):
        if isinstance(code, str):
            self.object_code = code
        else:
            error_msg = "Object code must be a string."
            self.add_error(error_msg)
            raise TypeError(error_msg)

    @staticmethod
    def test():
        """
        Rigorous testing of the SourceCodeLine class.
        """
        # Test basic initialization
        print("=== Testing Initialization ===")
        try:
            line = SourceCodeLine(line_number=1, line_text="START 1000")
            print(line)
            print("Initialization successful.")
        except Exception as e:
            print(f"Initialization failed: {e}")

        # Test invalid line number
        print("\n=== Testing Invalid Line Number ===")
        try:
            line = SourceCodeLine(line_number="ABC", line_text="START 1000")
        except ValueError as e:
            print(f"Passed: {e}")

        # Test setting operands
        print("\n=== Testing Operands Setting ===")
        try:
            line.set_operands(["BUFFER", "X"])
            print(f"Operands: {line.operands}")
        except Exception as e:
            print(f"Operands setting failed: {e}")

        # Test invalid operands setting
        try:
            line.set_operands("INVALID")
        except TypeError as e:
            print(f"Passed: {e}")

        # Test setting address
        print("\n=== Testing Address Setting ===")
        try:
            line.set_address(1000)
            print(f"Address: {line.address}")
        except Exception as e:
            print(f"Address setting failed: {e}")

        # Test invalid address setting
        try:
            line.set_address(-1)
        except ValueError as e:
            print(f"Passed: {e}")

        # Test updating object code
        print("\n=== Testing Object Code Update ===")
        try:
            line.update_object_code("4C0000")
            print(f"Object Code: {line.object_code}")
        except Exception as e:
            print(f"Object code update failed: {e}")

        # Test invalid object code update
        try:
            line.update_object_code(1234)
        except TypeError as e:
            print(f"Passed: {e}")

        # Test directive and instruction checks
        print("\n=== Testing Directive & Instruction Checks ===")
        line.opcode = "START"
        print(f"Is Directive: {line.is_directive()}")  # Expected: True
        line.opcode = "LDA"
        print(f"Is Instruction: {line.is_instruction()}")  # Expected: True

        # Test extended format and indexed addressing
        print("\n=== Testing Extended Format & Indexed Addressing ===")
        line.opcode = "+LDA"
        print(f"Is Extended Format: {line.is_extended_format()}")  # Expected: True
        line.operands = ["BUFFER,X"]
        print(f"Is Indexed Addressing: {line.is_indexed_addressing()}")  # Expected: True

        # Test error handling
        print("\n=== Testing Error Handling ===")
        line.add_error("Test error")
        print(f"Has Errors: {line.has_errors()}")  # Expected: True
        print(f"Errors: {line.errors}")
        line.clear_errors()
        print(f"Errors Cleared. Has Errors: {line.has_errors()}")  # Expected: False

        print("\n=== All Tests Completed ===")


# Run the test
if __name__ == "__main__":
    SourceCodeLine.test()
