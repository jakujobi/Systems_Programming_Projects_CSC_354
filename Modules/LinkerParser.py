# LinkerParser.py

import os
import sys
from typing import List, Optional

from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler

class LinkerParser:
    """
    Parses lines from .obj files without '^' delimiters.
    Record types: H, D, R, T, M, E.
    """

    def parse_line(self, line: str) -> dict:
        line = line.strip()
        if not line:
            raise ValueError("Empty line encountered.")
        
        record_type = line[0]  # first char
        if record_type == 'H':
            return self.parse_header_record(line)
        elif record_type == 'D':
            return self.parse_define_record(line)
        elif record_type == 'R':
            return self.parse_refer_record(line)
        elif record_type == 'T':
            return self.parse_text_record(line)
        elif record_type == 'M':
            return self.parse_mod_record(line)
        elif record_type == 'E':
            return self.parse_end_record(line)
        else:
            raise ValueError(f"Unknown record type: {record_type}")

    def parse_header_record(self, line: str) -> dict:
        # H + [progName?] + startAddr(6) + length(6)
        # e.g., HPROG00000000001F
        record_type = 'H'
        # assume program name is 4 chars after 'H' (like "PROG") 
        # then 6 chars for start address, 6 chars for length
        # Adjust these indices based on your exact format
        program_name = line[1:5].strip()
        start_addr_hex = line[5:11]
        length_hex = line[11:17]
        
        start_address = int(start_addr_hex, 16)
        length = int(length_hex, 16)
        
        return {
            "record_type": record_type,
            "program_name": program_name,
            "start_address": start_address,
            "length": length
        }

    def parse_define_record(self, line: str) -> dict:
        # D + repeated pairs of [symbol(4 chars) + address(6 hex digits)]
        # e.g., DFIFT000019SIXT00001C
        record_type = 'D'
        content = line[1:]  # skip 'D'
        
        definitions = []
        i = 0
        while i < len(content):
            symbol = content[i : i+4]
            addr_hex = content[i+4 : i+10]
            i += 10
            addr = int(addr_hex, 16)
            definitions.append((symbol.strip(), addr))
        
        return {
            "record_type": record_type,
            "definitions": definitions
        }

    def parse_refer_record(self, line: str) -> dict:
        """
        R + symbols, each symbol occupying 4 characters (with trailing spaces if <4).
        Example: 'RFUNCTWO THRE' => symbols: ['FUNC', 'TWO', 'THRE']
                    'RFIFTSIXT'     => symbols: ['FIFT', 'SIXT']
        """
        if line[0] != 'R':
            raise ValueError("Not a refer record")

        record_type = 'R'
        content = line[1:]  # skip the 'R'
        
        symbols = []
        i = 0
        while i < len(content):
            chunk = content[i : i+4]
            i += 4
            symbol = chunk.strip()
            # If the chunk is empty after stripping, ignore (could be trailing spaces)
            if symbol:
                symbols.append(symbol)
        
        return {
            "record_type": record_type,
            "symbols": symbols
        }

    def parse_text_record(self, line: str) -> dict:
        # T + startAddr(6) + length(2) + objectCode...
        # e.g., T0000010B4B454E2047414D52414454
        record_type = 'T'
        start_addr_hex = line[1:7]
        length_hex = line[7:9]
        obj_code_str = line[9:]
        
        start_address = int(start_addr_hex, 16)
        length = int(length_hex, 16)
        object_code = bytes.fromhex(obj_code_str)
        
        return {
            "record_type": record_type,
            "start_address": start_address,
            "length": length,
            "object_code": object_code
        }

    def parse_mod_record(self, line: str) -> dict:
        # M00000E05+FUNC
        # M + addr(6) + halfByteCount(2) + sign(+/-) + symbol
        record_type = 'M'
        start_addr_hex = line[1:7]
        half_byte_str = line[7:9]
        sign = line[9]
        symbol = line[10:].strip()
        
        start_address = int(start_addr_hex, 16)
        half_byte_count = int(half_byte_str, 10)  # or base=16, check your spec
        
        return {
            "record_type": record_type,
            "start_address": start_address,
            "half_byte_count": half_byte_count,
            "sign": sign,
            "symbol": symbol
        }

    def parse_end_record(self, line: str) -> dict:
        # E + optional address(6)
        # e.g., E00000D or just E
        record_type = 'E'
        rest = line[1:].strip()
        
        execution_address = None
        if len(rest) >= 6:
            exec_addr_hex = rest[:6]
            execution_address = int(exec_addr_hex, 16)
        
        return {
            "record_type": record_type,
            "execution_address": execution_address
        }