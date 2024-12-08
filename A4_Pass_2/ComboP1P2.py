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

def process_files(file_list):
    for file in file_list:
        try:
            source_file = str(file) + ".asm"
            intermediate_file = str(file) + ".int"

            pass1 = AssemblerPass1(source_file)
            
            # Ask for user input to proceed with Pass 2
            proceed = input(f"Proceed with Pass 2 for {intermediate_file}? (y/n): ") # accept enter
            if proceed.lower() == "y" or proceed == "":
                pass2 = AssemblerPass2(intermediate_file)
            else:
                print("Pass 2 skipped.")
        except:
            print("Error processing file: ", file)

if __name__ == "__main__":
    # Make an array of file names
    test_files = ["Htest3",
                  "Htest2",
                  "Htest1",
                  "t1",
                  "t2",
                  "t3",
                  ]

    process_files(test_files)
    # source_file = str(test_files[0]) + ".asm"
    # intermediate_file = str(test_files[0]) + ".int"

    # pass1 = AssemblerPass1(source_file)
    
    # # Ask for user input to proceed with Pass 2
    # proceed = input(f"Proceed with Pass 2 for {intermediate_file}? (y/n): ") # accept enter
    # if proceed.lower() == "y" or proceed == "":
    #     pass2 = AssemblerPass2(intermediate_file)
    # else:
    #     print("Pass 2 skipped.")