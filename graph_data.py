import matplotlib.pyplot as plt
from astroquery.nist import Nist
import astropy.units as u

# MATPLOTLIB SUPPORTED COLORS
COLORS = ['g', 'c', 'm', 'y', 'r']

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

def fetchData(lowerbound, upperbound, element):
    """
    Enter the lowerbound (in nm) and upperbound in nm
    Returns a list of x values in nm
    """

    print("FETCHING MOLECULAR LINES DATA...")

    x = list()

    # bounds 
    table = Nist.query(lowerbound *u.nm, upperbound * u.nm, linename=element, wavelength_type="vacuum")
    
    # USING ONLY OBSERVED VALUES
    for i in range(len(table)):
        
        # prevent if there are no observed values
        if table[i][0] != '--':
            x.append(round(float(table[i][0]), 3))
    return x

def plot(x_vals, y_vals, x_err, y_err, target_molecules=[], min_wl=0, max_wl=5):

    LOWERBOUND = min(x_vals)

    # Initialize Graph
    fig = plt.figure()
    ax = fig.add_subplot()

    # Plots Normal Data
    ax.errorbar(x_vals, y_vals, xerr=x_err, yerr=y_err, fmt='.', ls='none')

    # MOLECULAR ANALYSIS -------------------------
    # SETS THE TARGET MOLECULES in list for query 
    
    # Fetch atomic data + graph
    for i, molec in enumerate(target_molecules):

        print(f"CONDUCTING MOLECULAR ANALYSIS for {molec}")

        x_vals = fetchData(min_wl*1000, max_wl*1000, molec)
        print(f"    data fetched...")
        
        for j in range(len(x_vals)):
            if x_vals[j]/1000 >= LOWERBOUND:
                ax.axvspan(x_vals[j]/1000, (x_vals[j]+0.001)/1000, alpha=0.5, color=COLORS[i])

        
    # Paper-proof the graph
    ax.set_xlabel("Wavelength (micrometers)", loc='center')
    ax.set_ylabel("Transit Depth (%)", loc='center')
    ax.set_title(f"Transmission Spectrum of WASP-39b from {min_wl} to {max_wl} micrometers")

    fig.tight_layout()
    plt.grid()
    plt.show()


def main():

    # TRANSMISSION SPECTRA DATA ANALYSIS -----------------------
    # SETS THE GRAPHING BOUNDARY in micrometers
    min_val, max_val = 0, 5

    # sort data
    x_vals, y_vals, xerr_bars, yerr_bars = sortData(min_val, max_val)

    # plotting
    plot(x_vals, y_vals, xerr_bars, yerr_bars, ["H"], min_val, max_val)


if __name__ == "__main__":
    main()
