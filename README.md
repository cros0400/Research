# Research
## Beamer Template
This script will create a "plot dump" with the specified number of figure on each page. Refer to the 
documentation in [writeBeamer.py](BeamerTemplate/TeX/writeBeamer.py) for usage and options

## MakeUHTRPattern
This script will create a text file including the uHTR data pattern based on the mapping file "Lmap_ngHB_N_20200212.txt". This file and similar mapping files can be found at the following [link](https://cms-docs.web.cern.ch/cms-docs/hcaldocs//document/Mapping/Yuan/2020-feb-12/).

Below are the options for using the file:
  Usage: MakeUHTERpattern.py [options]

  Options:
    -h, --help          show this help message and exit
    -c CRATENUM, --crate=CRATENUM
                        Number of UHTR crate to test
    -u UHTRNUM, --uhtr=UHTRNUM
                        Number of UHTR to test
    -d DEPTH, --depth=DEPTH
                        Specify layer in detector
    -e ENERGY, --energy=ENERGY
                        Specify whether to look at phi or eta of each detector
    -f FILENAME, --filename=FILENAME
                        Desired name of output (will overwrite existing file)
    -n NUMBC, --numBC=NUMBC
                        Number of non-empty bunch crossings
