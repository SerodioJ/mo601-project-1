from simulation.signal import Signal
from .exceptions import (
    InvalidCircuitFormat,
    InvalidGate,
    InvalidSignalName,
    DoubleAssignment,
)


class CircuitParser:
    def __init__(self, filename):
        self.signals = {}
        self.filename = filename
        return

    def parse(self):
        with open(self.filename, "r") as f:
            for line in f:
                self._parse_line(line)
        return self.signals

    def _parse_line(self, line):
        content = line.split()
        is_not = False
        if len(content) == 4 and self._check_gate(content[2]) == 4:  # NOT gate
            indices = [0, 3]
        elif len(content) == 5 and self._check_gate(content[2]) == 5:  # other gates
            indices = [0, 3, 4]
        else:
            raise InvalidCircuitFormat
        for index in indices:
            self._check_signal(content[index])
        sig_out = self._register_signal(content[indices.pop(0)], gate=content[2])

        for index in indices:
            sig_in = self._register_signal(content[index], child=sig_out)

    def _register_signal(self, signal_name, gate=None, child=None):
        if signal_name in self.signals:
            signal = self.signals.get(signal_name)
            if (
                signal.gate != None and gate != None
            ):  # case where signal is being assigned a second time
                raise DoubleAssignment(signal_name)
            else:
                signal.gate = signal.gate or gate
        else:
            signal = Signal(signal_name, gate=gate)
            self.signals[signal_name] = signal

        if child:
            signal.children.append(child)
            child.parents.append(signal)

        return signal

    @staticmethod
    def _check_gate(gate):
        if gate in ["AND", "OR", "NAND", "NOR", "XOR"]:
            return 5
        elif gate == "NOT":
            return 4
        raise InvalidGate(gate)

    @staticmethod
    def _check_signal(signal):
        if len(signal) == 1 and signal.isupper():
            return
        raise InvalidSignalName(signal)
