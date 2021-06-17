import glob, os
import numpy as np
import argparse

# TO DO: add newly generated models to model_csv


def parseInputs(inputString):
    parsedVal = []
    if len(inputString.split(",")) > 1:
        parsedVal = inputString.split(",")
    else:
        parsedVal.append(inputString)
    return parsedVal


def main(molecule, molefrac, velocity, n):
    with open("model_params.bat", "w") as f:
        for x in n:
            for v in velocity:
                for mf in molefrac:
                    # ./new_script.bat 500  4 0.0 CO
                    f.write(
                        "./new_script.bat "
                        + v
                        + " "
                        + x
                        + " "
                        + mf
                        + " "
                        + molecule
                        + "\n"
                    )

    os.system("sh model_params.bat")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--molecule",
        dest="molecule",
        default="CO",
        help="molecule to calculate, CO or SiO",
    )
    parser.add_argument(
        "-mf",
        "--molefrac",
        dest="molefrac",
        default="0.0",
        help="molecular fraction of excited state to neutral, e.g. CO+/CO",
    )
    parser.add_argument(
        "-v",
        "--velocity",
        dest="velocity",
        default="4000",
        help="velocity or velocities, separated by commas",
    )
    parser.add_argument(
        "-n",
        "--density",
        dest="n",
        default="4",
        help="density slope or slopes, separated by commas",
    )
    args = parser.parse_args()

    molefrac = parseInputs(args.molefrac)
    velocity = parseInputs(args.velocity)
    n = parseInputs(args.n)

    if args.molecule != "CO" and args.molecule != "SiO":
        print("Not a valid molecular selection.")
    else:
        main(args.molecule, molefrac, velocity, n)
