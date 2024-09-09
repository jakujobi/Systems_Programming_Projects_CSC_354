import os
import random
import string

class SYMSGenerator:
    """
    Generates SYMS.DAT and SEARCH.TXT files with random valid and invalid symbol entries, challenging edge cases.
    Files are generated in the same directory where the script is located.
    """
    def __init__(self, num_lines):
        self.num_lines = num_lines  # Number of lines to generate
        self.symbols = set()  # Track generated symbols for SEARCH.TXT

    def get_script_directory(self):
        """
        Get the directory where the current script is located.
        """
        return os.path.dirname(os.path.realpath(__file__))

    def generate_symbol(self, valid=True):
        """
        Generate a random symbol. Some are valid, others are purposefully invalid.
        If valid=True, generates a valid symbol, otherwise generates invalid.
        """
        if valid:
            # Generate a valid symbol (starts with a letter, max 10 chars, alphanumeric or underscore)
            first_char = random.choice(string.ascii_letters)  # Must start with a letter
            rest = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=random.randint(0, 9)))
            symbol = first_char + rest
        else:
            # Generate an invalid symbol (incorrect length, bad characters, etc.)
            symbol = random.choice([
                random.choice(string.digits) + ''.join(random.choices(string.ascii_letters + string.digits, k=9)),  # Starts with a digit
                ''.join(random.choices(string.ascii_letters + "!@#$%^&*", k=random.randint(1, 11))),  # Special characters
                ''.join(random.choices(string.ascii_letters, k=random.randint(11, 15))),  # Over 10 characters
                '    ' + ''.join(random.choices(string.ascii_letters + string.digits + '_', k=8)) + ':    ',  # Excessive spaces
                ''
            ])
        return symbol

    def generate_value(self):
        """
        Generate a random value for the symbol, including valid and invalid values.
        """
        valid = random.choice([True, False])
        if valid:
            return random.randint(-5000, 5000)  # Valid value
        else:
            return random.choice([random.uniform(-10000, 10000), "not_a_number", 999999])  # Invalid values

    def generate_rflag(self):
        """
        Generate a random RFlag value (either 'true', 'false', or invalid).
        """
        return random.choice(["true", "false", "5", "random_value", ""])

    def generate_syms_line(self):
        """
        Generate a full line for SYMS.DAT, either valid or invalid.
        """
        symbol = self.generate_symbol()
        value = self.generate_value()
        rflag = self.generate_rflag()
        if symbol:  # Only add valid-looking symbols to SEARCH.TXT
            self.symbols.add(symbol[:4].upper())  # Store the first 4 chars (valid part of the symbol) for SEARCH.TXT
        return f"{symbol}:     {value}     {rflag}"

    def generate_syms_file(self):
        """
        Generate the SYMS.DAT file with random symbol data.
        Output it as 'test_SYMS.DAT' in the script's directory.
        """
        file_path = os.path.join(self.get_script_directory(), "test_SYMS.DAT")
        with open(file_path, 'w') as f:
            for _ in range(self.num_lines):
                f.write(self.generate_syms_line() + '\n')
        print(f"{self.num_lines} lines written to {file_path}.")

    def generate_search_symbol(self):
        """
        Generate a symbol for SEARCH.TXT, ensuring a mix of valid and invalid symbols.
        """
        valid = random.choice([True, False])  # Randomly decide if it's valid
        if valid and self.symbols:
            # Randomly select a valid symbol from the ones generated for SYMS.DAT
            return random.choice(list(self.symbols))
        else:
            # Generate an invalid symbol that wouldn't exist in SYMS.DAT
            return self.generate_symbol(valid=False)

    def generate_search_file(self):
        """
        Generate the SEARCH.TXT file with a mix of valid and invalid symbols based on SYMS.DAT.
        Output it as 'test_SEARCH.TXT' in the script's directory.
        """
        file_path = os.path.join(self.get_script_directory(), "test_SEARCH.TXT")
        with open(file_path, 'w') as f:
            for _ in range(self.num_lines):
                f.write(f"{self.generate_search_symbol()}\n")
        
        print(f"Search file written to {file_path}.")

    def generate_files(self):
        """
        Generate both SYMS.DAT and SEARCH.TXT files.
        """
        self.generate_syms_file()
        self.generate_search_file()


def main():
    """
    Main function to generate test_SYMS.DAT and test_SEARCH.TXT.
    Adjust the number of lines to generate as needed.
    """
    try:
        print("Generating test files 'test_SYMS.DAT' and 'test_SEARCH.TXT'...")

        # Adjust number of lines as desired
        num_lines = int(input("Enter the number of lines to generate: "))

        generator = SYMSGenerator(num_lines)
        generator.generate_files()

        print("Test files generated successfully.")
    except Exception as e:
        print(f"An error occurred during file generation: {e}")


if __name__ == "__main__":
    main()