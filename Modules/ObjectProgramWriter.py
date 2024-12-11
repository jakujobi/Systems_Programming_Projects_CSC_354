# ObjectProgramWriter.py

import os
import sys
from typing import List
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import *
        

class ObjectProgramWriter:
    """
    Manages the assembly of all records into the final object program and writes it to an output file.
    
    Responsibilities:
        - Assembles header, text, modification, and end records into the final object program.
        - Formats records according to the specified output format.
        - Writes the assembled object program to a designated output file.
        - Logs any errors encountered during the writing process.
    """
    
    def __init__(self,
                 header_record: str,
                 text_records: List[str],
                 modification_records: List[str],
                 end_record: str,
                 logger: ErrorLogHandler,
                 activate_separator: bool = False):
        """
        Initializes the ObjectProgramWriter with all necessary records and an error handler.
        
        :param header_record: The header record string.
        :param text_records: List of text record strings.
        :param modification_records: List of modification record strings.
        :param end_record: The end record string.
        :param logger: Instance of ErrorLogHandler for logging errors.
        """
        self.header_record = header_record
        self.text_records = text_records
        self.modification_records = modification_records
        self.end_record = end_record
        self.logger = logger
        
        self.separation_character = "^"
        self.activate_separator = activate_separator # Flag to activate the separation character
        
    @property
    def sp_ch(self):
        """
        Returns the separation character for formatting.
        """
        return self.separation_character if self.activate_separator else ""
    
    def assemble_object_program(self) -> str:
        """
        Assembles all records into the final object program string.
        
        :return: The complete object program as a single string.
        """
        object_program = ""
        
        # Append header record
        if self.header_record:
            object_program += f"{self.header_record}\n"
        else:
            self.logger.log_error("Header record is missing.")
        
        # Append text records
        for text_record in self.text_records:
            object_program += f"{text_record}\n"
        
        # Append modification records
        for modification_record in self.modification_records:
            object_program += f"{modification_record}\n"
        
        # Append end record
        if self.end_record:
            object_program += f"{self.end_record}\n"
        else:
            self.logger.log_error("End record is missing.")
        
        return object_program
    
    def write_to_file(self, file_name: str):
        """
        Writes the assembled object program to the specified output file.
        
        :param file_name: The name/path of the output file.
        """
        object_program = self.assemble_object_program()
        
        try:
            with open(file_name, 'w') as file:
                file.write(object_program)
            self.logger.log_action(f"Object program successfully written to {file_name}.")
        except IOError as e:
            self.logger.log_error(f"Failed to write object program to {file_name}: {e}")
    
    def validate_records(self) -> bool:
        """
        Validates that all necessary records are present and correctly formatted.
        
        :return: True if all records are valid, False otherwise.
        """
        is_valid = True
        
        # Validate header record
        if not self.header_record:
            self.logger.log_error("Header record is missing.")
            is_valid = False
        elif not self.header_record.startswith("H"):
            self.logger.log_error("Header record format is incorrect.")
            is_valid = False
        
        # Validate end record
        if not self.end_record:
            self.logger.log_error("End record is missing.")
            is_valid = False
        elif not self.end_record.startswith("E"):
            self.logger.log_error("End record format is incorrect.")
            is_valid = False
        
        # Validate text records
        for text_record in self.text_records:
            if not text_record.startswith("T"):
                self.logger.log_error(f"Invalid text record format: {text_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        # Validate modification records
        for modification_record in self.modification_records:
            if not modification_record.startswith("M"):
                self.logger.log_error(f"Invalid modification record format: {modification_record}")
                is_valid = False
                break  # Stop further validation on first error
        
        return is_valid
    
    def format_header_record(self, program_name: str, start_address: int, program_length: int) -> str:
        """
        Formats the header record according to the specification.
        
        :param program_name: The name of the program.
        :param start_address: The starting memory address of the program.
        :param program_length: The total length of the program.
        :return: The formatted header record string.
        """
        # Ensure program name is exactly 6 characters, padded with spaces if necessary
        program_name_formatted = f"{program_name:<6}"[:4]
        return f"H{self.sp_ch}{program_name_formatted}{self.sp_ch}{start_address:06X}{self.sp_ch}{program_length:06X}"
    
    def format_end_record(self, first_executable_address: int) -> str:
        """
        Formats the end record according to the specification.
        
        :param first_executable_address: The address of the first executable instruction.
        :return: The formatted end record string.
        """
        return f"E{self.sp_ch}{first_executable_address:06X}"