"""Interpret available instructions"""
from typing import List
from abc import ABC, abstractmethod

from types_ import *
from program import Program
from utils import Utils
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

        self.program: Program = Program.get_instance()


class Createframe(Instruction):
    def eval(self):
        self.program.tmp_frame = {}


class Pushframe(Instruction):
    def eval(self):
        if self.program.get_tmp_frame is None:
            Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.local_frame.append(self.program.get_tmp_frame)
        self.program.tmp_frame = None


class Popframe(Instruction):
    def eval(self):
        if len(self.program.get_local_frame) == 0:
            Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
        self.program.tmp_frame = self.program.local_frame.pop()


class Return(Instruction):
    def eval(self):
        if len(self.program.get_call_stack) == 0:
            Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.program_ptr = self.program.call_stack.pop()


class Break(Instruction):
    def eval(self):
        pass


class Defvar(Instruction):
    def eval(self):
        if self.program.is_exist(self.arguments[0]):
            Utils.error("redefinition of variable", RetCodes.SEMANTIC_ERR)
        self.program.var_init(self.arguments[0])


class Pops(Instruction):
    def eval(self):
        if len(self.program.get_data_stack) == 0:
            Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
        self.program.var_set(self.arguments[0], self.program.data_stack.pop())


class Jump(Instruction):
    def eval(self):
        if self.arguments[0].value not in self.program.get_labels.keys():
            Utils.error("undefined label", RetCodes.SEMANTIC_ERR)
        self.program.program_ptr(self.program.get_labels[self.arguments[0].value])  # set program pointer on jumped label


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
        if const.type_ == "nil":
            print("", end="")
        else:
            print(const.value)


class Exit(Instruction):
    def eval(self):
        const = self.program.get_value(self.arguments[0])   # TODO
        # if const.type_ != "int":
        #     Utils.error("", RetCodes.OPP_TYPE_ERR)
        # elif int(const.value) < 0 or int(const.value) > 49:
        #     Utils.error("bad exit code", RetCodes.OPP_VALUE_ERR)
        # else:
        #     exit(int(const.value))


class Dprint(Instruction):
    def eval(self):
        pass


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
        pass


class Gt(Instruction):
    def eval(self):
        pass


class Eq(Instruction):
    def eval(self):
        pass


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


class Jumpifeq(Instruction):
    def eval(self):
        pass


class Jumpifneq(Instruction):
    def eval(self):
        pass

