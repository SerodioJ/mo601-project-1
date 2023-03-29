class InvalidCircuitFormat(Exception):
    def __init__(self, line):
        super().__init__(
            f'Signal shoud be SIG1 = GATE SIG2 SIG3 or SIG1 = NOT SIG2, but instead got "{line}"'
        )


class InvalidGate(ValueError):
    def __init__(self, gate):
        super().__init__(
            f"Gate should be AND, OR, NOR, NAND, XOR or NOT, but got {gate}"
        )


class InvalidSignalName(ValueError):
    def __init__(self, signal):
        super().__init__(f"Signal name should be A-Z, but instead got {signal}")


class InvalidSignalInput(ValueError):
    def __init__(self, sig_input):
        super().__init__(f"Signal input should be 0 or 1, but instead got {sig_input}")


class InvalidAssignment(Exception):
    def __init__(self, left, right):
        super().__init__(
            f"Two sides of an input assignment must have the same size, but instead got size {len(left)} = size {len(right)}"
        )


class DoubleAssignment(Exception):
    def __init__(self, signal):
        super().__init__(f"Signal {signal} was defined more than once")
