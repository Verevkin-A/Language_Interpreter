"""Main program information"""

from typing import List, Dict, Union
from utils import Utils
from ret_codes import RetCodes
import instructions
import types_


class Program:
    """Contains code info

    Program class use Singleton pattern,
    so all program instances between all modules
    are the same
    """
    __instance = None

    @staticmethod
    def get_instance():
        if Program.__instance is None:
            Program()
        return Program.__instance

    def __init__(self):
        if Program.__instance is None:
            self.global_frame: Dict = {}
            self.local_frame: List = []
            self.tmp_frame: Union[Dict, None] = None
            self.data_stack: List[types_.Types] = []
            self.call_stack: List[int] = []

            self._bare_instructions: List = []
            self._labels: Dict = {}
            self._program_ptr = 0

            Program.__instance = self

    def process_instructions(self, insts):
        for inst in insts:
            if isinstance(inst, instructions.Label):
                self._labels[inst.eval()] = len(self._bare_instructions)
            else:
                self._bare_instructions.append(inst)

    def eval_program(self):
        while True:
            instruction = self._bare_instructions[self._program_ptr]
            instruction.eval()
            self._program_ptr += 1
            if self._program_ptr > len(self._bare_instructions) - 1:
                break

    def is_exist(self, var):
        if var.frame == "GF":
            return var.value in self.get_global_frame
        elif var.frame == "LF":
            if len(self.get_local_frame) == 0:
                Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
            return var.value in self.get_local_frame[-1]
        elif var.frame == "TF":
            if self.get_tmp_frame is None:
                Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
            return var.value in self.get_tmp_frame


    def var_init(self, var):
        if var.frame == "GF":
            self.global_frame[var.value] = None
        elif var.frame == "LF":
            self.local_frame[-1][var.value] = None
        elif var.frame == "TF":
            self.tmp_frame[var.value] = None

    def var_set(self, var, value):
        if not self.is_exist(var):
            Utils.error("undefined variable", RetCodes.VAR_NOT_EXIST_ERR)
        if var.frame == "GF":
            self.global_frame[var.value] = value
        elif var.frame == "LF":
            self.local_frame[-1][var.value] = value
        elif var.frame == "TF":
            self.tmp_frame[var.value] = value

    def get_value(self, var: Union[types_.Variable, types_.Constant]):
        if isinstance(var, types_.Constant):
            return var
        else:
            if not self.is_exist(var):
                Utils.error("undefined variable", RetCodes.VAR_NOT_EXIST_ERR)
            var_value = None
            if var.frame == "GF":
                var_value = self.get_global_frame[var.value]
            elif var.frame == "LF":
                var_value = self.get_local_frame[-1][var.value]
            elif var.frame == "TF":
                var_value = self.get_tmp_frame[var.value]
            if var_value is None:
                Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
            return var_value

    @property
    def get_labels(self):
        return self._labels

    @property
    def get_global_frame(self):
        return self.global_frame

    @property
    def get_local_frame(self):
        return self.local_frame

    @property
    def get_tmp_frame(self):
        return self.tmp_frame

    @property
    def get_data_stack(self):
        return self.data_stack

    @property
    def get_call_stack(self):
        return self.call_stack

    @property
    def program_ptr(self):
        return self._program_ptr

    @program_ptr.setter
    def program_ptr(self, value):
        self._program_ptr = value
