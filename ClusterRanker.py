import numpy as np
import pandas
from csv import writer
import os

# Imports a QuantiFish cluster output file. Sorts clusters by size (Descending) and calculates cumulative fluorescence.

def headers(savefile):
    headings = ('File Name', 'Cluster ID', 'Cluster Intensity', 'Percent Intensity', 'Cumulative Intensity',
                'Cumulative Percent Intensity')
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
    outputfile = "C:/Users/daves/Desktop/Test Stage/New/" + inputfile[-12:-4] + "_clustersort.csv"
    # Setup data export
    headers(outputfile)
    # Cycle fish images and generate coordinate list
    for imagename, miniframe in dataframe.groupby('File'):
        listintensities = miniframe['Integrated Intensity'].tolist()
        listintensities.sort(reverse=True)
        totalfluor = sum(listintensities)
        percentlist = [point/totalfluor*100 for point in listintensities]
        cumulativelist = np.cumsum(listintensities)
        cumulativepercent = np.cumsum(percentlist)
        for i in range(len(listintensities)):
            resultpack = (imagename, i+1, listintensities[i], percentlist[i], cumulativelist[i], cumulativepercent[i])
            datawriter(outputfile, resultpack)
        print("Completed sorting of:")
        print(imagename)

    print("Operations Complete")




for root, dirs, files in os.walk("C:\\Users\\daves\\Desktop\\Test Stage\\Clustering\\Leica\\"):
    for f in files:
        do_analysis(os.path.normpath(os.path.join(root, f)))
        print("Completed file:")
        print(f)
