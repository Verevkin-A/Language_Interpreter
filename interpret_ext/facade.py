"""Interpret facade class"""

from typing import TextIO

from args_parse import ArgsParse
from xml_parse import XMLParse


class Interpret:
    def __init__(self):
        args = ArgsParse()
        self._source: TextIO = args.get_source
        self._input: TextIO = args.get_input

        xml = XMLParse(self._source)

Interpret()
