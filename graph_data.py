import matplotlib.pyplot as plt
from astroquery.nist import Nist
import astropy.units as u

# MATPLOTLIB SUPPORTED COLORS
COLORS = ['r', 'y', 'silver', 'palegreen', 'slateblue', 'mistyrose', 'c', 'orange']

WAVELENGTH_GROUPING = 0.005

def sortData(min_wl=0, max_wl=10, remove_odd_points=True):
    """
    Inputs min-max wavelength range, in microns, to visualize (if any boundaries) and return x-y pofloats, 1D x-error bar values and 2D y-error bar values
    """

    x = list()
    y = list()
    x_errorbars = list()

    # first list is the minimum and second list is maximum
    y_errorbars = [[], []]

    with open("./clean_csv/all_data.csv", "r") as f:
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

    option determins whether the y value is an accumulation or an average

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

def fetchData(lowerbound, upperbound, element, field):
    """
    Enter the lowerbound (in nm) and upperbound in nm
    Returns a list of x values in micrometers; y=[1,1,1,...]'
    """

    print("\nFETCHING MOLECULAR LINES DATA...")
    print(f"    currently fetching data for {element}  between {lowerbound} and  {upperbound}")

    x = list()
    y = list()

    # bounds 
    table = Nist.query(lowerbound *u.nm, upperbound * u.nm, linename=element, wavelength_type="vacuum")
    # print(table)
    
    # USING ONLY OBSERVED VALUES
    for i in range(len(table)):
        
        # prevent if there are no observed values
        if table[i][field] != '--':
            x.append(round(float(table[i][field])/1000, 3))
            y.append(1)
    
    return x, y

def plotRaw(x_vals, y_vals, x_err, y_err, target_molecules=[], min_wl=0, max_wl=5):

    LOWERBOUND = min(x_vals)

    # Initialize Graph
    fig_raw = plt.figure()
    ax = fig_raw.add_subplot()

    # Plots Normal Data
    ax.errorbar(x_vals, y_vals, xerr=x_err, yerr=y_err, fmt='.', ls='none')

    # MOLECULAR ANALYSIS -------------------------
    # SETS THE TARGET MOLECULES in list for query 
    
    # Fetch atomic data + graph
    for i, molec in enumerate(target_molecules):

        print(f"\nCONDUCTING MOLECULAR ANALYSIS for {molec}")

        x_vals, y = fetchData(min_wl*1000, max_wl*1000, molec, "Ritz")
        print(f"    data fetched...")
        
        for j in range(len(x_vals)):
            if x_vals[j]/1000 >= LOWERBOUND:
                ax.axvspan(x_vals[j], x_vals[j]+0.000001, alpha=0.25, color=COLORS[i])

        
    # Paper-proof the graph
    ax.set_xlabel("Wavelength (micrometers)", loc='center')
    ax.set_ylabel("Transit Depth (%)", loc='center')
    ax.set_title(f"Transmission Spectrum of WASP-39b from {min_wl} to {max_wl} micrometers")

    fig_raw.tight_layout()
    plt.plot()

def plotClean(x, y, target_molecules=[], min_wl=0, max_wl=0):
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

    ax1.errorbar(x, y, marker='.', ls='none')

    # MOLECULAR ANALYSIS -----------------------------------

    # queries for database info
    for i, molec in enumerate(target_molecules):
        x, y = fetchData(min_wl*1000, max_wl*1000, molec, "Ritz")

        x, y = sortPlotCleanData(x, y, 's')

        # plot molecular data
        ax2.plot(x, y, marker='.', ls='none', color=COLORS[i], label=molec)

    # Paper-proof the graph
    ax1.set_title(f"Processed Transmission Spectrum of WASP-39b from {min_wl} to {max_wl} micrometers")
    ax1.set_xlabel("Wavelength (micrometers)", loc='center')
    ax1.set_ylabel("Transit Depth (%)", loc='center')
    ax2.set_label("relative frequency of atomic emission")
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
    plotRaw(x_vals, y_vals, xerr_bars, yerr_bars, ["H"], min_val, max_val)
    # plotClean(x_vals, y_vals, ["H"], min_val, max_val)

    plt.show()

if __name__ == "__main__":
    main()
