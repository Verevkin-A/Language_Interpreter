"""Interpret facade class"""

from typing import TextIO

from args_parse import ArgsParse
from xml_parse import XMLParse
from program import Program


class Interpret:
    def __init__(self):
        # parse arguments
        args = ArgsParse()
        self._source: TextIO = args.get_source
        self._input: TextIO = args.get_input
        # program info instance
        program = Program()

        xml = XMLParse(self._source)

Interpret()
