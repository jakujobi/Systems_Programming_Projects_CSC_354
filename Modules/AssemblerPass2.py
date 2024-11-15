import os
import sys
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import *
from Modules.ParsingHandler import *
from Modules.OpcodeHandler import *
from Modules.LocationCounter import *
from Modules.ErrorLogHandler import *
from Modules.Symbol_Table_Builder import *
from Modules.Literal_Table_Builder import *
from Modules.FileExplorer import *

class AssemblerPass2:
    def __init__(self, source_file_path: str, logger: ErrorLogHandler = None, character_literal_prefix: str = '0C', hex_literal_prefix: str = '0X', allow_error_lines_in_generated_document: bool = True, stop_on_error: bool = False, generated_file_extension: str = '.int'):
        self.source_file_path = source_file_path
        pass