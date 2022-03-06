from program import Program


class Types:
    def __init__(self, value, order: int = -1):
        self.order = order
        self.value = value
        self.program: Program = Program.get_instance()

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

    @property
    def get_type(self):
        return self.type_


class Label(Types):
    def __init__(self, value: str, order: int = -1):
        super().__init__(value, order)


class Type(Types):
    def __init__(self, value: str, order: int = -1):
        super().__init__(value, order)





