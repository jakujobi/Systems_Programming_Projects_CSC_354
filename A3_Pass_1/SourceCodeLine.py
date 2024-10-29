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
        self.operands = ''          # Changed from list to string
        self.operands_list = []     # List to store parsed operands when needed
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
        line_info += f"{self.operands} "     # Updated to use operands as string
        line_info += f"(Addr: {self.address or 'N/A'}, Obj Code: {self.object_code or 'N/A'})"
        if self.comment:
            line_info += f" ; {self.comment}"
        return line_info

    def _initialize_line(self):
        """
        Determines if the line is a comment or blank during initialization.
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
        """
        Determines if indexed addressing is used.
        This method now relies on operands_list after parsing operands.
        """
        # Ensure operands are parsed before checking
        if not self.operands_list:
            self.parse_operands()
        # Check for ',X' at the end of the operand
        return any(operand.strip().endswith(',X') for operand in self.operands_list)

    def get_operand_count(self):
        """
        Returns the number of operands after parsing.
        """
        if not self.operands_list:
            self.parse_operands()
        return len(self.operands_list)

    def set_operands(self, operands_str):
        """
        Sets operands as a single string.
        """
        if not isinstance(operands_str, str):
            error_msg = "Operands must be provided as a string."
            self.add_error(error_msg)
            raise TypeError(error_msg)
        self.operands = operands_str.strip()

    def parse_operands(self):
        """
        Parses the operands string into a list, handling special cases.
        """
        # Clear previous operands_list
        self.operands_list = []

        if self.operands:
            # Instructions with multiple operands
            if self.opcode in ['ADDR', 'COMPR', 'SHIFTL', 'SHIFTR', 'RMO', 'SVC', 'COMPR', 'DIVR', 'MULR', 'SUBR', 'TIXR', 'CLEAR']:
                # Split operands by comma
                self.operands_list = [operand.strip() for operand in self.operands.split(',')]
            else:
                # Single operand instructions or directives
                self.operands_list = [self.operands.strip()]
        else:
            self.operands_list = []

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

        print("=== Testing SourceCodeLine Class ===")

        # Test 1: Basic initialization with opcode and operand
        print("\n--- Test 1: Initialization with Opcode and Operand ---")
        try:
            line = SourceCodeLine(line_number=1, line_text="START 1000")
            line.opcode = "START"
            line.set_operands("1000")
            success = (
                line.line_number == 1 and
                line.opcode == "START" and
                line.operands == "1000" and
                line.is_directive()
            )
            log_test_result("Basic Initialization", success)
        except Exception as e:
            log_test_result("Basic Initialization", False, e)

        # Test 2: Initialization with a comment line
        print("\n--- Test 2: Comment Line Initialization ---")
        try:
            line = SourceCodeLine(line_number=2, line_text=". This is a comment")
            is_comment = line.is_comment
            success = (is_comment and line.comment == ". This is a comment")
            log_test_result("Comment Line Initialization", success)
        except Exception as e:
            log_test_result("Comment Line Initialization", False, e)

        # Test 3: Invalid line number
        print("\n--- Test 3: Invalid Line Number ---")
        try:
            line = SourceCodeLine(line_number="ABC", line_text="START 1000")
            log_test_result("Invalid Line Number", False, "No exception raised")
        except ValueError as e:
            log_test_result("Invalid Line Number", True)
        except Exception as e:
            log_test_result("Invalid Line Number", False, e)

        # Test 4: Setting operands
        print("\n--- Test 4: Operands Setting ---")
        try:
            line = SourceCodeLine(line_number=4, line_text="LDA BUFFER,X")
            line.set_operands("BUFFER,X")
            success = (line.operands == "BUFFER,X")
            log_test_result("Operands Setting", success)
        except Exception as e:
            log_test_result("Operands Setting", False, e)

        # Test 5: Setting complex operands
        print("\n--- Test 5: Complex Operands Setting ---")
        try:
            line.set_operands("@BUFFER+#LENGTH-2")
            success = (line.operands == "@BUFFER+#LENGTH-2")
            log_test_result("Complex Operands Setting", success)
        except Exception as e:
            log_test_result("Complex Operands Setting", False, e)

        # Test 6: Invalid operands setting
        print("\n--- Test 6: Invalid Operands Setting ---")
        try:
            line.set_operands(1234)  # Should raise TypeError
            log_test_result("Invalid Operands Setting", False, "No exception raised")
        except TypeError:
            log_test_result("Invalid Operands Setting", True)
        except Exception as e:
            log_test_result("Invalid Operands Setting", False, e)

        # Test 7: Setting address
        print("\n--- Test 7: Address Setting ---")
        try:
            line.set_address(1000)
            success = (line.address == 1000)
            log_test_result("Address Setting", success)
        except Exception as e:
            log_test_result("Address Setting", False, e)

        # Test 8: Invalid address setting
        print("\n--- Test 8: Invalid Address Setting ---")
        try:
            line.set_address(-1)  # Should raise ValueError
            log_test_result("Invalid Address Setting", False, "No exception raised")
        except ValueError:
            log_test_result("Invalid Address Setting", True)
        except Exception as e:
            log_test_result("Invalid Address Setting", False, e)

        # Test 9: Updating object code
        print("\n--- Test 9: Object Code Update ---")
        try:
            line.update_object_code("4C0000")
            success = (line.object_code == "4C0000")
            log_test_result("Object Code Update", success)
        except Exception as e:
            log_test_result("Object Code Update", False, e)

        # Test 10: Invalid object code update
        print("\n--- Test 10: Invalid Object Code Update ---")
        try:
            line.update_object_code(1234)  # Should raise TypeError
            log_test_result("Invalid Object Code Update", False, "No exception raised")
        except TypeError:
            log_test_result("Invalid Object Code Update", True)
        except Exception as e:
            log_test_result("Invalid Object Code Update", False, e)

        # Test 11: Directive check
        print("\n--- Test 11: Directive Check ---")
        try:
            line.opcode = "START"
            is_directive = line.is_directive()
            success = (is_directive)
            log_test_result("Directive Check", success)
        except Exception as e:
            log_test_result("Directive Check", False, e)

        # Test 12: Instruction check
        print("\n--- Test 12: Instruction Check ---")
        try:
            line.opcode = "LDA"
            is_instruction = line.is_instruction()
            success = (is_instruction)
            log_test_result("Instruction Check", success)
        except Exception as e:
            log_test_result("Instruction Check", False, e)

        # Test 13: Extended format and indexed addressing
        print("\n--- Test 13: Extended Format & Indexed Addressing ---")
        try:
            line.opcode = "+LDA"
            line.set_operands("BUFFER,X")
            is_extended = line.is_extended_format()
            is_indexed = line.is_indexed_addressing()
            success = (is_extended and is_indexed)
            log_test_result("Extended Format & Indexed Addressing", success)
        except Exception as e:
            log_test_result("Extended Format & Indexed Addressing", False, e)

        # Test 14: Pseudo-op identification
        print("\n--- Test 14: Pseudo-op Identification ---")
        try:
            line.opcode = "EQU"
            is_pseudo_op = line.is_pseudo_op()
            success = (is_pseudo_op)
            log_test_result("Pseudo-op Check", success)
        except Exception as e:
            log_test_result("Pseudo-op Check", False, e)

        # Test 15: Error handling
        print("\n--- Test 15: Error Handling ---")
        try:
            line.add_error("Test error")
            has_errors = line.has_errors()
            success = (has_errors and "Test error" in line.errors)
            log_test_result("Error Handling - Add Error", success)
        except Exception as e:
            log_test_result("Error Handling - Add Error", False, e)

        try:
            line.clear_errors()
            has_errors = line.has_errors()
            success = (not has_errors)
            log_test_result("Error Handling - Clear Errors", success)
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
