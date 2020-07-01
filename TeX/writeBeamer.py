#########################################################################
# Author: Bryan Crossman                                                #
# Email: cros0400@umn.edu                                               #
# Date: 7/1/20                                                          #
#                                                                       #
# This script will take in all figures in directory ./figures and       #
# writes a Beamer .tex file with figures tiled on slides using the UMN  #
# formating and color scheme                                            #
#                                                                       #
# Make sure that you change the author name, date, and title of slides  #
#                                                                       #
# !! MAKE SURE YOU RUN WITH THE FOLLOWING DIRECTORY CONFIGURATION !!    #
#   project_dir                                                         #
#       | -> figures                                                    #
#       | -> TeX                                                        #
#             | -> umn_template.tex                                     #
#             | -> master_preamble.tex                                  #
#             | -> goldy.pdf                                            #
#             | -> <desired_output_filename>.tex                        #
#             | -> writeBeamer.py                                       #
#       |-------------------------------                                #
#                                                                       #
# Arguments for use:                                                    #
# python writeBeamer.py <desired_output_filename> <Num. figs per slide> #
# <file extension for figures>                                          #
#                                                                       #
# Example usage:                                                        #
# python writeBeamer.py MySlides 8 .png                                 #
#########################################################################


from sys import argv
import glob

script, filename, NUM_TILE, ext = argv

# NUM_TILE is the max number of figures on slide
# Recommended to use 8 at most

# ext is the flie extension for figures, include the dot "."

class tile:
    name = ""
    figs = []

    def __init__(self, name, figs):
        self.name = name
        self.figs = figs

    def addFig(self, fig):
        self.figs.append(fig)

    def writeTile(self, f):
        count = 0
        f.write("""
        \\begin{frame}{%s}
            \\begin{columns}
        """ % self.name )
        size = 2.0 / len(self.figs)
        height = 1.0
        width = 1.0
        if (size == 2.0):
            height = 0.8
            width = 0.9
        elif (len(self.figs) == 2):
            height = 0.8
            width = 0.45
        elif (len(self.figs) % 2 != 0):
            width = 2.0 / ( len(self.figs) + 1 )
            height = 0.35
        else:
            width = 2.0 / len(self.figs)
            height = 0.35

        for fig in self.figs:
            if (count % 2 == 0 or len(self.figs) == 2):
                f.write(""" \t\\column{%f\\linewidth}
                """ % width )
            f.write("""
                        \\begin{figure}
                            \\includegraphics[width = \\textwidth, height = %f\\textheight, keepaspectratio]{%s}
                        \\end{figure}
            """ % (height, fig) )
            count += 1
            # print fig
        f.write("""
                \\end{columns}
            \\end{frame}
        """)

def divide_chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

print "Writing new Beamer file %s.tex" % filename

with open("umn_template.tex",'r') as temp:
    with open(filename + ".tex", 'w') as f:
        for line in temp:
            if (line.find("\\end{document} ") == 0): continue
            f.write(line);

        l = []
        tiles = []

        for fig in glob.glob("../figures/*" + ext):
            l.append(fig)

        #print l

        l_div = list(divide_chunk( l, int(NUM_TILE) ))
        #print l_div

        for t in l_div:
            tiles.append(tile("Slide name", t))

        for t in tiles:
            t.writeTile(f)

        f.write("\\end{document}")
