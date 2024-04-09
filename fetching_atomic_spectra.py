from astroquery.nist import Nist
import astropy.units as u

def fetchData(lowerbound, upperbound, element):
    """
    Enter the lowerbound (in micrometers) and upperbound in micrometers
    Returns a NIST table
    """

    # bounds 
    table = Nist.query(lowerbound*1000 *u.nm, upperbound*1000 * u.nm, linename=element, wavelength_type="vacuum")

    return table

def main():
    fetchData(400, 410, "H")

if __name__ == "__main__":
    main()