# TextRecordManager.py

import os
import sys
from pathlib import Path
from typing import List

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.LocationCounter import LocationCounter
from Modules.Validator import Validator


class TextRecordManager:
    """
    Manages the creation and organization of text records in the object program.
    
    Responsibilities:
        - Collects object codes and groups them into text records.
        - Ensures that each text record does not exceed 30 bytes.
        - Handles the continuity of addresses, starting new records as necessary.
        - Verifies address consistency using LocationCounter.
        - Formats text records for output.
    """

    def __init__(self, logger: ErrorLogHandler,
                 location_counter: LocationCounter):
        self.logger = logger
        self.location_counter = location_counter
        
        self.text_records = []
        self.current_record = []
        self.current_start_address = None     # Starting address of the current text record
        self.current_length = 0               # Current length of the text record in bytes
        self.MAX_RECORD_LENGTH = 30   
        self.validator = Validator(self.logger)        
    
    def set_current_start_address(self, address: int):
        """
        Sets the starting address for the current text record.

        :param address: The starting memory address.
        """
        self.current_start_address = address
        self.logger.log_action(f"Set current text record start address to {self.current_start_address}.")
    
    def add_object_code(self, address: int, object_code: str):
        """
        Adds an object code to the current text record, ensuring length and continuity constraints.

        :param address: The memory address of the object code.
        :param object_code: The hexadecimal string representing the machine code.
        """
        
        _action = f"Adding object code {object_code} at address {address}"
        self.logger.log_action(_action)
        
        object_length = self.calculate_length(object_code)
        
        if not self.current_record:
            # Start a new text record
            self.current_start_address = address
            self.current_record.append(object_code)
            self.current_length += object_length
            self.logger.log_action(f"Started new text record at address {self.current_start_address}.")
            return
        
        # Expected address for next object code
        expected_address = self.current_start_address + self.current_length
        
        if address != expected_address:
            # Address is not contiguous, finalize current record and start a new one
            self.logger.log_action(f"Non-contiguous address detected. Expected {expected_address}, found {address}. Finalizing current record.")
            self.finalize_current_record()
            self.current_start_address = address
            self.current_record.append(object_code)
            self.current_length += object_length
            self.logger.log_action(f"Started new text record at address {self.current_start_address}.")
            return
        
        # Check if adding the object code exceeds the maximum record length
        if self.current_length + object_length > self.MAX_RECORD_LENGTH:
            # Finalize the current record and start a new one
            self.logger.log_action(f"Current record length {self.current_length} bytes exceeds maximum {self.MAX_RECORD_LENGTH} bytes with new object code of length {object_length}. Finalizing current record.")
            self.finalize_current_record()
            self.current_start_address = address
            self.current_record.append(object_code)
            self.current_length += object_length
            self.logger.log_action(f"Started new text record at address {self.current_start_address}.")
            return
        
        # Add the object code to the current record
        self.current_record.append(object_code)
        self.current_length += object_length
        self.logger.log_action(f"Added object code {object_code} to current record at address {address}. Current record length: {self.current_length} bytes.")
    
    def finalize_current_record(self):
        """
        Finalizes the current text record by formatting and adding it to the list of text records.
        Resets the current record buffer and counters.
        """
        # Check if there are any object codes in the current record
        if self.current_record:
            # Log the number of object codes before finalizing
            num_object_codes = len(self.current_record)
            _action = f"Finalizing current record with {num_object_codes} object codes."
            self.logger.log_action(_action)

            # Calculate the total length of the current record in bytes
            record_length = self.current_length

            # Concatenate all object codes in the current record
            concatenated_object_code = ''.join(self.current_record)

            # Format the text record as per the specification
            formatted_record = f"T{self.current_start_address:06X}{record_length:02X}{concatenated_object_code}"

            # Add the formatted record to the list of text records
            self.text_records.append(formatted_record)

            # Reset the current record buffer and counters
            self.current_record = []
            self.current_start_address = None
            self.current_length = 0

            # Log confirmation
            _action = f"Finalized current record with {num_object_codes} object codes."
            self.logger.log_action(_action)
    
    def get_text_records(self) -> List[str]:
        """
        Retrieves all finalized text records.

        :return: A list of formatted text record strings.
        """
        # Finalize any remaining object codes in the current record
        self.finalize_current_record()
        # Return the list of all finalized text records
        return self.text_records
    
    def get_text_records_without_finalization(self) -> List[str]:
        """
        Retrieves the current text record without finalizing it.

        :return: A list of formatted text record strings.
        """
        return self.text_records
    

    def is_contiguous(self, last_address: int, new_address: int) -> bool:
        """
        Checks if the new address is contiguous or adjacent with the last address.

        :param last_address: The address where the last object code ended.
        :param new_address: The address of the incoming object code.
        :return: True if contiguous, False otherwise.
        """
        expected_address = last_address + (self.calculate_length(self.current_record[-1]))
        return new_address == expected_address

    def calculate_length(self, object_code: str) -> int:
        """
        Calculates the length of the object code in bytes.

        :param object_code: The hexadecimal string representing the machine code.
        :return: The length of the object code in bytes.
        """
        return len(object_code) // 2  # Each pair of hex digits represents one byte

    def verify_address_consistency(self, expected_address: int, actual_address: int, line_number: int):
        """
        Verifies that the actual address matches the expected address from the LocationCounter.

        :param expected_address: The address as per the LocationCounter.
        :param actual_address: The address from the SourceCodeLine.
        :param line_number: The line number in the source code for error reporting.
        """
        if actual_address != expected_address:
            # Log the error
            _error_message = f"Address mismatch at line {line_number}: expected {expected_address:06X}, found {actual_address:06X}."
            self.logger.log_error(_error_message)
