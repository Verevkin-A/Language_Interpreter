"""Input program types"""

import re


class Types:
    """General types class

    Inherited by all existing arguments types
    Provide methods for easier sorting and getters
    """
    def __init__(self, value: str, order: int = -1):
        """
        Types constructor

        :param value: argument value
        :param order: argument position
        """
        self.order = order
        self.value = value

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order

    def __gt__(self, other):
        return self.order > other.order

    @property
    def get_order(self) -> int:
        """Argument order getter"""
        return self.order

    @property
    def get_value(self) -> str:
        """Argument value getter"""
        return self.value


class Variable(Types):
    """Variable argument"""
    def __init__(self, value: str, order: int = -1):
        """
        Variable type constructor

        :param value: variable name
        :param order: variable order in instruction
        """
        self._frame, value = value.split("@")
        super().__init__(value, order)

    @property
    def get_frame(self) -> str:
        """Variable frame getter"""
        return self._frame


class Constant(Types):
    """Constant argument"""
    def __init__(self, type_: str, value: str, order: int = -1):
        """
        Constant type constructor

        :param type_: constant type
        :param value: constant value
        :param order: constant order in instruction arguments
        """
        # check if string is empty
        if value is None and type_ == "string":
            value = ""
        super().__init__(value, order)
        self.type_ = type_

        # if constant a string, check for escape sequences
        if self.type_ == "string":
            pattern = re.compile(r'(\\[0-9]{3})', re.UNICODE)
            self.value = re.sub(pattern, lambda x: chr(int(x.group()[1:])), self.value)

    @property
    def get_type(self) -> str:
        """Constant type getter"""
        return self.type_


class Label(Types):
    """Label argument"""
    def __init__(self, value: str, order: int = -1):
        """
        Label type constructor

        :param value: label name
        :param order: label order in instruction
        """
        super().__init__(value, order)


class Type(Types):
    """Type argument"""
    def __init__(self, value: str, order: int = -1):
        """
        'Type' type constructor

        :param value: type name
        :param order: type order in instruction
        """
        super().__init__(value, order)
