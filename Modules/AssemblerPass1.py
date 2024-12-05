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
   
    
    """
    AssemblerPass1 handles the first pass of the SIC/XE assembler.
    It processes the source code, builds the symbol table, and computes addresses.
    """

    def __init__(self,
                 filename: str,
                 logger: ErrorLogHandler = None,
                 character_literal_prefix: str = '0C',
                 hex_literal_prefix: str = '0X',
                 allow_error_lines_in_generated_document: bool = True,
                 stop_on_error: bool = False,
                 generated_file_extension: str = '.int',
                 Program_length_prefix_for_Hex = "Program Length (HEX):",
                 Program_length_prefix_for_Decimal = "Program Length (DEC):"):
        """
        Initializes the AssemblerPass1 instance.

        :param source_file_path: Path to the source code file.
        :param logger: Instance of ErrorLogHandler for logging.
        """
        self.character_literal_prefix = '0C' or character_literal_prefix
        self.hex_literal_prefix = '0X'or hex_literal_prefix
        
        self.generated_file_extension = '.int' or generated_file_extension
        
        self.source_file = filename
        self.intermediate_file = None
        
        self.allow_error_lines_in_generated_document = True or allow_error_lines_in_generated_document
        self.stop_on_error = False or stop_on_error
        
        self.source_lines = []
        # self.source_code_line = SourceCodeLine()
        
        self.FileExplorer = FileExplorer()
        self.logger = logger or ErrorLogHandler()
        
        self.opcode_handler = OpcodeHandler()
        self.location_counter = LocationCounter(opcode_handler=self.opcode_handler, logger=self.logger)

        # Symbol Table
        self.symbol_table = SymbolTable()
        self.symbol_table_driver = SymbolTableDriver(logger=self.logger)
        self.literal_table = LiteralTableList(logger=self.logger)
        
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0
        
        self.Program_length_prefix_for_Hex = Program_length_prefix_for_Hex or "Program Length (HEX):"
        self.Program_length_prefix_for_Decimal = Program_length_prefix_for_Decimal  or "Program Length (DEC):"
        
        self.Start_div_symbol_table = "===SYM_START==="
        self.End_div_symbol_table = "===SYM_END==="
        self.Start_div_literal_table = "===LIT_START==="
        self.End_div_literal_table = "===LIT_END==="
        self.Start_div_program_length = "===PROG_LEN_START==="
        self.End_div_program_length = "===PROG_LEN_END==="
    
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
        
        # Display the symbol table
        self.display_symbol_table()
        
        # add symbol table to the output
        self.add_symbol_table_to_output_file()
        
        self.display_literal_table()
        
        # add literal table to the output
        self.add_literal_table_to_output_file()
        
        # Print the length of the program using the location counter
        self.program_length = self.calculate_program_length()
        program_length_hex = format(self.program_length, '05X')
        self.logger.log_action(f"{self.Program_length_prefix_for_Hex} {program_length_hex}")
        self.logger.log_action(f"{self.Program_length_prefix_for_Decimal} {self.program_length}")
        self.add_program_length_to_output_file()
        
        # Close the intermediate file after processing
        if self.intermediate_file:
            self.intermediate_file.close()
            self.logger.log_action(f"Closed intermediate file.")
            
        # Close tthe program and exit
        self.logger.log_action(f"Program completed.")
        exit()
        
        
    def load_source_file(self):
        """
        Loads the source code from the file into source_lines list.
        """
        self.source_lines = self.FileExplorer.read_file_raw(self.source_file)
        # Check if the file is empty
        if not self.source_lines:
            self.logger.log_error(f"The file '{self.source_file}' is empty.")
            return
        # Log the number of lines read
        self.logger.log_action(f"Read {len(self.source_lines)} lines from '{self.source_file}'.")
        
    def create_intermediate_file(self):
        """
        Creates the intermediate file for writing.
        """
        # Split the source file name to remove the extension
        base_name, _ = os.path.splitext(self.source_file)
        
        # Create the intermediate file path with the new extension
        intermediate_file_path = self.FileExplorer.create_new_file_in_main(base_name, "int")
        if intermediate_file_path is None:
            self.logger.log_error(f"Failed to create intermediate file for '{self.source_file}'.")
            return
    
        # Open the intermediate file for writing and keep the file object
        try:
            self.intermediate_file = open(intermediate_file_path, "w")
            self.logger.log_action(f"Created and opened intermediate file '{intermediate_file_path}' for writing.")
        except Exception as e:
            self.logger.log_error(f"An error occurred while opening the intermediate file '{intermediate_file_path}': {e}")
            self.intermediate_file = None
        

    def process_source_lines(self, lines):
        """
        Processes multiple lines of source code.
        """
        self.location_counter.set_start_address(0)
        # Log the start of processing
        self.logger.log_action(f"Starting processing of source code lines.")
        line_number = 0
        lines_with_errors = 0
        for line in lines:
            line_number += 1
            source_line = SourceCodeLine(line_number, line)
            self.process_single_line(source_line)
            
            # If line has errors, increment the lines_with_errors counter
            if source_line.has_errors():
                lines_with_errors += 1
                
            # If stop_on_error is True, then stop processing the line if a line has errors
            if self.stop_on_error and lines_with_errors > 0:
                self.logger.log_action(f"Stopping processing of source code lines after {line_number} lines with errors.")
                break
            
            # If allow_error_lines_in_generated_document is False, then stop processing the line if a line has errors
            if not source_line.has_errors():
                print(source_line)
                self.add_line_to_generated_file(source_line)
            elif self.allow_error_lines_in_generated_document:
                print(source_line)
                self.add_line_to_generated_file(source_line)
            else:
                line_number -= 1
                continue
        
        # Log the end of processing
        self.logger.log_action(f"Finished processing of source code lines. {lines_with_errors} lines had errors.")
        
            

    def process_single_line(self, source_line: SourceCodeLine):
        """
        Processes a single line of source code.
        """
        # Create a ParsingHandler for the line and parse it
        
        parser = ParsingHandler(source_line,  validate_parsing=True, logger=self.logger, opcode_handler=self.opcode_handler)
        
        parser.parse_line()
        
        # Validate the source line
        self.valid_line(source_line)
        
        # stop if alllow_error_lines_in_generated_document is False
        if not self.allow_error_lines_in_generated_document and source_line.has_errors():
            return

        # Set address for the line
        source_line.set_address_from_hex_string(self.location_counter.get_current_address_hex())
        # source_line.address = self.location_counter.get_current_address_hex()
        
        # Check for START directive
        if source_line.opcode_mnemonic == "START":
            self.directive_START(source_line)
            return
        
        if source_line.opcode_mnemonic == "END":
            self.directive_END(source_line)
            return
        
        # if there is a symbol in the label field, process it
        if source_line.label:
            self.process_label_field(source_line)
            
        # if theres an opcode mnemonic, process it
        if source_line.opcode_mnemonic:
            self.process_opcode_field(source_line)
        
        # Process operands (for literals)
        if source_line.operands:
            self.process_operands(source_line)

        # if the line is not an error, then add its instruction length to the location counter
        if not source_line.has_errors():
            self.location_counter.increment_by_decimal(source_line.instruction_length)


    def process_label_field(self, source_line: SourceCodeLine):
        """
        Processes the label in the source line by inserting it into the symbol table.

        :param source_line: The current SourceCodeLine being processed.
        """
        label = source_line.label
        address = self.location_counter.get_current_address_int()
        rflag = True  # Assuming all symbols are relocatable

        # Validate the symbol using Validator
        validator = Validator()
        symbol_validation = validator.validate_symbol(label)
        if symbol_validation != "Success":
            self.logger.log_error(f"{symbol_validation} in line: '{source_line.line_text}'")
            return

        # Create a SymbolData instance
        symbol_data = SymbolData(symbol=label, value=address, rflag=rflag)

        # Insert the symbol into the symbol table
        try:
            self.symbol_table.insert(symbol_data)
            _action = f"Inserted symbol '{label}' at address {hex(address)} into the symbol table."
            self.logger.log_action(_action, False)
        except Exception as e:
            self.logger.log_error(f"Error inserting symbol '{label}': {e}")


    
    def process_opcode_field(self, source_line: SourceCodeLine):
        """
        Processes the opcode in the source line.
        """
        _action = f"Processing opcode '{source_line.opcode_mnemonic}' in line {source_line.line_number}."
        self.logger.log_action(_action, False)
        _opcode_mnemonic = source_line.opcode_mnemonic
        # Check if the opcode is a valid mnemonic
        if self.opcode_handler.is_opcode_mnemonic(_opcode_mnemonic):
            # check if it is a byte directive
            if self.opcode_handler.is_directive(_opcode_mnemonic):
                self.check_for_directives(source_line, handle_directives=True)
                return
            #Else, process the opcode
            self.process_opcode(source_line)
        _action = f"Processed opcode '{source_line.opcode_mnemonic}' in line {source_line.line_number}."
        self.logger.log_action(_action, False)
        # Process the opcode
        pass
    
    def process_opcode(self, source_line: SourceCodeLine):
        """
        Processes the opcode in the source line.
        """
        # Process the opcode
        # get the opcode format
        _action = f"Processing opcode '{source_line.opcode_mnemonic}' in line {source_line.line_number}."
        self.logger.log_action(_action, False)
        try:
            instr_format = self.opcode_handler.get_format(source_line.opcode_mnemonic)
            # add the instruction length to the source line
            source_line.instruction_length = instr_format
        except ValueError as e:
            Error = f"Could not get instruction format for opcode '{source_line.opcode_mnemonic}': {e}"
            self.logger.log_error(Error)
            source_line.add_error(Error)
            raise ValueError(Error)
        pass

    def process_operands(self, source_line: SourceCodeLine):
        """
        Processes operands to detect and handle literals.

        :param source_line: The current SourceCodeLine being processed.
        """
        _action = f"Processing operands in line {source_line.line_number}."
        self.logger.log_action(_action, False)
        operands = source_line.operands
        if not operands:
            return

        # Split operands by comma to handle multiple operands
        operand_list = [operand.strip() for operand in operands.split(',')]
        for operand in operand_list:
            if operand.startswith('='):
                self.process_literal(operand)
        _action = f"Processed operands in line {source_line.line_number}."
        self.logger.log_action(_action, False)

    def process_literal(self, literal_str: str):
        """
        Processes a single literal and inserts it into the literal table.
    
        :param literal_str: The literal operand (e.g., =0X05, =CEOF).
        """
        literal_name = literal_str
        literal = self.literal_table.search(literal_name)
    
        if not literal:
            try:
                # Check if the literal starts with =0C or =0X
                if literal_name.upper().startswith("=0C") or literal_name.upper().startswith("=0X"):
                    prefix = literal_name[1:3].upper()
                    literal_value = literal_name[3:]
    
                    if prefix == "0C":
                        # Handle character literals
                        if not all(c.isprintable() for c in literal_value):
                            _error_message = f"Invalid character literal value: {literal_value}"
                            self.logger.log_error(_error_message)
                            raise ValueError(_error_message)
                        literal_value = ''.join(f"{ord(c):02X}" for c in literal_value)
                        literal_length = len(literal_value) // 2  # Two characters per byte
    
                    elif prefix == "0X":
                        # Handle hexadecimal literals
                        if not all(c in '0123456789ABCDEFabcdef' for c in literal_value):
                            _error_message = f"Invalid hexadecimal value: {literal_value}"
                            self.logger.log_error(_error_message)
                            raise ValueError(_error_message)
                        if len(literal_value) % 2 != 0:
                            _error_message = f"Hexadecimal value length is not valid (must be even): {literal_value}"
                            self.logger.log_error(_error_message)
                            raise ValueError(_error_message)
                        literal_length = len(literal_value) // 2  # Two characters per byte
    
                    else:
                        raise ValueError(f"Invalid literal format: {literal_name}")
    
                    # Insert literal into the literal table
                    new_literal = LiteralData(name=literal_name, value=literal_value, length=literal_length)
                    self.literal_table.insert(new_literal)
    
                    self.logger.log_action(f"Inserted new literal '{literal_name}'", False)
                    return None  # Skip further processing for valid literals
    
                else:
                    _error_message = f"Invalid literal format: {literal_name}"
                    self.logger.log_error(_error_message)
                    raise ValueError(_error_message)
    
            except ValueError as e:
                self.logger.log_error(str(e), context_info=literal_name)
                return  # Return the invalid literal as an error
    
        self.logger.log_action(f"Used existing literal '{literal_name}'", False)

            
    def assign_addresses_to_literals(self):
        """
        Assigns addresses to all literals in the literal table.
        """
        current_address = self.location_counter.get_current_address_int()
        self.literal_table.update_addresses(start_address=current_address)
        # Update the location counter based on total literal size
        total_literal_size = self.literal_table.get_total_size()
        self.location_counter.increment_by_decimal(total_literal_size)
        self.logger.log_action(f"Assigned addresses to literals starting from {hex(current_address)}.")

    def display_literal_table(self):
        """
        Displays the contents of the literal table.
        """
        _action = "Displaying Literal Table:"
        self.logger.log_action(_action, False)
        self.literal_table.display_literals()

    def display_symbol_table(self):
        """
        Displays the contents of the symbol table.
        """
        _action = "Displaying Symbol Table:"
        self.logger.log_action(_action, False)
        self.symbol_table.view()


    def add_line_to_generated_file(self, source_line: SourceCodeLine):
        """
        Adds the source line to the intermediate file, including errors on the same line.
        """
        _action = f"Adding line {source_line.line_number} to the intermediate file."
        self.logger.log_action(_action, False)
        if self.intermediate_file:
            try:
                line_to_write = str(source_line)
                
                # Write the line to the intermediate file
                self.intermediate_file.write(line_to_write + "\n")
                _action = f"Added line {source_line.line_number} to the intermediate file."
                self.logger.log_action(_action, False)
            except Exception as e:
                self.logger.log_error(f"An error occurred while writing to the intermediate file: {e}")
        else:
            self.logger.log_error("Intermediate file is not open for writing.")

    def add_symbol_table_to_output_file(self):
        """
        Adds the symbol table to the output.
        """
        # add symbol table to the output
        self.logger.log_action("Adding symbol table to the output.")
        if self.symbol_table:
            try:
                _symbol_table = str(self.symbol_table)
                self.intermediate_file.write("\n\n" + self.Start_div_symbol_table + "\n")
                self.intermediate_file.write(_symbol_table)
                self.intermediate_file.write("\n" + self.End_div_symbol_table + "\n")
            except Exception as e:
                self.logger.log_error(f"An error occurred while writing the symbol table to the output: {e}")
        else:
            self.logger.log_error("Symbol table is empty.")

    def add_literal_table_to_output_file(self):
        """
        Adds the literal table to the output.
        """
        # Wrrite literal table to the output
        _action = "Adding literal table to the output."
        self.logger.log_action(_action, True)
        if self.literal_table:
            try:
                _literal_table = str(self.literal_table)
                self.intermediate_file.write("\n\n" + self.Start_div_literal_table + "\n")
                self.intermediate_file.write(_literal_table)
                self.intermediate_file.write("\n" +self.End_div_literal_table + "\n")
                self.logger.log_action("Literal table added to the output.")
            except Exception as e:
                self.logger.log_error(f"An error occurred while writing the literal table to the output: {e}")
        else:
            self.logger.log_error("Literal table is empty.")
        pass

    def calculate_program_length(self):
        """
        Calculates the program length.
        """
        try:
            return self.location_counter.get_current_address_int() - self.program_start_address
        except ValueError:
            Error = f"Error calculating program length."
            self.logger.log_error(Error)
            raise ValueError(Error)
    
    def add_program_length_to_output_file(self):
        """
        Adds the program length to the output.
        """
        # add program length to the output
        _action = "Adding program length to the output."
        self.logger.log_action(_action, True)
        try:
            program_length = self.calculate_program_length()
            program_length_hex = format(self.program_length, '05X')
            self.intermediate_file.write("\n\n" + self.Start_div_program_length + "\n")
            self.intermediate_file.write(f"{self.Program_length_prefix_for_Decimal} {program_length}\n")
            self.intermediate_file.write(f"{self.Program_length_prefix_for_Hex} {program_length_hex}\n")
            self.intermediate_file.write("\n" + self.End_div_program_length + "\n")
        except ValueError as e:
            self.logger.log_error(f"An error occurred while writing the program length to the output: {e}")

    def get_num_without_hashtag(self, num: str) -> int:
        """
        Gets the number without the '#' character.
        Handles cases like '#24', '24', and '# 24'.
        """
        num = num.strip()
        if num.startswith('#'):
            num = num[1:].strip()
        try:
            return int(num)
        except ValueError:
            self.logger.log_error(f"Invalid number format: '{num}'")
            return 0


    # *Directives* _________________________________________________________________________________________
    # region Directives
    def check_for_directives(self, source_line: SourceCodeLine, handle_directives: bool = True):
        """
        Checks for directives in the source line.
        """
        if handle_directives:
            directives = {
                "START": self.directive_START,
                "END": self.directive_END,
                "EQU": self.directive_EQU,
                "ORG": self.directive_ORG,
                "BYTE": self.directive_BYTE,
                "WORD": self.directive_WORD,
                "RESB": self.directive_RESB,
                "RESW": self.directive_RESW,
            }

            directive_handler = directives.get(source_line.opcode_mnemonic)
            if directive_handler:
                directive_handler(source_line)
        
        
    def directive_START(self, source_line: SourceCodeLine):
        """
        Handles the START directive.
        """
        # Set starting address
        if source_line.operands:
            operand = source_line.operands.strip()
            try:
                if operand.startswith('#'):
                    # Convert the operand to an integer (hexadecimal)
                    operand_value = int(operand[1:], 16)
                else:
                    # Convert the operand to an integer (decimal)
                    operand_value = int(operand, 10)
                # Set the starting address
                self.program_start_address = operand_value
                self.location_counter.set_start_address(self.program_start_address)
                self.logger.log_action(f"Set starting address to {self.program_start_address:X}")
            except ValueError:
                Error = f"Invalid operand for START directive: '{operand}'"
                self.logger.log_error(Error)
                source_line.add_error(Error)
        else:
            self.program_start_address = 0
            self.location_counter.set_start_address(self.program_start_address)
            self.logger.log_action(f"Set starting address to {self.program_start_address:X}")
    
        # Set the program name
        if source_line.label:
            self.program_name = source_line.label
            # Process the label as a symbol
            self.process_label_field(source_line)
        else:
            self.program_name = "program"
        self.logger.log_action(f"Set program name to {self.program_name}")


    def directive_END(self, source_line: SourceCodeLine):
        """
        Handles the END directive.
        """
        try:
            # Set the program length
            self.calculate_program_length()
            # add 0 to the instruction length
            source_line.instruction_length = 0
            self.logger.log_action(f"END directive reached")
        except ValueError:
            Error = f"Issue with END directive"
            self.logger.log_error(Error)
            source_line.add_error(Error)


    def directive_BYTE(self, source_line: SourceCodeLine):
        """
        Handles the BYTE directive.
        """
        # find length of constant in bytes
        # add length to instruction length
        try:
            source_line.instruction_length = self.calculate_byte_size(source_line.operands)
        except ValueError as e:
            Error = f"Invalid operand for BYTE directive: '{source_line.operands}'."
            self.logger.log_error(Error)
            source_line.add_error(Error)
            # raise ValueError(Error)

    def calculate_byte_size(self, operand):
        """
        Calculates the size of the BYTE directive.

        :param operand: The operand for the BYTE directive.
        :return: The size in bytes as an integer.
        """
        operand = operand.strip()
        try:
            if operand.startswith(self.character_literal_prefix):
                value = operand[2:]
                return len(value) - 1
            elif operand.startswith(self.hex_literal_prefix):
                value = operand[2:]
                if len(value) % 2 != 0:
                    raise ValueError("Hex string in BYTE directive must have even length")
                return len(value) // 2
            else:
                raise ValueError(f"Invalid operand '{operand}' for BYTE directive")
        except ValueError as e:
            self.logger.log_error(str(e))
            return 0
  
    def directive_WORD(self, source_line: SourceCodeLine):
        """
        Handles the WORD directive.
        """
        # add 3 to instruction length
        source_line.instruction_length = 3
    
    def directive_RESB(self, source_line: SourceCodeLine):
        """
        Handles the RESB directive.
        """
        try:
            n = self.get_num_without_hashtag(source_line.operands)
            # self.location_counter.increment_by_decimal(n)
            source_line.instruction_length = n
        except ValueError:
            Error = f"Invalid operand on line: '{source_line.operands}' for RESB"
            self.logger.log_error(Error)
            source_line.add_error(Error)
            # raise ValueError(Error)
    
    def directive_RESW(self, source_line: SourceCodeLine):
        """
        Handles the RESW directive.
        """
        try:
            n = self.get_num_without_hashtag(source_line.operands)
            # self.location_counter.increment_by_decimal(3 * n)
            source_line.instruction_length = 3 * n
        except ValueError:
            Error = f"Invalid operand: '{source_line.operands}' for RESW"
            source_line.add_error(Error)
            self.logger.log_error(Error)
            # raise ValueError(Error)
            
    def directive_EQU(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive.
        """
        label = source_line.label
        expression = source_line.operands.strip()
    
        try:
            # Evaluate the expression
            value = self.evaluate_EQU_expression(expression)
            # Create a SymbolData instance
            symbol_data = SymbolData(symbol=label, value=value, rflag=True)
            # Insert the symbol into the symbol table
            self.symbol_table.insert(symbol_data)
            self.logger.log_action(f"Set symbol '{label}' to value {value:X} with EQU directive.")
        except ValueError as e:
            Error = f"Invalid expression for EQU directive: '{expression}'"
            self.logger.log_error(Error)
            source_line.add_error(Error)

    def evaluate_EQU_expression(self, expression: str) -> int:
        """
        Evaluates an expression and returns its value.

        :param expression: The expression to evaluate.
        :return: The evaluated value as an integer.
        """
        try:
            if expression.split()[0] == '*':
                value = self.location_counter.get_current_address_int()
                # # Replace '*' with the current address
                # expression = expression.replace('*', str(self.location_counter.get_current_address_int()))
            elif expression.startswith('#'):
                value = int(expression[1:], 10)
            # else if the expression is not empty
            elif expression != '':
                # use parse line in Expression parser to parse the operands
                Expression_Evaluator = ExpressionEvaluator(self.symbol_table, self.literal_table, self.logger)
                ExpressionParser = ExpressionParser(self.symbol_table, self.literal_table, self.logger)
                parsed_expression = ExpressionParser.parse_line(expression)
                # Evaluate the parsed expression
                value = Expression_Evaluator.evaluate_expression(parsed_expression)

            if not isinstance(value, int):
                raise ValueError("Expression did not evaluate to an integer.")
            return value
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}. Error: {e}")
    
    def directive_ORG(self, source_line: SourceCodeLine):
        """
        Handles the ORG directive.
        """
        expression = source_line.operands.strip()
    
        try:
            # Evaluate the expression
        
            Expression_Evaluator = ExpressionEvaluator(self.symbol_table, self.literal_table, self.logger)
            ExpressionParser = ExpressionParser(self.symbol_table, self.literal_table, self.logger)
            parsed_expression = ExpressionParser.parse_line(expression)
            # Evaluate the parsed expression
            value = Expression_Evaluator.evaluate_expression(parsed_expression)
            # Set the location counter to the evaluated value
            self.location_counter.set_start_address(value)
            self.logger.log_action(f"Set location counter to {value:X} with ORG directive.")
        except ValueError as e:
            Error = f"Invalid expression for ORG directive: '{expression}'"
            self.logger.log_error(Error)
            source_line.add_error(Error)

    def directive_EXTREF(self, source_line: SourceCodeLine):
        """
        Handles the EXTREF directive.
        """
        operands = source_line.operands.strip().split(',')
        for operand in operands:
            operand = operand.strip()
            if operand:
                self.symbol_table_driver.add_external_reference(operand)
                self.logger.log_action(f"Declared external reference '{operand}' with EXTREF directive.")
        # Set instruction length to 0
        source_line.instruction_length = 0
    
    def directive_EXTDEF(self, source_line: SourceCodeLine):
        """
        Handles the EXTDEF directive.
        """
        operands = source_line.operands.strip().split(',')
        for operand in operands:
            operand = operand.strip()
            if operand:
                self.symbol_table_driver.add_external_definition(operand)
                self.logger.log_action(f"Declared external definition '{operand}' with EXTDEF directive.")
        # Set instruction length to 0
        source_line.instruction_length = 0
        
    # endregion



    # region Validation
    def valid_label(self, label: str, error_list: list = None) -> bool:
        """
        Validates a label based on the following rules:
        - Must be at most 10 characters.
        - Must start with a letter.
        - Cannot be just an underscore.
        - Can contain only letters, digits, and underscores.
        """
        label = label.strip().rstrip(":").upper()

        Errors = []
        # Check if the label length exceeds 10 characters
        if len(label) > 10:
            Errors.append(f"'{label}' length exceeds 10 characters.")
            self.logger.log_error(f"Label '{label}' length exceeds 10 characters.")

        # Check if the label starts with a letter
        if label and not label[0].isalpha():
            Errors.append(f"'{label}' must start with a letter.")
            self.logger.log_error(f"Label '{label}' must start with a letter.")
        
        # Check if the entire label is "_"
        if label == "_":
            Errors.append(f"'{label}' cannot be an underscore ('_') only.")
            self.logger.log_error(f"Label '{label}' cannot be an underscore ('_') only.")
            return False

        # Check for invalid characters
        for char in label:
            if not (char.isalnum() or char == '_'):
                Errors.append(f"Symbol '{label}' contains invalid character '{char}'.")
                self.logger.log_error(f"Symbol '{label}' contains invalid character '{char}'.")

        # Check if there are any errors
        if Errors:
            if error_list:
                error_list.extend(Errors)
            return False
        return True
    
    def valid_line(self, line: SourceCodeLine) -> bool:
        """
        Validates a label based on the following rules:
        - Must be at most 10 characters.
        - Must start with a letter.
        - Cannot be just an underscore.
        - Can contain only letters, digits, and underscores.
        """
        label = line.label.strip().rstrip(":").upper()

        Errors = []
        # Check if the label length exceeds 10 characters
        if len(label) > 10:
            Error = f"'{label}' length exceeds 10 characters."
            Errors.append(Error)
            line.add_error(Error)
            self.logger.log_error(Error)

        # Check if the label starts with a letter
        if label and not label[0].isalpha():
            Error = f"'{label}' must start with a letter."
            Errors.append(Error)
            line.add_error(Error)
            self.logger.log_error(Error)
        
        # Check if the entire label is "_"
        if label == "_":
            Error = f"'{label}' cannot be an underscore ('_') only."
            Errors.append(Error)
            line.add_error(Error)
            self.logger.log_error(Error)
            return False

        # Check for invalid characters
        for char in label:
            if not (char.isalnum() or char == '_'):
                Error = f"Label '{label}' contains invalid character '{char}'. "
                Errors.append(Error)
                line.add_error(Error)
                self.logger.log_error(Error)

        #validate opcode mnemonic
        # check if opcode mnemonic is empty
        if line.opcode_mnemonic:
            if not self.opcode_handler.is_opcode_mnemonic(line.opcode_mnemonic):
                Error = f"Invalid opcode mnemonic: '{line.opcode_mnemonic}'. "
                Errors.append(Error)
                line.add_error(Error)
                self.logger.log_error(Error)
        
        # check if only operand on line
        if line.operands:
            if line.label == "" and line.opcode_mnemonic == "" and line.operands != "" and not line.is_empty_line and not line.is_comment:
                Error = f"Line '{line.line_number}' has only an operand."
                Errors.append(Error)
                line.add_error(Error)
                self.logger.log_error(Error)
                
        # check if error list is not empty
        if Errors:
            return False
        return True

    def valid_opcode_mnemonic(self, mnemonic: str, error_list: list = None) -> bool:
        """
        Validates an opcode mnemonic based on the SIC/XE instruction set.
        """
        Errors = []
        if not self.opcode_handler.is_opcode_mnemonic(mnemonic):
            Errors.append(f"Invalid opcode mnemonic: '{mnemonic}'.")
            self.logger.log_error(f"Invalid opcode mnemonic: '{mnemonic}'.")
        
        if Errors:
            if error_list:
                error_list.extend(Errors)
            return False
        return True

    def check_if_only_operand_on_line(self, line: SourceCodeLine, error_list: list = None) -> bool:
        """
        Checks if there is only an operand on the source line.
            And the line has no opcode or label
            And the line is not an empty line or line is not a comment.
        """
        if line.label == "" and line.opcode_mnemonic == "" and line.operands != "" and not line.is_empty_line and not line.is_comment:
            error_list.append(f"Line '{line.line_number}' has only an operand.")
            self.logger.log_error(f"Line '{line.line_number}' has only an operand.")
            return False
        return True
    # endregion


# Example usage
if __name__ == "__main__":
    assembler = AssemblerPass1("source.asm")