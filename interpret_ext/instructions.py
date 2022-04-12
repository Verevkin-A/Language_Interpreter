"""Interpret available instructions"""

from typing import List
from abc import ABC, abstractmethod
from sys import stderr, stdin

from interpret_ext.types_ import Constant
from interpret_ext.program import Program
from interpret_ext.utils import Utils
from interpret_ext.ret_codes import RetCodes


class InstInterface(ABC):
    """Instructions interface"""
    @abstractmethod
    def eval(self):
        """Evaluate instruction"""
        pass


class Instruction:
    """
    General instruction class
    Inherited by all instructions
    """
    def __init__(self, arguments: List):
        self.arguments: List = arguments
        # get singleton program instance
        self.program: Program = Program.get_instance()


class Createframe(Instruction):
    """Create empty temporary frame"""
    def eval(self):
        self.program.tmp_frame = {}


class Pushframe(Instruction):
    """
    Push temporary frame on local frame
    Unset temporary frame after
    """
    def eval(self):
        if self.program.get_tmp_frame is None:
            Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.local_frame.append(self.program.get_tmp_frame)
        self.program.tmp_frame = None


class Popframe(Instruction):
    """
    Pop frame, from top of the local frames, on temporary frame
    Throws error if local frame is emplty
    """
    def eval(self):
        if len(self.program.get_local_frame) == 0:
            Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.tmp_frame = self.program.local_frame.pop()


class Return(Instruction):
    """
    Return from function on previous position
    Throws error if not called from function
    """
    def eval(self):
        if len(self.program.get_call_stack) == 0:
            Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.program_ptr = self.program.call_stack.pop()


class Break(Instruction):
    """Prints current program stats on stderr"""
    def eval(self):
        print(self.program.get_stats(), file=stderr)


class Defvar(Instruction):
    """
    New variable definition
    Throws error if variable with stated name already exist
    """
    def eval(self):
        if self.program.is_exist(self.arguments[0]):
            Utils.error("redefinition of variable", RetCodes.SEMANTIC_ERR)
        self.program.var_init(self.arguments[0])


class Pops(Instruction):
    """
    Pop value from top of the data stack
    Throws error if data stack is empty
    """
    def eval(self):
        if len(self.program.get_data_stack) == 0:
            Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.var_set(self.arguments[0], self.program.data_stack.pop())


class Jump(Instruction):
    """Jump on the stated label"""
    def eval(self):
        self.program.program_ptr = self.program.get_labels[self.arguments[0].get_value]  # set pointer on jumped label


class Call(Jump):
    """
    Function call
    Save program counter position on call stack for future return
    Throws error if label doesn't exist
    """
    def eval(self):
        if self.arguments[0].get_value not in self.program.get_labels.keys():
            Utils.error("undefined label", RetCodes.SEMANTIC_ERR)
        self.program.call_stack.append(self.program.program_ptr)
        Jump.eval(self)


class Label(Instruction):
    """New label definition"""
    def eval(self):
        return self.arguments[0].get_value


class Pushs(Instruction):
    def eval(self):
        """Push value on top of the data stack"""
        self.program.data_stack.append(self.program.get_value(self.arguments[0]))


class Write(Instruction):
    """Write argument value on stdout"""
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        if const.get_type == "nil":
            print("", end="")
        else:
            print(const.get_value, end="")


class Exit(Instruction):
    """
    Exit program with given return code
    Throws error on not existing error code or unsuitable argument type
    """
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        if const.get_type != "int":
            Utils.error("'EXIT' can be applied only on int type", RetCodes.OPP_TYPE_ERR)
        int_dec = int(const.get_value, 0)
        if int_dec < 0 or int_dec > 49:
            Utils.error("bad exit code", RetCodes.OPP_VALUE_ERR)
        exit(int_dec)


class Dprint(Instruction):
    """Print argument value on stderr"""
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        print(const.get_value, file=stderr)


class Move(Instruction):
    """Set variable with given value"""
    def eval(self):
        self.program.var_set(self.arguments[0], self.program.get_value(self.arguments[1]))


class Int2Char(Instruction):
    """
    Converting integer on suitable ascii character
    Throws error on unsuitable argument type
    """
    def eval(self):
        const = self.program.get_value(self.arguments[1])
        if const.get_type != "int":
            Utils.error("'INT2CHAR' can be applied only on int type", RetCodes.OPP_TYPE_ERR)
        try:
            answer: str = chr(int(const.get_value, 0))
            self.program.var_set(self.arguments[0], Constant("string", answer))
        except ValueError:
            Utils.error("", RetCodes.STRING_ERR)


class Strlen(Instruction):
    """
    Count length of given string
    Throws error on unsuitable argument type
    """
    def eval(self):
        const = self.program.get_value(self.arguments[1])
        if const.get_type != "string":
            Utils.error("'INT2CHAR' can be applied only on string type", RetCodes.OPP_TYPE_ERR)
        self.program.var_set(self.arguments[0], Constant("int", str(len(const.get_value))))


class Type(Instruction):
    """Get type of the given argument"""
    def eval(self):
        const = self.program.get_value(self.arguments[1], True)     # will return None in case of uninitialized variable
        if const is None:
            self.program.var_set(self.arguments[0], Constant("string", ""))
        else:
            self.program.var_set(self.arguments[0], Constant("string", const.get_type))


class Not(Instruction):
    """
    Set boolean value on opposite
    Throws error on unsuitable argument type
    """
    def eval(self):
        const = self.program.get_value(self.arguments[1])
        if const.get_type != "bool":
            Utils.error("'NOT' can be applied only on bool type", RetCodes.OPP_TYPE_ERR)
        answer: str = "true" if const.get_value == "false" else "false"
        self.program.var_set(self.arguments[0], Constant("bool", answer))


class Read(Instruction):
    """Read input"""
    def eval(self):
        type_: str = self.arguments[1].get_value
        if self.program.get_input is stdin:
            read = input().strip()
        else:
            read = self.program.get_input.readline().strip()
        if read == "":
            self.program.var_set(self.arguments[0], Constant("nil", "nil"))
        elif type_ == "bool":
            new_boolean = Constant("bool", "true" if read.lower() == "true" else "false")
            self.program.var_set(self.arguments[0], new_boolean)
        elif type_ == "int":
            try:
                self.program.var_set(self.arguments[0], Constant("int", str(int(read, 0))))
            except ValueError:
                self.program.var_set(self.arguments[0], Constant("nil", "nil"))
        elif type_ == "string":
            self.program.var_set(self.arguments[0], Constant("string", read))


class Add(Instruction):
    """
    Add 2 integer values
    Throws error on unsuitable type
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "int" or const2.get_type != "int":
            Utils.error("'ADD' can be applied only on int types", RetCodes.OPP_TYPE_ERR)
        answer: str = str(int(const1.get_value, 0) + int(const2.get_value, 0))
        self.program.var_set(self.arguments[0], Constant("int", answer))


class Sub(Instruction):
    """
    Subtract 2 integer values
    Throws error on unsuitable type
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "int" or const2.get_type != "int":
            Utils.error("'SUB' can be applied only on int types", RetCodes.OPP_TYPE_ERR)
        answer: str = str(int(const1.get_value, 0) - int(const2.get_value, 0))
        self.program.var_set(self.arguments[0], Constant("int", answer))


class Mul(Instruction):
    """
    Multiply 2 integer values
    Throws error on unsuitable type
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "int" or const2.get_type != "int":
            Utils.error("'MUL' can be applied only on int types", RetCodes.OPP_TYPE_ERR)
        answer: str = str(int(const1.get_value, 0) * int(const2.get_value, 0))
        self.program.var_set(self.arguments[0], Constant("int", answer))


class Idiv(Instruction):
    """
    Integer division of 2 integer values
    Throws error on unsuitable type
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "int" or const2.get_type != "int":
            Utils.error("'IDIV' can be applied only on int types", RetCodes.OPP_TYPE_ERR)
        try:
            answer: str = str(int(const1.get_value, 0) // int(const2.get_value, 0))
            self.program.var_set(self.arguments[0], Constant("int", answer))
        except ZeroDivisionError:
            Utils.error("division by zero", RetCodes.OPP_VALUE_ERR)


class Lt(Instruction):
    """
    Lesser than comparison 2 values
    Return boolean value
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = Utils.compare_consts(const1, const2, operation=lambda x, y: x < y)
        self.program.var_set(self.arguments[0], Constant("bool", str(answer).lower()))


class Gt(Instruction):
    """
    Greater than comparison 2 values
    Return boolean value
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = Utils.compare_consts(const1, const2, operation=lambda x, y: x > y)
        self.program.var_set(self.arguments[0], Constant("bool", str(answer).lower()))


class Eq(Instruction):
    """
    Equal comparison 2 values
    Return boolean value
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = Utils.compare_consts(const1, const2, operation=lambda x, y: x == y, eq=True)
        self.program.var_set(self.arguments[0], Constant("bool", str(answer).lower()))


class And(Instruction):
    """
    Logical operation AND on 2 boolean values
    Throws error on unsuitable argument types
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "bool" or const2.get_type != "bool":
            Utils.error("'AND' can be applied only on bool types", RetCodes.OPP_TYPE_ERR)
        value1: bool = True if const1.get_value == "true" else False
        value2: bool = True if const2.get_value == "true" else False
        answer: str = "true" if value1 and value2 else "false"
        self.program.var_set(self.arguments[0], Constant("bool", answer))


class Or(Instruction):
    """
    Logical operation OR on 2 boolean values
    Throws error on unsuitable argument types
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "bool" or const2.get_type != "bool":
            Utils.error("'AND' can be applied only on bool types", RetCodes.OPP_TYPE_ERR)
        value1: bool = True if const1.get_value == "true" else False
        value2: bool = True if const2.get_value == "true" else False
        answer: str = "true" if value1 or value2 else "false"
        self.program.var_set(self.arguments[0], Constant("bool", answer))


class Stri2Int(Instruction):
    """
    Get character ascii value on given position in string
    Throws error on unsuitable argument types
    """
    def eval(self):
        string = self.program.get_value(self.arguments[1])
        position = self.program.get_value(self.arguments[2])
        if string.get_type != "string" or position.get_type != "int":
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)
        position_int = int(position.get_value, 0)
        try:
            if position_int < 0:
                raise IndexError
            ord_value: str = str(ord(string.get_value[position_int]))
            self.program.var_set(self.arguments[0], Constant("int", ord_value))
        except IndexError:
            Utils.error("index out of range", RetCodes.STRING_ERR)


class Concat(Instruction):
    """
    Concatenate 2 strings
    Throws error on unsuitable argument types
    """
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type != "string" or const2.get_type != "string":
            Utils.error("'CONCAT' can be applied only on string types", RetCodes.OPP_TYPE_ERR)
        self.program.var_set(self.arguments[0], Constant("string", const1.get_value + const2.get_value))


class Setchar(Instruction):
    """
    Change character on given position in string
    Throws error on unsuitable argument types
    """
    def eval(self):
        string = self.program.get_value(self.arguments[0])
        position = self.program.get_value(self.arguments[1])
        change = self.program.get_value(self.arguments[2])
        if string.get_type != "string" or position.get_type != "int" or change.get_type != "string":
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)
        position_int = int(position.get_value, 0)
        try:
            if position_int < 0 or position_int >= len(string.get_value):
                raise IndexError
            new_string = string.get_value[:position_int] + change.get_value[0] + string.get_value[position_int + 1:]
            self.program.var_set(self.arguments[0], Constant("string", new_string))
        except IndexError:
            Utils.error("index out of range", RetCodes.STRING_ERR)


class Getchar(Instruction):
    """
    Get character from given position in string
    Throws error on unsuitable argument types
    """
    def eval(self):
        string = self.program.get_value(self.arguments[1])
        position = self.program.get_value(self.arguments[2])
        if string.get_type != "string" or position.get_type != "int":
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)
        position_int = int(position.get_value, 0)
        try:
            if position_int < 0:
                raise IndexError
            self.program.var_set(self.arguments[0], Constant("string", string.get_value[position_int]))
        except IndexError:
            Utils.error("index out of range", RetCodes.STRING_ERR)


class Jumpifeq(Jump):
    """
    Jump on given label if arguments types and values are equal
    Throws error on different argument types or undefined label
    """
    def eval(self):
        if self.arguments[0].get_value not in self.program.get_labels.keys():
            Utils.error("undefined label", RetCodes.SEMANTIC_ERR)
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type == const2.get_type:
            if const1.get_value == const2.get_value:
                Jump.eval(self)
        elif const1.get_type == "nil" or const2.get_type == "nil":
            Jump.eval(self)
        else:
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)


class Jumpifneq(Jump):
    """
    Jump on given label if arguments types and values are not equal
    Throws error on different argument types or undefined label
    """
    def eval(self):
        if self.arguments[0].get_value not in self.program.get_labels.keys():
            Utils.error("undefined label", RetCodes.SEMANTIC_ERR)
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type == const2.get_type:
            if const1.get_value != const2.get_value:
                Jump.eval(self)
        elif const1.get_type == "nil" or const2.get_type == "nil":
            Jump.eval(self)
        else:
            Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)
