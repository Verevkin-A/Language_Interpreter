class Types:
    def __init__(self, order, value):
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
    def __init__(self, order: int, value: str):
        self._frame, value = value.split("@")
        super().__init__(order, value)


class Constant(Types):
    def __init__(self, order: int, type_: str, value: str):
        super().__init__(order, value)
        self._type = type_


class Label(Types):
    def __init__(self, order: int, value: str):
        super().__init__(order, value)


class Type(Types):
    def __init__(self, order: int, value: str):
        super().__init__(order, value)





