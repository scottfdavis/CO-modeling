import numpy as np
import pandas as pd
import os, glob


def create_df(molecule):
    # create a dataframe for all the models of a given molecule
    files = glob.glob(path_CO + "plot.dat*" + molecule)
    vel, dataset, frac, tot_files, tot_temps, tot_ns = [[] for i in range(6)]
    d = {}
    file_count = 0

    print("Parsing", len(files), "files")
    for file in files:
        print(file_count)
        t = file.split("/")[-1]
        t = t.split("_")

        with open(file) as f:
            for i, l_ in enumerate(f):
                if "temp[K]" in l_:
                    temps = l_.split()[1:]
                if "n[part/ccm]" in l_:
                    ns = l_.split()[1:]
                if "lam [A]" in l_:
                    isave = i + 1
                    break

            if isave:
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
                tot_ns.append(ns[j])
                d[ns[j] + "/" + temps[j]] = data[:, j + 1]

            # write out model as a csv for easier look up later
            mdf = pd.DataFrame(d)
            mdf.to_csv(
                path_save + molecule + "_" + vel[-1] + "_" + frac[-1] + ".csv",
                index=False,
            )

        file_count += 1

    df = pd.DataFrame([tot_files, dataset, frac, tot_temps, tot_ns, vel])
    df = df.transpose()
    df.columns = ["filename", "dataset", "mole_frac", "temperature", "n", "velocity"]
    df["molecule"] = [molecule for i in range(len(df))]

    return df


cwd = os.getcwd()
path_CO = cwd + "/CO/"
path_save = cwd + "/models_csv/"
if __name__ == "__main__":
    if not os.path.isfile(path_save):
        os.system("mkdir " + path_save)

    print("Working on CO...")
    codf = create_df("CO")
    print("Working on SiO...")
    siodf = create_df("OSi")
    df = codf.append(siodf)

    df.to_csv("Hoeflich_models.csv", index=False)
