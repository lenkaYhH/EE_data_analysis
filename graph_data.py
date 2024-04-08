import matplotlib.pyplot as plt

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
                if abs(float(data[1])) > 0.5:
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

def plot(x, y, x_err=[], y_err=[], title=''):
    """
    plots the data given
    """

    plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='.')

    plt.xlabel("Wavelength (micrometers)", loc='center')
    plt.ylabel("Transit Depth (%)", loc='center')
    plt.title(title)

    plt.show()

def main():
    x_vals, y_vals, xerr_bars, yerr_bars = sortData()
    plot(x_vals, y_vals, xerr_bars, yerr_bars, "Transmission Spectrum of WASP 39b")

if __name__ == "__main__":
    main()
