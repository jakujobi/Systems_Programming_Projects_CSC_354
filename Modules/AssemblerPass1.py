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
    # region Validation
    # def validate_source_line(self, line: SourceCodeLine, error_list: list = None) -> bool:
    #     """
    #     Validates a single line of source code.
    #     """
    #     Errors = []
    #     self.valid_label(line.label, Errors)
    #     self.valid_opcode_mnemonic(line.opcode_mnemonic, Errors)
    #     self.check_if_only_operand_on_line(line, Errors)
        
    #     if Errors:
    #         if error_list:
    #             error_list.extend(Errors)
    #         # Add the errors to the SourceCodeLine instance
    #         line.add_error(Errors)
    #         return False
    #     return True
    
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
                Error = f"Symbol '{label}' contains invalid character '{char}'. "
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
        self.character_literal_prefix = '0C'
        self.hex_literal_prefix = '0X'
        
        self.source_file = filename
        self.intermediate_file = None
        self.log_file = None
        
        self.allow_error_lines_in_generated_document = True
        self.stop_on_error = False
        
        
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
        
        # # After processing all lines, calculate program length
        # self.calculate_program_length()
        
        # # Display the symbol table and write it to the generated file
        # self.add_symbol_table(add_to_file=True)
        
        # # Display the literal table and write it to the generated file
        # self.add_literal_table(add_to_file=True)
        
        # # Display the error log and write it to the generated file
        # self.create_log_file()
        
        # Close the intermediate file after processing
        if self.intermediate_file:
            self.intermediate_file.close()
            self.logger.log_action(f"Closed intermediate file.")
            
        # Close the log file after processing
        if self.log_file:
            self.log_file.close()
            self.logger.log_action(f"Closed log file.")
            
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
        # Create the intermediate file
        intermediate_file_path = self.FileExplorer.create_new_file_in_main(self.source_file, "int")
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
        
        # Print the length of the program using the location counter
        self.program_length = self.calculate_program_length()
        program_length_hex = format(self.program_length, '05X')
        self.logger.log_action(f"Program length (HEX): {program_length_hex}")
        self.logger.log_action(f"Program length (INT): {self.program_length}")
        
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
        source_line.address = self.location_counter.get_current_address_hex()
        
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
        

        # if the line is not an error, then add its instruction length to the location counter
        if not source_line.has_errors():
            self.location_counter.increment_by_decimal(source_line.instruction_length)



        
    def process_label_field(self, source_line: SourceCodeLine):
        """
        Processes the label in the source line.
        """
        # Process the label
        pass
    
    def process_opcode_field(self, source_line: SourceCodeLine):
        """
        Processes the opcode in the source line.
        """
        _opcode_mnemonic = source_line.opcode_mnemonic
        # Check if the opcode is a valid mnemonic
        if self.opcode_handler.is_opcode_mnemonic(_opcode_mnemonic):
            # check if it is a byte directive
            if self.opcode_handler.is_directive(_opcode_mnemonic):
                self.check_for_directives(source_line, handle_directives=True)
                return
            #Else, process the opcode
            self.process_opcode(source_line)
        # Process the opcode
        pass
    
    def process_opcode(self, source_line: SourceCodeLine):
        """
        Processes the opcode in the source line.
        """
        # Process the opcode
        # get the opcode format
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

    def add_symbol_to_symbol_table(self, source_line: SourceCodeLine):
        """
        Adds the symbol to the symbol table.
        """
        # Add the symbol to the symbol table
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



    def add_line_to_generated_file(self, source_line: SourceCodeLine):
        """
        Adds the source line to the intermediate file, including errors on the same line.
        """
        if self.intermediate_file:
            try:
                line_to_write = str(source_line)
                
                # Write the line to the intermediate file
                self.intermediate_file.write(line_to_write + "\n")
                self.logger.log_action(f"Added line {source_line.line_number} to the intermediate file.", False)
            except Exception as e:
                self.logger.log_error(f"An error occurred while writing to the intermediate file: {e}")
        else:
            self.logger.log_error("Intermediate file is not open for writing.")


    def calculate_program_length(self):
        """
        Calculates the program length.
        """
        return self.location_counter.get_current_address_int() - self.program_start_address

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
        # If it has an operand, verify it is an integer in decimal, then convert to hex then set the starting address
        # If it doesn't have an operand, set the starting address to 0
        # If it has an invalid operand, add an error
        if source_line.operands:
            try:
                # Convert the operand to an integer
                operand = int(source_line.operands[0])
                # Convert the integer to hex
                hex_operand = hex(operand)
                # Remove the '0x' prefix
                hex_operand = hex_operand[2:]
                # Set the starting address
                self.program_start_address = int(hex_operand, 16)
            except ValueError:
                Error = f"Invalid operand for START directive: '{source_line.operands[0]}'."
                self.logger.log_error(Error)
                source_line.add_error(Error)
        else:
            self.program_start_address = 0
        # Set the program name
        # If it has a label, set the program name to the label
        # If it doesn't have a label, set the program name to 'program'
        # If it has an invalid label, add an error
        if source_line.label:
            self.program_name = source_line.label
        else:
            self.program_name = "program"
        # Set the location counter to the starting address
        self.location_counter.set_start_address(self.program_start_address) 


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
            n = int(source_line.operands)
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
            n = int(source_line.operands)
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
        pass
    
    def directive_ORG(self, source_line: SourceCodeLine):
        """
        Handles the ORG directive.
        """
        expression = source_line.operands

    # endregion


# Example usage
if __name__ == "__main__":
    assembler = AssemblerPass1("source.asm")