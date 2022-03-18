"""Interpret facade"""

from typing import TextIO, List, Tuple

from interpret_ext.args_parse import ArgsParse
from interpret_ext.xml_parse import XMLParse
from interpret_ext.program import Program


class Interpret:
    """Interpret facade class

    Handle all parts of interpret execution
    """
    def __init__(self):
        self._source, self._input = self.process_arguments()

        # initialize instance of program
        self.prog = Program(self._input)
        self.process_xml()

        # start program evaluation
        self.prog.eval_program()

    @staticmethod
    def process_arguments() -> Tuple[TextIO, TextIO]:
        """Parse arguments

        :return: source file, input file
        """
        args: ArgsParse = ArgsParse()
        return args.get_source, args.get_input

    def process_xml(self) -> None:
        """Get instructions from XML"""
        xml = XMLParse(self._source)
        instructions: List = xml.get_instructions
        # save instructions into a program and filter out labels
        self.prog.process_instructions(instructions)
