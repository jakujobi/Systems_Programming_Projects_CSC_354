# ParsingHandler.py
# Created by: John Akujobi
# Date: 2024 - 11
# Description: ParsingHandler.py is a module that handles the parsing of assembly code into its components.


import re
import os
import sys

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.SourceCodeLine import SourceCodeLine
from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.OpcodeHandler import OpcodeHandler
from Modules.Symbol_Table_Builder import Validator

class ParsingHandler:
    """
    Handles parsing of a single line of assembly code into components: label, opcode, operands, and comments.
    Includes validation if validate_parsing is set to True.
    """
    
    def __init__(self, source_line, validate_parsing=False, logger=None, opcode_handler=None):
        self.source_line = source_line
        self.validate_parsing = validate_parsing
        self.logger = logger or ErrorLogHandler()
        self.opcode_handler = opcode_handler

    def parse_line(self):
        """
        Parses the line into components: label, opcode, operands, and comments.
        Validates the components if validate_parsing is True.
        Updates the SourceCodeLine instance accordingly.
        """
        if self.is_empty_or_comment():
            return

        line = self.source_line.line_text.strip()
        line = self.extract_label(line)
        line = self.extract_comment(line)
        line = self.extract_opcode(line)
        line = self.extract_operands(line)
        self.check_remaining_characters(line)

    def is_empty_or_comment(self) -> bool:
        """
        Checks if the line is empty or a comment.
        """
        if self.source_line.is_empty_line():
            #self.logger.log_action(f"Skipping empty line on Line {self.source_line.line_number}: {self.source_line.line_text}")
            return True

        if self.source_line.is_comment():
            self.source_line.comment = self.source_line.line_text.strip()
            return True

        return False

    def extract_label(self, line: str) -> str:
        """
        Extracts the label from the line.
        """
        label_end_index = line.find(SourceCodeLine.label_suffix_symbol)
        if label_end_index != -1:
            _label = line[:label_end_index].strip()
            self.source_line.set_label(_label)
            line = line[label_end_index + 1:].strip()
        return line

    def extract_comment(self, line: str) -> str:
        """
        Extracts the comment from the line.
        """
        comment_start_index = line.find(SourceCodeLine.comment_symbol)
        if comment_start_index != -1:
            self.source_line.comment = line[comment_start_index + 1:].strip()
            line = line[:comment_start_index].strip()
        return line

    def extract_opcode(self, line: str) -> str:
        """
        Extracts the opcode from the line.
        """
        parts = line.split()
        if parts:
            # make it uppercase
            opcode_mnemonic = parts[0].strip().upper()
            self.source_line.set_opcode_mnemonic(opcode_mnemonic)
            line = line[len(self.source_line.opcode_mnemonic):].strip()
        return line

    def extract_operands(self, line: str) -> str:
        """
        Extracts the operands from the line.
        """
        _operands = line.strip()
        if _operands:
            self.source_line.set_operands(_operands)
        return ''

    def check_remaining_characters(self, line: str):
        """
        Checks if there are any remaining characters after removing the label, opcode, and operands.
        """
        if line.strip():
            error_message = f"Invalid syntax on Line {self.source_line.line_number}: {self.source_line.line_text}\n Remaining characters after parsing: {line}"
            self.logger.log_error(error_message)
            raise SyntaxError(error_message)
        
    def parse_intermediate_line(self):
        """
        Parses a line from the intermediate file into components: line number, address, label, opcode, operands, comments, errors.
        Updates the SourceCodeLine instance accordingly.
        """
        line_text = self.source_line.line_text

        # Use regular expressions to parse the line
        # Pattern to match the line number, address, and the rest
        pattern = r"""
            ^\s*(?P<line_number>\d+)\s+      # Line number
            (?P<address>[0-9A-Fa-f]+)\s+     # Address in hex
            (?P<rest_of_line>.+)$            # The rest of the line
        """
        match = re.match(pattern, line_text, re.VERBOSE)
        if not match:
            # Handle lines without line number and address (e.g., blank lines, comments)
            self.logger.log_error(f"Unable to parse line: {line_text}")
            return

        # Extract line number and address
        line_number = int(match.group('line_number'))
        address = match.group('address')
        rest_of_line = match.group('rest_of_line').strip()

        # Update the source_line object
        self.source_line.line_number = line_number
        self.source_line.address = address

        # Now parse the rest of the line
        # Check for errors in square brackets
        error_pattern = r"""
            (\[ERROR:(?P<error_message>.*?)\])?\s*
            (?P<rest>.+)
        """
        error_match = re.match(error_pattern, rest_of_line, re.VERBOSE)
        if error_match:
            error_message = error_match.group('error_message')
            rest = error_match.group('rest').strip()
            if error_message:
                # Log the error
                error_message = error_message.strip()
                self.source_line.add_error(error_message)
                self.logger.log_error(f"Line {line_number}: {error_message}")

            # Now parse the rest (label, opcode, operands, comment)
            self.parse_rest_of_line(rest)
        else:
            # No error, parse the rest
            self.parse_rest_of_line(rest_of_line)

    def parse_rest_of_line(self, line: str):
        """
        Parses the rest of the line after line number and address.
        Extracts label, opcode, operands, and comments.
        """
        line = line.strip()
        if not line:
            return

        # Extract label if present
        label = ''
        if ':' in line:
            label_part, line = line.split(':', 1)
            label = label_part.strip()
            self.source_line.set_label(label)
            line = line.strip()

        # Split the remaining line into opcode and operands
        parts = line.split(None, 1)
        if parts:
            opcode = parts[0].strip()
            self.source_line.set_opcode_mnemonic(opcode)
            if len(parts) > 1:
                operands_and_comment = parts[1].strip()
                # Check for comments after operands
                if '    ' in operands_and_comment:
                    # Assuming comments are after 4 spaces
                    operands_part, comment = operands_and_comment.split('    ', 1)
                    self.source_line.set_operands(operands_part.strip())
                    self.source_line.comment = comment.strip()
                else:
                    self.source_line.set_operands(operands_and_comment)
        else:
            self.logger.log_error(f"Unable to parse opcode and operands in line: {line}")
            
    def parse_symbol_table(self, lines):
        """
        Parses the symbol table from a list of lines.
        """
        symbol_table_start = False
        symbol_table = {}

        for line in lines:
            line = line.strip()
            if 'Symbol Table:' in line:
                symbol_table_start = True
                continue
            if not symbol_table_start:
                continue
            if line.startswith('______________________________________________'):
                continue
            if not line:
                continue
            # Now parse the symbol table entries
            parts = line.split()
            if len(parts) >= 5:
                symbol = parts[0]
                value = parts[1]
                rflag = parts[2]
                iflag = parts[3]
                mflag = parts[4]
                # Store in symbol table dictionary
                symbol_table[symbol] = {
                    'value': value,
                    'rflag': rflag,
                    'iflag': iflag,
                    'mflag': mflag
                }
        return symbol_table

    
    


def test_parsing_source_code():
    """
    Tests the ParsingHandler class with various lines of assembly code.
    """
    lines = [
        "PROG:   START  1000",
        "FIRST:  STL    ReTADR        .first comment",
        "        LdB    #LENGTH",
        "        BaSE   LENGTH",
        "        lDA    DATA,X",
        "        COMp   LENGTH",
        "+JEQ   END",
        "LOOP:   ADDR   A, B",
        "        SUBR   X,L",
        "        MULR   S, T",
        "        DIVR   SW, PC",
        "        AND    DATA",
        "        OR     COUNT",
        "        SHIFTL Y, 4",
        "        SHIFTR F, P .bad",
        "        TIXR   T",
        "        CLEAR  X",
        "        JSUB   PRINT",
        "        LDT    @#DATA,X",
        "        LDX    @#DATA",
        "idkwhatimdoingonthislinespace: ",
        "ikcwhatimdoingonthisline:",
        "+LDCH  CHARZ,X",
        "+STCH  @CHARZ",
        "HERE:   +LDF   #FLOATZ",
        "+STF   @#FLOATZ",
        "+STCH  @CHARZ,X",
        "+LDF   #FLOATZ,X",
        "+STF   @#FLOATZ,X",
        "MULF   COUNT .random comment",
        "ADDF   RETADR",
        "ADD    #2",
        "DIV    3",
        "MUL    #5",
        "SUB    4",
        "SUBF   =0x45",
        "DIVF   =0cdw",
        "SUBF   0xf3",
        "DIVF   =0xCs",
        "COMPF  DATa",
        "EXTREF GOTEM",
        "J      GOTEM",
        "JLT    LOOP",
        "JGT    LOOP",
        "+TD    DEVICE",
        "RD     DEVICE      .tabs here",
        "+WD    DEVICE",
        "FIX",
        "FLOAT",
        "HIO",
        "STB    #FOUR",
        "STI    @FOUR",
        "STS    #@FOUR",
        "STT    #ONE,X",
        "STX    @ONE,X",
        "NORM",
        "RMO    B",
        "SVC    #HERE",
        "SIO",
        "EQUAL:  EQU    HERE",
        "ALPHA:  EQU    #1000",
        "BETA:   EQU    ALPHA",
        "ADD    ALPHA-@BETA",
        "ADD    ALPHA+#BETA",
        "ADD    @EQUAL+HERE",
        "ADD    #EQUAL-HERE",
        "ADD    ALPHA-HERE,X",
        "ADD    HERE-ALPHA,X",
        "ADD    ALPHA+HERE",
        "ADD    HERE+ALPHA",
        "ADD    16+HERE",
        "ADD    HERE+#16",
        "ADD    #HERE+ALPHA",
        "TIO",
        "SVC    @ALPHA",
        "LPS    BREAK",
        "SSK    DEVICE",
        "COMPR  A, 5 .bad",
        "TIX    COUNT",
        "CLEAR  S",
        "RSUB",
        "LDA    WHAT",
        "BAD    #3",
        "STSW   FOUR",
        "PRINT:  LDS    LENGTH",
        "STA    RETADR",
        "LDL    CHARZ",
        "RSUB",
        "DATA:   BYTE   0Xf1",
        "DATA:   BYTE   0XF1",
        "DATA:   BYTE   =0XF1",
        "DA_2:   BYTE   0XF11",
        "DAT3:   BYTE   0XG1",
        "DAT4:   BYTE   X'G1'",
        "!BAD:   BYTE   d",
        "1BAD:   BYTE   =",
        "_GOOD:  BYTE   1",
        "t123456789: BYTE 1",
        "t1234567890: BYTE 1",
        "GOO:    BYTE   1",
        "BA3D:   BYTE   #1",
        "BA#D:   BYTE   1",
        "Z:      BYTE   20",
        "CHARZ:  BYTE   0CA",
        "FLOATZ: BYTE   0C'\"1.dD",
        "FOUR:   RESB   #4",
        "HABR:   RESW   637     .should make anything past use B reg",
        "COUNT:  WORD   #1",
        "LENGTH: WORD   4096",
        "ONE:    RESB   1",
        "RETaDR: RESW   #1",
        "BREAK:  RESb   1911     .should make anything past use format 4",
        "DEVICE: BYTE   0X'\"F8'",
        "RESB   DATA",
        "RESB   HERE-ALPHA",
        "RESB   ALpHA-7777",
        "ZA:     EQU    ALPHA-BETA",
        "ZB:     EQU    ALPHA+BETA",
        "ZC:     EQU    EQUAL+HERE",
        "ZD:     EQU    eQUAL-HERE",
        "ZE:     EQU    ALPHA-HERE",
        "ZF:     EQU    HERE-ALPHA",
        "ZG:     EQU    ALPHA+HERE",
        "ZH:     EQU    HERE+ALPHA",
        "ZI:     EQU    16+HERE",
        "ZJ:     EQU    HERE+#16",
        "ZK:     EQU    #HERE+ALPHA",
        "ZL:     EQU",
        "TEST:   EQU    heir",
        "EQU    HERE!",
        "EQU    #HERE",
        "ZZ:     EQU    =0CABC",
        "EXTDEF ZA, ZB,DEVICE, ZD,ZE,ZF,AH,Zz",
        "EXTDEF ZG",
        "EXTREF OTRFUN,AAA ,AAB",
        "JSUB   PRINT",
        "JSUB   TEST",
        "JSUB   OTRFUN",
        "+JSUB  OTRFUN",
        "LDA    OTRFUN",
        "+LDA    TEST",
        "END    PROG"
    ]

    for idx, line_text in enumerate(lines, start=1):
        source_line = SourceCodeLine(line_number=idx, line_text=line_text)
        parser = ParsingHandler(source_line, validate_parsing=True)
        try:
            parser.parse_line()
            print(f"Line {idx}: label = {source_line.label}, opcode = {source_line.opcode_mnemonic}, operands = {source_line.operands}, comment = {source_line.comment}")
        except SyntaxError as e:
            print(f"Line {idx}: {e}")
            
def test_parsing_intermediate_code():
    """
    Tests the ParsingHandler class with lines from an intermediate file.
    """
    lines = [
        "1          00000     PROG:       START      1000",
        "2          003E8     FIRST:      STL        ReTADR    first comment",
        "3          003EB                 LDB        #LENGTH",
        "4          003EE     [ERROR: Invalid opcode mnemonic: 'BASE'. ]                BASE       LENGTH",
        "5          003EE                 LDA        DATA,X",
        "6          003F1                 COMP       LENGTH",
        "7          003F4                 +JEQ       END",
        "8          003F8     LOOP:       ADDR       A, B",
        "9          003FA                 SUBR       X,L",
        "10         003FC                 MULR       S, T",
        "11         003FE                 DIVR       SW, PC",
        "12         00400                 AND        DATA",
        "13         00403                 OR         COUNT",
        "14         00406                 SHIFTL     Y, 4",
        "15         00408                 SHIFTR     F, P    bad",
        "16         0040A                 TIXR       T",
        "17         0040C                 CLEAR      X",
        "18         0040E                 JSUB       PRINT",
        "19         00411                 LDT        @#DATA,X",
        "20         00414                 LDX        @#DATA",
        "21         00417     [ERROR: 'IDKWHATIMDOINGONTHISLINESPACE' length exceeds 10 characters.]    idkwhatimdoingonthislinespace:",
        "22         00417     [ERROR: 'IKCWHATIMDOINGONTHISLINE' length exceeds 10 characters.]    ikcwhatimdoingonthisline:",
        "23         00417                 +LDCH      CHARZ,X",
        "24         0041B                 +STCH      @CHARZ",
        "25         0041F     HERE:       +LDF       #FLOATZ",
        "26         00423                 +STF       @#FLOATZ",
        "27         00427                 +STCH      @CHARZ,X",
        "28         0042B                 +LDF       #FLOATZ,X",
        "29         0042F                 +STF       @#FLOATZ,X",
        "30         00433                 MULF       COUNT    random comment",
        "31         00436                 ADDF       RETADR",
        "32         00439                 ADD        #2",
        "33         0043C                 DIV        3",
        "34         0043F                 MUL        #5-4",
        "35         00442                 SUB        HERE-LOOP",
        "36         00445                 LDA        ALPHA+LOOP",
        "37         00448                 SUBF       =0x45",
        "38         0044B                 DIVF       =0cdw",
        "39         0044E                 SUBF       0xf3",
        "40         00451                 DIVF       =0xCs",
        "41         00454                 COMPF      DATa",
        "42         00457                 EXTREF     GOTEM",
        "43         00457                 J          GOTEM",
        "44         0045A                 JLT        LOOP",
        "45         0045D                 JGT        LOOP",
        "46         00460                 +TD        DEVICE",
        "47         00464                 RD         DEVICE    tabs here",
        "48         00467                 +WD        DEVICE",
        "49         0046B                 FIX",
        "50         0046C                 FLOAT",
        "51         0046D                 HIO",
        "52         0046E                 STB        #FOUR",
        "53         00471                 STI        @FOUR",
        "54         00474                 STS        #@FOUR",
        "55         00477                 STT        #ONE,X",
        "56         0047A                 STX        @ONE,X",
        "57         0047D                 NORM",
        "58         0047E                 RMO        B",
        "59         00480                 SVC        #HERE",
        "60         00482                 SIO",
        "61         00483     [ERROR: Invalid expression for EQU directive: 'HERE']    EQUAL:      EQU        HERE",
        "62         00483     ALPHA:      EQU        #1000",
        "63         00483     [ERROR: Invalid expression for EQU directive: 'ALPHA']    BETA:       EQU        ALPHA",
        "64         00483                 ADD        ALPHA-@BETA",
        "65         00486                 ADD        ALPHA+#BETA",
        "66         00489                 ADD        @EQUAL+HERE",
        "67         0048C                 ADD        #EQUAL-HERE",
        "68         0048F                 ADD        ALPHA-HERE,X",
        "69         00492                 ADD        HERE-ALPHA,X",
        "70         00495                 ADD        ALPHA+HERE",
        "71         00498                 ADD        HERE+ALPHA",
        "72         0049B                 ADD        16+HERE",
        "73         0049E                 ADD        HERE+#16",
        "74         004A1                 ADD        #HERE+ALPHA",
        "75         004A4                 TIO",
        "76         004A5                 SVC        @ALPHA",
        "77         004A7                 LPS        BREAK",
        "78         004AA                 SSK        DEVICE",
        "79         004AD                 COMPR      A, 5    bad",
        "80         004AF                 TIX        COUNT",
        "81         004B2                 CLEAR      S",
        "82         004B4                 RSUB",
        "83         004B7                 LDA        WHAT",
        "84         004BA     [ERROR: Invalid opcode mnemonic: 'BAD'. ]                BAD        #3",
        "85         004BA                 STSW       FOUR",
        "86         004BD     PRINT:      LDS        LENGTH",
        "87         004C0                 STA        RETADR",
        "88         004C3                 LDL        CHARZ",
        "89         004C6                 RSUB",
        "90         004C9",
        "91         004C9                            . ha BLANK",
        "92         004C9     DATA:       BYTE       0Xf1",
        "93         004CA     DATA:       BYTE       0XF1",
        "94         004CB     DATA:       BYTE       =0XF1",
        "95         004CB     DA_2:       BYTE       0XF11",
        "96         004CB     DAT3:       BYTE       0XG1",
        "97         004CC     DAT4:       BYTE       X'G1'",
        "98         004CC     [ERROR: '!BAD' must start with a letter.; Label '!BAD' contains invalid character '!'. ]    !BAD:       BYTE       d",
        "99         004CC     [ERROR: '1BAD' must start with a letter.]    1BAD:       BYTE       =",
        "100        004CC     [ERROR: '_GOOD' must start with a letter.]    _GOOD:      BYTE       1",
        "101        004CC     t123456789: BYTE       1",
        "102        004CC     [ERROR: 'T1234567890' length exceeds 10 characters.]    t1234567890: BYTE       1",
        "103        004CC     GOO:        BYTE       1",
        "104        004CC     BA3D:       BYTE       #1",
        "105        004CC     [ERROR: Label 'BA#D' contains invalid character '#'. ]    BA#D:       BYTE       1",
        "106        004CC     Z:          BYTE       20",
        "107        004CC     CHARZ:      BYTE       0CA",
        "108        004CC     FLOATZ:     BYTE       0C'\"1    dD",
        "109        004CF     FOUR:       RESB       #4",
        "110        004D3     HABR:       RESW       637    should make anything past use B reg",
        "111        00C4A     COUNT:      WORD       #1",
        "112        00C4D     LENGTH:     WORD       4096",
        "113        00C50                 WORD       COUNT",
        "114        00C53                 WORD       COUNT-HABR",
        "115        00C56     ONE:        RESB       1",
        "116        00C57     RETaDR:     RESW       #1",
        "117        00C5A     FIVE:       RESW       #3    partial line comment - ignore (actual tabs here)",
        "118        00C63     BREAK:      RESB       1911    should make anything past use format 4",
        "119        013DA     DEVICE:     BYTE       0X'\"F8'",
        "120        013DD                 RESB       DATA",
        "121        013DD                 RESB       HERE-ALPHA",
        "122        013DD                 RESB       ALpHA-7777",
        "123        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA-BETA']    ZA:         EQU        ALPHA-BETA",
        "124        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA+BETA']    ZB:         EQU        ALPHA+BETA",
        "125        013DD     [ERROR: Invalid expression for EQU directive: 'EQUAL+HERE']    ZC:         EQU        EQUAL+HERE",
        "126        013DD     [ERROR: Invalid expression for EQU directive: 'eQUAL-HERE']    ZD:         EQU        eQUAL-HERE",
        "127        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA-HERE']    ZE:         EQU        ALPHA-HERE",
        "128        013DD     [ERROR: Invalid expression for EQU directive: 'HERE-ALPHA']    ZF:         EQU        HERE-ALPHA",
        "129        013DD     [ERROR: Invalid expression for EQU directive: 'ALPHA+HERE']    ZG:         EQU        ALPHA+HERE",
        "130        013DD     [ERROR: Invalid expression for EQU directive: 'HERE+ALPHA']    ZH:         EQU        HERE+ALPHA",
        "131        013DD     [ERROR: Invalid expression for EQU directive: '16+HERE']    ZI:         EQU        16+HERE",
        "132        013DD     [ERROR: Invalid expression for EQU directive: 'HERE+#16']    ZJ:         EQU        HERE+#16",
        "133        013DD     [ERROR: Invalid expression for EQU directive: '#HERE+ALPHA']    ZK:         EQU        #HERE+ALPHA",
        "134        013DD     [ERROR: Invalid expression for EQU directive: '']    ZL:         EQU",
        "135        013DD     [ERROR: Invalid expression for EQU directive: 'heir']    TEST:       EQU        heir",
        "136        013DD     T2:         EQU        *",
        "137        013DD     [ERROR: Invalid expression for EQU directive: 'HERE!']                EQU        HERE!",
        "138        013DD     [ERROR: Invalid expression for EQU directive: '#HERE']                EQU        #HERE",
        "139        013DD     [ERROR: Invalid expression for EQU directive: '=0CABC']    ZZ:         EQU        =0CABC",
        "140        013DD                 EXTDEF     ZA, ZB,DEVICE, ZD,ZE,ZF,AH,Zz",
        "141        013DD                 EXTDEF     ZG",
        "142        013DD                 EXTREF     OTRFUN,AAA ,AAB",
        "143        013DD                 WORD       DEVICE-AAA",
        "144        013E0                 WORD       AAA-AAB",
        "145        013E3                 JSUB       PRINT",
        "146        013E6                 JSUB       TEST",
        "147        013E9                 JSUB       OTRFUN",
        "148        013EC                 +JSUB      OTRFUN",
        "149        013F0                 LDA        OTRFUN",
        "150        013F3                 +LDA       TEST",
        "151        013F7                 LDA        =0x45",
        "152        013FA                 LDA        =0Cdw",
        "153        013FD                 END        PROG"
    ]

    for idx, line_text in enumerate(lines, start=1):
        source_line = SourceCodeLine(line_number=idx, line_text=line_text)
        parser = ParsingHandler(source_line, validate_parsing=True)
        try:
            parser.parse_intermediate_line()
            print(f"Line {idx}: {source_line}")
        except SyntaxError as e:
            print("error")
            # print(f"Line {idx}: {e}")

# Example usage
if __name__ == "__main__":
    test_parsing_intermediate_code()    

# # Example usage
# if __name__ == "__main__":
#     source_line = SourceCodeLine(line_number=1, line_text="LABEL: LDA BUFFER,X . This is a comment")
#     parser = ParsingHandler(source_line, validate_parsing=True)
#     parser.parse_line()
#     print(source_line)
#     test_parsing_source_code()
