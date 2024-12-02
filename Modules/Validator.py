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