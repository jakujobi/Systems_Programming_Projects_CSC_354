"""
/*********************************************************************
***  FILE  : ErrorLogHandler.py                                    ***
***  Author : John Akujobi                                         ***
**********************************************************************
***  DESCRIPTION :                                                 ***
***  This program defines a class `ErrorLogHandler` that handles   ***
***  logging of actions and errors throughout the program. It      ***
***  provides methods to log actions, log errors, retrieve logs,   ***
***  display all messages, and manage logs. The class ensures that ***
***  logs are displayed with pagination to prevent excessive       ***
***  scrolling.                                                    ***
***                                                                ***
***  The `ErrorLogHandler` class includes the following methods:   ***
***                                                                ***
***  - __init__():                                                 ***
***      Initializes empty logs for actions and errors.            ***
***                                                                ***
***  - log_action(message):                                        ***
***      Logs an action by appending the message to the action log ***
***      and prints the message to the console. Paginates the      ***
***      output after every 18 lines.                              ***
***                                                                ***
***  - log_error(error_message, context_info=None):                ***
***      Logs an error message, optionally with context            ***
***      information, and prints it to the console. Paginates the  ***
***      output after every 18 lines.                              ***
***                                                                ***
***  - display_log():                                              ***
***      Asks the user if they want to display the log entries.    ***
***      Displays the log entries with pagination if the user      ***
***      agrees.                                                   ***
***                                                                ***
***  - display_errors():                                           ***
***      Asks the user if they want to display the error logs.     ***
***      Displays the errors with pagination if the user agrees.   ***
***                                                                ***
***  - ask_to_display(question):                                   ***
***      Asks the user if they want to display logs or errors,     ***
***      with retry logic for invalid inputs.                      ***
***                                                                ***
***  - paginate_output(log_entries, header):                       ***
***      Displays the log entries with pagination to prevent       ***
***      excessive scrolling.                                      ***
***                                                                ***
***  - press_continue():                                           ***
***      Pauses the program and waits for the user to press Enter  ***
***      before continuing.                                        ***
***                                                                ***
***  - clear_logs():                                               ***
***      Clears all the logs of actions and errors.                ***
***                                                                ***
***  - has_errors():                                               ***
***      Checks if there are any logged errors.                    ***
***      Returns True if there are errors, otherwise False.        ***
***                                                                ***
***  USAGE:                                                        ***
***  - To use this program, create an instance of the              ***
***    `ErrorLogHandler` class and call its methods to log actions ***
***    and errors, display logs, and manage logs.                  ***
***                                                                ***
***  - Example:                                                    ***
***      logger = ErrorLogHandler()                                ***
***      logger.log_action("Action performed")                     ***
***      logger.log_error("Error occurred", "Context info")        ***
***      logger.display_log()                                      ***
***      logger.display_errors()                                   ***
***                                                                ***
********************************************************************/
"""
import inspect


class ErrorLogHandler:
    """
    /***************************************************************************************
    ***  CLASS NAME : ErrorLogHandler                                                     ***
    ***  DESCRIPTION :                                                                   ***
    ***      Handles logging of actions and errors throughout the program. Provides      ***
    ***      methods to log, display, and manage logs and errors.                        ***
    ***************************************************************************************/

    Class to handle both logging actions and error messages throughout the program.
    Provides mechanisms to log actions, log errors, retrieve logs, and display all messages.
    """


    def __init__(self, print_log_actions: bool = False):
        """
        /***************************************************************************************
        ***  METHOD : __init__                                                               ***
        ***  DESCRIPTION :                                                                   ***
        ***      Initializes empty logs for actions and errors.                              ***
        ***************************************************************************************/

        Initialize the ErrorLogHandler with empty logs for actions and errors.
        """
        self.log_entries: list[str] = []
        self.error_log: list[str] = []
        self.print_log_actions = print_log_actions


    def get_caller_info(self) -> str:
        """
        Retrieves information about the caller of the log method.

        :return: A string containing the class name, method name, and line number of the caller.
        """
        frame = inspect.currentframe().f_back.f_back
        class_name = frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else ''
        method_name = frame.f_code.co_name
        line_number = frame.f_lineno
        return f"{class_name}.{method_name} (line {line_number})"



    def log_action(self, message: str, print_actions: bool = None):
        """
        /***************************************************************************************
        ***  METHOD : log_action                                                             ***
        ***  DESCRIPTION :                                                                   ***
        ***      Logs an action by appending the message to the action log and prints the    ***
        ***      message to the console if print_actions is True. Paginates the output       ***
        ***      after every 18 lines.                                                       ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      message : str   : The message describing the action performed.              ***
        ***      print_actions : bool : Whether to print the message to the console.         ***
        ***************************************************************************************/

        Log an action performed during the program's execution.

        :param message: The message describing the action.
        :param print_actions: Whether to print the message to the console.
        """
        caller_info = self.get_caller_info()
        log_message = f"[ACTION] {caller_info}: {message}"
        self.log_entries.append(log_message)
        
        if self.print_log_actions or print_actions:
            print(f"[ACTION]: {message}")
            # Paginate after every 18 lines of actions
            if len(self.log_entries) % 18 == 0:
                self.paginate_output(self.log_entries, "Displaying Actions Log")




    def log_error(self, error_message: str, context_info: str = None):
        """
        /***************************************************************************************
        ***  METHOD : log_error                                                              ***
        ***  DESCRIPTION :                                                                   ***
        ***      Logs an error message, optionally with context information, and prints      ***
        ***      it to the console. Paginates the output after every 18 lines.               ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      error_message  : str  : The error message to log.                           ***
        ***      context_info   : str  : Optional context about where the error occurred.    ***
        ***************************************************************************************/

        Log an error message with optional context information for better clarity.

        :param error_message: The error message to be logged.
        :param context_info: Additional context about where the error occurred (optional).
        """
        caller_info = self.get_caller_info()
        log_message = f"[ERROR] {caller_info}: {error_message}"
        if context_info:
            log_message += f" | Context: {context_info}"
        self.error_log.append(log_message)
        
        self.print_colored(log_message, 'red', 'black')
        # Paginate after every 18 lines of errors
        if len(self.error_log) % 18 == 0:
            self.paginate_output(self.error_log, "Displaying Error Log")

    @staticmethod
    def print_colored(text, color, bg_color='black'):
        """
        Prints the given text in the specified foreground and background colors.

        Parameters:
        - text (str): The string to be printed.
        - color (str): The foreground color name.
        - bg_color (str, optional): The background color name. Defaults to 'black'.
        
        Supported Colors:
        - black, red, green, yellow, blue, magenta, cyan, white
        """
        
        # Mapping of color names to ANSI codes
        colors = {
            'black': '30',
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'magenta': '35',
            'cyan': '36',
            'white': '37'
        }

        bg_colors = {
            'black': '40',
            'red': '41',
            'green': '42',
            'yellow': '43',
            'blue': '44',
            'magenta': '45',
            'cyan': '46',
            'white': '47'
        }

        # Get the ANSI codes for the specified colors
        color_code = colors.get(color.lower())
        bg_color_code = bg_colors.get(bg_color.lower(), '40')  # Default to black background

        if color_code is None:
            raise ValueError(f"Unsupported color: '{color}'. Supported colors are: {', '.join(colors.keys())}")

        if bg_color_code is None:
            raise ValueError(f"Unsupported background color: '{bg_color}'. Supported colors are: {', '.join(bg_colors.keys())}")

        # ANSI escape sequence
        ansi_sequence = f"\033[{color_code};{bg_color_code}m{text}\033[0m"

        print(ansi_sequence)

        
    def display_log(self):
        """
        /***************************************************************************************
        ***  METHOD : display_log                                                            ***
        ***  DESCRIPTION :                                                                   ***
        ***      Asks the user if they want to display the log entries. Displays the log     ***
        ***      entries with pagination if the user agrees.                                 ***
        ***************************************************************************************/

        Ask the user if they want to view the log entries. Paginate if they agree.
        """
        if not self.log_entries:
            print("No actions have been logged.")
        else:
            if self.ask_to_display("Do you want to view the log entries?"):
                print("\nLog of Actions:")
                print("=" * 50)
                self.paginate_output(self.log_entries, "Log of Actions")

        
    def display_errors(self):
        """
        /***************************************************************************************
        ***  METHOD : display_errors                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Asks the user if they want to display the error logs. Displays the errors   ***
        ***      with pagination if the user agrees.                                         ***
        ***************************************************************************************/

        Ask the user if they want to view the error logs. Paginate if they agree.
        """
        if not self.error_log:
            print("No errors have been logged.")
        else:
            if self.ask_to_display("Do you want to view the error log?"):
                print("\nError Log:")
                print("=" * 50)
                self.paginate_output(self.error_log, "Error Log")


    def ask_to_display(self, question: str) -> bool:
        """
        /***************************************************************************************
        ***  METHOD : ask_to_display                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Asks the user if they want to display logs or errors, with retry logic for  ***
        ***      invalid inputs.                                                             ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      question : str   : The question to ask the user.                            ***
        ***                                                                                  ***
        ***  RETURN : bool                                                                   ***
        ***      Returns True if the user agrees, False otherwise.                           ***
        ***************************************************************************************/

        Ask the user if they want to display the logs/errors with retry logic for invalid inputs.

        :param question: The question to ask the user.
        :return: True if the user agrees to display, False otherwise.
        """
        valid_yes = {'y', 'yes', '', 'Y', 'YES', 'YeS'}
        valid_no = {'n', 'no', 'N', 'NO'}
        retry_limit = 5
        retries = 0

        while retries < retry_limit:
            user_input = input(f"{question} (y/n): ").strip()
            if user_input in valid_yes:
                return True
            elif user_input in valid_no:
                return False
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")
                retries += 1

        # If the user reaches the retry limit, display an "annoyed" message and skip the logs/errors
        print("Seriously? You can't just type 'y' or 'n'? Fine, I won't show it.")
        return False

    
    def paginate_output(self, log_entries, header: str):
        """
        /***************************************************************************************
        ***  METHOD : paginate_output                                                        ***
        ***  DESCRIPTION :                                                                   ***
        ***      Displays the log entries with pagination to prevent excessive scrolling.    ***
        ***                                                                                  ***
        ***  INPUT PARAMETERS :                                                              ***
        ***      log_entries : list  : The list of log entries to be displayed.              ***
        ***      header      : str   : The header to display before showing the entries.     ***
        ***************************************************************************************/

        Paginate the log/error output to prevent excessive scrolling.
        
        :param log_entries: The log or error entries to be displayed.
        :param header: The header for the log/error output.
        """
        counter = 0
        for entry in log_entries:
            print(entry)
            counter += 1
            if counter % 18 == 0:
                self.press_continue()

    def press_continue(self):
        """
        /***************************************************************************************
        ***  METHOD : press_continue                                                         ***
        ***  DESCRIPTION :                                                                   ***
        ***      Pauses the program and waits for the user to press Enter before continuing. ***
        ***************************************************************************************/

        Pause the program and wait for the user to press Enter before continuing.
        """
        input("Press Enter to continue...")
        print("\033[F\033[K", end='')  # Clear the line after pressing enter to clean the screen

    def clear_logs(self):
        """
        /***************************************************************************************
        ***  METHOD : clear_logs                                                             ***
        ***  DESCRIPTION :                                                                   ***
        ***      Clears all the logs of actions and errors.                                  ***
        ***************************************************************************************/

        Clear all logs of actions and errors.
        """
        self.log_entries.clear()
        self.error_log.clear()

    def has_errors(self) -> bool:
        """
        /***************************************************************************************
        ***  METHOD : has_errors                                                             ***
        ***  DESCRIPTION :                                                                   ***
        ***      Checks if there are any logged errors.                                      ***
        ***                                                                                  ***
        ***  RETURN : bool                                                                   ***
        ***      Returns True if there are errors, otherwise False.                          ***
        ***************************************************************************************/

        Check if there are any logged errors.

        :return: True if there are errors, False otherwise.
        """
        return bool(self.error_log)
