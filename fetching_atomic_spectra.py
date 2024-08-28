from astroquery.nist import Nist
import astropy.units as u
import matplotlib.pyplot as plt
from pylab import plot
from hapi import *

def fetchData(lowerbound, upperbound, element):
    """
    Enter the lowerbound (in micrometers) and upperbound in micrometers
    Returns a NIST table
    """

    # bounds 
    table = Nist.query(lowerbound*1000 *u.nm, upperbound*1000 * u.nm, linename=element, wavelength_type="vacuum")

    return table

def main():
    # t = fetchData(0.4, 0.7, "H2O")
    # print(t)

    fetch('CO2', 2, 1, 2000, 3333)
    fetch('H2O', 1, 1, 2000, 3333)
    nu, coef = absorptionCoefficient_Lorentz(SourceTables=['CO2', 'H2O'], Diluent={'self': 0.5, 'air': 0.5})

    wv = list()

    for n in nu:
        wv.append(1e4/n)

    plt.plot(wv, coef)
    plt.show()

if __name__ == "__main__":
    main()