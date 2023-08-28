import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *


def read_flim_data(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".asc"):
            # Prints only text file present in My Folder
            files.append(file)
    return files

def read_photons(file_asc, path):
    for f in file_asc:
        if "_photons" in f:
            ascii_grid = np.loadtxt(path + "\\" + f)
            ascii_grid_lim = [ascii_grid.min(), ascii_grid.max()]
            print(f)
    return ascii_grid, ascii_grid_lim

def get_tau_m(file_asc, path):
    # returns mean lifetime as weighted arithmetic mean tm = (sum(a_i*tau_i)/sum(a_i))
    for f in file_asc:
        if "_a1[%]" in f:
            a1 = np.loadtxt(path + "\\" + f)
            a2 = np.subtract(100, a1)
            print(f)
        elif "_t1" in f:
            t1 = np.loadtxt(path + "\\" + f)
            print(f)
        elif "_t2" in f:
            t2 = np.loadtxt(path + "\\" + f)
            print(f)
    tm = ((a1*t1)+(a2*t2))/(a1+a2)
    tm_lim = [np.min(tm[np.nonzero(tm)]), np.max(tm[np.nonzero(tm)])]
    tm = np.ma.masked_where(tm < 10, tm)
    cmap = plt.colormaps.get_cmap("afmhot").copy()
    cmap.set_bad(color='gray')
    return tm, tm_lim, cmap
        
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    path_in = filedialog.askdirectory()
    print(path_in)
    file_in = read_flim_data(path_in)
    [im_photons, im_lim] = read_photons(file_in, path_in)
    [im_tau, tau_lim, tau_map] = get_tau_m(file_in, path_in)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6))
    ax1.imshow(im_photons, interpolation="none", cmap="gray",vmin=im_lim[0],vmax=im_lim[1])
    ax2.hist(im_photons.flatten(), bins=256)
    # tau_m min and max are based on tau_lim, i.e. maximum and minimum lifetime in the image
    # for fixed limits us: vmin = 500, vmax = 2800 in the line below
    # im3 = ax3.imshow(im_tau, interpolation="None", cmap=tau_map, vmin=tau_lim[0],vmax=tau_lim[1])
    im3 = ax3.imshow(im_tau, interpolation="None", cmap=tau_map, vmin=50,vmax=1700)
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04, orientation='vertical')
    plt.show()