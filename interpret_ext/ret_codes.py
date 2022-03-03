"""Interpret return codes"""


class RetCodes:
    """Error return codes for interpret"""
    PARAM_ERR = 10              # wrong parameters count or using forbidden parameters combination
    OPEN_IN_ERR = 11            # opening of input files (existence, insufficient rights)
    OPEN_OUT_ERR = 12           # opening of output files (existence, insufficient rights, writing error)

    XML_FORMAT_ERR = 31         # bad XML format in input file (file isn't "well-formed")
    XML_STRUCT_ERR = 32         # unexpected XML structure (argument element isn't in instruction element)

    SEMANTIC_ERR = 52           # semantic check of IPPcode22 (undefined label, redefinition of variable)
    OPP_TYPE_ERR = 53           # runtime - bad operands types
    VAR_NOT_EXIST_ERR = 54      # runtime - accessing not existing variable (frame exist)
    FRAME_NOT_EXIST_ERR = 55    # runtime - frame don't exist (read from empty frame stack)
    VALUE_NOT_EXIST_ERR = 56    # runtime - missing value (in variable, data stack, call stack)
    OPP_VALUE_ERR = 57          # runtime - bad operand value (zero division, bad EXIT return code)
    STRING_ERR = 58             # runtime - bad work with string

    INTERNAL_ERR = 99           # internal error (memory allocation)
