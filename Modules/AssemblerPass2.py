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
from Modules.ObjectCodeGenerator import *
from Modules.TextRecordManager import *
from Modules.ObjectProgramWriter import *
from Modules.ModificationRecordManager import *


# ! BUGS
# * 1. The object program file is not being written to the output file.
# * 2. It seems liek the locationcounter is not updating after processing each instruction.
# TODO I think i need to check everywhere the location counter is being updated.
# TODO And if it is even passed correctly through the classes.


class AssemblerPass2:
    """
    Coordinates the second pass of the assembler, handling object code generation,
    record management, and final assembly of the object program.
    
    Attributes:
        - int_file_name (str): Path to the intermediate file.
        - int_file_content (List[str]): Raw lines from the intermediate file.
        - int_source_code_lines (List[SourceCodeLine]): Parsed source lines.
        - logger (ErrorLogHandler): Handles logging of actions and errors.
        - symbol_table (SymbolTable): Contains symbol definitions and addresses.
        - literal_table (LiteralTableList): Contains literals and their addresses.
        - program_name (str): Name of the program being assembled.
        - program_start_address (int): Starting address of the program.
        - program_length (int): Total length of the program.
        - Program_length_prefix_for_Hex (str): Prefix for hexadecimal program length.
        - Program_length_prefix_for_Decimal (str): Prefix for decimal program length.
        - character_literal_prefix (str): Prefix for character literals.
        - hex_literal_prefix (str): Prefix for hexadecimal literals.
        - file_explorer (FileExplorer): Handles file operations.
        - location_counter (LocationCounter): Manages current address and program length.
        - object_code_generator (ObjectCodeGenerator): Generates object codes.
        - text_record_manager (TextRecordManager): Manages text records.
        - modification_record_manager (ModificationRecordManager): Manages modification records.
        - object_program_writer (ObjectProgramWriter): Assembles and writes the object program.
    """
    

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
        
        self.object_program_file_name = None
        
        self.logger = logger or ErrorLogHandler()
        self.opcode_handler = OpcodeHandler(logger=self.logger)
        
        self.file_explorer = file_explorer or FileExplorer()
        self.location_counter = LocationCounter(
            opcode_handler=self.opcode_handler,
            logger=self.logger
            )

        # Symbol Table
        self.symbol_table = SymbolTable(logger=self.logger)
        #self.symbol_table_driver = SymbolTableDriver(logger=self.logger)
        self.literal_table = LiteralTableList(logger=self.logger)
        
        self.program_name = None
        self.program_start_address = 0
        self.program_length = 0
        self.first_executable_address = 0
        
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
        
        self.allow_error_lines_in_generated_document = allow_error_lines_in_generated_document
        
        
        
    def run(self):
        self.load_intermediate_file()
        self.parse_intermediate_lines()
        self.initialize_generators_and_managers()
        self.process_source_lines()
        self.finalize_records()
        self.assemble_object_program()
        self.write_output_files()
        self.report_errors()
        
    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.

        Prepares the object code generator and record managers for a new assembly run.
        :return: None
        """
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            logger=self.logger,
            location_counter=self.location_counter  # Pass LocationCounter
        )
        self.text_record_manager = TextRecordManager(logger=self.logger)
        self.modification_record_manager = ModificationRecordManager(
            location_counter=self.location_counter,
            logger=self.logger
            )
        self.object_program_writer = ObjectProgramWriter(
            header_record=None,
            text_records=[],
            modification_records=[],
            end_record=None,
            logger=self.logger
        )
        self.logger.log_action("Initialized generators and managers.")
        

    def load_intermediate_file(self):
        """
        Loads the intermediate file content into memory.
        """
        try:
            self.int_file_content = self.file_explorer.read_file_raw(self.int_file_name)
            if not self.int_file_content:
                self.logger.log_error("Intermediate file is empty.")
                return
            self.logger.log_action(f"Read {len(self.int_file_content)} lines from '{self.int_file_name}'.")
        except FileNotFoundError:
            self.logger.log_error(f"Intermediate file '{self.int_file_name}' not found.")
        except IOError as e:
            self.logger.log_error(f"Error reading intermediate file '{self.int_file_name}': {e}")

    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.

        Utilizes IntermediateFileParser to convert raw lines into SourceCodeLine objects.
        Logs the number of parsed lines or any errors encountered during parsing.
        """
        if not self.int_file_content:
            self.logger.log_error(f"No content to parse in intermediate file '{self.int_file_name}'.")
            return
        
        int_file_parser = IntermediateFileParser(
            symbol_table_passed=self.symbol_table,
            literal_table_passed=self.literal_table,
            logger=self.logger,
            int_file_content=self.int_file_content
            )
        int_file_parser.parse_intermediate_file_content()
        self.int_source_code_lines = int_file_parser.parsed_code_lines
        
        self.logger.log_action(f"Parsed {len(self.int_source_code_lines)} source lines.")
    
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

    
    def process_source_lines(self):
        """
        Iterates through each SourceCodeLine to generate object codes and manage records.

        For each instruction:
            - Skips comments and erroneous lines.
            - Handles directives appropriately.
            - Generates object code using ObjectCodeGenerator.
            - Adds object code to TextRecordManager.
            - Records modifications if necessary using ModificationRecordManager.
            - Logs actions and errors.
        """
        if not hasattr(self, 'int_source_code_lines') or not self.int_source_code_lines:
            self.logger.log_error("No source lines to process.")
            return

        for source_line in self.int_source_code_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue  # Skip comments and erroneous lines

            if self.check_if_sourceline_is_directive(source_line):
                self.handle_directive(source_line)
                continue  # Directives are handled separately

            # Generate object code for the instruction
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)

            if object_code:
                # Add object code to text records
                self.text_record_manager.add_object_code(source_line.address, object_code)
                self.logger.log_action(f"Processed and Added object code '{object_code}' at address {source_line.address:X}.")

                # If modification is required, add to modification records
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    self.modification_record_manager.add_modification(
                        address=source_line.address + modification_offset,
                        length=modification_length
                    )
                    self.logger.log_action(f"Added modification record for address {source_line.address + modification_offset:X} with length {modification_length}.")
            else:
                # Object code generation failed
                #self.logger.log_error(f"Failed to generate object code for line: {source_line}")
                continue
            
    def check_if_sourceline_is_directive(self, source_line):
        """
        Checks if a given source line is a directive.

        :param source_line: The source line to check.
        :return: True if the source line is a directive, False otherwise.
        """
        opcode = source_line.opcode_mnemonic.upper()
        return opcode in self.opcode_handler.directives

    def finalize_records(self):
        """
        Finalizes text and modification records, creates header and end records, and prepares them for assembly.

        Finalizes current text records, retrieves all text and modification records, creates header and end records,
        assigns them to ObjectProgramWriter, and logs the finalization.
        """
        # Finalize any pending text records
        self.text_record_manager.finalize_current_record()

        # Retrieve text and modification records
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()

        # Create header and end records
        header_record = self.create_header_record()
        end_record = self.create_end_record()

        # Assign records to ObjectProgramWriter
        self.object_program_writer.header_record = header_record
        self.object_program_writer.text_records = text_records
        self.object_program_writer.modification_records = modification_records
        self.object_program_writer.end_record = end_record

        self.logger.log_action("Finalized all records for object program assembly.")

    def create_header_record(self) -> str:
        """
        Constructs the header record based on program metadata.

        Ensures proper formatting and logs the creation of the header record.

        :return: The formatted header record string.
        """
        program_name_formatted = f"{self.program_name:<6}"[:6]  # Ensure 6 characters
        _current_address = self.location_counter.get_current_address_int()
        program_length = _current_address - self.program_start_address
        self.program_length = program_length  # Store the program length
        header_record = f"H^{program_name_formatted}^{self.program_start_address:06X}^{program_length:06X}"
        self.logger.log_action(f"Created header record: {header_record}")
        return header_record

    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.

        Ensures proper formatting and logs the creation of the end record.

        :return: The formatted end record string.
        """
        end_record = f"E^{self.first_executable_address:06X}"
        self.logger.log_action(f"Created end record: {end_record}")
        return end_record


    def assemble_object_program(self):
        """
        Assembles all records into the final object program using ObjectProgramWriter.

        Logs the successful assembly of the object program.
        """
        self.object_program = self.object_program_writer.assemble_object_program()
        self.logger.log_action("Assembled the complete object program.")

    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.

        Handles any exceptions during file writing and logs the outcome.
        """
        try:
            self.object_program_writer.write_to_file(self.object_program_file_name)
            self.logger.log_action(f"Object program successfully written to '{self.object_program_file_name}'.")
        except Exception as e:
            self.logger.log_error(f"Failed to write object program to '{self.object_program_file_name}': {e}")

    def report_errors(self):
        """
        Reports all errors collected during the assembly process.

        Displays errors if any exist and logs the final assembly status.
        Optionally raises an exception to halt the assembly process if critical errors are present.
        """
        if self.logger.has_errors():
            self.logger.display_errors()
            self.logger.log_action("Assembly completed with errors.")
            if not self.allow_error_lines_in_generated_document:
                raise Exception("Assembly terminated due to errors.")
        else:
            self.logger.log_action("Assembly completed successfully without errors.")

    def evaluate_expression(self, expression: str) -> int:
        """
        Safely evaluates arithmetic expressions used in directives like EQU.

        Restricts allowed characters and prevents execution of arbitrary code.

        :param expression: The arithmetic expression to evaluate.
        :return: The evaluated integer value, or None if evaluation fails.
        """
        try:
            # For simplicity, allow only digits, operators, and spaces
            allowed_chars = "0123456789ABCDEFabcdef+-*/() "
            if any(char not in allowed_chars for char in expression):
                self.logger.log_error(f"Invalid characters in expression '{expression}'.")
                return None
            value = eval(expression, {"__builtins__": None}, {})
            if isinstance(value, int):
                return value
            else:
                self.logger.log_error(f"Expression '{expression}' did not evaluate to an integer.")
                return None
        except Exception as e:
            self.logger.log_error(f"Failed to evaluate expression '{expression}': {e}")
            return None

    def reset(self):
        """
        Resets the AssemblerPass2 instance to its initial state.

        Clears all tables, managers, writers, and metadata, preparing for a new assembly run.
        """
        # [Method implementation as shown above]
        

# *Directives Region ______________________________________________________
#region Directives

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.

        Delegates handling to specific methods based on the directive type.

        :param source_line: The SourceCodeLine object representing the directive.
        """
        directive = source_line.opcode_mnemonic.upper()
        operands = source_line.operands

        if directive == "START":
            self.handle_start_directive(source_line)
        elif directive == "END":
            self.handle_end_directive(source_line)
        elif directive == "LTORG":
            self.handle_ltorg_directive()
        elif directive == "EQU":
            self.handle_equ_directive(source_line)
        elif directive == "BASE":
            self.handle_base_directive(operands)
        elif directive == "NOBASE":
            self.handle_nobase_directive()
        else:
            self.logger.log_error(f"Unknown directive '{directive}' at line {source_line.line_number}.")


    def handle_start_directive(self, source_line: SourceCodeLine):
        """
        Handles the START directive to initialize program metadata.

        Sets the program start address and name based on the directive's operands and label.

        :param source_line: The SourceCodeLine object representing the START directive.
        """
        operand = source_line.operands
        if operand:
            try:
                self.program_start_address = int(operand)
                self.program_name = source_line.label.strip()
                self.text_record_manager.set_curret_start_address(self.program_start_address)
                self.location_counter = self.location_counter.set_start_address(self.program_start_address)
                self.logger.log_action(f"Program '{self.program_name}' starting at address {self.program_start_address:X}.")
            except ValueError:
                self.logger.log_error(f"Invalid start address '{operand}' in START directive at line {source_line.line_number}.")
        else:
            self.logger.log_error(f"Missing start address in START directive at line {source_line.line_number}.")

    def handle_end_directive(self, source_line: SourceCodeLine):
        """
        Handles the END directive to finalize the assembly process.

        Sets the first executable address based on the directive's operand or defaults to the program start address.

        :param source_line: The SourceCodeLine object representing the END directive.
        """
        operand = source_line.operands
        if operand:
            symbol = operand.strip()
            executable_address = self.symbol_table.get(symbol)
            if executable_address is not None:
                self.first_executable_address = executable_address
                self.logger.log_action(f"Execution begins at address {self.first_executable_address}.")
            else:
                self.logger.log_error(f"Undefined symbol '{symbol}' in END directive at line {source_line.line_number}.")
        else:
            # If no operand, default to program start address
            self.first_executable_address = self.program_start_address
            self.logger.log_action(f"Execution begins at program start address {self.first_executable_address:X}.")

    def handle_ltorg_directive(self):
        """
        Handles the LTORG directive by assigning addresses to literals and generating their object codes.

        Iterates through unassigned literals, assigns addresses, generates object codes, and logs actions.
        """
        unassigned_literals = self.literal_table.get_unassigned_literals()
        for literal in unassigned_literals:
            literal.address = self.location_counter.get_current_address_int()
            object_code = self.object_code_generator.generate_object_code_for_literal(literal)
            if object_code:
                self.text_record_manager.add_object_code(literal.address, object_code)
                self.logger.log_action(f"Assigned address {literal.address:X} to literal '{literal.value}' with object code '{object_code}'.")
                # Increment location counter by literal length
                self.location_counter.increment_by_decimal(len(object_code) // 2)  # Assuming object code is hex string
            else:
                self.logger.log_error(f"Failed to generate object code for literal '{literal.value}'.")

    def handle_equ_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive to define symbols with constant values.

        Evaluates the expression in the directive and updates the symbol table accordingly.

        :param source_line: The SourceCodeLine object representing the EQU directive.
        """
        symbol = source_line.label.strip()
        expression = source_line.operands.strip()
        value = self.evaluate_expression(expression)
        if value is not None:
            self.symbol_table.define(symbol, value, relocatable=False)
            self.logger.log_action(f"Defined symbol '{symbol}' with value {value:X} using EQU directive.")
        else:
            self.logger.log_error(f"Invalid expression '{expression}' in EQU directive at line {source_line.line_number}.")


    def handle_base_directive(self, operand: str):
        """
        Handles the BASE directive to set the base register for base-relative addressing.

        Updates the base register value in ObjectCodeGenerator and logs the action.

        :param operand: The operand specifying the base symbol or address.
        """
        symbol = operand.strip()
        base_address = self.symbol_table.get_symbol_address(symbol)
        if base_address is not None:
            self.base_register = base_address
            self.object_code_generator.set_base_register_value(base_address)
            self.logger.log_action(f"Base register set to symbol '{symbol}' with address {base_address:X}.")
        else:
            self.logger.log_error(f"Undefined symbol '{symbol}' in BASE directive.")

    def handle_nobase_directive(self):
        """
        Handles the NOBASE directive to unset the base register.

        Clears the base register value in ObjectCodeGenerator and logs the action.
        """
        self.base_register = None
        self.object_code_generator.unset_base_register()
        self.logger.log_action("Base register unset using NOBASE directive.")     
#endregion

