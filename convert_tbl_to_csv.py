import csv

COLUMN_LABELS = ["CENTRALWAVELNG", "BANDWIDTH", "PL_TRANDEP", "PL_TRANDEPERR1", "PL_TRANDEPERR2", "PL_TRANDEPLIM", "PL_TRANDEP_AUTHORS", "PL_TRANDEP_URL", "PL_RATROR", "PL_RATRORERR1", "PL_RATRORERR2", "PL_RATRORLIM", "PL_RATROR_AUTHORS", "PL_RATROR_URL", "PL_RADJ", "PL_RADJERR1", "PL_RADJERR2", "PL_RADJLIM", "PL_RADJ_AUTHORS", "PL_RADJ_URL", "PL_TRANMID", "PL_TRANMIDERR1", "PL_TRANMIDERR2", "PL_TRANMIDLIM", "ST_RAD", "ST_RADERR1", "ST_RADERR2", "ST_RAD_AUTHORS", "ST_RAD_URL"]
# |CENTRALWAVELNG|BANDWIDTH|PL_TRANDEP|PL_TRANDEPERR1|PL_TRANDEPERR2|PL_TRANDEPLIM|PL_TRANDEP_AUTHORS|                         PL_TRANDEP_URL|PL_RATROR|PL_RATRORERR1|PL_RATRORERR2|PL_RATRORLIM|   PL_RATROR_AUTHORS|                                                 PL_RATROR_URL|      PL_RADJ|PL_RADJERR1|PL_RADJERR2|PL_RADJLIM|PL_RADJ_AUTHORS|                            PL_RADJ_URL|PL_TRANMID|PL_TRANMIDERR1|PL_TRANMIDERR2|PL_TRANMIDLIM|     ST_RAD|ST_RADERR1|ST_RADERR2|   ST_RAD_AUTHORS|                                                    ST_RAD_URL|

# data.iat(row, col) << syntax
# data.to_csv(sep=",", index=False, columns=COLUMN_LABELS)
# print(data)


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
                items = [x.strip() for x in items if x]

                DATA.append(items)

    print(len(COLUMN_LABELS))
    print(len(DATA[0]))
    return INFO, DATA


def main():
    reformat_data('./WASP-39b Data/WASP_39_b_3.11466_4132_1.tbl')

if __name__ == "__main__":
    main()