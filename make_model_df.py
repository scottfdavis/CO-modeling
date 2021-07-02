import numpy as np
import pandas as pd
import os, glob

# can't have it only add new models when not given a specific set of files
# because the T/density grid can be changed and there's no way to know without
# opening the file to see what the grid is

CODIR = os.environ["CODIR"]
path_CO = CODIR + "/CO/"
path_save = CODIR + "/models_csv/"

def create_df(molecule, files):
    # create a dataframe for all the models of a given molecule
    vel, dataset, frac, tot_files, tot_temps, tot_dens = [[] for i in range(6)]
    d = {}
    file_count = 0

    print("Parsing", len(files), "models")
    for file in files:
        print(file_count)
        isave = 0
        t = file.split("/")[-1]
        t = t.split("_")

        with open(file) as f:
            for i, l_ in enumerate(f):
                if "temp[K]" in l_:
                    temps = l_.split()[1:]
                if "n[part/ccm]" in l_:
                    dens = l_.split()[1:]
                if "lam [A]" in l_:
                    isave = i + 1
                    break

            if isave != 0:
                data = np.genfromtxt(file, skip_header=isave, skip_footer=1)
                try:
                    d["wl"] = data[:, 0]
                except:
                    print("Error reading", file, "check if empty.")
                    continue

                for j in range(len(temps)):
                    vel.append(t[1])
                    dataset.append(t[2])
                    frac.append(t[3])
                    tot_files.append(file.split("/")[-1])
                    tot_temps.append(temps[j])
                    tot_dens.append(dens[j])
                    d[dens[j] + "/" + temps[j]] = data[:, j + 1]

                # write out model as a csv for easier look up later
                mdf = pd.DataFrame(d)
                mdf.to_csv(
                    path_save
                    + molecule
                    + "_"
                    + dataset[-1]
                    + "_"
                    + vel[-1]
                    + "_"
                    + frac[-1]
                    + ".csv",
                    index=False,
                )

        file_count += 1

    df = pd.DataFrame([tot_files, dataset, frac, tot_temps, tot_dens, vel])
    df = df.transpose()
    df.columns = [
        "filename",
        "dataset",
        "mole_frac",
        "temperature",
        "density",
        "velocity",
    ]
    df["molecule"] = [molecule for i in range(len(df))]

    return df


def add_models(molecule, files):
    try:
        hdf = pd.read_csv(CODIR + "Hoeflich_models.csv")
    except:
        hdf = pd.DataFrame()
        print("No previous model dataframe found, consider running make_model_df.py")

    newdf = create_df(molecule, files)
    # dropping duplicates to make sure we don't append a model that already exists
    df = hdf.append(newdf).drop_duplicates()

    df.to_csv(CODIR + "Hoeflich_models.csv", index=False)

    return

if __name__ == "__main__":
    if not os.path.isfile(path_save):
        os.system("mkdir " + path_save)

    print("Working on CO...")
    molecule = "CO"
    files = glob.glob(path_CO + "plot.dat*" + molecule)
    codf = create_df(molecule, files)

    print("Working on SiO...")
    molecule = "OSi"
    files = glob.glob(path_CO + "plot.dat*" + molecule)
    siodf = create_df(molecule, files)
    df = codf.append(siodf)

    df.to_csv(CODIR + "Hoeflich_models.csv", index=False)
