import sys
import re
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.FileExplorer import FileExplorer
from Modules.ErrorLogHandler import ErrorLogHandler

class OpcodeHandler:
    directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'EQU', 'ORG', 'EXTDEF', 'EXTREF']
    pseudo_ops = ['EXTDEF', 'EXTREF', 'EQU', 'ORG']
        # Default opcodes list
    default_opcodes = [
        "ADD        18       3",
        "ADDF       58       3",
        "ADDR       90       2",
        "AND        40       3",
        "CLEAR      B4       2",
        "COMP       28       3",
        "COMPF      88       3",
        "COMPR      A0       2",
        "DIV        24       3",
        "DIVF       64       3",
        "DIVR       9C       2",
        "FIX        C4       1",
        "FLOAT      C0       1",
        "HIO        F4       1",
        "J          3C       3",
        "JEQ        30       3",
        "JGT        34       3",
        "JLT        38       3",
        "JSUB       48       3",
        "LDA        00       3",
        "LDB        68       3",
        "LDCH       50       3",
        "LDF        70       3",
        "LDL        08       3",
        "LDS        6C       3",
        "LDT        74       3",
        "LDX        04       3",
        "LPS        D0       3",
        "MUL        20       3",
        "MULF       60       3",
        "MULR       98       2",
        "NORM       C8       1",
        "OR         44       3",
        "RD         D8       3",
        "RMO        AC       2",
        "RSUB       4C       3",
        "SHIFTR     A8       2",
        "SHIFTL     A4       2",
        "SIO        F0       1",
        "SSK        EC       3",
        "STA        0C       3",
        "STB        78       3",
        "STCH       54       3",
        "STF        80       3",
        "STI        D4       3",
        "STL        14       3",
        "STS        7C       3",
        "STSW       E8       3",
        "STT        84       3",
        "STX        10       3",
        "SUB        1C       3",
        "SUBF       5C       3",
        "SUBR       94       2",
        "SVC        B0       2",
        "TD         E0       3",
        "TIO        F8       1",
        "TIX        2C       3",
        "TIXR       B8       2",
        "WD         DC       3"
    ]
    
    
    def __init__(self, file_path='opcodes.txt', logger=None):
        """
        Initializes the OpcodeHandler with an empty opcode dictionary.
        Creates an instance of FileExplorer to handle file operations.
        Uses ErrorLogHandler to manage error and action logging.
        """
        self.opcodes = {}
        self.format_4 =[]
        self.file_explorer = FileExplorer()
        self.logger = logger if logger else ErrorLogHandler()
        self.file_path = file_path
        self._load_opcodes()
        self.make_format_4()
        

    def _load_opcodes(self):
        """
        Reads the opcodes from the file using FileExplorer and loads them into the dictionary.
        Expects a space-separated file with 'name hex format' structure.
        """
        try:
            # Use FileExplorer's method to get the file contents as a list of lines
            lines = self.file_explorer.process_file(self.file_path)

            if not lines:
                raise FileNotFoundError(f"No lines found in '{self.file_path}' or file is empty.")

            self.logger.log_action(f"Loading opcodes from file: {self.file_path}", False)

            for line_num, line in enumerate(lines, start=1):
                # Use regex to handle inconsistent spacing
                parts = re.split(r'\s+', line.strip())

                # Ensure the line has exactly 3 parts
                if len(parts) != 3:
                    self.logger.log_error(f"Invalid format on line {line_num}: '{line.strip()}'")
                    continue

                name, hex_code, format_type = parts

                # Validate and convert the format type
                try:
                    format_parsed = int(format_type)
                except ValueError:
                    self.logger.log_error(f"Invalid format type on line {line_num}: '{format_type}'")
                    continue

                # Validate and convert the hex code
                try:
                    hex_value = int(hex_code, 16)
                except ValueError:
                    self.logger.log_error(f"Invalid hex code on line {line_num}: '{hex_code}'")
                    continue

                # Store the opcode information
                self.opcodes[name] = {
                    'format': format_parsed,
                    'hex': hex_value
                }
                self.logger.log_action(f"Loaded opcode '{name}' with format {format_parsed} and hex {hex_value:02X}", False)

        except FileNotFoundError as e:
            self.logger.log_error(str(e), "File Error")
        except Exception as e:
            self.logger.log_error(f"Unexpected error while loading opcodes: {e}", "Unexpected Error")

    def make_format_4(self):
        # check for opcodes that have format 3, insert a `+` in front of the opcode then add them to format 4 list
        for opcode in self.opcodes:
            if self.opcodes[opcode]['format'] == 3:
                self.format_4.append('+' + opcode)
        
    def get_opcode(self, name):
        """
        Retrieves the opcode information for the given mnemonic.
        """
        try:
            opcode_info = self.opcodes[name]
            self.logger.log_action(f"Retrieved opcode '{name}': {opcode_info}", False)
            return opcode_info
        except KeyError:
            error_message = f"Opcode '{name}' not found."
            self.logger.log_error(error_message, "Lookup Error")
            raise ValueError(error_message)

    def get_format(self, name):
        """
        Returns the format of the specified opcode, if found.
        """
        try:
            opcode = self.get_opcode(name)
            return opcode['format']
        except ValueError as e:
            self.logger.log_error(str(e), "Format Retrieval Error")
            raise

    def get_hex(self, name):
        """
        Returns the hexadecimal representation of the specified opcode, if found.
        """
        try:
            opcode = self.get_opcode(name)
            return opcode['hex']
        except ValueError as e:
            self.logger.log_error(str(e), "Hex Retrieval Error")
            raise

    def is_opcode_mnemonic(self, name):
        """
        Checks if the given name is a valid opcode.
        
        :param name: The name to check.
        :return: True if the name is a valid opcode, False otherwise.
        """
        return name in self.opcodes or name in self.directives or name in self.pseudo_ops or name in self.format_4
    
    def is_directive(self, name ) -> bool:
        """
        Checks if the given name is a valid directive.

        :param name: The name to check.
        :return: True if the name is a valid directive, False otherwise.
        """
        return name in self.directives
    
    def is_pseudo_op(self, name) -> bool:
        """
        Checks if the given name is a valid pseudo-op.
        :param name: The name to check.
        :return: True if the name is a valid pseudo-op, False otherwise.
        """
        return name in self.pseudo_ops
    
    def is_valid_format_4(self, opcode) -> bool:
        """
        Checks if the given opcode is a valid format 4 opcode.
        :param opcode: The opcode to check.
        :return: True if the opcode is a valid format 4 opcode, False otherwise.
        """
        return opcode in self.format_4

    def print_opcodes(self):
        """
        Prints all loaded opcodes to the screen in a readable format.
        """
        if not self.opcodes:
            self.logger.log_action("No opcodes loaded.", False)
            print("No opcodes loaded.")
            return

        print(f"{'Mnemonic':<10} {'Hex Code':<10} {'Format':<10}")
        print("=" * 30)
        for name, info in self.opcodes.items():
            format_str = f"{info['format']}"  # Convert format to string for display
            hex_str = f"{info['hex']:02X}"  # Convert hex to uppercase string
            print(f"{name:<10} {hex_str:<10} {format_str:<10}")

    @staticmethod
    def test():
        """
        Thoroughly tests the OpcodeHandler class.
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

        # Create a logger for testing
        logger = ErrorLogHandler()

        # Test initialization with a valid file
        print("=== Testing Initialization with Valid File ===")
        try:
            handler = OpcodeHandler(file_path='opcodes.txt', logger=logger)
            log_test_result("Initialization with Valid File", True)
        except Exception as e:
            log_test_result("Initialization with Valid File", False, e)

        # # Test initialization with an invalid file
        # print("\n=== Testing Initialization with Invalid File ===")
        # try:
        #     handler = OpcodeHandler(file_path='invalid_file.txt', logger=logger)
        #     log_test_result("Initialization with Invalid File", False, "No exception raised")
        # except FileNotFoundError:
        #     log_test_result("Initialization with Invalid File", True)
        # except Exception as e:
        #     log_test_result("Initialization with Invalid File", False, e)

        # Test get_opcode with a valid opcode
        print("\n=== Testing get_opcode with Valid Opcode ===")
        try:
            opcode_info = handler.get_opcode('ADD')
            print(f"Opcode Info: {opcode_info}")
            log_test_result("get_opcode with Valid Opcode", True)
        except Exception as e:
            log_test_result("get_opcode with Valid Opcode", False, e)

        # Test get_opcode with an invalid opcode
        print("\n=== Testing get_opcode with Invalid Opcode ===")
        try:
            handler.get_opcode('INVALID')
            log_test_result("get_opcode with Invalid Opcode", False, "No exception raised")
        except ValueError:
            log_test_result("get_opcode with Invalid Opcode", True)
        except Exception as e:
            log_test_result("get_opcode with Invalid Opcode", False, e)

        # Test get_format with a valid opcode
        print("\n=== Testing get_format with Valid Opcode ===")
        try:
            format_type = handler.get_format('ADD')
            print(f"Format: {format_type}")
            log_test_result("get_format with Valid Opcode", True)
        except Exception as e:
            log_test_result("get_format with Valid Opcode", False, e)

        # Test get_format with an invalid opcode
        print("\n=== Testing get_format with Invalid Opcode ===")
        try:
            handler.get_format('INVALID')
            log_test_result("get_format with Invalid Opcode", False, "No exception raised")
        except ValueError:
            log_test_result("get_format with Invalid Opcode", True)
        except Exception as e:
            log_test_result("get_format with Invalid Opcode", False, e)

        # Test get_hex with a valid opcode
        print("\n=== Testing get_hex with Valid Opcode ===")
        try:
            hex_code = handler.get_hex('ADD')
            print(f"Hex Code: {hex_code:02X}")
            log_test_result("get_hex with Valid Opcode", True)
        except Exception as e:
            log_test_result("get_hex with Valid Opcode", False, e)

        # Test get_hex with an invalid opcode
        print("\n=== Testing get_hex with Invalid Opcode ===")
        try:
            handler.get_hex('INVALID')
            log_test_result("get_hex with Invalid Opcode", False, "No exception raised")
        except ValueError:
            log_test_result("get_hex with Invalid Opcode", True)
        except Exception as e:
            log_test_result("get_hex with Invalid Opcode", False, e)

        # Test is_opcode_mnemonic with a valid opcode
        print("\n=== Testing is_opcode_mnemonic with Valid Opcode ===")
        try:
            is_valid = handler.is_opcode_mnemonic('ADD')
            print(f"Is Valid Opcode: {is_valid}")
            log_test_result("is_opcode_mnemonic with Valid Opcode", is_valid)
        except Exception as e:
            log_test_result("is_opcode_mnemonic with Valid Opcode", False, e)

        # Test is_opcode_mnemonic with an invalid opcode
        print("\n=== Testing is_opcode_mnemonic with Invalid Opcode ===")
        try:
            is_valid = handler.is_opcode_mnemonic('INVALID')
            print(f"Is Valid Opcode: {is_valid}")
            log_test_result("is_opcode_mnemonic with Invalid Opcode", not is_valid)
        except Exception as e:
            log_test_result("is_opcode_mnemonic with Invalid Opcode", False, e)

        # Summary of test results
        print("\n=== Test Results Summary ===")
        print(f"Total Tests Passed: {passed_tests}")
        print(f"Total Tests Failed: {failed_tests}")
        if failed_tests > 0:
            print("\nFailed Test Details:")
            for detail in failed_test_details:
                print(detail)

        print("\n=== All Tests Completed ===")

def main():
    # Create an instance of ErrorLogHandler
    logger = ErrorLogHandler()

    # Check if a file name is provided as a command-line argument
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'opcodes.txt'

    # Create an instance of OpcodeHandler with the provided file name
    try:
        opcode_handler = OpcodeHandler(file_name, logger)
    except Exception as e:
        logger.log_error(f"Failed to create OpcodeHandler: {e}", "Initialization Error")
        logger.display_errors()
        return

    # Print all loaded opcodes
    logger.log_action("\nLoaded Opcodes:", False)
    try:
        opcode_handler.print_opcodes()
    except Exception as e:
        logger.log_error(f"Failed to print opcodes: {e}", "Print Error")


    # Run tests
    print("\n=== Running OpcodeHandler Tests ===")
    OpcodeHandler.test()

# Run the main program
if __name__ == "__main__":
    main()