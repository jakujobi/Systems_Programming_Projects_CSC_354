import re
import os
import sys


repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import SourceCodeLine
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.OpcodeHandler import OpcodeHandler
from Modules.Symbol_Table_Builder import Validator

class ParsingHandler:
    """
    Handles parsing of a single line of assembly code into components: label, opcode, operands, and comments.
    Includes validation if validate_parsing is set to True.
    """
    
    def __init__(self, source_line, validate_parsing=False, logger=None, opcode_handler=None):
        self.source_line = source_line
        self.validate_parsing = validate_parsing
        self.logger = logger or ErrorLogHandler()
        self.opcode_handler = opcode_handler

    def parse_line(self):
        """
        Parses the line into components: label, opcode, operands, and comments.
        Validates the components if validate_parsing is True.
        Updates the SourceCodeLine instance accordingly.
        """
        # Check if the line is empty
        if self.source_line.is_empty_line():
            self.logger.log_action(f"Skipping empty line on Line {self.source_line.line_number}: {self.source_line.line_text}")
            return

        # Check if the line is a comment
        if self.source_line.is_comment():
            self.source_line.comment = self.source_line.line_text.strip()
            return
        
        # Copy the line text to avoid modifying the original line        
        copy_of_line = self.source_line.line_text
        # strip the line text
        copy_of_line = copy_of_line.strip()
        
        
        ### Now we know that the line is not empty and not a comment
        #Fish out the label. It ends with the symbol stored in source_line.label_suffix_symbol. For example, in "LABEL:", the label is "LABEL".
        self.source_line.label = copy_of_line.split(SourceCodeLine.label_suffix_symbol)[0].strip()
        #Remove the label from the line
        copy_of_line = copy_of_line.replace(self.source_line.label, "").strip()

        # Extract the comment if it exists
        self.source_line.comment = copy_of_line.split(SourceCodeLine.comment_symbol, 1)[-1].strip()
        # Remove the comment from the line
        copy_of_line = copy_of_line.split(SourceCodeLine.comment_symbol, 1)[0].strip()
        
        # Extract the opcode
        self.source_line.opcode_mnemonic = copy_of_line.split()[0].strip()
        # Remove the opcode from the line
        copy_of_line = copy_of_line.replace(self.source_line.opcode_mnemonic, "").strip()
        
        # Extract the operands
        self.source_line.operands = copy_of_line.strip()
        # Remove the operands from the line
        copy_of_line = copy_of_line.replace(self.source_line.operands, "").strip()
        
        # Check if there are any remaining characters after removing the label, opcode, and operands
        if copy_of_line.strip():
            error_message = f"Invalid syntax on Line {self.source_line.line_number}: {self.source_line.line_text}\n Remaining characters after parsing: {copy_of_line}"
            self.logger.log_error(error_message)
            raise SyntaxError(error_message)