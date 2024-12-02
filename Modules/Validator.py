import sys
import re
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler

class Validator:
    def __init__(self, logger=None):
        self.logger = logger or ErrorLogHandler()
        
    def valid_label(self, label: str, error_list: list = None) -> bool:
        """
        Validates a label based on specified rules.

        Parameters:
        - label: The label to be validated.
        - error_list: A list to append error messages to if provided.

        Returns:
        - True if the label is valid, False otherwise.
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
                Errors.append(f"Label '{label}' contains invalid character '{char}'.")
                self.logger.log_error(f"Label '{label}' contains invalid character '{char}'.")

        # Check if there are any errors
        if Errors:
            if error_list:
                error_list.extend(Errors)
            return False

        return True
    
    
    def valid_symbol_flag(self, flag):
        # if flag is an int, check if it is a 1 or 0
        """
        Checks if a given flag is valid.

        A valid flag is either an integer (1 or 0), a boolean string ("TRUE" or "FALSE"), a boolean, or None.

        Args:
            flag: The value to be validated.

        Returns:
            True if the flag is valid, False otherwise.
        """
        if isinstance(flag, int):
            return flag in [0, 1]
        # if flag is a string, check if it is a boolean
        elif isinstance(flag, str):
            return flag.strip().upper() in ["TRUE", "FALSE", "0", "1"]
        elif isinstance(flag, bool):
            return True
        # if flag is neither an int nor a string, return False
        else:
            _error = f"Invalid symbol flag: {flag}"
            self.logger.log_error(_error)
            return False
        
    def convert_flag_to_bool(self, flag):
        """
        Converts a symbol flag to a boolean value.

        Args:
            flag: The value to be converted.

        Returns:
            A boolean value if the flag is valid, None otherwise.
        """

        if self.valid_symbol_flag(flag):
            if isinstance(flag, int):
                return bool(flag)
            if isinstance(flag, str):
                if flag.strip().upper() == "FALSE" or flag == "0":
                    return False
                if flag.strip().upper() == "TRUE" or flag == "1":
                    return True
        else:
            _error = f"Invalid symbol flag: {flag}"
            self.logger.log_error(_error)
            return None
        
    def valid_hex_address_value(self, value):
        """
        Validates a hexadecimal address value.

        Args:
            value (str): The hexadecimal address value to validate.

        Returns:
            bool: True if the value is a valid hexadecimal address, False otherwise.
        
        Logs an error if the value is invalid.
        """
        if re.fullmatch(r'^[0-9A-Fa-f]{4,5}$', value.upper()):
            return True
        else:
            _error = f"Invalid hex address value: {value}"
            self.logger.log_error(_error)
            return False
        
    def convert_string_hex_str_to_int(self, hex_str):
        """
        Converts a hexadecimal string to an integer.

        Args:
            hex_str (str): The hexadecimal string to convert.

        Returns:
            int: The integer value of the hexadecimal string if valid, None otherwise.

        Logs an error if the value is invalid.
        """
        if self.valid_hex_address_value(hex_str):
            return int(hex_str, 16)
        else:
            return None
                
    def convert_symbol(self, symbol):
        """
        /********************************************************************
        ***  FUNCTION : convert_symbol                                      ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Converts the symbol to uppercase and truncates   ***
        ***  it to the first 4 characters.                                  ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - symbol (str): The symbol to be converted.                  ***
        ***  RETURNS :                                                      ***
        ***    - str: The converted symbol.                                 ***
        ********************************************************************/
        """
        return symbol.strip().rstrip(":").upper()[:4]


    def validate_symbol_search_line(self, line):
        """
        /********************************************************************
        ***  FUNCTION : validate_search_line                                ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a line from the search file, which     ***
        ***  should contain only a symbol. Returns the processed symbol     ***
        ***  (converted, uppercase, truncated) if valid, or an error        ***
        ***  message if invalid.                                            ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - line (str): The line from the search file to be validated. ***
        ***  RETURNS :                                                      ***
        ***    - str: The validated symbol or an error message.             ***
        ********************************************************************/
        """
        parts = line.split()

        if len(parts) != 1:
            return f"Error: Search file line '{line}' must contain only a symbol."
        
        symbol = parts[0].strip()

        symbol_validation = self.valid_label(symbol)
        
        if symbol_validation:
            converted_symbol = self.convert_symbol(symbol)
            return converted_symbol
        else:
            return f"Error: Invalid symbol '{symbol}' in line: '{line}'"