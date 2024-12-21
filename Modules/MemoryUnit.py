# MemoryUnit.py

import os
import sys
from typing import Optional
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler


class MemoryUnit:
    """
    Represents a single byte of memory.
    Integrates with ErrorLogHandler to log actions and errors.
    """
    def __init__(self, logger: ErrorLogHandler, value: int = None, empty_symbol: str = "??"):
        """
        Initializes the MemoryUnit.

        :param logger: An instance of ErrorLogHandler for logging.
        :param value: Optional initial byte value (0-255). If None, the unit is uninitialized.
        """
        if isinstance(logger, ErrorLogHandler):
            self.logger = logger
        else:
            self.logger = ErrorLogHandler()
            self.logger.log_error("Invalid logger provided, using default logger.", "MemoryUnit.__init__")
        
        self.initialized = False  # Ensure initialized is always set

        if value is not None:
            try:
                self.set_value(value)
            except (ValueError, TypeError):
                pass  # Error already logged in set_value
        else:
            self.value = None
            self.logger.log_action("MemoryUnit initialized as uninitialized.")
            
        self.empty_symbol = empty_symbol if isinstance(empty_symbol, str) else "??"

    def __repr__(self) -> str:
        """
        Returns a string representation of the memory unit.

        :return: "??" if uninitialized, else two-digit hexadecimal string.
        """
        return self.empty_symbol if not self.initialized else f"{self.value:02X}"

    def set_value(self, value: int):
        """
        Sets the byte value and marks the unit as initialized.

        :param value: Integer value to set (0-255).
        :raises ValueError: If value is not in 0-255.
        :raises TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            self.logger.log_error("Attempted to set non-integer value.", "MemoryUnit.set_value")
            raise TypeError(f"Value must be an integer, got {type(value).__name__}")
        if not (0 <= value <= 0xFF):
            self.logger.log_error(f"Byte value {value} out of range.", "MemoryUnit.set_value")
            raise ValueError(f"Byte value must be between 0 and 255 (0x00 to 0xFF), got {value}")
        self.value = value
        self.initialized = True
        self.logger.log_action(f"Set value to {value:02X}.")

    def get_value(self) -> Optional[int]:
        """
        Retrieves the byte value.

        :return: The byte value if initialized, else None.
        """
        if self.initialized:
            self.logger.log_action(f"Retrieved value {self.value:02X}.")
            return self.value
        else:
            self.logger.log_action("Attempted to retrieve uninitialized value.")
            return None