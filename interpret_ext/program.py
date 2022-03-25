"""Main program information"""

from typing import List, Dict, Union, TextIO

from interpret_ext.utils import Utils
from interpret_ext.ret_codes import RetCodes
import interpret_ext.instructions as instructions
import interpret_ext.types_ as types


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
            Program(None)
        return Program.__instance

    def __init__(self, input_):
        if Program.__instance is None:
            self._input: TextIO = input_
            self.global_frame: Dict = {}
            self.local_frame: List = []
            self.tmp_frame: Union[Dict, None] = None
            self.data_stack: List[types.Types] = []
            self.call_stack: List[int] = []

            self._bare_instructions: List = []
            self._labels: Dict = {}
            self._program_ptr = 0

            Program.__instance = self

    def process_instructions(self, insts: List):
        for inst in insts:
            if isinstance(inst, instructions.Label):
                if self._labels.get(inst.eval()) is None:
                    self._labels[inst.eval()] = len(self._bare_instructions) - 1
                else:
                    Utils.error(f"label already exist ({inst.eval()})", RetCodes.SEMANTIC_ERR)
            else:
                self._bare_instructions.append(inst)

    def eval_program(self):
        # check if file without instructions
        if len(self._bare_instructions) == 0:
            return
        # loop through the instructions
        while True:
            instruction = self._bare_instructions[self._program_ptr]
            instruction.eval()
            self._program_ptr += 1
            if self._program_ptr > len(self._bare_instructions) - 1:
                break

    def is_exist(self, var):
        if var.get_frame == "GF":
            return var.value in self.get_global_frame
        elif var.get_frame == "LF":
            if len(self.get_local_frame) == 0:
                Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
            return var.value in self.get_local_frame[-1]
        elif var.get_frame == "TF":
            if self.get_tmp_frame is None:
                Utils.error("accessing not existing frame", RetCodes.FRAME_NOT_EXIST_ERR)
            return var.value in self.get_tmp_frame

    def var_init(self, var):
        if var.get_frame == "GF":
            self.global_frame[var.value] = None
        elif var.get_frame == "LF":
            self.local_frame[-1][var.value] = None
        elif var.get_frame == "TF":
            self.tmp_frame[var.value] = None

    def var_set(self, var, value):
        if not self.is_exist(var):
            Utils.error("undefined variable", RetCodes.VAR_NOT_EXIST_ERR)
        if var.get_frame == "GF":
            self.global_frame[var.value] = value
        elif var.get_frame == "LF":
            self.local_frame[-1][var.value] = value
        elif var.get_frame == "TF":
            self.tmp_frame[var.value] = value

    def get_value(self, var, type_=False):
        if isinstance(var, types.Constant):
            return var
        else:
            if not self.is_exist(var):
                Utils.error("undefined variable", RetCodes.VAR_NOT_EXIST_ERR)
            var_value = None
            if var.get_frame == "GF":
                var_value = self.get_global_frame[var.value]
            elif var.get_frame == "LF":
                var_value = self.get_local_frame[-1][var.value]
            elif var.get_frame == "TF":
                var_value = self.get_tmp_frame[var.value]
            if var_value is None and type_ is False:
                Utils.error("missing value", RetCodes.VALUE_NOT_EXIST_ERR)
            return var_value

    def get_stats(self):
        return f"Global frame: {self.get_global_frame}" \
               f"Local frame: {self.get_local_frame}" \
               f"Temporary frame: {self.get_tmp_frame}" \
               f"Data stack: {self.get_data_stack}" \
               f"Call stack: {self.get_call_stack}" \
               f"Labels: {self.get_labels}" \
               f"Program pointer: {self.program_ptr}"

    @property
    def get_input(self):
        return self._input

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
