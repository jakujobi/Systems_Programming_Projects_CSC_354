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
    def __init__(self, source_line, line_text):
        self.source_line = source_line
        self.line_text = line_text

    def parse_line(self):
        self.reset_source_line()
        line = self.line_text.strip()

        # Handle empty or comment lines
        if not line or line.startswith(SourceCodeLine.comment_symbol):
            self.handle_comment_line(line)
            return

        # Handle inline comments
        comment_split = line.split(SourceCodeLine.comment_symbol, 1)
        code_part = comment_split[0].strip()
        comment_part = comment_split[1].strip() if len(comment_split) > 1 else ''
        self.source_line.comment = SourceCodeLine.comment_symbol + comment_part if comment_part else ''

        tokens = code_part.split()
        label = None
        opcode = None
        operands = []

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
            operands = [operand.strip() for operand in operands_str.split(',')]

        # Update SourceCodeLine
        self.source_line.label = label
        self.source_line.opcode = opcode
        self.source_line.set_operands(operands)

    def reset_source_line(self):
        self.source_line.label = None
        self.source_line.opcode = None
        self.source_line.operands = []
        self.source_line.comment = ''
        self.source_line.is_comment = False
        self.source_line.clear_errors()

    def handle_comment_line(self, line):
        self.source_line.is_comment = True
        self.source_line.comment = line.strip()

    @classmethod
    def test(cls):
        """
        Tests various parsing scenarios for ParsingHandler.
        """
        test_cases = [
            ("LOOP: LDA BUFFER,X . Load A register with BUFFER indexed", 
             {'label': 'LOOP', 'opcode': 'LDA', 'operands': ['BUFFER,X'], 'comment': '. Load A register with BUFFER indexed'}),
            ("START 1000", 
             {'label': None, 'opcode': 'START', 'operands': ['1000'], 'comment': None}),
            ("BUFFER,X", 
             {'label': None, 'opcode': None, 'operands': ['BUFFER,X'], 'comment': None}),
            ("RSUB", 
             {'label': None, 'opcode': 'RSUB', 'operands': [], 'comment': None}),
            ("  . This is a full line comment", 
             {'label': None, 'opcode': None, 'operands': [], 'comment': '. This is a full line comment', 'is_comment': True}),
            ("  ", 
             {'label': None, 'opcode': None, 'operands': [], 'comment': None, 'is_comment': True}),
            ("+LDA @BUFFER", 
             {'label': None, 'opcode': '+LDA', 'operands': ['@BUFFER'], 'comment': None}),
            ("LDA #LENGTH+2", 
             {'label': None, 'opcode': 'LDA', 'operands': ['#LENGTH+2'], 'comment': None}),
            ("BUFFER:   ", 
             {'label': 'BUFFER', 'opcode': None, 'operands': [], 'comment': None}),
            ("EQU   HERE-ALPHA,X", 
             {'label': None, 'opcode': 'EQU', 'operands': ['HERE-ALPHA,X'], 'comment': None})
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
                if actual_value != value:
                    success = False
                    print(f"Failed: {key} | Expected: {value} | Got: {actual_value}")
                    failed_test_details.append(f"Test Case {i}: {key} | Expected: {value} | Got: {actual_value}")
            
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



