import sys
import os
import re

from Modules.Literal_Table_Builder import *
from Modules.Symbol_Table_Builder import *
from Modules.ErrorLogHandler import *
from Modules.FileExplorer import *
from OpcodeHandler import *
from SourceCodeLine import *
from AssemblerPass1 import *
from LocationCounter import *
from ParsingHandler import *
from SourceCodeLine import *

if __name__ == "__main__":
    # Get the source file from the command-line argument or use the default
    source_file = sys.argv[1] if len(sys.argv) > 1 else "source_code.asm"
    
    # Create an instance of AssemblerPass1 with the source file
    assembler_pass1 = AssemblerPass1(source_file)
    
    # Run the assembler pass 1
    assembler_pass1.run()