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
        if self.is_empty_or_comment():
            return

        line = self.source_line.line_text.strip()
        line = self.extract_label(line)
        line = self.extract_comment(line)
        line = self.extract_opcode(line)
        line = self.extract_operands(line)
        self.check_remaining_characters(line)

    def is_empty_or_comment(self) -> bool:
        """
        Checks if the line is empty or a comment.
        """
        if self.source_line.is_empty_line():
            self.logger.log_action(f"Skipping empty line on Line {self.source_line.line_number}: {self.source_line.line_text}")
            return True

        if self.source_line.is_comment():
            self.source_line.comment = self.source_line.line_text.strip()
            return True

        return False

    def extract_label(self, line: str) -> str:
        """
        Extracts the label from the line.
        """
        label_end_index = line.find(SourceCodeLine.label_suffix_symbol)
        if label_end_index != -1:
            self.source_line.label = line[:label_end_index].strip()
            line = line[label_end_index + 1:].strip()
        return line

    def extract_comment(self, line: str) -> str:
        """
        Extracts the comment from the line.
        """
        comment_start_index = line.find(SourceCodeLine.comment_symbol)
        if comment_start_index != -1:
            self.source_line.comment = line[comment_start_index + 1:].strip()
            line = line[:comment_start_index].strip()
        return line

    def extract_opcode(self, line: str) -> str:
        """
        Extracts the opcode from the line.
        """
        parts = line.split()
        if parts:
            self.source_line.opcode_mnemonic = parts[0].strip()
            line = line[len(self.source_line.opcode_mnemonic):].strip()
        return line

    def extract_operands(self, line: str) -> str:
        """
        Extracts the operands from the line.
        """
        self.source_line.operands = line.strip()
        return ''

    def check_remaining_characters(self, line: str):
        """
        Checks if there are any remaining characters after removing the label, opcode, and operands.
        """
        if line.strip():
            error_message = f"Invalid syntax on Line {self.source_line.line_number}: {self.source_line.line_text}\n Remaining characters after parsing: {line}"
            self.logger.log_error(error_message)
            raise SyntaxError(error_message)

# Example usage
if __name__ == "__main__":
    source_line = SourceCodeLine(line_number=1, line_text="LABEL: LDA BUFFER,X . This is a comment")
    parser = ParsingHandler(source_line, validate_parsing=True)
    parser.parse_line()
    print(source_line)