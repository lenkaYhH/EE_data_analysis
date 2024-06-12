from hapi import *


def convertMicroToFreq(lambda_micro):
    return 10e4/lambda_micro

def fetchHitran(molecule, hitran_globalID, hitran_localID):
    """
    enter molecule name and hitran IDs

    saves data files into folder of the molecule
    """

    HITRAN_ids = ["H2O","CO2","O3"," N2O","CO","CH4","O2","NO","SO2","NO2","NH3","HNO3","OH","HF","HCl","HBr","HI","ClO","OCS"," H2CO"," HOCl"," N2"," HCN"," CH3Cl"," H2O2"," C2H2"," C2H6"," PH3"," COF2"," SF6"," H2S"," HCOOH"," HO2"," O"," ClONO2"," NO+"," HOBr"," C2H4"," CH3OH"," CH3Br"," CH3CN"," CF4"," C4H2"," HC3N"," H2"," CS"," SO3"," C2N2"," COCl2"," SO"," CH3F"," GeH4"," CS2"," CH3I"," NF3"]

    db_begin()

    fetch(molecule, hitran_globalID, hitran_localID, convertMicroToFreq(5), 50000)

def main():
    fetchHitran("H2O", 1, 1)

if __name__ == "__main__":
    main()