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


def test_parsing_handler():
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

# Example usage
if __name__ == "__main__":
    source_line = SourceCodeLine(line_number=1, line_text="LABEL: LDA BUFFER,X . This is a comment")
    parser = ParsingHandler(source_line, validate_parsing=True)
    parser.parse_line()
    print(source_line)
    test_parsing_handler()
