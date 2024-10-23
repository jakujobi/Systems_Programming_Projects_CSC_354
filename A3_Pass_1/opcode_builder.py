import sys
import re
from FileExplorer import FileExplorer
from ErrorLogHandler import ErrorLogHandler

class OpcodeHandler:
    def __init__(self, file_path='opcodes.txt', logger=None):
        """
        Initializes the OpcodeHandler with an empty opcode dictionary.
        Creates an instance of FileExplorer to handle file operations.
        Uses ErrorLogHandler to manage error and action logging.
        """
        self.opcodes = {}  # Dictionary to store opcode info
        self.file_explorer = FileExplorer()  # Create a new instance of FileExplorer
        self.logger = logger if logger else ErrorLogHandler()  # Use provided logger or create one
        self.file_path = file_path
        self._load_opcodes()  # Private method to load opcodes on initialization

    def _load_opcodes(self):
        """
        Reads the opcodes from the file using FileExplorer and loads them into the dictionary.
        Expects a space-separated file with 'name format hex' structure.
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

                name, format_type, hex_code = parts

                # Validate and convert the format type
                try:
                    format_parsed = (3, 4) if format_type == "3/4" else int(format_type)
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

    def print_opcodes(self):
        """
        Prints all loaded opcodes to the screen in a readable format.
        """
        if not self.opcodes:
            self.logger.log_action("No opcodes loaded.", False)
            print("No opcodes loaded.")
            return

        print(f"{'Mnemonic':<10} {'Format':<10} {'Hex Code':<10}")
        print("=" * 30)
        for name, info in self.opcodes.items():
            format_str = f"{info['format']}"  # Convert format to string for display
            hex_str = f"{info['hex']:02X}"  # Convert hex to uppercase string
            print(f"{name:<10} {format_str:<10} {hex_str:<10}")


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
        #logger.display_errors()
        return

    # Print all loaded opcodes
    logger.log_action("\nLoaded Opcodes:", False)
    try:
        opcode_handler.print_opcodes()
    except Exception as e:
        logger.log_error(f"Failed to print opcodes: {e}", "Print Error")

    # Test retrieval of specific opcode information
    test_mnemonics = ['ADD', 'SUB', 'LDA', 'INVALID']
    for mnemonic in test_mnemonics:
        try:
            logger.log_action(f"\nRetrieving details for '{mnemonic}':", False)
            opcode_info = opcode_handler.get_opcode(mnemonic)
            print(f"Format: {opcode_info['format']}, Hex Code: {opcode_info['hex']:02X}")
        except ValueError as e:
            logger.log_error(str(e), "Lookup Error")
        except Exception as e:
            logger.log_error(f"Unexpected error while retrieving '{mnemonic}': {e}", "Unexpected Error")

    # Display logs and errors
    logger.display_log()
    logger.display_errors()


# Run the main program
if __name__ == "__main__":
    main()
