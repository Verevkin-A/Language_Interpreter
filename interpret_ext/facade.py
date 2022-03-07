"""Interpret facade class"""

from typing import TextIO, List

from interpret_ext.args_parse import ArgsParse
from interpret_ext.xml_parse import XMLParse
from interpret_ext.program import Program


class Interpret:
    def __init__(self):
        # parse arguments
        args = ArgsParse()
        self._source: TextIO = args.get_source
        self._input: TextIO = args.get_input

        prog = Program(self._input)

        xml = XMLParse(self._source)
        self._instructions = xml.get_instructions

        prog.process_instructions(self._instructions)

        prog.eval_program()
