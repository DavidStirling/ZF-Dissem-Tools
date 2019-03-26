import numpy as np
import pandas
from csv import writer
import os
from math import hypot
from ast import literal_eval as make_tuple
from itertools import combinations

# Imports coordinates of clusters from a QuantiFish cluster output file.
# Generates the sum of distances between all possible pairs of coordinates

# For testing array shape with real image
#inputarray = Image.open("C:\\Users\\daves\\Desktop\\Test Stage\\2017-2-7_WTMm400_Series011_ch00.tif")
#inputarray = np.array(inputarray)



def mapcoords(inputlist):
    # Generate blank array same shape as original image
    blankimage = np.zeros((imydim, imxdim), dtype=bool)
    for coord in inputlist:
        y, x = coord
        blankimage[y,x] = True
    print("Coordinates written successfully")
    return blankimage


def headers(savefile):
    headings = ('File Name', 'Total Objects', 'Number of Pairs', 'Sum of Distances')
    with open(savefile, 'w', newline="\n", encoding="utf-8") as f:
        writer(f).writerow(headings)
        print("Output file created successfully")


# Exports data to csv file
def datawriter(savefile, savedata):
    try:
        with open(savefile, 'a', newline="\n", encoding="utf-8") as f:
            writer(f).writerow(savedata)
    except Exception as e:
        print(e)



def do_analysis(inputfile):
    # Import data from file
    dataframe = pandas.read_csv(inputfile)
    outputfile = "C:/Users/daves/Desktop/Test Stage/New/R2/" + inputfile[-12:-4] + "_sumtest.csv"
    # Setup data export
    headers(outputfile)
    # Cycle fish images and generate coordinate list
    for imagename, miniframe in dataframe.groupby('File'):
        listcoords = miniframe['Cluster Location'].tolist()
        listcoords = [make_tuple(coord) for coord in listcoords]
        mappedcoords = mapcoords(listcoords)
        numdistances, totaldistance = sumdistances(listcoords)
        totalpoints = len(listcoords)
        plottedpoints = np.sum(mappedcoords)
        resultpack = (imagename, totalpoints, numdistances, totaldistance)
        datawriter(outputfile, resultpack)
        print("Completed analysis of:")
        print(imagename)

    print("Analysis Complete")


def sumdistances(coords):

    if len(coords) >= 2:
        def distance(coord1, coord2):
            """Euclidean distance between two points."""
            x1, y1 = coord1
            x2, y2 = coord2
            return hypot(x2 - x1, y2 - y1)

        listdistances = [distance(*combo) for combo in combinations(coords, 2)]
        numcomparisons = len(listdistances)
        sumcomparisons = sum(listdistances)
    else:
        numcomparisons = 0
        sumcomparisons = 0
    return numcomparisons, sumcomparisons

# Set initial parameters
#imxdim = 1392
#imydim = 1040
# Parameters for Hermes Images
imxdim = 4801
imydim = 1040



#for root, dirs, files in os.walk("C:\\Users\\daves\\Desktop\\Test Stage\\Clustering\\Hermes\\New\\"):
for root, dirs, files in os.walk("C:\\Users\\daves\\Desktop\\Test Stage\\Clustering\\Leica\\"):
    for f in files:
        do_analysis(os.path.normpath(os.path.join(root,f)))
        print("Completed file:")
        print(f)

