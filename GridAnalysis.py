import numpy as np
import pandas
from csv import writer
import os
from ast import literal_eval as make_tuple
from scipy.spatial import ConvexHull, distance_matrix, distance

# Imports coordinates of clusters from a QuantiFish cluster output file.
# Divides the source images into a grid of boxes, any boxes containing a point are considered positive.
# Also generates convex hull area for each set of clusters.

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


def gridtest(inputarray):
    positivecount = 0
    totalcount = 0

    arraylist = np.array_split(inputarray, splitfactory,0)
    arraycatcher = []
    for array in arraylist:
        subarrays = np.array_split(array, splitfactorx, 1)
        arraycatcher.append(subarrays)

    for arrayset in arraycatcher:
        for subarray in arrayset:
            totalcount += 1
            if np.max(subarray):
                positivecount += 1
    return positivecount, totalcount

def headers(savefile):
    headings = ('File Name', 'Total Objects', 'Box Size', 'Total Grid Boxes', 'Positive Grid Boxes', 'Convex Hull Area', 'Furthest Points Distance')
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
    outputfile = "C:/Users/daves/Desktop/Test Stage/New/" + inputfile[-12:-4] + "_testing.csv"
    # Setup data export
    headers(outputfile)
    # Cycle fish images and generate coordinate list
    for imagename, miniframe in dataframe.groupby('File'):
        listcoords = miniframe['Cluster Location'].tolist()
        listcoords = [make_tuple(coord) for coord in listcoords]
        mappedcoords = mapcoords(listcoords)
        convexhullarea, eucdist = findconvexhull(listcoords)
        totalpoints = len(listcoords)
        plottedpoints = np.sum(mappedcoords)
        positives, boxes = gridtest(mappedcoords)
        resultpack = (imagename, totalpoints, numpixels, boxes, positives, convexhullarea, eucdist)
        datawriter(outputfile, resultpack)
        print("Completed analysis of:")
        print(imagename)

    print("Analysis Complete")

def findconvexhull(coords):
    # Add coords to array
    if len(coords) > 2:
        test = np.array(coords)
        hull = ConvexHull(test)
        # Restrict test points to those around the hull to minimise work.
        candidates = test[hull.vertices]
        dist_mat = distance_matrix(candidates, candidates)
        i, j = np.unravel_index(dist_mat.argmax(), dist_mat.shape)
        maxdist = distance.euclidean(candidates[i], candidates[j])
        return hull.area, maxdist
    elif len(coords) == 2:
        test = np.array(coords)
        maxdist = distance.euclidean(test[0], test[1])
        return "Insufficient points", maxdist
    else:
        return "Insufficient points", "Insufficient Points"


# Set initial parameters
#imxdim = 1392
#imydim = 1040
# Parameters for Hermes Images
imxdim = 4801
imydim = 1040

numpixels = 50
# Deduce number of array splits needed
splitfactory = int(imydim/numpixels)
splitfactorx = int(imxdim/numpixels)
# Split does y first

for root, dirs, files in os.walk("C:\\Users\\daves\\Desktop\\Test Stage\\Clustering\\Hermes\\"):
    for f in files:
        do_analysis(os.path.normpath(os.path.join(root,f)))
        print("Completed file:")
        print(f)

