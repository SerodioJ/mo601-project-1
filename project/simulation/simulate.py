import csv
import os

from .exceptions import InvalidInputStimulus, CircuitDidNotStabilized


class Simulation:
    def __init__(self, circuit, stimulus, output_folder, delay=1):
        self.circuit = circuit
        self.stimulus = stimulus
        self.cycle = 0
        self.delay = delay
        self.inputs = self._get_circuit_inputs()
        self.file = open(os.path.join(output_folder, f"saida{delay}.csv"), "w")
        self.csv_writer = csv.writer(self.file, lineterminator="\n")

    def run(self):
        self.csv_writer.writerow(["Tempo"] + sorted(self.circuit.keys()))
        prev_line = None
        while True:
            self._run_cycle()
            line = self._circuit_snapshot()
            self.csv_writer.writerow([self.cycle] + line)
            if prev_line == line: # circuit is stable
                if self.stimulus == {}: # finish simulation
                    break
                else: # print same circuit state until next event (signal change) occurs
                    next_change = sorted(self.stimulus.keys())[0]
                    for stable_cycle in range(self.cycle + 1, next_change):
                        self.csv_writer.writerow([stable_cycle] + line)
                    self.cycle = next_change
                    continue
            self.cycle += 1
            self._update_state()
            prev_line = line
        self.file.close()

    def _run_cycle(self):
        cycle_inputs = (
            self.stimulus.pop(self.cycle) if self.cycle in self.stimulus else {}
        )
        if self.delay == 1:
            self._run_cycle_delay_1(cycle_inputs)
        else:
            self._run_cycle_delay_0(cycle_inputs)

    def _run_cycle_delay_0(self, cycle_inputs):
        for sig_in, sig_val in cycle_inputs.items():
            self.circuit[sig_in].value = sig_val
            self.circuit[sig_in].prev_value = sig_val
        for i in range(10000):
            for _, sig_obj in self.circuit.items():
                sig_obj.update()

            if self._stabilized():
                return
            self._update_state()
        raise CircuitDidNotStabilized()

    def _run_cycle_delay_1(self, cycle_inputs):
        for sig_name, sig_obj in self.circuit.items():
            sig_obj.update(cycle_inputs.get(sig_name))

    def _stabilized(self):
        for _, sig_obj in self.circuit.items():
            if sig_obj.prev_value != sig_obj.value:
                return False
        return True

    def _update_state(self):
        for _, sig_obj in self.circuit.items():
            sig_obj.prev_value = sig_obj.value

    def _circuit_snapshot(self):
        return [self.circuit[signal].value for signal in sorted(self.circuit.keys())]

    def _get_circuit_inputs(self):
        inputs = []
        for signal, sig_data in self.circuit.items():
            if sig_data.parents == []:
                inputs.append(signal)
        stimulus_inputs = set()
        for sig_dict in self.stimulus.values():
            stimulus_inputs.update(sig_dict.keys())
        for sig in stimulus_inputs:
            if sig not in inputs:
                raise InvalidInputStimulus()
        return inputs
