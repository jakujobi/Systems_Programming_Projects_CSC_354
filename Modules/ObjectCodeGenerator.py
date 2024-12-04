# ObjectCodeGenerator.py    

import os
import sys
from typing import List
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import *
from Modules.Symbol_Table_Builder import *
from Modules.Literal_Table_Builder import *
from Modules.OpcodeHandler import *
from Modules.LocationCounter import *
from Modules.SourceCodeLine import *
from Modules.TextRecordManager import *
from Modules.ModificationRecordManager import *
from Modules.ObjectCodeGenerator import *
from Modules.Validator import *
    
# Updated ObjectCodeGenerator.py

class ObjectCodeGenerator:
    """
    Translates assembly instructions into machine code (object code).
    Resolves symbols and literals, handles different instruction formats and addressing modes,
    manages the location counter, and performs error checking.
    """
    
    def __init__(self,
                 symbol_table,
                 literal_table,
                 opcode_handler,
                 logger,
                 location_counter):
        """
        Initializes the ObjectCodeGenerator with necessary references.
        
        :param symbol_table: Instance of SymbolTable.
        :param literal_table: Instance of LiteralTableList.
        :param opcode_handler: Instance of OpcodeHandler.
        :param logger: Instance of ErrorLogHandler.
        :param location_counter: Instance of LocationCounter.
        """
        self.logger = logger
        self.location_counter = location_counter
        self.symbol_table = symbol_table
        self.literal_table = literal_table
        self.opcode_handler = opcode_handler
        self.validator = Validator(logger = self.logger)


        self.text_record_manager = TextRecordManager(
            location_counter = self.location_counter,
            logger = self.logger
            )
        
        self.modification_record_manager = ModificationRecordManager(
            location_counter = self.location_counter,
            logger = self.logger
            )
        
        self.base_register_value = None
        self.nixbpe_flags = [0, 0, 0, 0, 0, 0]  # [n, i, x, b, p, e]
    
    def generate_object_code(self, source_lines):
        """
        Generates object code for all source lines.
        
        :param source_lines: List of SourceCodeLine instances.
        """
        for source_line in source_lines:
            if source_line.is_comment() or source_line.has_errors():
                continue
            if source_line.is_instruction():
                object_code = self.generate_object_code_for_line(source_line)
                if object_code:
                    self.text_record_manager.add_object_code(source_line.address, object_code)
                    if self.requires_modification(source_line):
                        modification_offset, modification_length = self.get_modification_details(source_line)
                        self.modification_record_manager.add_modification(
                            address=source_line.address + modification_offset,
                            length=modification_length
                        )
            # Directives are handled by AssemblerPass2
    
    def generate_object_code_for_line(self, source_line):
        """
        Generates object code for a single source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        # # Verify address consistency
        # expected_address = self.location_counter.get_current_address_int()
        # # Commpare the int conversion of the address to the expected address
        # # If they don't match, log an error and return None
        # int_address = self.validator.convert_string_hex_str_to_int(source_line.address)
        # if int_address != expected_address:
        #     _error_msg = f"Address mismatch at line {source_line.line_number}: expected {expected_address}, found {source_line.address} hex or {self.validator.convert_string_hex_str_to_int(source_line.address)} int."
        #     self.logger.log_error(
        #         f"Address mismatch at line {source_line.line_number}: expected {expected_address}, found {source_line.address}."
        #     )
        #     source_line.add_error(_error_msg)
        #     return None
        
        # Handle '+' prefix for format 4 instructions
        opcode_mnemonic = source_line.opcode_mnemonic
        format4 = False
        if opcode_mnemonic.startswith('+'):
            opcode_mnemonic = opcode_mnemonic[1:]  # Remove '+' prefix
            format4 = True
        
        # Retrieve opcode info
        try:
            opcode_info = self.opcode_handler.get_opcode(opcode_mnemonic)
        except ValueError:
            self.logger.log_error(f"Undefined opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Get opcode hexadecimal value and format
        opcode = opcode_info['hex']
        format_type = 4 if format4 else opcode_info['format']
        
        # Detect illegal addressing
        self.detect_illegal_addressing(source_line, opcode_info)
        if source_line.has_errors():
            return None
        
        # Handle based on instruction format
        if format_type == 1:
            object_code = self.handle_format1(source_line, opcode)
        elif format_type == 2:
            object_code = self.handle_format2(source_line, opcode)
        elif format_type == 3:
            object_code = self.handle_format3(source_line, opcode)
        elif format_type == 4:
            object_code = self.handle_format4(source_line, opcode)
        else:
            self.logger.log_error(f"Unsupported instruction format '{format_type}' for opcode '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
            return None
        
        # Add object code to text record
        self.text_record_manager.add_object_code(source_line.address, object_code)
        
        # add object code to source line
        source_line.object_code = object_code
        
        # Update LocationCounter based on instruction length
        instruction_length = format_type  # Assuming format corresponds to instruction length
        source_line.instruction_length = instruction_length
        self.location_counter.increment_by_decimal(instruction_length)
        
        # Handle modification records if necessary
        if self.requires_modification(source_line):
            modification_offset, modification_length = self.get_modification_details(source_line)
            self.modification_record_manager.add_modification(
                address=source_line.address + modification_offset,
                length=modification_length
            )
        
        return object_code
    
    def handle_format1(self, source_line, opcode):
        """
        Handles format 1 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode: Opcode hexadecimal value.
        :return: Object code as a hexadecimal string.
        """
        self.logger.log_action(f"Handling format 1 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
        object_code = f"{opcode:02X}"
        return object_code
    
    def handle_format2(self, source_line, opcode):
        """
        Handles format 2 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode: Opcode hexadecimal value.
        :return: Object code as a hexadecimal string.
        """
        self.logger.log_action(f"Handling format 2 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
        
        operands = source_line.operands.split(',')
        if len(operands) != 2:
            _error_msg = f"Incorrect number of operands for format 2 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}."
            self.logger.log_error(_error_msg)
            source_line.add_error(_error_msg)
            return None
        reg1 = operands[0].strip().upper()
        reg2 = operands[1].strip().upper()
        reg1_code = self.validate_register(reg1, source_line)
        reg2_code = self.validate_register(reg2, source_line)
        if reg1_code is None or reg2_code is None:
            return None
        object_code = f"{opcode:02X}{reg1_code:X}{reg2_code:X}"
        return object_code
    
    def handle_format3(self, source_line, opcode):
        """
        Handles format 3 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode: Opcode hexadecimal value.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        self.logger.log_action(f"Handling format 3 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
        operand = source_line.operands
        current_address = source_line.address
        
        # Initialize nixbpe flags
        self.nixbpe_flags = [1, 1, 0, 0, 0, 0]  # [n, i, x, b, p, e]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.logger.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # Calculate displacement
        displacement = self.calculate_displacement(resolved_value, current_address)
        if displacement is None:
            self.logger.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Check address range
        if not self.check_address_range(displacement, 3):
            self.logger.log_error(f"Displacement out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 3)
        return object_code
    
    def handle_format4(self, source_line, opcode):
        """
        Handles format 4 instructions.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode: Opcode hexadecimal value.
        :return: Object code as a hexadecimal string or None if error occurred.
        """
        self.logger.log_action(f"Handling format 4 instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
        operand = source_line.operands
        current_address = source_line.address
        
        # Initialize nixbpe flags for extended format
        self.nixbpe_flags = [1, 1, 0, 0, 0, 1]  # [n, i, x, b, p, e]
        
        # Process addressing modes
        operand, self.nixbpe_flags = self.process_addressing_modes(operand, self.nixbpe_flags, source_line)
        
        # Resolve operand
        resolved_value, relocation = self.resolve_operand(operand, current_address)
        if resolved_value is None:
            self.logger.log_error(f"Undefined symbol '{operand}' at line {source_line.line_number}.")
            return None
        
        # For format 4, address is absolute or relocatable
        displacement = resolved_value
        
        # Check address range for format 4 (20 bits)
        if displacement < 0 or displacement > 0xFFFFF:
            self.logger.log_error(f"Address out of range for operand '{operand}' at line {source_line.line_number}.")
            return None
        
        # Encode object code
        object_code = self.encode_object_code(opcode, self.nixbpe_flags, displacement, 4)
        
        # Add modification record for relocation
        self.modification_record_manager.add_modification(
            address=current_address + 1,  # Assuming the address starts at the next byte
            length=5  # Number of half-bytes to modify
        )
        
        return object_code
    
    # ... rest of the methods remain unchanged, but ensure that all uses of 'opcode_info' are adjusted accordingly

    
    def resolve_operand(self, operand, current_address):
        """
        Resolves an operand to its address or value.
        
        :param operand: Operand string.
        :param current_address: Current address from LocationCounter.
        :return: Tuple (resolved_value, relocation_info)
        """
        # log
        self.logger.log_action(f"Resolving operand '{operand}' at address {current_address}.")
        relocation_info = 'A'  # Default to absolute
        
        if operand.startswith('='):
            # Literal
            literal = self.literal_table.get_literal(operand)
            if not literal:
                self.logger.log_error(f"Literal '{operand}' not found in literal table.")
                return (None, None)
            resolved_value = literal.address
            relocation_info = 'R'
        elif operand.isdigit():
            # Immediate numeric value
            resolved_value = int(operand)
        else:
            # Symbol
            symbol = self.symbol_table.get_symbol(operand)
            if not symbol:
                return (None, None)
            resolved_value = symbol.value
            relocation_info = 'R' if symbol.is_relocatable else 'A'
        
        return (resolved_value, relocation_info)
    
    def calculate_displacement(self, target_address, current_address):
        """
        Calculates displacement for format 3 instructions.
        
        :param target_address: The resolved address of the operand.
        :param current_address: The current address from LocationCounter.
        :return: Displacement as an integer or None if out of range.
        """
        # log
        self.logger.log_action(f"Calculating displacement for format 3 instruction at address {current_address}.")
        
        displacement = target_address - (current_address + 3)
        
        if -2048 <= displacement <= 2047:
            # PC-relative addressing
            self.nixbpe_flags[4] = 1  # Set p flag
            return displacement & 0xFFF  # 12-bit signed
        elif self.base_register_value is not None:
            displacement = target_address - self.base_register_value
            if 0 <= displacement <= 4095:
                # Base-relative addressing
                self.nixbpe_flags[3] = 1  # Set b flag
                return displacement
        return None
    
    def check_address_range(self, displacement, format_type):
        """
        Checks if the displacement is within the allowable range for the instruction format.
        
        :param displacement: The calculated displacement value.
        :param format_type: The instruction format (3 or 4).
        :return: True if within range, False otherwise.
        """
        # log
        self.logger.log_action(f"Checking address range for {displacement} in the format {format_type} instruction.")
        if format_type == 3:
            return -2048 <= displacement <= 4095  # Considering both PC and base-relative
        elif format_type == 4:
            return 0 <= displacement <= 0xFFFFF  # 20-bit address
        return False
    
    def detect_illegal_addressing(self, source_line, opcode_info):
        """
        Detects illegal addressing modes for the given instruction.
        
        :param source_line: Instance of SourceCodeLine.
        :param opcode_info: Dictionary containing opcode details.
        """
        self.logger.log_action(f"Checking for illegal addressing modes for instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}.")
        operand = source_line.operands
        addressing_mode = self.identify_addressing_mode(operand)
        allowed_modes = opcode_info.get('allowed_addressing_modes', [])
        
        if addressing_mode not in allowed_modes:
            _error = f"Illegal addressing mode '{addressing_mode}' for instruction '{source_line.opcode_mnemonic}' at line {source_line.line_number}."
            self.logger.log_error(_error)
            source_line.add_error(_error)
    
    def identify_addressing_mode(self, operand):
        """
        Identifies the addressing mode based on the operand prefix/suffix.
        
        :param operand: Operand string.
        :return: Addressing mode as a string ('immediate', 'indirect', 'simple', 'indexed').
        """
        # log
        self.logger.log_action(f"Identifying addressing mode for operand '{operand}'.")
        operand = operand.strip()
        if operand.startswith('#'):
            return 'immediate'
        elif operand.startswith('@'):
            return 'indirect'
        elif ',X' in operand.upper():
            return 'indexed'
        else:
            return 'simple'
    
    def process_addressing_modes(self, operand, flags, source_line):
        """
        Processes the addressing modes and sets the nixbpe flags accordingly.
        
        :param operand: Operand string.
        :param flags: List of nixbpe flags.
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (processed_operand, flags)
        """
        # log
        self.logger.log_action(f"Processing addressing modes for operand '{operand}' at line {source_line.line_number}.")
        operand = operand.strip()
        
        # Immediate addressing
        if operand.startswith('#'):
            flags[0] = 0  # n
            flags[1] = 1  # i
            operand = operand[1:].strip()
        
        # Indirect addressing
        elif operand.startswith('@'):
            flags[0] = 1  # n
            flags[1] = 0  # i
            operand = operand[1:].strip()
        
        # Simple addressing
        else:
            flags[0] = 1  # n
            flags[1] = 1  # i
        
        # Indexed addressing
        if ',X' in operand.upper():
            flags[2] = 1  # x
            operand = operand.upper().replace(',X', '').strip()
        
        return (operand, flags)
    
    def encode_object_code(self, opcode, flags, displacement, format_type):
        """
        Encodes the final object code based on opcode, flags, and displacement.
        
        :param opcode: Opcode as an integer.
        :param flags: List of nixbpe flags.
        :param displacement: Displacement value as an integer.
        :param format_type: Instruction format (3 or 4).
        :return: Encoded object code as a hexadecimal string.
        """
        # log
        self.logger.log_action(f"Encoding object code for format {format_type} instruction.")
        # Convert opcode to binary (6 bits)
        opcode_bin = format(opcode, '06b')
        
        # Convert nixbpe flags to binary (6 bits)
        flags_bin = ''.join(str(flag) for flag in flags)
        
        # Convert displacement to binary
        if format_type == 3:
            # Handle signed displacement for format 3
            if displacement < 0:
                displacement = (1 << 12) + displacement  # Two's complement
            displacement_bin = format(displacement, '012b')  # 12 bits
        elif format_type == 4:
            displacement_bin = format(displacement, '020b')  # 20 bits
        else:
            displacement_bin = '0' * 12  # Default
        
        # Concatenate all parts
        object_code_bin = opcode_bin + flags_bin + displacement_bin
        
        # Convert binary to hexadecimal
        object_code_hex = format(int(object_code_bin, 2), 'X').upper()
        
        # Pad with leading zeros
        if format_type == 3:
            object_code_hex = object_code_hex.zfill(6)
        elif format_type == 4:
            object_code_hex = object_code_hex.zfill(8)
        
        return object_code_hex
    
    def validate_register(self, register, source_line):
        """
        Validates the register name and returns its code.
        
        :param register: Register name as a string.
        :param source_line: Instance of SourceCodeLine.
        :return: Register code as an integer or None if invalid.
        """
        self.logger.log_action(f"Validating register '{register}' at line {source_line.line_number}.")
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            _error = f"Invalid register '{register}' at line {source_line.line_number}."
            self.logger.log_error(_error)
            source_line.add_error(_error)
            return None
        self.logger.log_action(f"Register '{register}' validated.")
        return REGISTER_CODES[register]
    
    def set_base_register(self, register):
        """
        Sets the base register value for base-relative addressing.
        
        :param register: Register name as a string (e.g., 'B').
        """
        self.logger.log_action(f"Setting base register to '{register}'.")
        register = register.upper()
        REGISTER_CODES = {
            "A": 0, "X": 1, "L": 2, "B": 3, "S": 4, "T": 5, "F": 6,
            "PC": 8, "SW": 9
        }
        if register not in REGISTER_CODES:
            self.logger.log_error(f"Invalid base register '{register}'.")
            return
        symbol = register  # Assuming register symbols are defined in the symbol table
        symbol_entry = self.symbol_table.get_symbol(symbol)
        if not symbol_entry:
            self.logger.log_error(f"Symbol for base register '{register}' not found in symbol table.")
            return
        self.base_register_value = symbol_entry.value
        self.logger.log_action(f"Base register set to {register} with value {self.base_register_value:X}.")
    
    def unset_base_register(self):
        """
        Unsets the base register value, disabling base-relative addressing.
        """
        self.base_register_value = None
        self.logger.log_action("Base register unset.")
    
    def generate_object_code_for_literal(self, literal):
        """
        Generates object code for a literal.
        
        :param literal: Instance of a Literal (from LiteralTableList).
        :return: Object code as a hexadecimal string.
        """
        self.logger.log_action(f"Generating object code for literal '{literal.name}'.")
        if literal.type == 'C':
            # Convert each character to its ASCII hexadecimal value
            object_code = ''.join([format(ord(char), '02X') for char in literal.value])
        elif literal.type == 'X':
            # Use the hexadecimal value directly
            object_code = literal.value.upper()
        else:
            self.logger.log_error(f"Unsupported literal type '{literal.type}' for literal '{literal.name}'.")
            return None
        return object_code
    
    def requires_modification(self, source_line):
        """
        Determines if the instruction requires a modification record.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Boolean indicating if modification is required.
        """
        self.logger.log_action(f"Checking if instruction '{source_line.opcode_mnemonic}' requires modification.")
        # Typically, format 4 instructions require modification
        opcode_info = self.opcode_handler.get_info(source_line.opcode_mnemonic)
        if not opcode_info:
            return False
        return opcode_info['format'] == 4
    
    def get_modification_details(self, source_line):
        """
        Retrieves modification details for a source line.
        
        :param source_line: Instance of SourceCodeLine.
        :return: Tuple (modification_offset, modification_length).
        """
        self.logger.log_action(f"Getting modification details for instruction '{source_line.opcode_mnemonic}'.")
        # Assuming the modification occurs at the address after the opcode byte
        # and spans the next 5 half-bytes (20 bits)
        modification_offset = 1  # Address offset where modification starts
        modification_length = 5  # Number of half-bytes to modify
        return (modification_offset, modification_length)