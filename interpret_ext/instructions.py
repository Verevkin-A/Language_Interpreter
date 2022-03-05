"""Interpret available instructions"""
from typing import List
from abc import ABC, abstractmethod


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


class Createframe(Instruction):
    def eval(self):
        pass


class Pushframe(Instruction):
    def eval(self):
        pass


class Popframe(Instruction):
    def eval(self):
        pass


class Return(Instruction):
    def eval(self):
        pass


class Break(Instruction):
    def eval(self):
        pass


class Defvar(Instruction):
    def eval(self):
        pass


class Pops(Instruction):
    def eval(self):
        pass


class Call(Instruction):
    def eval(self):
        pass


class Lable(Instruction):
    def eval(self):
        pass


class Jump(Instruction):
    def eval(self):
        pass


class Pushs(Instruction):
    def eval(self):
        pass


class Write(Instruction):
    def eval(self):
        pass


class Exit(Instruction):
    def eval(self):
        pass


class Dprint(Instruction):
    def eval(self):
        pass


class Move(Instruction):
    def eval(self):
        pass


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

