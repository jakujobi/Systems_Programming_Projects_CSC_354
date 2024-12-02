import sys
import re
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler



class Validator:
    def __init__(self,
                 logger = None):
        self.logger = logger or ErrorLogHandler()
        
    
    def valid_label(self, label: str, error_list: list = None) -> bool:
        """
        Validates a label based on specified rules.

        Parameters:
        - label: The label to be validated.
        - error_list: A list to append error messages to if provided.

        Returns:
        - True if the label is valid, False otherwise.

        Validation Rules:
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
        if isinstance(flag, int):
            return flag in [0, 1]
        # if flag is a string, check if it is a boolean
        elif isinstance(flag, str):
            return flag.strip().upper in ["True", "False"]
        # if flag is neither an int nor a string, return False
        else:
            _error = f"Invalid symbol flag: {flag}"
            self.logger.log_error(_error)
            return False
        
    def convert_flag_to_bool(self, flag):
        if self.valid_symbol_flag(flag):
            if isinstance(flag, int):
                if flag == 1:
                    return True
                elif flag == 0:
                    return False
            if isinstance(flag, str):
                if flag.strip().upper() == "True":
                    return True
                elif flag.strip().upper() == "False":
                    return False
        else:
            _error = f"Invalid symbol flag: {flag}"
            self.logger.log_error(_error)
            return None
        
    def valid_hex_address_value(self, value):
        if re.fullmatch(r'^[0-9A-Fa-f]{4}$', value.upper()):
            return True
        else:
            _error = f"Invalid hex address value: {value}"
            self.logger.log_error(_error)
            return False
        
    def convert_string_hex_str_to_int(self, hex_str):
        self.valid_hex_address_value(hex_str)
        return int(hex_str, 16)
            

    
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

    def validate_syms_line(self, line):
        """
        /********************************************************************
        ***  FUNCTION : validate_syms_line                                  ***
        ***  CLASS  : Validator                                             ***
        *********************************************************************
        ***  DESCRIPTION : Validates a line from the SYMS.DAT file, which   ***
        ***  must contain exactly three parts: symbol, value, and rflag.    ***
        ***  Returns a SymbolData object if valid, or an error message if   ***
        ***  invalid.                                                       ***
        ***                                                                 ***
        ***  INPUTS :                                                       ***
        ***    - line (str): The line from SYMS.DAT to be validated.        ***
        ***  RETURNS :                                                      ***
        ***    - SymbolData or str: The validated SymbolData object or an   ***
        ***      error message if invalid.                                  ***
        ********************************************************************/
        """
        parts = line.split(maxsplit=2)
        if len(parts) != 3:
            return f"Error: SYMS.DAT line '{line}' must contain symbol, value, and rflag."
        
        symbol, value, rflag = parts
        
        symbol_validation = self.validate_symbol(symbol)
        value_validation = self.validate_value(value)
        rflag_validation = self.validate_rflag(rflag)
        
        if symbol_validation == "Success" and value_validation == "Success" and rflag_validation == "Success":
            converted_symbol = self.convert_symbol(symbol)
            rflag_bool = rflag.lower() == "true"
            return SymbolData(converted_symbol, int(value), rflag_bool)
        
        if symbol_validation != "Success":
            return f"{symbol_validation} in line: '{line}'"
        if value_validation != "Success":
            return f"{value_validation} in line: '{line}'"
        if rflag_validation != "Success":
            return f"{rflag_validation} in line: '{line}'"

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

        symbol_validation = self.validate_symbol(symbol)
        
        if symbol_validation == "Success":
            converted_symbol = self.convert_symbol(symbol)
            return converted_symbol
        else:
            return f"{symbol_validation} in line: '{line}'"