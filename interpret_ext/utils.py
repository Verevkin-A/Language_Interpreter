"""Interpret general helping functions"""

from sys import stderr


class Utils:
    @staticmethod
    def error(err_msg: str, ret_code: int) -> None:
        """Error exit

        Print error message on stderr,
        exit program with given return code
        """
        stderr.write(err_msg + "\n")
        exit(ret_code)
