import argparse
import filecmp
from copy import deepcopy
from glob import glob
from pathlib import Path
from tqdm import tqdm

from parsing import CircuitParser, StimulusParser
from simulation.simulate import Simulation


def run_simulations(args):
    folders = args.folders
    if args.folders == None:
        folders = glob("../test/*")

    for folder in tqdm(folders):
        circuit = CircuitParser(f"{folder}/circuito.hdl").parse()
        stimulus = StimulusParser(f"{folder}/estimulos.txt").parse()

        simulation_0 = Simulation(
            deepcopy(circuit), deepcopy(stimulus), folder, delay=0
        )
        simulation_1 = Simulation(circuit, stimulus, folder, delay=1)
        simulation_0.run()
        simulation_1.run()

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--folders",
        help="path to test folder to use, if not set will run with all folders at ../test/",
        type=Path,
        nargs="+",
    )

    args = parser.parse_args()
    run_simulations(args)
