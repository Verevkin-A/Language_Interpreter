import re


class Types:
    def __init__(self, value, order: int = -1):
        self.order = order
        self.value = value

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order

    def __gt__(self, other):
        return self.order > other.order

    @property
    def get_order(self):
        return self.order

    @property
    def get_value(self):
        return self.value


class Variable(Types):
    def __init__(self, value: str, order: int = -1):
        self._frame, value = value.split("@")
        super().__init__(value, order)

    @property
    def get_frame(self):
        return self._frame


class Constant(Types):
    def __init__(self, type_: str, value: str, order: int = -1):
        super().__init__(value, order)
        self.type_ = type_
        if self.type_ == "string":
            pattern = re.compile(r'(\\[0-9]{3})', re.UNICODE)
            self.value = re.sub(pattern, lambda x: chr(int(x.group()[1:])), self.value)

    @property
    def get_type(self):
        return self.type_


class Label(Types):
    def __init__(self, value: str, order: int = -1):
        super().__init__(value, order)


class Type(Types):
    def __init__(self, value: str, order: int = -1):
        super().__init__(value, order)





