import sys
import re
from FileExplorer import FileExplorer

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
            # Use FileExplorer's method to get the file contents as a list of lines
            lines = self.file_explorer.process_file(self.file_path)

            if not lines:
                raise FileNotFoundError(f"No lines found in '{self.file_path}' or file is empty.")

            for line_num, line in enumerate(lines, start=1):
                # Use regex to handle inconsistent spacing
                parts = re.split(r'\s+', line.strip())

                # Ensure the line has exactly 3 parts
                if len(parts) != 3:
                    print(f"[Error] Line {line_num} has an invalid format: '{line.strip()}'")
                    continue

                name, format_type, hex_code = parts

                # Validate and convert the format type
                try:
                    format_parsed = (3, 4) if format_type == "3/4" else int(format_type)
                except ValueError:
                    print(f"[Error] Line {line_num} has an invalid format type: '{format_type}'")
                    continue

                # Validate and convert the hex code
                try:
                    hex_value = int(hex_code, 16)
                except ValueError:
                    print(f"[Error] Line {line_num} has an invalid hex code: '{hex_code}'")
                    continue

                # Store the opcode information
                self.opcodes[name] = {
                    'format': format_parsed,
                    'hex': hex_value
                }

        except FileNotFoundError as e:
            print(f"[File Error] {e}")
        except Exception as e:
            print(f"[Unexpected Error] An error occurred while loading opcodes: {e}")

    def get_opcode(self, name):
        """
        Retrieves the opcode information for the given mnemonic.
        """
        try:
            return self.opcodes[name]
        except KeyError:
            raise ValueError(f"Opcode '{name}' not found.")

    def get_format(self, name):
        """
        Returns the format of the specified opcode, if found.
        """
        opcode = self.get_opcode(name)
        return opcode['format']

    def get_hex(self, name):
        """
        Returns the hexadecimal representation of the specified opcode, if found.
        """
        opcode = self.get_opcode(name)
        return opcode['hex']

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