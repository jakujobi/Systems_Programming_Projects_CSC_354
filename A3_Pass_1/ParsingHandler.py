import re
from SourceCodeLine import SourceCodeLine
from ErrorLogHandler import ErrorLogHandler
from OpcodeHandler import OpcodeHandler

class ParsingHandler:
    """
    Handles parsing of a single line of assembly code into components: label, opcode, operands, and comments.
    Includes validation if validate_parsing is set to True.
    """

    def __init__(self, source_line, line_text, validate_parsing=False, logger=None, opcode_handler=None):
        """
        Initializes the ParsingHandler with a SourceCodeLine instance and a line of assembly code.

        :param source_line: An instance of SourceCodeLine to store parsed results.
        :param line_text: The raw line of code to parse.
        :param validate_parsing: Boolean flag to enable or disable validation.
        :param logger: An instance of ErrorLogHandler for logging errors and actions.
        :param opcode_handler: An instance of OpcodeHandler for opcode validation.
        """
        if not isinstance(source_line, SourceCodeLine):
            raise TypeError("source_line must be an instance of SourceCodeLine")

        self.source_line = source_line
        self.line_text = line_text
        self.validate_parsing = validate_parsing
        self.logger = logger or ErrorLogHandler()
        self.opcode_handler = opcode_handler

    def parse_line(self):
        """
        Parses the line into components: label, opcode, operands, and comments.
        Validates the components if validate_parsing is True.
        Updates the SourceCodeLine instance accordingly.
        """
        self.reset_source_line()
        line = self.line_text.strip()

        # Handle empty or comment lines
        if not line or line.startswith(SourceCodeLine.comment_symbol):
            self.handle_comment_line(line)
            return

        try:
            # Handle inline comments
            if SourceCodeLine.comment_symbol in line:
                code_part, comment_part = line.split(SourceCodeLine.comment_symbol, 1)
                self.source_line.comment = SourceCodeLine.comment_symbol + ' ' + comment_part.strip()
            else:
                code_part = line

            tokens = code_part.strip().split()

            label = None
            opcode = None
            operands_str = ''

            # Extract label and opcode
            if tokens:
                # Check if first token is a label (not an opcode)
                first_token = tokens[0]
                # Remove ':' if present
                if first_token.endswith(':'):
                    label = tokens.pop(0).rstrip(':')
                else:
                    opcode_candidate = first_token.lstrip('+').upper()
                    if self.opcode_handler and self.opcode_handler.is_opcode(opcode_candidate):
                        opcode = tokens.pop(0)
                    else:
                        # Assume it's a label
                        label = tokens.pop(0)
                # Extract opcode if not yet set
                if not opcode and tokens:
                    opcode = tokens.pop(0)
            else:
                # Line with only comment or empty
                pass

            # Extract operands
            if tokens:
                operands_str = ' '.join(tokens)

            # Update SourceCodeLine
            self.source_line.label = label
            self.source_line.opcode = opcode
            self.source_line.set_operands(operands_str)

            if self.validate_parsing:
                self.validate_line()

        except Exception as e:
            error_msg = f"Exception occurred while parsing line: {e}"
            self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
            self.source_line.add_error(error_msg)

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

    def validate_line(self):
        """
        Validates the parsed line components: label, opcode, operands.
        Adds errors to SourceCodeLine and logs them using ErrorLogHandler if validation fails.
        """
        self.validate_label()
        self.validate_opcode()
        self.validate_operands()

    def validate_label(self):
        """
        Validates the label for correctness according to assembly language rules.
        """
        label = self.source_line.label
        if label:
            if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', label):
                error_msg = f"Invalid label '{label}'. Labels must start with a letter and contain only alphanumeric characters."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)
            elif len(label) > 10:
                error_msg = f"Label '{label}' is too long. Maximum length is 10 characters."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)

    def validate_opcode(self):
        """
        Validates the opcode using OpcodeHandler.
        """
        opcode = self.source_line.opcode
        if opcode:
            opcode_clean = opcode.lstrip('+').upper()
            if self.opcode_handler:
                if not self.opcode_handler.is_opcode(opcode_clean):
                    error_msg = f"Invalid opcode '{opcode}'."
                    self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                    self.source_line.add_error(error_msg)
            else:
                error_msg = "OpcodeHandler not provided. Cannot validate opcode."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)

    def validate_operands(self):
        """
        Validates the operands for correctness according to assembly language rules.
        """
        operands = self.source_line.operands
        if operands:
            # Check for balanced parentheses and quotes
            if operands.count('(') != operands.count(')'):
                error_msg = f"Unbalanced parentheses in operands '{operands}'."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)
            if operands.count("'") % 2 != 0:
                error_msg = f"Unmatched quotes in operands '{operands}'."
                self.logger.log_error(error_msg, context_info=f"Line {self.source_line.line_number}")
                self.source_line.add_error(error_msg)
            # Additional operand validations can be added here


    @classmethod
    def test(cls):
        """
        Tests various parsing scenarios for ParsingHandler.
        """
        logger = ErrorLogHandler()
        opcode_handler = OpcodeHandler(logger=logger)  # Ensure the opcodes are loaded
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
            source_line = SourceCodeLine(line_number=i, line_text=line_text)
            parser = cls(source_line, line_text, validate_parsing=True, logger=logger, opcode_handler=opcode_handler)
            parser.parse_line()

            # Verify results
            success = True
            for key, value in expected.items():
                actual_value = getattr(source_line, key)
                if key == 'errors':
                    # Extract the error messages
                    actual_errors = [e.split(': ')[-1] for e in actual_value]
                    if sorted(actual_errors) != sorted(value):
                        success = False
                        print(f"Failed: {key} | Expected: {value} | Got: {actual_errors}")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: {value} | Got: {actual_errors}")
                else:
                    if actual_value != value:
                        success = False
                        print(f"Failed: {key} | Expected: '{value}' | Got: '{actual_value}'")
                        failed_test_details.append(f"Test Case {i}: {key} | Expected: '{value}' | Got: '{actual_value}'")

            if success:
                print(f"Test Case {i}: Passed")
                passed_tests += 1
            else:
                print(f"Test Case {i}: Failed")
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

# Run the test if this script is executed directly
if __name__ == "__main__":
    ParsingHandler.test()
