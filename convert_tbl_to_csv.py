import csv
import os

COLUMN_LABELS = ["CENTRALWAVELNG", "BANDWIDTH", "PL_TRANDEP", "PL_TRANDEPERR1", "PL_TRANDEPERR2", "PL_TRANDEPLIM", "PL_TRANDEP_AUTHORS", "PL_TRANDEP_URL", "PL_RATROR", "PL_RATRORERR1", "PL_RATRORERR2", "PL_RATRORLIM", "PL_RATROR_AUTHORS", "PL_RATROR_URL", "PL_RADJ", "PL_RADJERR1", "PL_RADJERR2", "PL_RADJLIM", "PL_RADJ_AUTHORS", "PL_RADJ_URL", "PL_TRANMID", "PL_TRANMIDERR1", "PL_TRANMIDERR2", "PL_TRANMIDLIM", "ST_RAD", "ST_RADERR1", "ST_RADERR2", "ST_RAD_AUTHORS", "ST_RAD_URL"]

COMMON_CSV_PATH = './clean_csv/all_data.csv'

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

        return f"""
        ----------------------------------------------------------------------
        FILE DETAILS FOR: {self.path} 
            Planet Name: {self.specs["planet_name"]}
            Spectrum Type: {self.specs["spectrum_type"]}
            Instrument: {self.specs["instrument"]}
            Facility: {self.specs["facility"]}
            Note: {self.specs["note"]}
            Reference: {self.specs["reference"]}

            DATA STORAGE DETAILS:
            In clean_csv > all_data.csv
            Index {self.loc_in_csv[0]} to and not including index {self.loc_in_csv[1]}
        ----------------------------------------------------------------------

            """

    
    def add_info(self, info):
        info_labels = ["planet_name", "spectrum_type", "instrument", "facility", "note", "reference"]
        
        for i, label in enumerate(info_labels):
            self.specs[label] = info[i]
    
def reformat_data(file_name):
    """
    Reads the raw tbl files and processes the raw values data
    :param file_name:
    :return 1D list of the specs and 2D list of data based on the global column labels:

    FOR ALL DATA FILES:
    - make sure all the names-dates are connected via DASH!
    e.g. "Wakeford et al. 2018" -> "Wakeford-et-al.-2018"

    INPUT RAW DATA FILE FORMAT
    \\NAME FIELD = SPECS VALUE
    \\ NAME FIELD = SPECS VALUE
    \\
    \\
    |COLUMN TITLES | COLUMN TITLES | ... |
              data |         data  | ... |
    """

    INFO = list()
    DATA = list()

    with open(file_name, 'r') as data_file:
        all_lines = data_file.readlines()
        # print(len(all_lines))

        for line in all_lines:
            # Append only the SPECS VALUES into the INFO list
            if line[0] == "\\" and line[1:].strip():
                INFO.append(line.strip()[1:].split(" = ")[-1])

            # ignores the column titles (COLUMN TITLES are already globalized)
            elif line[0] == "|":
                pass
            
            # append the line of data into a list
            elif line[0] != "\\":
                # print(line)
                items = line.split(" ")
                items = [x.strip() for x in items if len(x.strip())]

                DATA.append(items)

    return INFO, DATA

def main():
    # CLEARING COMMON CSV FILE
    f = open(COMMON_CSV_PATH, 'w+')
    f.close()

    # CLEARING COMMON TEXT FILE
    f = open('./clean_csv/file_details.txt', 'w+')
    f.close()

    with open(COMMON_CSV_PATH, 'w', newline='') as csvfile, open('./clean_csv/file_details.txt', 'a') as details_file:
        CSVwriter = csv.writer(csvfile)

        # WRITING HEADINGS INTO COMMON CSV FILE
        CSVwriter.writerow(COLUMN_LABELS)

        # starts counting in 2 because first row is headers
        row_counter = 2

        # GOING THROUGH EACH RAW DATA FILE
        for j, filename in enumerate(os.listdir('./WASP-39b Data')):
            print(f"ON FILE NUMBER {j}")
            print(f"    Reformatting data...")

            i, d = reformat_data(f"./WASP-39b Data/{filename}")

            print("    Data Reformatted")

            #  WRITING FILE DATA INTO COMMON CSV
            print("    Writing reformatted data into common CSV file...")
            CSVwriter.writerows(d)
            print("    Done")
            
            # WRITING FILE SPECIFICATIONS INTO COMMON TEXTFILE
            print("     Reorganizing file details and specifications into the common textfile")
            file_info_base = File(filename, row_counter, row_counter+len(d), i)
            details_file.write(str(file_info_base))
            print("     Done")

            print(f"data of FILE NUMBER {j} can now be found from index {row_counter} to {row_counter+len(d)-1}\n\n")

            # UPDATE ROW COUNTER
            row_counter += len(d)

if __name__ == "__main__":
    main()