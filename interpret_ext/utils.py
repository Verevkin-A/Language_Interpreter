"""Interpret general helping functions"""

from sys import stderr
from typing import Callable

from interpret_ext.types_ import Constant
from interpret_ext.ret_codes import RetCodes


class Utils:
    @staticmethod
    def error(err_msg: str, ret_code: int) -> None:
        """Error exit

        Print error message on stderr,
        exit program with given return code
        """
        stderr.write(err_msg + "\n")
        exit(ret_code)

    @staticmethod
    def compare_consts(const1: Constant, const2: Constant, operation: Callable) -> bool:
        allowed_types =["int", "bool", "string"]
        if const1.get_type not in allowed_types or const2.get_type not in allowed_types or \
                const1.get_type != const2.get_type:
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)
        if const1.get_type == "int":
            return operation(int(const1.get_value, 0), int(const2.get_value, 0))
        elif const2.get_type == "bool":
            return operation(True if const1.get_value == "true" else False,
                             True if const2.get_value == "true" else False)
        else:
            return operation(const1.get_value, const2.get_value)
