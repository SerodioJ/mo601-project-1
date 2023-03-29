from .exceptions import InvalidSignalName, InvalidSignalInput, InvalidAssignment


class StimulusParser:
    def __init__(self, filename):
        self.circuit_inputs = {}
        self.filename = filename
        self.cycle = 0
        return

    def parse(self):
        with open(self.filename, "r") as f:
            for line in f:
                self._parse_line(line)
        return self.circuit_inputs

    def _parse_line(self, line):
        if line[0] == "+":
            self._parse_offset(line)
        else:
            self._parse_input(line)

    def _parse_offset(self, line):
        offset = int(line[1:])
        self.cycle += offset

    def _parse_input(self, line):
        right, _, left = line.split()
        if len(right) != len(left):
            raise InvalidAssignment(left, right)
        if self.cycle not in self.circuit_inputs:
            self.circuit_inputs[self.cycle] = {}
        for signal, sig_input in zip(right, left):
            self._check_signal(signal)
            self._check_input(sig_input)
            self.circuit_inputs[self.cycle][signal] = int(sig_input)

    @staticmethod
    def _check_signal(signal):
        if len(signal) == 1 and signal.isupper():
            return
        raise InvalidSignalName(signal)

    @staticmethod
    def _check_input(sig_input):
        if sig_input in ["0", "1"]:
            return
        raise InvalidSignalInput(sig_input)
