import sys
import os
import re

from symbol_table_builder import *
from OpcodeHandler import *
from SourceCodeLine import *
from ErrorLogHandler import *
from FileExplorer import *
from Literal_table_builder import *


import re
from SourceCodeLine import SourceCodeLine  # Assuming you have SourceCodeLine defined in a separate module

class ParsingHandler:
    """
    Handles parsing of a single line of assembly code into components: label, opcode, operands, and comments.
    """

    def __init__(self, source_line, line_text):
        """
        Initializes the ParsingHandler with a SourceCodeLine instance and a line of assembly code.
        
        :param source_line: An instance of SourceCodeLine to store parsed results.
        :param line_text: The raw line of code to parse.
        """
        if not isinstance(source_line, SourceCodeLine):
            raise TypeError("source_line must be an instance of SourceCodeLine")
        
        self.source_line = source_line
        self.line_text = line_text

    def parse_line(self):
        """
        Parses the line into components: label, opcode, operands, and comments.
        Updates the SourceCodeLine instance accordingly.
        """
        self.reset_source_line()
        line = self.line_text.strip()

        # Handle empty or comment lines
        if not line or line.startswith(SourceCodeLine.comment_symbol):
            self.handle_comment_line(line)
            return

        # Handle inline comments
        if SourceCodeLine.comment_symbol in line:
            code_part, comment_part = line.split(SourceCodeLine.comment_symbol, 1)
            comment_part = comment_part.strip()
            self.source_line.comment = SourceCodeLine.comment_symbol + ' ' + comment_part
        else:
            code_part = line

        tokens = code_part.strip().split()

        label = None
        opcode = None
        operands_str = ''

        # Extract label
        if tokens and ':' in tokens[0]:
            label_token = tokens.pop(0)
            label = label_token.rstrip(':')
        elif tokens and tokens[0].endswith(':'):
            label_token = tokens.pop(0)
            label = label_token.rstrip(':')

        # Extract opcode
        if tokens:
            opcode = tokens.pop(0)

        # Extract operands
        if tokens:
            operands_str = ' '.join(tokens)

        # Update SourceCodeLine
        self.source_line.label = label
        self.source_line.opcode = opcode
        self.source_line.set_operands(operands_str)

    def reset_source_line(self):
        """
        Clears the attributes of SourceCodeLine before parsing a new line.
        Ensures that previous data doesn't interfere with the new parsing process.
        """
        self.source_line.label = None
        self.source_line.opcode = None
        self.source_line.operands = ''
        self.source_line.operands_list = []
        self.source_line.comment = ''
        self.source_line.is_comment = False
        self.source_line.clear_errors()

    def handle_comment_line(self, line):
        """
        Handles lines that are purely comments and sets is_comment to True in SourceCodeLine.
        """
        self.source_line.comment = line.strip()
        self.source_line.is_comment = True

    @classmethod
    def test(cls):
        """
        Tests various parsing scenarios for ParsingHandler.
        """
        test_cases = [
            ("LOOP: LDA BUFFER,X . Load A register with BUFFER indexed", 
             {'label': 'LOOP', 'opcode': 'LDA', 'operands': 'BUFFER,X', 'comment': '. Load A register with BUFFER indexed'}),
            ("START 1000", 
             {'label': None, 'opcode': 'START', 'operands': '1000', 'comment': ''}),
            ("BUFFER,X", 
             {'label': None, 'opcode': 'BUFFER,X', 'operands': '', 'comment': ''}),
            ("RSUB", 
             {'label': None, 'opcode': 'RSUB', 'operands': '', 'comment': ''}),
            ("  . This is a full line comment", 
             {'label': None, 'opcode': None, 'operands': '', 'comment': '. This is a full line comment', 'is_comment': True}),
            ("  ", 
             {'label': None, 'opcode': None, 'operands': '', 'comment': '', 'is_comment': True}),
            ("+LDA @BUFFER", 
             {'label': None, 'opcode': '+LDA', 'operands': '@BUFFER', 'comment': ''}),
            ("LDA #LENGTH+2", 
             {'label': None, 'opcode': 'LDA', 'operands': '#LENGTH+2', 'comment': ''}),
            ("BUFFER:   ", 
             {'label': 'BUFFER', 'opcode': None, 'operands': '', 'comment': ''}),
            ("EQU   HERE-ALPHA,X", 
             {'label': None, 'opcode': 'EQU', 'operands': 'HERE-ALPHA,X', 'comment': ''}),
            # Additional complex cases
            ("ALPHA: EQU #1000", 
             {'label': 'ALPHA', 'opcode': 'EQU', 'operands': '#1000', 'comment': ''}),
            ("ADD ALPHA-@BETA", 
             {'label': None, 'opcode': 'ADD', 'operands': 'ALPHA-@BETA', 'comment': ''}),
            ("ADD ALPHA+#BETA", 
             {'label': None, 'opcode': 'ADD', 'operands': 'ALPHA+#BETA', 'comment': ''}),
            ("EQUAL: EQU HERE", 
             {'label': 'EQUAL', 'opcode': 'EQU', 'operands': 'HERE', 'comment': ''}),
            ("idkwhatimdoingonthislinespace:", 
             {'label': 'idkwhatimdoingonthislinespace', 'opcode': None, 'operands': '', 'comment': ''}),
            ("+JSUB   @RDREC", 
             {'label': None, 'opcode': '+JSUB', 'operands': '@RDREC', 'comment': ''}),
            ("JLT     LOOP", 
             {'label': None, 'opcode': 'JLT', 'operands': 'LOOP', 'comment': ''}),
            ("BYTE    C'EOF'", 
             {'label': None, 'opcode': 'BYTE', 'operands': "C'EOF'", 'comment': ''}),
            ("WORD    -1", 
             {'label': None, 'opcode': 'WORD', 'operands': '-1', 'comment': ''}),
            ("END     FIRST", 
             {'label': None, 'opcode': 'END', 'operands': 'FIRST', 'comment': ''}),
        ]
    
        passed_tests = 0
        failed_tests = 0
        failed_test_details = []
    
        for i, (line_text, expected) in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i} ---")
            source_line = SourceCodeLine(line_number=i, line_text=line_text)
            parser = cls(source_line, line_text)
            parser.parse_line()
    
            # Verify results
            success = True
            for key, value in expected.items():
                actual_value = getattr(source_line, key)
                if key == 'operands':
                    # Compare operands after stripping
                    if actual_value.strip() != value.strip():
                        success = False
                        print(f"Failed: {key} | Expected: '{value}' | Got: '{actual_value}'")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: '{value}' | Got: '{actual_value}'")
                elif key == 'comment':
                    if actual_value.strip() != value.strip():
                        success = False
                        print(f"Failed: {key} | Expected: '{value}' | Got: '{actual_value}'")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: '{value}' | Got: '{actual_value}'")
                else:
                    if actual_value != value:
                        success = False
                        print(f"Failed: {key} | Expected: '{value}' | Got: '{actual_value}'")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: '{value}' | Got: '{actual_value}'")
    
            if success:
                print("Test passed.")
                passed_tests += 1
            else:
                failed_tests += 1
    
        # Summary of test results
        print("\n=== Test Results Summary ===")
        print(f"Total Tests Passed: {passed_tests}")
        print(f"Total Tests Failed: {failed_tests}")
        if failed_tests > 0:
            print("\nFailed Test Details:")
            for detail in failed_test_details:
                print(detail)
    
        print("\n=== All Tests Completed ===")

# Example usage
if __name__ == "__main__":
    ParsingHandler.test()
