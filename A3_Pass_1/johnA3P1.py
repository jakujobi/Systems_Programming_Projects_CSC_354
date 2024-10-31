import sys
import os
import re
import sys
from pathlib import Path

# Add the parent directory to the system path
repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.Literal_Table_Builder import *
from Modules.Symbol_Table_Builder import *
from Modules.ErrorLogHandler import *
from Modules.FileExplorer import *
from Modules.OpcodeHandler import *
from Modules.SourceCodeLine import *
from Modules.AssemblerPass1 import *
from Modules.LocationCounter import *
from Modules.ParsingHandler import *
from Modules.SourceCodeLine import *

if __name__ == "__main__":
    # Get the source file from the command-line argument or use the default
    source_file = sys.argv[1] if len(sys.argv) > 1 else "source_code.asm"
    
    # Create an instance of AssemblerPass1 with the source file
    assembler_pass1 = AssemblerPass1(source_file)
    
    # Run the assembler pass 1
    assembler_pass1.run()