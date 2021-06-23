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


def main(molecule, molefrac, velocity, temperature, density, nco):
    with open("model_params.bat", "w") as f1:
        for x in nco:
            for v in velocity:
                for mf in molefrac:
                    # ./new_script.bat 500  4 0.0 CO
                    f1.write(
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

    if temperature is not None or density is not None:
        with open("trho.dat", "w") as f2:
            if temperature is not None:
                temperature = temperature.split(",")
                temperature = np.linspace(int(temperature[1]), int(temperature[0]), 8)
            else:
                temperature = np.linspace(5000.0, 1500.0, 8)
            for x in temperature:
                f2.write(str(float(x)) + " ")
            f2.write("\n")

            if density is not None:
                density = density.split(",")
                density = np.linspace(int(density[0]), int(density[1]), 4)
            else:
                density = [7, 8, 9, 11]
            for x in density:
                f2.write("1.E+" + str(int(x)) + " ")
            f2.write("\n")

    os.system("sh model_params.bat")
    return


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
        help="molecular fraction of excited state to neutral, e.g. 0.1",
    )
    parser.add_argument(
        "-v",
        "--velocity",
        dest="velocity",
        default="4000",
        help="velocity or velocities, separated by commas, must be integers",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        dest="temperature",
        default=None,
        help="temperature grid in format <lower limit>, <upper limit>, e.g. 1000,5000",
    )
    parser.add_argument(
        "-d",
        "--density",
        dest="density",
        default=None,
        help="density grid in format <lower limit>, <upper limit>, e.g. 7,11",
    )
    parser.add_argument(
        "-nco",
        "--nco",
        dest="nco",
        default=4,
        help="""1: CO molecules are included,
        2: CO and SiO molecules are included,
        3: CO, CO+, and SiO molecules are included,
        4: CO+ is determinded by E- + CO+ <=> CO,
        5: CO+/CO ratio is given as input""",
    )
    args = parser.parse_args()

    molefrac = parseInputs(args.molefrac)
    velocity = parseInputs(args.velocity)
    nco = parseInputs(args.nco)

    if args.molecule != "CO" and args.molecule != "SiO":
        print("Not a valid molecular selection.")
    else:
        main(args.molecule, molefrac, velocity, args.temperature, args.density, nco)
