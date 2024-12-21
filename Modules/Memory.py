# Memory.py

import os
import sys
from typing import List, Optional

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



class Memory:
    """
    Represents a byte-addressable memory space using MemoryUnit instances.
    Integrates with ErrorLogHandler to log all actions and errors.
    """
    def __init__(self, size: int, start_address: int = 0, logger: Optional['ErrorLogHandler'] = None):
        """
        Initializes the Memory with a given size and starting address.

        :param size: Total number of bytes in memory.
        :param start_address: The absolute starting address of the memory.
        :param logger: An instance of ErrorLogHandler for logging. If None, a new instance is created.
        :raises ValueError: If size or start_address are invalid.
        """
        if logger is None:
            from ErrorLogHandler import ErrorLogHandler
            self.logger = ErrorLogHandler()
        else:
            self.logger = logger

        if not isinstance(size, int) or size <= 0:
            self.logger.log_error(f"Invalid memory size: {size}. Must be a positive integer.", "Memory.__init__")
            raise ValueError(f"Size must be a positive integer, got {size}")
        if not isinstance(start_address, int) or start_address < 0:
            self.logger.log_error(f"Invalid start address: {start_address}. Must be a non-negative integer.", "Memory.__init__")
            raise ValueError(f"Start address must be a non-negative integer, got {start_address}")

        self.size = size
        self.start_address = start_address
        self.units: List[MemoryUnit] = [MemoryUnit(logger=self.logger) for _ in range(size)]
        self.logger.log_action(f"Memory initialized with size {self.size} bytes starting at address {self.start_address:05X}.")

    def translate_address(self, address: int) -> int:
        """
        Translates an absolute address to an internal index.

        :param address: The absolute memory address.
        :return: The internal index corresponding to the address.
        :raises ValueError: If the address is out of the memory range.
        """
        index = address - self.start_address
        if 0 <= index < self.size:
            return index
        self.logger.log_error(f"Address {address:05X} is out of range ({self.start_address:05X} - {self.start_address + self.size -1:05X}).", "Memory.translate_address")
        raise ValueError(f"Address {address:05X} is out of range ({self.start_address:05X} - {self.start_address + self.size -1:05X}).")

    def write_byte(self, address: int, value: int):
        """
        Writes a single byte to the specified address.

        :param address: The absolute memory address to write to.
        :param value: The byte value to write (0-255).
        :raises ValueError: If the address is out of range or value is invalid.
        """
        try:
            index = self.translate_address(address)
            self.units[index].set_value(value)
            self.logger.log_action(f"Wrote byte {value:02X} to address {address:05X}.")
        except (ValueError, TypeError) as e:
            self.logger.log_error(str(e), "Memory.write_byte")

    def read_byte(self, address: int) -> Optional[int]:
        """
        Reads a single byte from the specified address.

        :param address: The absolute memory address to read from.
        :return: The byte value if initialized, else None.
        :raises ValueError: If the address is out of range.
        """
        try:
            index = self.translate_address(address)
            value = self.units[index].get_value()
            if value is not None:
                self.logger.log_action(f"Read byte {value:02X} from address {address:05X}.")
            else:
                self.logger.log_action(f"Read uninitialized byte from address {address:05X}.")
            return value
        except ValueError as e:
            self.logger.log_error(str(e), "Memory.read_byte")
            return None

    def is_initialized(self, address: int) -> bool:
        """
        Checks if the specified address has been initialized.

        :param address: The absolute memory address to check.
        :return: True if initialized, False otherwise.
        :raises ValueError: If the address is out of range.
        """
        try:
            index = self.translate_address(address)
            status = self.units[index].initialized
            self.logger.log_action(f"Checked initialization at address {address:05X}: {status}.")
            return status
        except ValueError as e:
            self.logger.log_error(str(e), "Memory.is_initialized")
            return False

    def write_bytes(self, start_address: int, data: bytes):
        """
        Writes multiple bytes starting from a specified address.

        :param start_address: The absolute starting address to write to.
        :param data: The bytes data to write.
        :raises TypeError: If data is not bytes or bytearray.
        :raises ValueError: If any address is out of range or data is invalid.
        """
        if not isinstance(data, (bytes, bytearray)):
            self.logger.log_error("Data must be bytes or bytearray for write_bytes.", "Memory.write_bytes")
            raise TypeError("Data must be bytes or bytearray")
        for offset, byte in enumerate(data):
            current_address = start_address + offset
            self.write_byte(current_address, byte)
        self.logger.log_action(f"Wrote {len(data)} bytes starting at address {start_address:05X}.")

    def read_bytes(self, start_address: int, length: int) -> List[Optional[int]]:
        """
        Reads multiple bytes starting from a specified address.

        :param start_address: The absolute starting address to read from.
        :param length: The number of bytes to read.
        :return: A list of byte values or None if uninitialized.
        :raises ValueError: If length is invalid or addresses are out of range.
        """
        if not isinstance(length, int) or length < 0:
            self.logger.log_error("Length must be a non-negative integer for read_bytes.", "Memory.read_bytes")
            raise ValueError(f"Length must be a non-negative integer, got {length}")
        bytes_list = []
        for i in range(length):
            current_address = start_address + i
            byte = self.read_byte(current_address)
            bytes_list.append(byte)
        self.logger.log_action(f"Read {length} bytes starting at address {start_address:05X}.")
        return bytes_list

    def get_dump(self, start: int, end: int, width: int = 16) -> str:
        """
        Generates a formatted memory dump between start and end addresses.

        :param start: The starting absolute address.
        :param end: The ending absolute address (non-inclusive).
        :param width: Number of bytes per row.
        :return: A string representing the memory dump.
        :raises ValueError: If any address in the range is out of memory bounds.
        """
        if start > end:
            self.logger.log_error("Start address must be less than or equal to end address for get_dump.", "Memory.get_dump")
            raise ValueError("Start address must be less than or equal to end address.")
        dump_str = ""
        for addr in range(start, end, width):
            row_bytes = []
            for offset in range(width):
                current_addr = addr + offset
                if current_addr >= end:
                    break
                try:
                    byte = self.read_byte(current_addr)
                    row_bytes.append(f"{byte:02X}" if byte is not None else "??")
                except ValueError:
                    row_bytes.append("??")
            row_str = f"{addr:05X} " + " ".join(row_bytes).ljust(width * 3)
            dump_str += row_str + "\n"
        self.logger.log_action(f"Generated memory dump from {start:05X} to {end:05X}.")
        return dump_str.strip()

    def __repr__(self) -> str:
        """
        Returns the full memory dump.

        :return: A string representing the entire memory.
        """
        return self.get_dump(self.start_address, self.start_address + self.size)