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


class AssemblerPass2:
    def __init__(self, int_filename: str, logger: ErrorLogHandler = None, character_literal_prefix: str = '0C', hex_literal_prefix: str = '0X', allow_error_lines_in_generated_document: bool = True, stop_on_error: bool = False, generated_file_extension: str = '.int'):
        self.int_file_name = int_filename
        self.int_file_content = []

        # Symbol Table
        self.symbol_table = SymbolTable()
        self.symbol_table_driver = SymbolTableDriver(logger=self.logger)
        self.literal_table = LiteralTableList(log_handler=self.logger)
        
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0
        
        self.Program_length_prefix_for_Hex = "Program Length (HEX):" or Program_length_prefix_for_Hex
        self.Program_length_prefix_for_Decimal = "Program Length (DEC):" or Program_length_prefix_for_Decimal
        
        self.Start_div_symbol_table = "===SYM_START==="
        self.End_div_symbol_table = "===SYM_END==="
        self.Start_div_literal_table = "===LIT_START==="
        self.End_div_literal_table = "===LIT_END==="
        self.Start_div_program_length = "===PROG_LEN_START==="
        self.End_div_program_length = "===PROG_LEN_END==="
        
        pass
    def run(self):
        pass
    def load_immediate_file(self):
        """
        Loads the source code from the file into int_file_content list.
        """
        self.int_file_content = self.FileExplorer.read_file_raw(self.int_file_name)
        # Check if the file is empty
        if not self.int_file_content:
            self.logger.log_error(f"The file '{self.int_file_name}' is empty.")
            return
        # Log the number of lines read
        self.logger.log_action(f"Read {len(self.int_file_content)} lines from '{self.int_file_name}'.")
        pass
    def parse_intermediate_lines(self):
        pass