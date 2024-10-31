# How to impport

# import sys
# from pathlib import Path

# # Add the parent directory to the system path
# repo_home_path = Path(__file__).resolve().parent.parent
# sys.path.append(str(repo_home_path))

# # Now you can import the modules
# from Modules.Mod1 import Class1  # replace `Class1` with the class you want to import
# from Modules.ModB import ClassB
# from Modules.ModC import ClassC


# import os
# import glob
# from pathlib import Path

# # Get the absolute path to the directory where this file (__init__.py) is located
# module_dir = Path(__file__).parent

# # Dynamically import all modules in the directory
# for module_file in glob.glob(str(module_dir / "*.py")):
#     module_name = Path(module_file).stem
#     if module_name != "__init__":
#         __import__(f"{__name__}.{module_name}")


# #To import all the modules into a program located in Modules directory, you can use the following code:
# # Import all modules from the Modules directory
# module_dir = Path(__file__).parent

# for module_file in glob.glob(str(module_dir / "*.py")):
#     module_name = Path(module_file).stem
#     if module_name != "Mod1" and module_name != "__init__":
#         __import__(f"{module_dir.name}.{module_name}")
        
# # TO import all the modules in the Modules directoryinto a program in the sibling folder, you can use the following code:
# import sys
# from pathlib import Path

# # Add the parent directory to the system path
# repo_home_path = Path(__file__).resolve().parent.parent
# sys.path.append(str(repo_home_path))

# # Import all from Modules
# from Modules import *
