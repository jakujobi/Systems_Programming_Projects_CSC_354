# ComboP1P2.py

import sys
from pathlib import Path

# Add the parent directory to the system path
repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.ComboAssembler import ComboAssembler
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.AssemblerPass1 import AssemblerPass1
from Modules.AssemblerPass2 import AssemblerPass2

if __name__ == "__main__":
    # Make an array of file names
    test_files = ["Htest1",
                  "Htest2",
                  "Htest3",
                  "t1",
                  "t2",
                  "t3",
                  ]

    source_file = str(test_files[0]) + ".asm"
    intermediate_file = str(test_files[0]) + ".int"

    # remove the file extension
    pass1 = AssemblerPass1(source_file)
    
    # Ask for user input to proceed with Pass 2
    proceed = input(f"Proceed with Pass 2 for {intermediate_file}? (y/n): ") # accept enter
    if proceed.lower() == "y" or proceed == "":
        pass2 = AssemblerPass2(intermediate_file)
    else:
        print("Pass 2 skipped.")