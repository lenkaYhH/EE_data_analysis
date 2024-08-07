import matplotlib.pyplot as plt
from astroquery.nist import Nist
import astropy.units as u
import math

# MATPLOTLIB SUPPORTED COLORS
COLORS = ['r', 'forestgreen', 'darkorange', 'dodgerblue']

# in micrometers
WAVELENGTH_GROUPING = 0.005

# for all 1600 datapoints
DATA_FILE = "./clean_csv/all_data.csv"

# for only one file
DATA_FILE = "./clean_csv/one_file.csv"
FILE_NUM = 4988.1

# special molecules
SPECIAL_MOLECULES = ["H2O", "CO2", "CO", "CH4"]

# abundances from hitran's isotopogue
ABUNDANCES  = {
    "H2O": 0.9973,
    "CO2": 0.9842,
    "CO": 0.9865,
    "CH4": 0.98827
}


def sortData(min_wl=0, max_wl=10, remove_odd_points=True):
    """
    Inputs min-max wavelength range, in microns, to visualize (if any boundaries) and return x-y pofloats, 1D x-error bar values and 2D y-error bar values
    """

    x = list()
    y = list()
    x_errorbars = list()

    # first list is the minimum and second list is maximum
    y_errorbars = [[], []]

    with open(DATA_FILE, "r") as f:
        lines = f.readlines()

        for l in lines[1:]:
            data = l.split(",")

            # for removing weird points
            if abs(float(data[3])) > 0.2 or abs(float(data[4])) > 0.2:
                print(f"ODD DATA POINTS FOUND: wavelength of {data[0]} has very high transit depth errors of {data[3]} and {data[4]}")

                # skip this outlier
                if remove_odd_points:
                    continue
            
            if data[1] != 'null':
                if abs(float(data[1])) > 0.35:
                    print(f"ODD DATA POINTS FOUND: wavelength of {data[0]} has very high wavelength absolute uncertainty of {data[1]}")

                    # skip this outlier
                    if remove_odd_points:
                        continue

            # if data is within plottable range
            if min_wl <= float(data[0]) <= max_wl:
                x.append(float(data[0]))
                x_errorbars.append(float(data[1]) if data[1] != "null" else 0)

                y.append(float(data[2]))

                # makes sure the minimum bounds of y-error isn't negative
                y_errorbars[0].append(abs(float(data[3])))
                y_errorbars[1].append(abs(float(data[4])))

                
    return x, y, x_errorbars, y_errorbars

def sortPlotCleanData(x, y, option):
    """
    Takes the sorted data from sortData()

    option determins whether the y value is an accumulation (s) or an average (a)

    Returns two lists (list of x values) (list of corresponding y values) that are grouped by wavelength range specified in global WAVELENGTH_GROUPING
    """

    print("Sorting through the clean data...")

    ret_list = list()

    for i in range(len(x)):
        ret_list.append((x[i], y[i]))

    ret_list.sort()

    # further groups the data into blocks
    x_plot, y_plot = list(), list()

    avrg_x = list()
    avrg_y = list()
    counter = 0

    while len(ret_list) != 0:

        # if a new group needs to be started
        while not counter <= ret_list[0][0] <= counter + WAVELENGTH_GROUPING:
            
            # block is ready to be officially plotted
            if len(avrg_x) != 0:
                x_plot.append(sum(avrg_x)/len(avrg_x))

                if option == 'a':
                    y_plot.append(sum(avrg_y)/len(avrg_y))
                else:
                    y_plot.append(sum(avrg_y))

            # reset
            avrg_x, avrg_y = list(), list()

            # update the next block
            counter += WAVELENGTH_GROUPING
        
        # update the average of the block
        avrg_x.append(ret_list[0][0])
        avrg_y.append(ret_list[0][1])
    
        # remove the point once it has been processed
        ret_list = ret_list[1:]

    return x_plot, y_plot

def fetchElementData(lowerbound, upperbound, molec, field):
    """
    Enter the lowerbound (in nm) and upperbound in nm
    Returns a list of x values in micrometers; y=[1,1,1,...]'
    """

    print("\nFETCHING MOLECULAR LINES DATA...")
    print(f"    currently fetching data for {molec}  between {lowerbound} and  {upperbound}")

    x = list()
    y = list()

    if not molec in SPECIAL_MOLECULES:

        # bounds 
        table = Nist.query(lowerbound *u.nm, upperbound * u.nm, linename=molec, wavelength_type="vacuum")
        # print(table)
        
        # USING ONLY OBSERVED VALUES
        for i in range(len(table)):
            
            # prevent if there are no values
            if table[i][field] != '--' and not '+' in str(table[i][field]):
                x.append(round(float(table[i][field])/1000, 3))
                y.append(1)
        
        return x, y    
    return x, y

def fetchMolecularData(file_name, molec):
    """
    given a txt file that per line follows the following format:
    wavenumber(cm^-1) intensities cm^-1/(molecule cm^-2)

    read from the file and returns a list of x values (wavelength in micrometers) and list of y values (intensity, adjusted for abundance)
    """

    wavenumbers = list()
    wavelength = list()
    relative_intensities = list()

    with open(file_name, 'r') as f:
        lines = f.readlines()

        for l in lines:
            # try:
            #     w, i = l.split(" ")[1:]
            # except:
            #     print(molec)
            #     print(l.split(" ")[1:])
            #     break
            w, i = l.split(" ")[1:]
            
            # removing points that have very minor intensities (TODO: ADJUST BASED ON MEASUREMENT INACCURACY IN HITRAN)
            if float(i) > 1e-24:
                # wavenumbers in cm^-1
                wavenumbers.append(float(w))

                # wavelength in micrometers
                wavelength.append(1/(float(w))*1e4)

                # relative_intensities.append(float(i)/ABUNDANCES[molec])
                relative_intensities.append(float(i))

    # normalizing everything to 1
    # max_val = max(relative_intensities)
    # relative_intensities = list(map(lambda x: x/max_val, relative_intensities))

    return wavelength, relative_intensities

def plotRaw(x_vals, y_vals, x_err, y_err, target_molecules=[]):

    LOWERBOUND = math.floor(min(x_vals))
    UPPERBOUND = math.ceil(max(x_vals))

    # Initialize Graph
    fig_raw = plt.figure()
    ax = fig_raw.add_subplot()

    if len(target_molecules):
        ax2 = ax.twinx()

    # Plots Normal Data
    ax.errorbar(x_vals, y_vals, xerr=x_err, yerr=y_err, fmt='.', ls='none')

    # MOLECULAR ANALYSIS -------------------------
    # SETS THE TARGET MOLECULES in list for query 
    
    # Fetch atomic data + graph
    for i, molec in enumerate(target_molecules):

        if molec in SPECIAL_MOLECULES:
            x, y = fetchMolecularData(f"./hitran_data/{molec}.txt", molec)

            ax2.errorbar(x, y, marker='.', color=COLORS[SPECIAL_MOLECULES.index(molec)], label=molec, ls='none')

        else: 
            print(f"\nCONDUCTING MOLECULAR ANALYSIS for {molec}")

            x_vals, y = fetchElementData(LOWERBOUND*1000, UPPERBOUND*1000, molec, "Ritz")
            print(f"    data fetched...")
            
            for j in range(len(x_vals)):
                if x_vals[j] >= LOWERBOUND:
                    ax.axvspan(x_vals[j], x_vals[j]+0.001, alpha=0.25, color=COLORS[i])

        
    # Paper-proof the graph
    ax.set_xlabel("Wavelength (micrometers)", loc='center')
    ax.set_ylabel("Transit Depth (%)", loc='center')
    ax.set_title(f"Transmission Spectrum of WASP-39b from {LOWERBOUND} to {UPPERBOUND} micrometers")

    if len(target_molecules):
        ax2.set_ylabel("relative intensity of molecular spectra")
        ax2.legend()

    fig_raw.tight_layout()
    plt.plot()

def plotClean(x, y, target_molecules=[]):
    """
    Takes in raw x and y values, cleans up the values and plots it

    Afterwards plots the target molecules on the same axes, using the RITZ WAVELENGTH

    """

    # initialize graph
    print("\nInitializing clean plotting graph...")
    fig_clean = plt.figure()
    ax1 = fig_clean.add_subplot()
    ax2 = ax1.twinx()

    # DATA CLEANING -----------------------------------
    x, y = sortPlotCleanData(x, y, 'a')

    min_wl = math.floor(min(x))
    max_wl = math.ceil(max(x))

    ax1.errorbar(x, y, marker='.', ls='none')
    # ax1.errorbar(x, y, marker='.')

    # MOLECULAR ANALYSIS -----------------------------------

    # queries for database info
    for i, molec in enumerate(target_molecules):

        if molec in SPECIAL_MOLECULES:
            x, y = fetchMolecularData(f"./hitran_data/{molec}.txt", molec)

        else:
            x, y = fetchElementData(min_wl*1000, max_wl*1000, molec, "Ritz")

            x, y = sortPlotCleanData(x, y, 's')

            # plot molecular data
            # ax2.plot(x, y, marker='.', ls='none', color=COLORS[i], label=molec)

        ax2.errorbar(x, y, marker='.', color=COLORS[i], label=molec, ls='none')

    # Paper-proof the graph
    ax1.set_title(f"Processed Transmission Spectrum of WASP-39b from {min_wl} to {max_wl} micrometers, file name {FILE_NUM}")
    ax1.set_xlabel("Wavelength (micrometers)", loc='center')
    ax1.set_ylabel("Transit Depth (%) (transmission spectra)", loc='center')
    ax1.legend()
    ax2.set_ylabel("relative frequency (atomic spectra)")
    ax2.legend()

    # show graph
    fig_clean.tight_layout()
    plt.plot()

def main():

    # TRANSMISSION SPECTRA DATA ANALYSIS -----------------------
    # SETS THE GRAPHING BOUNDARY in micrometers
    min_val, max_val = 0, 5

    # sort data
    x_vals, y_vals, xerr_bars, yerr_bars = sortData(min_val, max_val)

    # plotting
    to_plot = ["H2O", "CO2", "CO", "CH4"]
    # to_plot = ["H2O", "CO2", "CO"]

    for a in to_plot:
        plotRaw(x_vals, y_vals, xerr_bars, yerr_bars, [a])
    
    plotRaw(x_vals, y_vals, xerr_bars, yerr_bars, to_plot)
    plotRaw(x_vals, y_vals, xerr_bars, yerr_bars)

    # plotClean(x_vals, y_vals, elements)
    # plotClean(x_vals, y_vals, ["Na"])

    # plotClean(x_vals, y_vals, ["H2O"])


    plt.show()

if __name__ == "__main__":
    main()
