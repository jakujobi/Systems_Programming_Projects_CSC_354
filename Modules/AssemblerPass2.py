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
from Modules.IntermediateFileParser import *


class AssemblerPass2:
    def __init__(self, int_filename: str,
                 file_explorer: FileExplorer = None,
                 logger: ErrorLogHandler = None,
                 Program_length_prefix_for_Hex: str = "Program Length (HEX):",
                 Program_length_prefix_for_Decimal: str = "Program Length (DEC):",
                 character_literal_prefix: str = '0C',
                 hex_literal_prefix: str = '0X',
                 allow_error_lines_in_generated_document: bool = True):
        
        self.int_file_name = int_filename
        self.int_file_content = []
        self.int_source_code_lines = []
        
        self.logger = logger or ErrorLogHandler()


        # Symbol Table
        self.symbol_table = SymbolTable()
        #self.symbol_table_driver = SymbolTableDriver(logger=self.logger)
        self.literal_table = LiteralTableList(logger=self.logger)
        
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0
        
        self.Program_length_prefix_for_Hex = Program_length_prefix_for_Hex or "Program Length (HEX):"
        self.Program_length_prefix_for_Decimal = Program_length_prefix_for_Decimal or "Program Length (DEC):"
        
        self.Start_div_symbol_table = "===SYM_START==="
        self.End_div_symbol_table = "===SYM_END==="
        self.Start_div_literal_table = "===LIT_START==="
        self.End_div_literal_table = "===LIT_END==="
        self.Start_div_program_length = "===PROG_LEN_START==="
        self.End_div_program_length = "===PROG_LEN_END==="
        
        self.character_literal_prefix = character_literal_prefix or '0C'
        self.hex_literal_prefix = hex_literal_prefix or '0X'
        
        self.file_explorer = file_explorer or FileExplorer()
        
        
    def run(self):
        self.load_immediate_file()
        self.parse_intermediate_lines()
        self.print_all_things()

    def load_immediate_file(self):
        """
        Loads the source code from the file into int_file_content list.
        """
        self.int_file_content = self.file_explorer.read_file_raw(self.int_file_name)
        # Check if the file is empty
        if not self.int_file_content:
            self.logger.log_error(f"The file '{self.int_file_name}' is empty.")
            return
        # Log the number of lines read
        self.logger.log_action(f"Read {len(self.int_file_content)} lines from '{self.int_file_name}'.")

    def parse_intermediate_lines(self):
        int_file_parser = IntermediateFileParser(symbol_table_passed=self.symbol_table,
                                                 literal_table_passed=self.literal_table,
                                                 logger=self.logger,
                                                 int_file_content=self.int_file_content)
        int_file_parser.parse_intermediate_file_content()
        self.int_source_code_lines = int_file_parser.parsed_code_lines
    
    def print_all_things(self):
        """
        Prints out the symbol table, literal table and the parsed content of the intermediate file.

        :return: None
        """
        # print the int file content
        for line in self.int_source_code_lines:
            print(line)
        
        print(self.symbol_table)
        print(self.literal_table)
