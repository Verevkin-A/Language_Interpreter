"""Interpret available instructions"""
from typing import List
from abc import ABC, abstractmethod
from sys import stderr

import types_
import program
import utils
from ret_codes import RetCodes


class InstInterface(ABC):
    """Instructions interface"""
    @abstractmethod
    def eval(self):
        """Evaluate instruction"""
        pass


class Instruction:
    def __init__(self, arguments: List, name: str):
        self.name = name
        self.arguments: List = arguments

        self.program: program.Program = program.Program.get_instance()


class Createframe(Instruction):
    def eval(self):
        self.program.tmp_frame = {}


class Pushframe(Instruction):
    def eval(self):
        if self.program.get_tmp_frame is None:
            utils.Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.local_frame.append(self.program.get_tmp_frame)
        self.program.tmp_frame = None


class Popframe(Instruction):
    def eval(self):
        if len(self.program.get_local_frame) == 0:
            utils.Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.tmp_frame = self.program.local_frame.pop()


class Return(Instruction):
    def eval(self):
        if len(self.program.get_call_stack) == 0:
            utils.Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.program_ptr = self.program.call_stack.pop()


class Break(Instruction):
    def eval(self):
        print(self.program.get_stats(), file=stderr)


class Defvar(Instruction):
    def eval(self):
        if self.program.is_exist(self.arguments[0]):
            utils.Utils.error("redefinition of variable", RetCodes.SEMANTIC_ERR)
        self.program.var_init(self.arguments[0])


class Pops(Instruction):
    def eval(self):
        if len(self.program.get_data_stack) == 0:
            utils.Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.var_set(self.arguments[0], self.program.data_stack.pop())


class Jump(Instruction):
    def eval(self):
        if self.arguments[0].value not in self.program.get_labels.keys():
            utils.Utils.error("undefined label", RetCodes.SEMANTIC_ERR)
        self.program.program_ptr(self.program.get_labels[self.arguments[0].value])  # set pointer on jumped label


class Call(Jump):
    def eval(self):
        self.program.call_stack.append(self.program.program_ptr)
        Jump.eval(self)


class Label(Instruction):
    def eval(self):
        return self.arguments[0].get_value


class Pushs(Instruction):
    def eval(self):
        self.program.data_stack.append(self.program.get_value(self.arguments[0]))


class Write(Instruction):
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        if const.get_type == "nil":
            print("", end="")
        else:
            print(const.value)


class Exit(Instruction):
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        if const.get_type != "int":
            utils.Utils.error("", RetCodes.OPP_TYPE_ERR)
        int_dec = int(const.value, 0)
        if int_dec < 0 or int_dec > 49:
            utils.Utils.error("bad exit code", RetCodes.OPP_VALUE_ERR)
        exit(int_dec)


class Dprint(Instruction):
    def eval(self):
        const = self.program.get_value(self.arguments[0])
        print(const.value, file=stderr)


class Move(Instruction):
    def eval(self):
        self.program.var_set(self.arguments[0], self.program.get_value(self.arguments[1]))


class Int2char(Instruction):
    def eval(self):
        pass


class Strlen(Instruction):
    def eval(self):
        pass


class Type(Instruction):
    def eval(self):
        pass


class Not(Instruction):
    def eval(self):
        pass


class Read(Instruction):
    def eval(self):
        pass


class Add(Instruction):
    def eval(self):
        pass


class Sub(Instruction):
    def eval(self):
        pass


class Mul(Instruction):
    def eval(self):
        pass


class Idiv(Instruction):
    def eval(self):
        pass


class Lt(Instruction):
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = utils.Utils.compare_consts(const1, const2, operation=lambda x, y: x < y)
        self.program.var_set(self.arguments[0], types_.Constant("bool", str(answer).lower()))


class Gt(Instruction):
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = utils.Utils.compare_consts(const1, const2, operation=lambda x, y: x > y)
        self.program.var_set(self.arguments[0], types_.Constant("bool", str(answer).lower()))


class Eq(Instruction):
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        answer: bool = utils.Utils.compare_consts(const1, const2, operation=lambda x, y: x == y)
        self.program.var_set(self.arguments[0], types_.Constant("bool", str(answer).lower()))


class And(Instruction):
    def eval(self):
        pass


class Or(Instruction):
    def eval(self):
        pass


class Stri2int(Instruction):
    def eval(self):
        pass


class Concat(Instruction):
    def eval(self):
        pass


class Setchar(Instruction):
    def eval(self):
        pass


class Getchar(Instruction):
    def eval(self):
        pass


class Jumpifeq(Jump):
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type == const2.get_type:
            if const1.get_value == const2.get_value:
                Jump.eval(self)
        elif const1.get_type == "nil" or const2.get_type == "nil":
            Jump.eval(self)
        else:
            utils.Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)


class Jumpifneq(Jump):
    def eval(self):
        const1 = self.program.get_value(self.arguments[1])
        const2 = self.program.get_value(self.arguments[2])
        if const1.get_type == const2.get_type:
            if const1.get_value != const2.get_value:
                Jump.eval(self)
        elif const1.get_type == "nil" or const2.get_type == "nil":
            Jump.eval(self)
        else:
            utils.Utils.error("bad operand type", RetCodes.OPP_TYPE_ERR)

