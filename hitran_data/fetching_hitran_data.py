from hapi import *
import matplotlib.pyplot as plt

def convertMicroToFreq(lambda_micro):
    return int(1e4/lambda_micro)

def fetchHitran(min_w=3, max_w=5):
    """
    fetches molecular data for first 3 prominent isotopes of H2O, CO2 CH4 and CO
    """

    # HITRAN_ids = ["H2O","CO2","O3"," N2O","CO","CH4","O2","NO","SO2","NO2","NH3","HNO3","OH","HF","HCl","HBr","HI","ClO","OCS"," H2CO"," HOCl"," N2"," HCN"," CH3Cl"," H2O2"," C2H2"," C2H6"," PH3"," COF2"," SF6"," H2S"," HCOOH"," HO2"," O"," ClONO2"," NO+"," HOBr"," C2H4"," CH3OH"," CH3Br"," CH3CN"," CF4"," C4H2"," HC3N"," H2"," CS"," SO3"," C2N2"," COCl2"," SO"," CH3F"," GeH4"," CS2"," CH3I"," NF3"]

    db_begin("data")

    # fetch("CO2", 2, 1, convertMicroToFreq(5), convertMicroToFreq(3))

    fetch_by_ids("H2O", [1, 2, 3], convertMicroToFreq(max_w), convertMicroToFreq(min_w))
    select("H2O",ParameterNames=('nu',"sw"), File="H2O.txt")

    fetch_by_ids("CO2", [7, 8, 9], convertMicroToFreq(max_w), convertMicroToFreq(min_w))
    select("CO2",ParameterNames=('nu',"sw"), File="CO2.txt")

    fetch_by_ids("CO", [26, 27, 28], convertMicroToFreq(max_w), convertMicroToFreq(min_w))
    select("CO",ParameterNames=('nu',"sw"), File="CO.txt")
    
    fetch_by_ids("CH4", [32, 33, 34], convertMicroToFreq(max_w), convertMicroToFreq(min_w))
    select("CH4",ParameterNames=('nu',"sw"), File="CH4.txt")

def processHitran(file_name, factor):

    wavenumbers = list()
    wavelength = list()
    relative_intensities = list()

    with open(file_name, 'r') as f:
        lines = f.readlines()

        for l in lines:
            w, i = l.split(" ")

            # wavenumbers in cm^-1
            wavenumbers.append(float(w))

            # wavelength in micrometers
            wavelength.append(1/(float(w))*10e4)

            # relative_intensities.append(float(i)/factor)
            relative_intensities.append(float(i))

    # print("wavenumbers:")
    # print(wavenumbers)

    # print("\nrelative intensities")
    # print(relative_intensities)

    print("plotting...")
    # plt.errorbar(wavenumbers, relative_intensities, marker='.', ls='none')
    plt.errorbar(wavelength, relative_intensities, marker='.', ls='none')
    plt.show()

def convertManual(start_file, dest_file):
    
    with open(start_file, 'r') as readfile, open(dest_file, 'w+') as writefile:
        lines = readfile.readlines()

        for l in lines:
            writefile.write(" ".join(l.split(" ")[2:4])+'\n')

def main():
    fetchHitran()
    # getHelp(fetch_by_ids)
    # getHelp(iso_id)

    # fetch_by_ids("test", [3, 4, 5], convertMicroToFreq(5), convertMicroToFreq(3))

    # processHitran("./H2O.txt", 0.9973)

    # convertManual("./CO2.data", "./CO2.txt")
  

if __name__ == "__main__":
    main()