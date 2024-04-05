import csv
import os

COLUMN_LABELS = ["CENTRALWAVELNG", "BANDWIDTH", "PL_TRANDEP", "PL_TRANDEPERR1", "PL_TRANDEPERR2", "PL_TRANDEPLIM", "PL_TRANDEP_AUTHORS", "PL_TRANDEP_URL", "PL_RATROR", "PL_RATRORERR1", "PL_RATRORERR2", "PL_RATRORLIM", "PL_RATROR_AUTHORS", "PL_RATROR_URL", "PL_RADJ", "PL_RADJERR1", "PL_RADJERR2", "PL_RADJLIM", "PL_RADJ_AUTHORS", "PL_RADJ_URL", "PL_TRANMID", "PL_TRANMIDERR1", "PL_TRANMIDERR2", "PL_TRANMIDLIM", "ST_RAD", "ST_RADERR1", "ST_RADERR2", "ST_RAD_AUTHORS", "ST_RAD_URL"]

class File:
    def __init__(self, path, start_index, end_index, info):
        """
        include path of the raw data file

        start index (including) -> end index (excluding) in the processed csv file
        """
        self.path = path
        self.loc_in_csv = (start_index, end_index)
        self.specs = dict()

        self.add_info(info)
    
    def __str__(self):

        return f"""FILE DETAILS FOR: {self.path} 
            Planet Name: {self.specs["planet_name"]}
            Spectrum Type: {self.specs["spectrum_type"]}
            Instrument: {self.specs["instrument"]}
            Facility: {self.specs["facility"]}
            Note: {self.specs["note"]}
            Reference: {self.specs["reference"]}

            DATA STORAGE DETAILS:
            In clean_csv > all_data.csv
            Index {self.loc_in_csv[0]} to and not including index {self.loc_in_csv[1]}
            """

    
    def add_info(self, info):
        info_labels = ["planet_name", "spectrum_type", "instrument", "facility", "note", "reference"]
        
        for i, label in enumerate(info_labels):
            self.specs[label] = info[i]
    
def reformat_data(file_name):
    """
    Reads the raw tbl files and processes the raw values data
    :param file_name:
    :return 2D list of data based on the global column labels:

    FOR ALL DATA FILES:
    - make sure all the names-dates are connected via DASH!
    e.g. "Wakeford et al. 2018" -> "Wakeford-et-al.-2018"
    """

    INFO = list()
    DATA = list()

    with open(file_name, 'r') as data_file:
        all_lines = data_file.readlines()
        # print(len(all_lines))

        for line in all_lines:
            if line[0] == "\\":
                INFO.append(line.strip()[1:])

            elif line[0] == "|":
                pass

            else:
                items = line.split(" ")
                items = [x.strip() for x in items if len(x.strip())]

                DATA.append(items)

    # for i, item in enumerate(COLUMN_LABELS):
    #     print(item)
    #     print(DATA[0][i])
    #     print('\n')

    # print(len(COLUMN_LABELS))
    # print(len(DATA[0]))
    # print(DATA)

    return INFO, DATA

def disassemble_info(info):
    raise NotImplementedError

def write_data_to_csv(data):
    raise NotImplementedError

def main():
    # reformat_data('./WASP-39b Data/WASP_39_b_3.11466_4132_1.tbl')
    reformat_data('./WASP-39b Data/WASP_39_b_3.11466_3491_1.tbl')

if __name__ == "__main__":
    main()