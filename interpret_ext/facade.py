"""Interpret facade class"""

from typing import TextIO, List

from args_parse import ArgsParse
from xml_parse import XMLParse
from program import Program
from instructions import *


class Interpret:
    def __init__(self):
        # parse arguments
        args = ArgsParse()
        self._source: TextIO = args.get_source
        self._input: TextIO = args.get_input

        program = Program()

        xml = XMLParse(self._source)
        self._instructions = xml.get_instructions

        program.process_instructions(self._instructions)

        program.eval_program()


Interpret()
# import re
# value = r"string\032haha\032lol"
#
# escapePattern = re.compile(r'(\\[0-9]{3})', re.UNICODE)
# string = re.sub(escapePattern, lambda x: chr(int(x.group()[1:])), value)
# print(string)
