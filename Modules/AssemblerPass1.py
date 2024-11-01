# AssemblerPass1.py

import os
import sys
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import SourceCodeLine
from Modules.ParsingHandler import ParsingHandler
from Modules.OpcodeHandler import OpcodeHandler
from Modules.LocationCounter import LocationCounter
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.Symbol_Table_Builder import *




class AssemblerPass1:
    """
    AssemblerPass1 handles the first pass of the SIC/XE assembler.
    It processes the source code, builds the symbol table, and computes addresses.
    """

    def __init__(self, source_file_path, logger=None):
        """
        Initializes the AssemblerPass1 instance.

        :param source_file_path: Path to the source code file.
        :param logger: Instance of ErrorLogHandler for logging.
        """
        self.source_file_path = source_file_path
        self.source_lines = []
        self.symbol_table = SymbolTable()
        self.opcode_handler = OpcodeHandler()
        self.logger = logger or ErrorLogHandler()
        self.location_counter = LocationCounter(opcode_handler=self.opcode_handler,
                                                symbol_table=self.symbol_table,
                                                logger=self.logger)
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0

    def load_source_file(self):
        """
        Loads the source code from the file into source_lines list.
        """
        if not os.path.exists(self.source_file_path):
            raise FileNotFoundError(f"Source file '{self.source_file_path}' not found.")

        with open(self.source_file_path, 'r') as file:
            lines = file.readlines()

        for idx, line in enumerate(lines, start=1):
            source_line = SourceCodeLine(line_number=idx, line_text=line.rstrip('\n'))
            self.source_lines.append(source_line)

    def process_lines(self):
        """
        Processes each line in the source code.
        """
        # Initialize the location counter
        self.location_counter.set_start_address(0)

        for source_line in self.source_lines:
            # Create a ParsingHandler for the line
            parser = ParsingHandler(source_line, source_line.line_text, validate_parsing=True,
                                    logger=self.logger, opcode_handler=self.opcode_handler)
            parser.parse_line()

            # Handle START directive
            if source_line.opcode and source_line.opcode.upper() == 'START':
                # Set starting address
                if source_line.operands:
                    try:
                        start_address = int(source_line.operands, 16)
                        self.program_start_address = start_address
                        self.location_counter.set_start_address(start_address)
                        if source_line.label:
                            self.program_name = source_line.label
                            # Also, add program name to symbol table
                            self.symbol_table.insert_symbol(source_line.label, start_address)
                        continue  # Skip further processing for START line
                    except ValueError:
                        error_msg = f"Invalid starting address '{source_line.operands}'."
                        self.logger.log_error(error_msg)
                        source_line.add_error(error_msg)
                else:
                    error_msg = "Missing starting address in START directive."
                    self.logger.log_error(error_msg)
                    source_line.add_error(error_msg)
                    continue  # Skip further processing for START line

            # Handle END directive
            if source_line.opcode and source_line.opcode.upper() == 'END':
                # Optionally, handle any necessary processing for END
                break  # Assuming END indicates end of source code

            # Set the current label in location counter (for directives like EQU)
            # Note: The label is used in handle_equ_directive()
            self.location_counter.current_label = source_line.label

            # Increment the location counter
            self.location_counter.increment(source_line)

        # After processing all lines, calculate program length
        self.program_length = self.location_counter.calculate_program_length()

    def run(self):
        """
        Runs the assembler pass 1.
        """
        try:
            self.load_source_file()
            self.process_lines()
            # Optionally, generate intermediate file
            # self.generate_intermediate_file()
            # Display symbol table
            self.display_symbol_table()
            # Display program length
            print(f"\nProgram Length: {self.program_length:04X}h")
        except Exception as e:
            print(f"An error occurred during Pass 1: {e}")

    def display_symbol_table(self):
        """
        Displays the symbol table.
        """
        print("\nSymbol Table:")
        self.symbol_table.view()

    def generate_intermediate_file(self, output_file_path="Pass1.txt"):
        """
        Generates an intermediate file for use in Pass 2.

        :param output_file_path: Path to the intermediate file.
        """
        with open(output_file_path, 'w') as file:
            for source_line in self.source_lines:
                # Use the line's address if available, else '----'
                address = f"{source_line.address:04X}" if hasattr(source_line, 'address') else '----'
                line = f"{address} {source_line.line_text}"
                file.write(line + "\n")
