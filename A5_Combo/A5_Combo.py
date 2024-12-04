import os
import re
import sys
from pathlib import Path



# Add the parent directory to the system path
repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.ComboAssembler import ComboAssembler

if __name__ == "__main__":
    # Get the source file from the command-line argument or use the default
    source_file = sys.argv[1] if len(sys.argv) > 1 else "source.int"
    
    # Create an instance of AssemblerPass1 with the source file
    ComboAssembler = ComboAssembler(source_file)
    
    # Run the assembler pass 1
    ComboAssembler.assemble()