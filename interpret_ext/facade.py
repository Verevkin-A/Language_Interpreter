"""Interpret facade class"""

from args_parse import ArgsParse


class Interpret:
    def __init__(self):
        args = ArgsParse().args
        self._source = args.source
        self._input = args.input


Interpret()