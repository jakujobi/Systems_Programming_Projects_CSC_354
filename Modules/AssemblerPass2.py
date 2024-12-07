# AssemberPass2.py
import os
import sys
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import *
from Modules.ParsingHandler import *
from Modules.OpcodeHandler import *
from Modules.ErrorLogHandler import *
from Modules.Symbol_Table_Builder import *
from Modules.Literal_Table_Builder import *
from Modules.FileExplorer import *
from Modules.IntermediateFileParser import *
from Modules.ObjectCodeGenerator import *
from Modules.TextRecordManager import *
from Modules.ObjectProgramWriter import *
from Modules.ModificationRecordManager import *
from Modules.Validator import *
from Modules.LocationCounter import LocationCounter

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
        - int_file (str): Path to the intermediate file.
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
    

    def __init__(self,
                 int_filename: str,
                 file_explorer: FileExplorer = None,
                #  logger: ErrorLogHandler = None,
                 Program_length_prefix_for_Hex: str = "Program Length (HEX):",
                 Program_length_prefix_for_Decimal: str = "Program Length (DEC):",
                 character_literal_prefix: str = '0C',
                 hex_literal_prefix: str = '0X',
                 allow_error_lines_in_generated_document: bool = True,
                 Listing_File_Extension: str = "lst",
                 Object_Program_File_Extension: str = "obj",
                 ):
        
        self.int_file = int_filename
        self.int_file_extension = self.int_file.split('.')[-1]
        self.int_file_name = self.int_file.replace(self.int_file_extension, '').rstrip('.')
        self.int_file_content = []
        self.int_source_code_lines = []
        
        self.external_definitions = []
        self.external_references = []
        

        
        # self.logger = logger or ErrorLogHandler()
        self.logger = ErrorLogHandler(print_log_actions=True)
        self.logger.set_print_log_actions(True)
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
        
        
        self.listing_file_extension = Listing_File_Extension if Listing_File_Extension else "lst"
        self.object_program_file_extension = Object_Program_File_Extension if Object_Program_File_Extension else "obj"
        self.object_program_file = None
        self.listing_file = None
        
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
        self.create_output_files()
        self.print_all_things
        self.write_output_files()
        self.create_and_write_listing_file()
        self.print_all_things()
        self.report_errors()
        # print the log
        self.logger.display_log()
        
        
    def initialize_generators_and_managers(self):
        """
        Initializes object code generator, record managers, and object program writer.

        Prepares the object code generator and record managers for a new assembly run.
        :return: None
        """
        self.logger.log_action("Initializing generators and managers.")
        self.object_code_generator = ObjectCodeGenerator(
            symbol_table=self.symbol_table,
            literal_table=self.literal_table,
            opcode_handler=self.opcode_handler,
            logger=self.logger,
            location_counter=self.location_counter  # Pass LocationCounter
        )
        self.text_record_manager = TextRecordManager(logger=self.logger, location_counter=self.location_counter)
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
        self.logger.log_action(f"Loading intermediate file '{self.int_file}'.")
        try:
            self.int_file_content = self.file_explorer.read_file_raw(self.int_file)
            if not self.int_file_content:
                self.logger.log_error("Intermediate file is empty.")
                return
            self.logger.log_action(f"Read {len(self.int_file_content)} lines from '{self.int_file}'.")
        except FileNotFoundError:
            self.logger.log_error(f"Intermediate file '{self.int_file}' not found.")
        except IOError as e:
            self.logger.log_error(f"Error reading intermediate file '{self.int_file}': {e}")

    def create_output_files(self):
        """
        Creates the output files for the object program.
        """
        self.logger.log_action("Creating output files.")
        self.object_program_file = self.file_explorer.create_new_file_in_main(self.int_file_name, self.object_program_file_extension)
        self.logger.log_action(f"Created object program file '{self.object_program_file}'.")
        
        # Confirm the file was created
        if not self.file_explorer.file_exists(self.object_program_file):
            self.logger.log_error(f"Failed to create object program file '{self.object_program_file}'.")
            return

    def parse_intermediate_lines(self):
        """
        Parses the loaded intermediate file into structured SourceCodeLine objects.

        Utilizes IntermediateFileParser to convert raw lines into SourceCodeLine objects.
        Logs the number of parsed lines or any errors encountered during parsing.
        """
        self.logger.log_action("Parsing intermediate file.")
        if not self.int_file_content:
            self.logger.log_error(f"No content to parse in intermediate file '{self.int_file}'.")
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
        self.logger.log_action("Processing source lines.")
    
        if not self.int_source_code_lines:
            self.logger.log_error("No source lines to process.")
            return
    
        for source_line in self.int_source_code_lines:
            if source_line.is_comment() or source_line.has_errors():
                self.logger.log_action(f"Skipping comment or erroneous line: {source_line}")
                continue  # Skip comments and erroneous lines
    
            # **Set the address for the source line**
            source_line.address = self.location_counter.get_current_address_int()
            self.logger.log_action(f"Set source line address to {source_line.address:X}")
    
            if self.check_if_sourceline_is_directive(source_line):
                self.logger.log_action(f"Handling directive: {source_line}")
                self.handle_directive(source_line)
                continue  # Directives are handled separately
    
            # Generate object code for the instruction
            self.logger.log_action(f"Generating object code for line: {source_line}")
            object_code = self.object_code_generator.generate_object_code_for_line(source_line)
    
            if object_code:
                # Add object code to the source line
                source_line.set_object_code_int_from_hex_string(object_code)
                self.logger.log_action(f"Generated object code: {object_code}")
    
                # Add object code to text records
                self.text_record_manager.add_object_code(source_line.address, object_code)
    
                # Handle modification records if necessary
                if self.object_code_generator.requires_modification(source_line):
                    modification_offset, modification_length = self.object_code_generator.get_modification_details(source_line)
                    self.modification_record_manager.add_modification(
                        address=source_line.address + modification_offset,
                        length=modification_length
                    )
            else:
                self.logger.log_error(f"Failed to generate object code for line: {source_line}")
                continue
    
            # # **Increment the location counter**
            # instruction_length = source_line.get_instruction_length(source_line.opcode_mnemonic)
            # self.location_counter.increment_by_decimal(instruction_length)
            # self.logger.log_action(f"Incremented location counter by {instruction_length}. New address: {self.location_counter.get_current_address_int():X}")
            
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
        # mention that this method is being called
        self.logger.log_action("Creating header record with create_header_record method.")
        program_name_formatted = f"{self.program_name}"
        # program_name_formatted = f"{self.program_name:<6}"[:6]  # Ensure 6 characters
        # check if location counter exists
        if self.location_counter is None:
            self.logger.log_error("Location counter is not initialized.")
            self.logger.log_error("Location counter is not initialized.")
            return None
        # print address from location counter
        self.logger.log_action(f"Current address: {self.location_counter.get_current_address_int()}")
        _current_address = self.location_counter.get_current_address_int()
        program_length = _current_address - self.program_start_address
        self.program_length = program_length  # Store the program length
        header_record = f"H^{program_name_formatted}^{self.program_start_address:06X}^{program_length:06X}"
        self.logger.log_action(f"Created header record: {header_record}")
        return header_record

    def create_definition_record(self) -> str:
        """
        Creates the definition record (D) for external definitions.
        """
        if not self.external_definitions:
            return ''

        record = 'D'
        for symbol in self.external_definitions:
            address = self.symbol_table.get(symbol)
            if address is not None:
                record += f"{symbol:<6}{address:06X}"
            else:
                self.logger.log_error(f"Undefined symbol '{symbol}' in EXTDEF.")
        return record

    def create_reference_record(self) -> str:
        """
        Creates the reference record (R) for external references.
        """
        if not self.external_references:
            return ''

        record = 'R'
        for symbol in self.external_references:
            record += f"{symbol:<6}"
        return record

    def create_end_record(self) -> str:
        """
        Constructs the end record based on the first executable instruction's address.

        Ensures proper formatting and logs the creation of the end record.

        :return: The formatted end record string.
        """
        self.logger.log_action("Creating end record with create_end_record method.")
        # as hex string
        end_record = f"E^{self.first_executable_address:06X}"
        self.logger.log_action(f"Created end record: {end_record}")
        return end_record


    def assemble_object_program(self):
        self.logger.log_action("Assembling object program.")
        header_record = self.create_header_record()
        definition_record = self.create_definition_record()
        reference_record = self.create_reference_record()
        text_records = self.text_record_manager.get_text_records()
        modification_records = self.modification_record_manager.get_modification_records()
        end_record = self.create_end_record()
    
        object_program = [header_record]
        if definition_record:
            object_program.append(definition_record)
        if reference_record:
            object_program.append(reference_record)
        object_program.extend(text_records)
        object_program.extend(modification_records)
        object_program.append(end_record)
    
        self.object_program = self.object_program_writer.assemble_object_program()
        self.logger.log_action("Assembled the complete object program.")

    def write_output_files(self):
        """
        Writes the assembled object program to the designated output file.

        Handles any exceptions during file writing and logs the outcome.
        """
        # create the output file
        self.logger.log_action("Creating the output file with create_output_file method.")
        self.logger.log_action("Writing the assembled object program to the output file with write_to_file method.")  
        try:
            self.object_program_writer.write_to_file(self.object_program_file)
            self.logger.log_action(f"Object program successfully written to '{self.object_program_file}'.")
        except Exception as e:
            self.logger.log_error(f"Failed to write object program to '{self.object_program_file}': {e}")

    def create_and_write_listing_file(self):
        """
        This contains all the sourcelines from the intermediate file without errors
        """
        self.logger.log_action("Creating and writing the listing file.")
        self.listing_file = self.file_explorer.create_new_file_in_main(self.int_file_name, self.listing_file_extension)
        if not self.file_explorer.file_exists(self.listing_file):
            self.logger.log_error(f"Failed to create listing file '{self.listing_file}'.")
            return

        try:
            with open(self.listing_file, 'w') as file:
                for source_line in self.int_source_code_lines:
                    if not source_line.has_errors():
                        file.write(str(source_line) + '\n')
            self.logger.log_action(f"Listing file successfully written to '{self.listing_file}'.")
        except IOError as e:
            self.logger.log_error(f"Failed to write listing file to '{self.listing_file}': {e}")
        

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

    def remove_immediate_hash_from_numbers(self, operand):
        """
        Converts '#number' to 'number' in the operand string,
        but leaves '#Name' intact. It also handles cases like 'S,#4' to 'S,4'.

        :param operand: The operand string to process.
        :return: Modified operand string.
        """
        # Regular expression to match '#' followed by digits, ensuring '#' is not part of a word
        pattern = re.compile(r'(?<![\w])#(\d+)\b')
        return pattern.sub(r'\1', operand)

    def handle_directive(self, source_line: SourceCodeLine):
        """
        Processes assembly directives that control the assembly process.

        Delegates handling to specific methods based on the directive type.

        :param source_line: The SourceCodeLine object representing the directive.
        """
        directive = source_line.opcode_mnemonic.upper()
        operands = source_line.operands
    
        # Process operands to remove '#' from numbers for specific directives
        if directive in ["BYTE", "WORD", "RESB", "RESW", "EQU", "ORG"]:
            original_operand = source_line.operands
            source_line.operands = self.remove_immediate_hash_from_numbers(source_line.operands)
            self.logger.log_action(f"Processed operand from '{original_operand}' to '{source_line.operands}' for directive '{directive}'.")
    
        if directive == "START":
            self.handle_start_directive(source_line)
        elif directive == "END":
            self.handle_end_directive(source_line)
        elif directive == "BYTE":
            self.handle_byte_directive(source_line)
        elif directive == "WORD":
            self.handle_word_directive(source_line)
        elif directive == "RESB":
            self.handle_resb_directive(source_line)
        elif directive == "RESW":
            self.handle_resw_directive(source_line)
        elif directive == "EQU":
            self.handle_equ_directive(source_line)
        elif directive == "ORG":
            self.handle_org_directive(source_line)
        elif directive == "EXTDEF":
            self.handle_extdef_directive(source_line)
        elif directive == "EXTREF":
            self.handle_extref_directive(source_line)
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
        self.logger.log_action(f"Handling START directive with source_line: {source_line}")
        self.logger.log_action(f"Label: {source_line.label}")
        self.logger.log_action(f"Operands: {source_line.operands}")
        operand = self.get_num_without_hashtag(source_line.operands)
        self.logger.log_action(f"Operand: {operand}")
        if operand is not None:
            self.logger.log_action(f"Program start address set to: {operand}")
            try:
                self.program_start_address = int(operand)
                self.program_name = source_line.label.strip()
                self.text_record_manager.set_current_start_address(self.program_start_address)
                self.location_counter.set_start_address(self.program_start_address)
                self.logger.log_action(f"Program '{self.program_name}' starting at address {self.program_start_address}.")
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
            executable_address = self.symbol_table.get_value(symbol)
            if executable_address is not None:
                self.first_executable_address = executable_address
                self.logger.log_action(f"Execution begins at address {self.first_executable_address}.")
            else:
                self.logger.log_error(f"Undefined symbol '{symbol}' in END directive at line {source_line.line_number}.")
        else:
            # If no operand, default to program start address
            self.first_executable_address = self.program_start_address
            self.logger.log_action(f"Execution begins at program start address {self.first_executable_address}.")

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
                self.logger.log_action(f"Assigned address {literal.address} to literal '{literal.value}' with object code '{object_code}'.")
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
            self.logger.log_action(f"Defined symbol '{symbol}' with value {value} using EQU directive.")
        else:
            self.logger.log_error(f"Invalid expression '{expression}' in EQU directive at line {source_line.line_number}.")


    def handle_base_directive(self, operand: str):
        """
        Handles the BASE directive to set the base register for base-relative addressing.

        Updates the base register value in ObjectCodeGenerator and logs the action.

        :param operand: The operand specifying the base symbol or address.
        """
        symbol = operand.strip()
        if symbol is not None:
            self.object_code_generator.set_base_register_value_from_symbol(symbol)
            self.logger.log_action(f"Base register set to symbol '{symbol}'.")
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
        

    def handle_byte_directive(self, source_line: SourceCodeLine):
        """
        Handles the BYTE directive by generating object code for constants.
        """
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling BYTE directive with operand '{operand}' at line {source_line.line_number}.")
        instruction_length = 3
        object_code = ''
        if operand.startswith("C'") and operand.endswith("'"):
            chars = operand[2:-1]
            object_code = ''.join(f"{ord(c):02X}" for c in chars)
            source_line.set_object_code_int_from_hex_string(object_code)
        elif operand.startswith("X'") and operand.endswith("'"):
            object_code = operand[2:-1].upper()
            source_line.set_object_code_int_from_hex_string(object_code)
        else:
            error = f"Invalid operand '{operand}' for BYTE directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)
            return
        
        source_line.set_object_code_int_from_hex_string(object_code)
        self.text_record_manager.add_object_code(source_line.address, object_code)
        instruction_length = len(object_code) // 2
        self.location_counter.increment_by_decimal(instruction_length)
        self.logger.log_action(f"Generated object code '{object_code}' for BYTE directive.")
    
    def handle_word_directive(self, source_line: SourceCodeLine):
        """
        Handles the WORD directive by generating object code for constants.
        """
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling WORD directive with operand '{operand}' at line {source_line.line_number}.")

        try:
            value = int(operand)
            object_code = f"{value:06X}"
            source_line.set_object_code_int_from_hex_string(object_code)
            self.text_record_manager.add_object_code(source_line.address, object_code)
            instruction_length = 3
            self.location_counter.increment_by_decimal(instruction_length)
            source_line.set_instruction_length(instruction_length)
            self.logger.log_action(f"Generated object code '{object_code}' for WORD directive.")
        except ValueError:
            error = f"Invalid operand '{operand}' for WORD directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)

    def handle_resb_directive(self, source_line: SourceCodeLine):
        """
        Handles the RESB directive by updating the location counter.
        """
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling RESB directive with operand '{operand}' at line {source_line.line_number}.")

        try:
            bytes_to_reserve = int(self.get_num_without_hashtag(operand))
            self.location_counter.increment_by_decimal(bytes_to_reserve)
            source_line.set_instruction_length(bytes_to_reserve)
            self.logger.log_action(f"Reserved {bytes_to_reserve} bytes.")
        except ValueError:
            error = f"Invalid operand '{operand}' for RESB directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)

    def handle_resw_directive(self, source_line: SourceCodeLine):
        """
        Handles the RESW directive by updating the location counter.
        """
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling RESW directive with operand '{operand}' at line {source_line.line_number}.")

        try:
            words_to_reserve = int(operand)
            bytes_to_reserve = words_to_reserve * 3
            self.location_counter.increment_by_decimal(bytes_to_reserve)
            source_line.set_instruction_length(bytes_to_reserve)
            self.logger.log_action(f"Reserved {bytes_to_reserve} bytes.")
        except ValueError:
            error = f"Invalid operand '{operand}' for RESW directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)
            
    def handle_equ_directive(self, source_line: SourceCodeLine):
        """
        Handles the EQU directive by assigning a value to a symbol.
        """
        label = source_line.label.strip()
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling EQU directive with label '{label}' and operand '{operand}' at line {source_line.line_number}.")

        if operand == '*':
            value = self.location_counter.get_current_address_int()
        else:
            try:
                value = self.evaluate_expression(operand)
            except Exception as e:
                error = f"Invalid expression '{operand}' in EQU directive at line {source_line.line_number}."
                self.logger.log_error(error)
                source_line.add_error(error)
                return

        if label:
            self.symbol_table.add_symbol(label, value)
            self.logger.log_action(f"Assigned value {value:X} to symbol '{label}'.")
        else:
            error = f"Missing label in EQU directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)
            
    def handle_org_directive(self, source_line: SourceCodeLine):
        """
        Handles the ORG directive by setting the location counter.
        """
        operand = source_line.operands.strip()
        self.logger.log_action(f"Handling ORG directive with operand '{operand}' at line {source_line.line_number}.")

        if operand == '':
            error = f"Missing operand in ORG directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)
            return

        try:
            new_address = self.evaluate_expression(operand)
            self.location_counter.set_current_address(new_address)
            self.logger.log_action(f"Set location counter to {new_address:X}.")
        except Exception as e:
            error = f"Invalid expression '{operand}' in ORG directive at line {source_line.line_number}."
            self.logger.log_error(error)
            source_line.add_error(error)

    def handle_extdef_directive(self, source_line: SourceCodeLine):
        """
        Handles the EXTDEF directive by adding symbols to the external definitions.
        """
        operands = source_line.operands.strip().split(',')
        self.logger.log_action(f"Handling EXTDEF directive with operands '{operands}' at line {source_line.line_number}.")

        for symbol in operands:
            symbol = symbol.strip()
            if symbol:
                self.external_definitions.append(symbol)
                self.logger.log_action(f"Added '{symbol}' to external definitions.")
            else:
                error = f"Invalid symbol in EXTDEF directive at line {source_line.line_number}."
                self.logger.log_error(error)
                source_line.add_error(error)

    def handle_extdef_directive(self, source_line: SourceCodeLine):
        """
        Handles the EXTDEF directive by adding symbols to the external definitions.
        """
        operands = source_line.operands.strip().split(',')
        self.logger.log_action(f"Handling EXTDEF directive with operands '{operands}' at line {source_line.line_number}.")

        for symbol in operands:
            symbol = symbol.strip()
            if symbol:
                self.external_definitions.append(symbol)
                self.logger.log_action(f"Added '{symbol}' to external definitions.")
            else:
                error = f"Invalid symbol in EXTDEF directive at line {source_line.line_number}."
                self.logger.log_error(error)
                source_line.add_error(error)


#endregion