"""Class for arguments handling"""

from argparse import ArgumentParser, RawTextHelpFormatter
from sys import stdin, argv

from utils import Utils
from ret_codes import RetCodes


class ArgsParse:
    """Parameters parsing

    Public attributes:
    parser -- instance of program ArgumentParser
    args -- given parameters
    """
    _PROGRAM = "interpret.py"
    _DESCRIPTION = "The script reads an XML representation of the program,\n" \
                   "interprets it using command line parameters and generates output."
    _EPILOG = "At least one of the parameters (source or input) must be always assigned.\n" \
              "If one of them is missing, reads missing data from standard input.\n"

    def __init__(self):
        """Parameters parsing constructor

        Create ArgumentParser instance and take given parameters,
        check if parameters are valid
        """
        self.check_help()
        self.parser = ArgumentParser(prog=self._PROGRAM, description=self._DESCRIPTION, epilog=self._EPILOG,
                                     formatter_class=RawTextHelpFormatter)
        self.parser.add_argument("--source", nargs="?", type=open, default=stdin, metavar="~/src",
                                 help="path to program XML representation")
        self.parser.add_argument("--input", nargs="?", type=open, default=stdin, metavar="~/src",
                                 help="path to file with input")
        try:
            self.args, self._unknown_args = self.parser.parse_known_args()
        except FileNotFoundError:
            Utils.error("Error: can't open file", RetCodes.OPEN_IN_ERR)
        except PermissionError:
            Utils.error("Error: insufficient permissions", RetCodes.OPEN_IN_ERR)
        except Exception:
            Utils.error("Error: internal", RetCodes.INTERNAL_ERR)
        self.check_args()

    def check_args(self):
        """Parameters check

        Method check if was given right combination of parameters
        and check if parameters are valid
        """
        if self.args.source is stdin and self.args.input is stdin:
            Utils.error("Error: must exist at least one of the source or input parameters", RetCodes.PARAM_ERR)
        elif self.args.source is None or self.args.input is None:
            Utils.error("Error: can't open file", RetCodes.OPEN_IN_ERR)
        elif self._unknown_args:
            Utils.error("Error: unknown parameter", RetCodes.PARAM_ERR)

    @staticmethod
    def check_help():
        """Method check if help parameter is present with other parameters

        Raise parameter error if it's true
        """
        if ("--help" in argv or "-h" in argv) and len(argv) > 2:
            Utils.error("Error: -h/--help can't be combined with other parameters", RetCodes.PARAM_ERR)
