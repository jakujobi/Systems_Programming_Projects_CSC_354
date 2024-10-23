import sys
import re
from FileExplorer import FileExplorer

# Include the OpcodeHandler class here (from the previous code)
class OpcodeHandler:
    def __init__(self, file_path='opcodes.txt'):
        """
        Initializes the OpcodeHandler with an empty opcode dictionary.
        Creates an instance of FileExplorer to handle file operations.
        """
        self.opcodes = {}  # Dictionary to store opcode info
        self.file_explorer = FileExplorer()  # Create a new instance of FileExplorer
        self.file_path = file_path
        self._load_opcodes()  # Private method to load opcodes on initialization

    def _load_opcodes(self):
        """
        Reads the opcodes from the file using FileExplorer and loads them into the dictionary.
        Expects a space-separated file with 'name format hex' structure.
        """
        try:
            # Use the FileExplorer's method to get the file contents as a list of lines
            lines = self.file_explorer.process_file(self.file_path)

            if not lines:
                print("No lines found in the file.")
                return

            for line_num, line in enumerate(lines, start=1):
                # Use regex to handle inconsistent spacing
                parts = re.split(r'\s+', line.strip())

                if len(parts) != 3:
                    print(f"Invalid format on line {line_num}: {line.strip()}")
                    continue

                name, format_type, hex_code = parts

                # Convert format to tuple for "3/4" and integer for others
                if format_type == "3/4":
                    format_parsed = (3, 4)
                else:
                    try:
                        format_parsed = int(format_type)
                    except ValueError:
                        print(f"Invalid format type on line {line_num}: {format_type}")
                        continue

                # Convert hex to integer
                try:
                    hex_value = int(hex_code, 16)
                except ValueError:
                    print(f"Invalid hex code on line {line_num}: {hex_code}")
                    continue

                # Store opcode information
                self.opcodes[name] = {
                    'format': format_parsed,
                    'hex': hex_value
                }

        except Exception as e:
            print(f"An error occurred while loading opcodes: {e}")

    def get_opcode(self, name):
        """
        Retrieves the opcode information for the given mnemonic.
        """
        return self.opcodes.get(name, None)

    def get_format(self, name):
        """
        Returns the format of the specified opcode, if found.
        """
        opcode = self.get_opcode(name)
        if opcode:
            return opcode['format']
        else:
            raise ValueError(f"Opcode '{name}' not found.")

    def get_hex(self, name):
        """
        Returns the hexadecimal representation of the specified opcode, if found.
        """
        opcode = self.get_opcode(name)
        if opcode:
            return opcode['hex']
        else:
            raise ValueError(f"Opcode '{name}' not found.")

    def print_opcodes(self):
        """
        Prints all loaded opcodes to the screen in a readable format.
        """
        if not self.opcodes:
            print("No opcodes loaded.")
            return
        
        print(f"{'Mnemonic':<10} {'Format':<10} {'Hex Code':<10}")
        print("=" * 30)
        for name, info in self.opcodes.items():
            format_str = f"{info['format']}"  # Convert format to string for display
            hex_str = f"{info['hex']:02X}"  # Convert hex to uppercase string
            print(f"{name:<10} {format_str:<10} {hex_str:<10}")


def main():
    # Check if a file name is provided as a command-line argument
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'opcodes.txt'

    # Create an instance of OpcodeHandler with the provided file name
    opcode_handler = OpcodeHandler(file_name)

    # Print all loaded opcodes
    print("\nLoaded Opcodes:")
    opcode_handler.print_opcodes()

    # Test retrieval of specific opcode information
    test_mnemonics = ['ADD', 'SUB', 'LDA', 'INVALID']
    for mnemonic in test_mnemonics:
        try:
            print(f"\nDetails for '{mnemonic}':")
            opcode_info = opcode_handler.get_opcode(mnemonic)
            if opcode_info:
                print(f"Format: {opcode_info['format']}, Hex Code: {opcode_info['hex']:02X}")
            else:
                print("Opcode not found.")
        except ValueError as e:
            print(e)


# Run the main program
if __name__ == "__main__":
    main()
