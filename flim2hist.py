import numpy as np
import sys
import os
import matplotlib.pyplot as plt

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
            print(path + "\\" + f)
            ascii_grid = np.loadtxt(path + "\\" + f)
            ascii_grid_lim = [ascii_grid.min(), ascii_grid.max()]
    return ascii_grid, ascii_grid_lim

def get_tau_m(file_asc, path):
    # returns mean lifetime as weighted arithmetic mean tm = (sum(a_i*tau_i)/sum(a_i))
    
    
if __name__ == "__main__":
    path_in = sys.argv[1]
    file_in = read_flim_data(path_in)
    [im_photons, im_lim] = read_photons(file_in, path_in)
    [im_tau, tau_map] = get_tau_m(file_in, path_in)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6))
    ax1.imshow(im_photons, cmap="gray",vmin=im_lim[0],vmax=im_lim[1])
    ax2.hist(im_photons.flatten(), bins=256)
    ax3.imshow()
    plt.show()