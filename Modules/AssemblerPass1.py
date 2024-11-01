# AssemblerPass1.py

import os
import sys
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import *
from Modules.ParsingHandler import *
from Modules.OpcodeHandler import *
from Modules.LocationCounter import *
from Modules.ErrorLogHandler import *
from Modules.Symbol_Table_Builder import *
from Modules.Literal_Table_Builder import *
from Modules.FileExplorer import *

class AssemblerPass1:
    """
    AssemblerPass1 handles the first pass of the SIC/XE assembler.
    It processes the source code, builds the symbol table, and computes addresses.
    """

    def __init__(self, filename: str, logger: ErrorLogHandler = None):
        """
        Initializes the AssemblerPass1 instance.

        :param source_file_path: Path to the source code file.
        :param logger: Instance of ErrorLogHandler for logging.
        """
        self.source_file = filename
        self.intermediate_file = None
        self.log_file = None
        
        
        
        
        self.source_lines = []
        self.generated_lines = []
        self.FileExplorer = FileExplorer()
        self.symbol_table = SymbolTable()
        self.opcode_handler = OpcodeHandler()
        self.logger = logger or ErrorLogHandler()
        self.location_counter = LocationCounter(opcode_handler=self.opcode_handler, symbol_table=self.symbol_table, logger=self.logger)
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0
    
        self.run()

    def run(self):
        """
        Executes the first pass of the assembler.
        """
        # Load the source code from the file
        self.load_source_file()
        
        # Create the intermediate file and keep it open for writing
        self.create_intermediate_file()
        
        # Process all the source code lines
        self.process_source_lines(self.source_lines)
        
        # After processing all lines, calculate program length
        self.calculate_program_length()
        
        # Display the symbol table and write it to the generated file
        self.add_symbol_table(add_to_file=True)
        
        # Display the literal table and write it to the generated file
        self.add_literal_table(add_to_file=True)
        
        # Display the error log and write it to the generated file
        self.create_log_file()
        
    def load_source_file(self):
        """
        Loads the source code from the file into source_lines list.
        """
        if not os.path.exists(self.source_file_path):
            raise FileNotFoundError(f"Source file '{self.source_file_path}' not found.")

        lines = []
        lines = self.
    
    def process_source_lines(self, lines):
        """
        Processes multiple lines of source code.
        """
        self.location_counter.set_start_address(0)
        for line in lines:
            self.process_single_line(line)

    def process_single_line(self, source_line: SourceCodeLine):
        """
        Processes a single line of source code.
        """
        # Create a ParsingHandler for the line and parse it
        parser = ParsingHandler(source_line, source_line.line_text, validate_parsing=True, logger=self.logger, opcode_handler=self.opcode_handler)
        parser.parse_line()

        # Handle directives
        self.check_for_directives(source_line, handle_directives=True)

        # Calculate instruction length
        self.calculate_instruction_length(source_line)

        # Update the symbol table
        self.update_symbol_table(source_line)

        # Update the literal table
        self.update_literal_table(source_line)

        # Increment the location counter
        self.location_counter.increment(source_line.instruction_length)

        # Update the source line with address and object code
        self.update_source_line(source_line)

        # Check for errors
        self.check_for_errors(source_line)

        # Print the source line with address and object code
        self.print_source_line(source_line)

        # Add line to generated file
        self.add_line_to_generated_file(source_line)

    def check_for_directives(self, source_line: SourceCodeLine, handle_directives: bool = True):
        """
        Checks for directives in the source line.
        """

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Handles a directive in the source line.
        """
        
        
    def handle_START_directive(self, source_line: SourceCodeLine):
        """
        Handles the START directive.
        """
        # Set starting address
        # If it has an operand, verify, then set the starting address
        # If it doesn't have an operand, set the starting address to 0


    def handle_EQU_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive.
        """
        # Update the symbol table

    def handle_END_directive(self, source_line: SourceCodeLine):
        """
        Handles the END directive.
        """
        # Set the program length

    def handle_other_directives(self, source_line: SourceCodeLine):
        """
        Handles other directives.
        """
        pass

    def calculate_instruction_length(self, source_line: SourceCodeLine):
        """
        Calculates the instruction length for the source line.
        """
        # Calculate instruction length based on opcode and operands
        pass

    def update_symbol_table(self, source_line: SourceCodeLine):
        """
        Updates the symbol table with the source line information.
        """
        # Update symbol table
        pass

    def update_literal_table(self, source_line: SourceCodeLine):
        """
        Updates the literal table with the source line information.
        """
        # Update literal table
        pass

    def update_source_line(self, source_line: SourceCodeLine):
        """
        Updates the source line with address and object code.
        """
        # Update source line
        pass

    def check_for_errors(self, source_line: SourceCodeLine):
        """
        Checks for errors in the source line.
        """
        # Check for errors
        pass

    def print_source_line(self, source_line: SourceCodeLine):
        """
        Prints the source line with address and object code.
        """
        # Print source line
        pass

    def add_line_to_generated_file(self, source_line: SourceCodeLine):
        """
        Adds the source line to the generated file.
        """
        # Add line to generated file
        pass

    def calculate_program_length(self):
        """
        Calculates the program length.
        """
        self.program_length = self.location_counter.get_current_address() - self.program_start_address

    def add_symbol_table(self, add_to_file: bool = False):
        """
        Adds the symbol table to the output.
        """
        # Display and write the symbol table
        pass

    def add_literal_table(self, add_to_file: bool = False):
        """
        Adds the literal table to the output.
        """
        # Display and write the literal table
        pass

    def create_log_file(self):
        """
        Creates the log file with errors and actions.
        """
        # Create log file
        pass

# Example usage
if __name__ == "__main__":
    assembler = AssemblerPass1("source.asm")