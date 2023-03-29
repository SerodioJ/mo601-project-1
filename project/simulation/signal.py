class Signal:
    def __init__(self, name, gate=None):
        self.name = name
        self.gate = gate
        self.parents = []
        self.children = []
        self.value = 0
        self.prev_value = None

    def __repr__(self):
        children = [sig.name for sig in self.children]
        parents = [sig.name for sig in self.parents]
        return f"Signal(name={self.name}, gate={self.gate}, parents={parents}, children={children}, value={self.value}, prev_value={self.prev_value})"

    def update(self, value=None):
        if value is not None:
            self.value = value
            return
        if (
            self.gate == None
            or self.parents[0].prev_value == None
            or (len(self.parents) == 2 and self.parents[1].prev_value == None)
        ):
            return

        operation = {
            "AND": self._AND,
            "OR": self._OR,
            "NOT": self._NOT,
            "NAND": self._NAND,
            "NOR": self._NOR,
            "XOR": self._XOR,
        }
        self.value = 1 if operation[self.gate]() else 0

    def _AND(self):
        return self.parents[0].prev_value and self.parents[1].prev_value

    def _OR(self):
        return self.parents[0].prev_value or self.parents[1].prev_value

    def _NOT(self):
        return not self.parents[0].prev_value

    def _NAND(self):
        return not self._AND()

    def _NOR(self):
        return not self._OR()

    def _XOR(self):
        return self.parents[0].prev_value ^ self.parents[1].prev_value
