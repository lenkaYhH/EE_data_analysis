import string

def main():
    # open the file to read from with the raw H2O data
    file_read = open('./molecular_spectroscopy_data/H2O_RAW.txt', 'r')

    x = list()
    y = list()

    for line in file_read.readlines()[2:]:

        # reads every line and removes the empty spaces
        processed_line = list(filter(lambda x: x, line.split(" ")))
        
        # finds the frequency and ignores the different isotopes of water
        if any(letter in string.ascii_uppercase for letter in processed_line[0]):
            freq = float(processed_line[1])
        else:
            freq = float(processed_line[0])

        # converts frequency in MHz to wavelength in micrometers (MHz and micrometer conversions cancel out)
        # speed of light 299792458ms^-1
        # lambda = v/f
        x.append(299792458/freq)
        y.append(1)

    print(x)


if __name__ == "__main__":
    main()
