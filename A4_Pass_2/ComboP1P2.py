# ComboP1P2.py

import sys
from pathlib import Path

# Add the parent directory to the system path
repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.AssemblerPass1 import AssemblerPass1
from Modules.AssemblerPass2 import AssemblerPass2

def process_files(file_list):
    for file in file_list:
        try:
            process_single_file(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            
def process_single_file(file):
    try:
        source_file = str(file) + ".asm"
        intermediate_file = str(file) + ".int"

        AssemblerPass1(source_file)
        
        # Ask for user input to proceed with Pass 2
        proceed = input(f"Proceed with Pass 2 for {intermediate_file}? (y/n): ") # accept enter
        if proceed.lower() in ["y", ""]:
            AssemblerPass2(intermediate_file)
        else:
            print("Pass 2 skipped.")
    except Exception as e:
        print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    # Make an array of file names
    test_files = [
                "Htest3",
                "Htest2",
                "Htest1",
                "t1",
                "t2",
                "t3",
                ]
    
    if len(sys.argv) > 1:
        file = sys.argv[1]
        process_single_file(file)
    else:
        process_files(test_files)
