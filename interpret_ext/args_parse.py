"""Class for arguments handling"""

from argparse import ArgumentParser, RawTextHelpFormatter
from sys import stdin, argv
from typing import TextIO

from utils import Utils
from ret_codes import RetCodes


class ArgsParse:
    """Parameters parsing

    Attributes:
    parser -- instance of program ArgumentParser
    args -- given parameters
    """

    _PROGRAM = "interpret.py"
    _DESCRIPTION = "The script reads an XML representation of the program,\n" \
                   "interprets it using command line parameters and generates output."
    _EPILOG = "At least one of the parameters (source or input) must be always assigned.\n" \
              "If one of them is missing, reads missing data from standard input.\n"

    def __init__(self) -> None:
        """Parameters parsing constructor

        Create ArgumentParser instance and take given parameters,
        check if parameters are valid
        """
        self.check_help()
        self._parser = ArgumentParser(prog=self._PROGRAM, description=self._DESCRIPTION, epilog=self._EPILOG,
                                      formatter_class=RawTextHelpFormatter)
        self._parser.add_argument("--source", nargs="?", type=open, default=stdin, metavar="~/src",
                                  help="path to program XML representation")
        self._parser.add_argument("--input", nargs="?", type=open, default=stdin, metavar="~/src",
                                  help="path to file with input")
        try:
            self.args, self._unknown_args = self._parser.parse_known_args()
        except FileNotFoundError:
            Utils.error("Error: can't open file", RetCodes.OPEN_IN_ERR)
        except PermissionError:
            Utils.error("Error: insufficient permissions", RetCodes.OPEN_IN_ERR)
        except Exception:
            Utils.error("Error: internal", RetCodes.INTERNAL_ERR)
        self.check_args()

    def check_args(self) -> None:
        """Parameters check

        Method check if was given right combination of parameters
        and check if parameters are valid
        """
        if self.get_source is stdin and self.get_input is stdin:
            Utils.error("Error: must exist at least one of the source or input parameters", RetCodes.PARAM_ERR)
        elif self.get_source is None or self.get_input is None:
            Utils.error("Error: can't open file", RetCodes.OPEN_IN_ERR)
        elif self._unknown_args:
            Utils.error("Error: unknown parameter", RetCodes.PARAM_ERR)

    @staticmethod
    def check_help() -> None:
        """Method check if help parameter is present with other parameters

        Raise parameter error if it's true
        """
        if ("--help" in argv or "-h" in argv) and len(argv) > 2:
            Utils.error("Error: -h/--help can't be combined with other parameters", RetCodes.PARAM_ERR)

    @property
    def get_source(self) -> TextIO:
        """Source file getter"""
        return self.args.source

    @property
    def get_input(self) -> TextIO:
        """Input file getter"""
        return self.args.input
