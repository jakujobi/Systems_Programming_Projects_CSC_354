
import os
import sys
from typing import List
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.AssemblerPass1 import AssemblerPass1
from Modules.AssemblerPass2 import AssemblerPass2

class ComboAssembler:
    """
    Assembles a source program in two passes: Pass 1 and Pass 2.
    """
    def __init__(self, source_file):
        # remove the file extension
        self.source_file = source_file
        self.pass1 = AssemblerPass1(self.source_file)
        
        #replace the file extension with .int
        self.intermediate_file = source_file.split(".")[0]+ ".int"
        self.pass2 = AssemblerPass2(self.intermediate_file)
    
    def assemble(self):
        self.pass1.run()
        # Ask the user if they want to proceed with Pass 2
        proceed = input("Proceed with Pass 2? (y/n): ") # accept enter 
        if proceed.lower() == "y":
            self.pass2.run()
        else:
            print("Pass 2 skipped.")

        