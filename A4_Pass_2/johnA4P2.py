import os
import re
import sys
from pathlib import Path

# Add the parent directory to the system path
repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.AssemblerPass2 import AssemblerPass2

if __name__ == "__main__":
    
    hardcoded_file = "Htest2.int"
    
    # Get the source file from the command-line argument or use the default
    source_file = sys.argv[1] if len(sys.argv) > 1 else hardcoded_file
    
    # Create an instance of AssemblerPass1 with the source file
    AssemblerPass2(source_file)