"""Parsing instructions and their arguments from XML"""

import xml.etree.ElementTree as ET
from typing import TextIO, Dict, List, Tuple
from re import match

from ret_codes import RetCodes
from utils import Utils


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
        self.sort_xml()

    def sort_xml(self) -> None:
        """Sort XML source file into dictionary with instructions"""
        instructions_data: Dict[int, List] = {}
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

            try:
                instructions_data[inst_order]
            except KeyError:
                arguments: List = self.sort_arguments(inst)
                instructions_data[inst_order] = arguments
            else:
                Utils.error(f"instruction order key already exist ({inst_order})", RetCodes.XML_STRUCT_ERR)

        instructions_data = dict(sorted(instructions_data.items()))     # sort instructions by their order
        print(instructions_data)

    def check_header(self) -> None:
        """Check program header for correct name and attributes"""
        if self._xml_root.tag != "program":
            Utils.error(f"invalid root name ({self._xml_root.tag})", RetCodes.XML_STRUCT_ERR)
        if "language" not in self._xml_root.attrib.keys():
            Utils.error("root language attribute not stated", RetCodes.XML_STRUCT_ERR)
        if self._xml_root.attrib["language"].lower() != "ippcode22":
            Utils.error(f"only IPPcode22 language in root supported (given: {self._xml_root.attrib['language']})",
                        RetCodes.XML_STRUCT_ERR)
        for attr in self._xml_root.attrib.keys():
            if attr not in self._ROOT_ATTRIBUTES:
                Utils.error(f"unsupported root attribute ({attr})", RetCodes.XML_STRUCT_ERR)

    @staticmethod
    def sort_arguments(inst: ET.Element) -> list:
        """Getting arguments from XML instruction

        :param inst: instruction
        :return: list with arguments as tuples
        """
        instruction_args: List[Tuple] = []
        for arg in inst:
            if match(r"^(arg[123])$", arg.tag):
                # check if type attribute was given
                if len(arg.attrib) != 1 or arg.attrib.get("type") is None:
                    Utils.error("bad argument attributes", RetCodes.XML_STRUCT_ERR)
                arg_order = int(arg.tag[-1])
                # check if type attribute was given more than once
                if arg_order in [argument[0] for argument in instruction_args]:
                    Utils.error("repeating argument order", RetCodes.XML_STRUCT_ERR)
                else:
                    instruction_args.append(tuple([arg_order, arg.attrib["type"], arg.text]))
            else:
                Utils.error("unknown argument name", RetCodes.XML_STRUCT_ERR)
        instruction_args = sorted(instruction_args, key=lambda x: x[0])
        # check if arguments aren't missing
        if (len(instruction_args) == 2 and instruction_args[1][0] != 2) or \
                (len(instruction_args) == 1 and instruction_args[0][0] != 1):
            Utils.error("missing arguments", RetCodes.XML_STRUCT_ERR)
        return instruction_args
