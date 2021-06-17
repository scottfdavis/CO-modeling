import numpy as np
import pandas as pd


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def get_model(path, file, temp, n):
    with open(path + file) as f:
        for i, l_ in enumerate(f):
            if "temp[K]" in l_:
                temps = l_.split()[1:]
            if "n[part/ccm]" in l_:
                ns = l_.split()[1:]
            if "lam [A]" in l_:
                isave = i + 1
                break
        if isave:
            data = np.genfromtxt(path + file, skip_header=isave, skip_footer=1)
        else:
            return None

    temps = [float(x) for x in temps]
    ns = [float(x) for x in ns]
    if len(data):
        (indn,) = np.where(np.asarray(ns) == n)
        (indt,) = np.where(np.asarray(temps) == temp)
        ind = intersection(list(indn), list(indt))
        if len(ind) == 0:
            return None

        wl = data[:, 0]
        opac = data[:, ind[0] + 1]
        return [wl, opac]

def get_csv(path,temp,n,velocity,mole_frac,molecule):
    modeldf = pd.read_csv(path+molecule+'_'+str(velocity)+'_'+str(mole_frac)+'.csv')

    n = str(format(n, "10.2E")).strip()
    temp = str(format(temp, ".2f")).strip()

    return [modeldf['wl'].values, modeldf[n+'/'+temp].values]
