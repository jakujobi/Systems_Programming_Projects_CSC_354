import re

class SourceCodeLine:
    """
    Represents a single line of assembly code in a SIC/XE assembler.
    """
    comment_symbol = '.'  # Default comment symbol
    directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 
                  'EQU', 'ORG', 'EXTDEF', 'EXTREF']
    pseudo_ops = ['EXTDEF', 'EXTREF', 'EQU', 'ORG']

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

        self._initialize_line()

    def __str__(self):
        line_info = f"Line {self.line_number}: "
        line_info += f"{self.label or ''} {self.opcode or ''} "
        line_info += f"{', '.join(self.operands)} "
        line_info += f"(Addr: {self.address or 'N/A'}, Obj Code: {self.object_code or 'N/A'})"
        if self.comment:
            line_info += f" ; {self.comment}"
        return line_info

    def _initialize_line(self):
        """
        Determines if the line is a comment or pseudo-op during initialization.
        """
        line_stripped = self.line_text.strip()
        if line_stripped.startswith(SourceCodeLine.comment_symbol):
            self.is_comment = True
            self.comment = line_stripped
        elif not line_stripped:
            self.is_comment = True
            self.comment = 'Blank line'

    def add_error(self, error_message):
        if isinstance(error_message, str):
            self.errors.append(error_message)
            self.log_error(error_message)
        else:
            raise TypeError("Error message must be a string.")

    def log_error(self, message):
        """
        Logs errors with line number context for debugging.
        """
        error_msg = f"[Line {self.line_number}] ERROR: {message}"
        self.errors.append(error_msg)
        print(error_msg)

    def log_action(self, message):
        """
        Logs actions for debugging purposes.
        """
        action_msg = f"[Line {self.line_number}] ACTION: {message}"
        print(action_msg)

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

    def is_pseudo_op(self):
        """
        Checks if the opcode is a pseudo-operation (like EXTDEF, EQU).
        """
        return self.opcode in self.pseudo_ops

    def is_extended_format(self):
        return self.opcode is not None and self.opcode.startswith('+')

    def is_indexed_addressing(self):
        return any(',' in operand and operand.split(',')[-1].strip() == 'X' for operand in self.operands)

    def get_operand_count(self):
        return len(self.operands)

    def set_operands(self, operands):
        """
        Sets operands and handles complex expressions.
        Supports expressions like '#LENGTH+2' or '@BUFFER-4'.
        """
        if not isinstance(operands, list):
            error_msg = "Operands must be provided as a list."
            self.add_error(error_msg)
            raise TypeError(error_msg)

        # Enhanced operand handling
        for operand in operands:
            if re.match(r'[@#]?[A-Z0-9]+([-+][A-Z0-9]+)?', operand, re.IGNORECASE):
                self.operands.append(operand)
            else:
                error_msg = f"Invalid operand format: {operand}"
                self.add_error(error_msg)

    def set_address(self, address):
        if isinstance(address, int) and address >= 0:
            self.address = address
            self.log_action(f"Address set to {address}")
        else:
            error_msg = f"Invalid address: {address}. Address must be a non-negative integer."
            self.add_error(error_msg)
            raise ValueError(error_msg)

    def update_object_code(self, code):
        if isinstance(code, str):
            self.object_code = code
            self.log_action(f"Object code updated to {code}")
        else:
            error_msg = "Object code must be a string."
            self.add_error(error_msg)
            raise TypeError(error_msg)

    @staticmethod
    def test():
        """
        Rigorous testing of the SourceCodeLine class.
        """
        passed_tests = 0
        failed_tests = 0
        failed_test_details = []

        def log_test_result(test_name, success, exception=None):
            nonlocal passed_tests, failed_tests
            if success:
                passed_tests += 1
                print(f"{test_name}: Passed")
            else:
                failed_tests += 1
                print(f"{test_name}: Failed - {exception}")
                failed_test_details.append(f"{test_name}: {exception}")

        # Test basic initialization
        print("=== Testing Initialization ===")
        try:
            line = SourceCodeLine(line_number=1, line_text="START 1000")
            print(line)
            log_test_result("Initialization", True)
        except Exception as e:
            log_test_result("Initialization", False, e)

        # Test initialization with a comment line
        print("\n=== Testing Comment Line Initialization ===")
        try:
            line = SourceCodeLine(line_number=2, line_text=". This is a comment")
            is_comment = line.is_comment
            print(f"Is Comment: {is_comment}")  # Expected: True
            log_test_result("Comment Line Initialization", is_comment)
        except Exception as e:
            log_test_result("Comment Line Initialization", False, e)

        # Test invalid line number
        print("\n=== Testing Invalid Line Number ===")
        try:
            line = SourceCodeLine(line_number="ABC", line_text="START 1000")
            log_test_result("Invalid Line Number", False, "No exception raised")
        except ValueError as e:
            log_test_result("Invalid Line Number", True)
        except Exception as e:
            log_test_result("Invalid Line Number", False, e)

        # Test setting operands
        print("\n=== Testing Operands Setting ===")
        try:
            line.set_operands(["BUFFER", "X"])
            print(f"Operands: {line.operands}")
            log_test_result("Operands Setting", True)
        except Exception as e:
            log_test_result("Operands Setting", False, e)

        # Test setting complex operands
        print("\n=== Testing Complex Operands Setting ===")
        try:
            line.set_operands(["@BUFFER", "#LENGTH+2"])
            print(f"Operands: {line.operands}")  # Expected: ['@BUFFER', '#LENGTH+2']
            log_test_result("Complex Operands Setting", True)
        except Exception as e:
            log_test_result("Complex Operands Setting", False, e)

        # Test invalid operands setting
        try:
            line.set_operands("INVALID")
            log_test_result("Invalid Operands Setting", False, "No exception raised")
        except TypeError as e:
            log_test_result("Invalid Operands Setting", True)
        except Exception as e:
            log_test_result("Invalid Operands Setting", False, e)

        # Test setting address
        print("\n=== Testing Address Setting ===")
        try:
            line.set_address(1000)
            print(f"Address: {line.address}")
            log_test_result("Address Setting", True)
        except Exception as e:
            log_test_result("Address Setting", False, e)

        # Test invalid address setting
        try:
            line.set_address(-1)
            log_test_result("Invalid Address Setting", False, "No exception raised")
        except ValueError as e:
            log_test_result("Invalid Address Setting", True)
        except Exception as e:
            log_test_result("Invalid Address Setting", False, e)

        # Test updating object code
        print("\n=== Testing Object Code Update ===")
        try:
            line.update_object_code("4C0000")
            print(f"Object Code: {line.object_code}")
            log_test_result("Object Code Update", True)
        except Exception as e:
            log_test_result("Object Code Update", False, e)

        # Test invalid object code update
        try:
            line.update_object_code(1234)
            log_test_result("Invalid Object Code Update", False, "No exception raised")
        except TypeError as e:
            log_test_result("Invalid Object Code Update", True)
        except Exception as e:
            log_test_result("Invalid Object Code Update", False, e)

        # Test directive and instruction checks
        print("\n=== Testing Directive & Instruction Checks ===")
        try:
            line.opcode = "START"
            is_directive = line.is_directive()
            print(f"Is Directive: {is_directive}")  # Expected: True
            log_test_result("Directive Check", is_directive)
        except Exception as e:
            log_test_result("Directive Check", False, e)

        try:
            line.opcode = "LDA"
            is_instruction = line.is_instruction()
            print(f"Is Instruction: {is_instruction}")  # Expected: True
            log_test_result("Instruction Check", is_instruction)
        except Exception as e:
            log_test_result("Instruction Check", False, e)

        # Test extended format and indexed addressing
        print("\n=== Testing Extended Format & Indexed Addressing ===")
        try:
            line.opcode = "+LDA"
            is_extended_format = line.is_extended_format()
            print(f"Is Extended Format: {is_extended_format}")  # Expected: True
            log_test_result("Extended Format Check", is_extended_format)
        except Exception as e:
            log_test_result("Extended Format Check", False, e)

        try:
            line.operands = ["BUFFER,X"]
            is_indexed_addressing = line.is_indexed_addressing()
            print(f"Is Indexed Addressing: {is_indexed_addressing}")  # Expected: True
            log_test_result("Indexed Addressing Check", is_indexed_addressing)
        except Exception as e:
            log_test_result("Indexed Addressing Check", False, e)

        # Test pseudo-op identification
        print("\n=== Testing Pseudo-op Identification ===")
        try:
            line.opcode = "EQU"
            is_pseudo_op = line.is_pseudo_op()
            print(f"Is Pseudo-op: {is_pseudo_op}")  # Expected: True
            log_test_result("Pseudo-op Check", is_pseudo_op)
        except Exception as e:
            log_test_result("Pseudo-op Check", False, e)

        # Test error handling
        print("\n=== Testing Error Handling ===")
        try:
            line.add_error("Test error")
            has_errors = line.has_errors()
            print(f"Has Errors: {has_errors}")  # Expected: True
            log_test_result("Error Handling - Add Error", has_errors)
        except Exception as e:
            log_test_result("Error Handling - Add Error", False, e)

        try:
            print(f"Errors: {line.errors}")
            line.clear_errors()
            has_errors = line.has_errors()
            print(f"Errors Cleared. Has Errors: {has_errors}")  # Expected: False
            log_test_result("Error Handling - Clear Errors", not has_errors)
        except Exception as e:
            log_test_result("Error Handling - Clear Errors", False, e)

        # Summary of test results
        print("\n=== Test Results Summary ===")
        print(f"Total Tests Passed: {passed_tests}")
        print(f"Total Tests Failed: {failed_tests}")
        if failed_tests > 0:
            print("\nFailed Test Details:")
            for detail in failed_test_details:
                print(detail)

        print("\n=== All Tests Completed ===")


# Run the test
if __name__ == "__main__":
    SourceCodeLine.test()
