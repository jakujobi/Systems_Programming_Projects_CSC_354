# ModificaionRecordManager.py

import os
import sys
from typing import List

from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import *
from Modules.LocationCounter import *
        
class ModificationRecordManager:
    """
    Manages the creation and organization of modification records in the object program.
    
    Responsibilities:
        - Tracks addresses that require modification for relocation.
        - Generates formatted modification records.
        - Validates modification parameters.
        - Integrates with LocationCounter for address management and error logging.
    """

    def __init__(self, location_counter: LocationCounter,
                 logger: ErrorLogHandler,
                 activate_separator: bool = False):
        """
        Initializes the ModificationRecordManager with an empty list of modification records.
        
        :param location_counter: Instance of LocationCounter for address verification.
        """
        self.logger = logger or ErrorLogHandler()
        self.modification_records = []             # List to store finalized modification records
        self.location_counter = location_counter   # Reference to the LocationCounter
        self.separation_character = "^"
        self.activate_separator = activate_separator # Flag to activate the separation character 
        
        self.logger.log_action("ModificationRecordManager initialized.")

    @property
    def sp_ch(self):
        """
        Returns the separation character for formatting.
        """
        return self.separation_character if self.activate_separator else ""

    def add_modification(self, address: int, length: int):
        """
        Records a modification at the specified address with the given length.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        """
        # Validate modification parameters
        
        # log the type of address
        self.logger.log_action(f"Address type: {type(address)}")
        self.logger.log_action(f"Address: {address}")
        
        
        
        
        # # convert the address to an integer from hex string
        # address = int(address)
        
        # if not self.validate_modification(address, length):
        #     return  # Validation failed; error already logged
        
        # Check for duplicate modification records
        if any(record.startswith(f"M{self.sp_ch}{address:06X}") for record in self.modification_records):
            self.logger.log_error(
                f"Duplicate modification record for address {address:06X}."
            )
            return
        
        # Format the modification record
        formatted_record = f"M{self.sp_ch}{address:06X}{self.sp_ch}{length:02X}"
        
        # Add the formatted record to the list of modification records
        self.modification_records.append(formatted_record)
        
        # Optional: Log the action
        self.logger.log_action(f"Added modification record: {formatted_record}")

    def finalize_modification_records(self):
        """
        Finalizes all modification records, performing any necessary final processing.
        Currently, modification records are stored as formatted strings.
        """
        # Placeholder for future enhancements, such as grouping records or additional formatting
        pass

    def get_modification_records(self) -> List[str]:
        """
        Retrieves all finalized modification records.
        
        :return: A list of formatted modification record strings.
        """
        # Finalize any remaining modification records
        self.finalize_modification_records()
        
        return self.modification_records

    def validate_modification(self, address: int, length: int) -> bool:
        """
        Validates the modification parameters.
        
        :param address: The memory address that requires modification.
        :param length: The length in half-bytes (nibbles) that need to be modified.
        :return: True if valid, False otherwise.
        """
        # Example validation: address should be within program range
        program_length = self.location_counter.program_length
        if address < 0 or address + (length // 2) > program_length:
            self.logger.log_error(
                f"Invalid modification address or length: Address={address}, Length={length}"
            )
            return False
        
        return True