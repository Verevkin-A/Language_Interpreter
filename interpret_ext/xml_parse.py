"""Parsing instructions and their arguments from XML"""

import xml.etree.ElementTree as ET
from typing import TextIO, Dict, List
from re import match

from interpret_ext.ret_codes import RetCodes
from interpret_ext.utils import Utils
from interpret_ext.instructions import *
import interpret_ext.types_


class XMLParse:
    """XML parsing
    
    # TODO
    """
    _ROOT_ATTRIBUTES: List = ["language", "name", "description"]

    def __init__(self, xml_source: TextIO):
        """XML parser constructor
        
        Create XML element tree instance,
        check if xml is valid
        """
        try:
            self._xml_tree: ET.ElementTree = ET.parse(xml_source)
        except ET.ParseError:
            Utils.error("bad xml format", RetCodes.XML_FORMAT_ERR)
        self._xml_root = self._xml_tree.getroot()

        self.check_header()
        self._instructions = self.sort_xml()

    def sort_xml(self) -> List:
        """Sort XML source file into dictionary with instructions"""
        instructions_data: Dict[int, Instruction] = {}
        for inst in self._xml_root:
            if inst.tag != "instruction":
                Utils.error(f"unknown element ({inst.tag})", RetCodes.XML_STRUCT_ERR)
            inst_attributes = inst.attrib.keys()
            if "order" not in inst_attributes or "opcode" not in inst_attributes or len(inst_attributes) != 2:
                Utils.error("bad instruction attributes", RetCodes.XML_STRUCT_ERR)

            try:
                inst_order: int = int(inst.attrib["order"])
                if inst_order <= 0:
                    raise ValueError
            except ValueError:
                Utils.error(f"order must be positive integer (given: {inst.attrib['order']})", RetCodes.XML_STRUCT_ERR)

            arguments: List = self.sort_arguments(inst)
            instr_cls: str = inst.attrib["opcode"].title()
            try:
                instruction = eval(instr_cls)(arguments)
            except NameError:
                Utils.error(f"unknown opcode (inst.attrib['opcode'])", RetCodes.XML_STRUCT_ERR)
            if instructions_data.get(inst_order) is None:
                instructions_data[inst_order] = instruction
            else:
                Utils.error(f"instruction order key already exist ({inst_order})", RetCodes.XML_STRUCT_ERR)

        sorted_instructions = dict(sorted(instructions_data.items()))     # sort instructions by their order
        return [value for value in sorted_instructions.values()]  # return only instructions

    def check_header(self) -> None:
        """Check program header for correct name and attributes"""
        if self._xml_root.tag != "program":
            Utils.error(f"invalid root name ({self._xml_root.tag})", RetCodes.XML_STRUCT_ERR)
        try:
            if self._xml_root.attrib["language"].lower() != "ippcode22":
                Utils.error(f"only IPPcode22 language in root supported (given: {self._xml_root.attrib['language']})",
                            RetCodes.XML_STRUCT_ERR)
            for attr in self._xml_root.attrib.keys():
                if attr not in self._ROOT_ATTRIBUTES:
                    Utils.error(f"unsupported root attribute ({attr})", RetCodes.XML_STRUCT_ERR)
        except KeyError:
            Utils.error("root language attribute not stated", RetCodes.XML_STRUCT_ERR)

    def sort_arguments(self, inst: ET.Element) -> list:
        """Getting arguments from XML instruction

        :param inst: instruction
        :return: list with arguments
        """
        instruction_args: List = [Types]
        for arg in inst:
            if not match(r"^(arg[123])$", arg.tag):
                Utils.error("unknown argument name", RetCodes.XML_STRUCT_ERR)
            else:
                # check if type attribute was given
                if len(arg.attrib) != 1 or arg.attrib.get("type") is None:
                    Utils.error("bad argument attributes", RetCodes.XML_STRUCT_ERR)
                arg_order = int(arg.tag[-1])
                # check if type attribute was given more than once
                if arg_order in [argument.get_order for argument in instruction_args]:
                    Utils.error("repeating argument order", RetCodes.XML_STRUCT_ERR)
                else:
                    instruction_args.append(self.assign_type(arg_order, arg.attrib["type"], arg.text))

        instruction_args = sorted(instruction_args[1:])
        # check if arguments aren't missing
        if (len(instruction_args) == 2 and instruction_args[1].get_order != 2) or \
                (len(instruction_args) == 1 and instruction_args[0].get_order != 1):
            Utils.error("missing arguments", RetCodes.XML_STRUCT_ERR)
        return instruction_args

    @staticmethod
    def assign_type(order: int, type_: str, value: str) -> Types:
        if type_ == "int" or type_ == "bool" or type_ == "string":
            return interpret_ext.types_.Constant(type_, value, order=order)
        elif type_ == "var":
            return interpret_ext.types_.Variable(value, order=order)
        elif type_ == "label":
            return interpret_ext.types_.Label(value, order=order)
        elif type_ == "type":
            return interpret_ext.types_.Type(value, order=order)

    @property
    def get_instructions(self):
        """Instructions getter method"""
        return self._instructions
