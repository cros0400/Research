from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--crate", action = "store", type = "str", dest = "crateNum", default = "0",
    help = "Number of UHTR crate to test")
parser.add_option("-u", "--uhtr", action = "store", type = "str", dest = "uhtrNum", default = "0",
    help = "Number of UHTR to test")
parser.add_option("-d", "--depth", action = "store", type = "str", dest = "depth", default = "0",
    help = "Specify layer in detector")
parser.add_option("-e", "--energy", action = "store", type = "str", dest = "energy", default = "eta",
    help = "Specify whether to look at phi or eta of each detector")
parser.add_option("-f", "--filename", action = "store", type = "str", dest = "filename", default = "outfile",
    help = "Desired name of output (will overwrite existing file)")
parser.add_option("-n", "--numBC", action = "store", type = "str", dest = "numBC", default = "1000",
    help = "Number of non-empty bunch crossings")

(options, args) = parser.parse_args()

NUM_FIBERS = 24
NUM_CHANNELS = 8

energy = ''

if (options.energy == "eta"):
    energy = "Eta"
if (options.energy == "phi"):
    energy = "Phi"


# Function which writes a blank bunch crossing with capID specified to file f
def write_blank(f, capID):
    f.write("""10%sbc
00000
00000
00000
00000
00000
""" % capID)

# Function which handles the incrementing of the capID
def inc_capID(n):
    n += 1
    if (n % 4 == 0):
        n = 0
    return n

# Return the energy value requested for a given fiber or channel
def getEnergy( valid_, fiber, channel ):
    for v in valid_:
        if (v["uHTR_FI"] == str(fiber) and v["FI_CH"] == str(channel)):
            if (int(v[energy]) <= 9):
                return '0' + v[energy]
            else:
                return v[energy]
    return '00'

while True:
    try:
        open('Lmap_ngHB_N_20200212.txt')
        break
    except FileNotFoundError:
        print("Could not open \'Lmap_ngHB_N_20200212.txt\'. Please include the mapping file in local HCALTrigger directory")
        raise

with open('Lmap_ngHB_N_20200212.txt') as f:
    # Read in lines of the text file and split at spaces
    Lmap = f.readlines()
    lines = []
    for line in Lmap:
        lines.append(line.split())
    f.close()

    # Delete first element of header since it does not match with any of the data
    del lines[0][0]

    #Create list of dicts in order to access data by name of variable it represents
    data = []
    for line in lines:
        data.append({lines[0][i]: line[i] for i in range(len(line))})

    #Loop over all dicts in list. Determine if a given dict corresponds to the correct
    #Crate and UHTR
    valid = []
    for d in data:
        if (d["Crate"] == options.crateNum and d["uHTR"] == options.uhtrNum):
            if (d["Depth"] == options.depth or options.depth == '0'):
                valid.append(d)

    # Open write file and prepare for writing
    filename = options.filename + '.txt'
    outfile = open(filename, 'w')

    #Loop over all channels in each fiber. Write out specified value of energy (eta/phi)
    #for each channel
    print("Writing uHTR pattern to file %s" % filename)

    for i_fib in range(0,NUM_FIBERS):
        capID = 0
        outfile.write('# Fiber %d\n' % i_fib)
        for i_bc in range(0,int(options.numBC)):
            temp = '0'
            for i_ch in range(0,NUM_CHANNELS):
                if(i_ch == 0):
                    outfile.write("10%dbc\n" % capID)
                    capID = inc_capID(capID)
                temp += getEnergy(valid, i_fib, i_ch)
                if (i_ch % 2 == 1):
                    outfile.write('%s\n' % temp)
                    temp = '0'
            for i in range(0,2):
                write_blank(outfile, capID)
                capID = inc_capID(capID)

    outfile.close()
