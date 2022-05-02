### by shervin nia ###

import numpy as np
from scipy import ndimage, signal, misc
import sys
import starfile
import os
import pandas as pd
from alive_progress import alive_bar
import csv

def mult(x, n):
    return x * n

def unbin(df, unbinfac):

    df["rlnCoordinateX"] = df["rlnCoordinateX"].apply(mult, n = unbinfac)
    df["rlnCoordinateY"] = df["rlnCoordinateY"].apply(mult, n = unbinfac)
    
    return df

#################################################
###DEPRECATED FUNCTION, MIGHT DELETE LATER IDK###
#################################################

def zclear(dataframe, origPixSize, ZBinFac, IPD):
    pixDist = int(IPD / (origPixSize * ZBinFac))
    goodZ = np.arange(dataframe["rlnCoordinateZ"].min(), dataframe["rlnCoordinateZ"].max(), pixDist)
    print(dataframe)
    with alive_bar(int(dataframe.size)) as bar:
        for i in reversed(dataframe.index):
            print(i)
            if dataframe.iat[i,3] not in goodZ:
                dataframe.drop(int(i), axis = 0, inplace = True)
            bar()
    return dataframe


#################################################
############## PARAMETERS #######################
#################################################
directory = sys.argv[1]
coordsdirectory = sys.argv[2]
origPixelSize = float(1.57)       #original pixel size of tomogram, IN ANGSTROMS
ZBinFac = int(1)                 #binning factor of Z-direction of tomogram/slices
IPD = 100                         #interparticle distance in Z-direction IN ANGSTROMS


#imports coordinates file generated from SelVol script
coords = []
with open(str(coordsdirectory)+"coords.csv", 'r') as file:
    csvreader = csv.reader(file)
    coords=next(csvreader)

    minx = int(coords[0])
    print("MinX = " + str(minx))
    maxx = int(coords[1])
    print("MaxX = " + str(maxx))
    miny = int(coords[2])
    print("MinY = " + str(miny))
    maxy = int(coords[3])
    print("MaxY = " + str(maxy))
    

pixDist = int(IPD / (origPixelSize * ZBinFac)) 

##################################################
###GENERATE LIST OF ALL SLICE NUMBERS IN FOLDER###
##################################################

slicelist = []
for filename in os.listdir(directory):
    slicelist.append(int(filename.split('_')[0]))


############################################################################
###GENERATE LIST OF ALL DESIRED SLICES BASED ON MINIMUM PARTICAL DISTANCE###
############################################################################

goodZ = np.arange(min(slicelist), max(slicelist), pixDist)
print("minimum slice: " + str(min(slicelist)))
print("maximum slice: " + str(max(slicelist)))
print(goodZ)
print("pixDist: " + str(pixDist))


df = dict()
coords = pd.DataFrame({"rlnCoordinateX": [], "rlnCoordinateY": [], "rlnCoordinateZ": []})



##############################################
###ADD REQUESTED COORDINATES TO COORDS FILE###
##############################################

with alive_bar(len(os.listdir(directory))) as bar:
    for filename in os.listdir(directory):
        #print(filename)
        if int(filename.split('_')[0]) in goodZ:
            df[filename] = starfile.read(str(directory) + str(filename))
            df[filename].insert(2, "rlnCoordinateZ", int(filename.split('_')[0]), True)
            #for i in df[filename].index:
                #print("x to compare: " + str(int(df[filename].iat[i,0])) + "     y to compare: " + str(int(df[filename].iat[i, 1])))
                #if (minx < int(df[filename].iat[i,0]) < maxx) and (miny < int(df[filename].iat[i,1]) < maxy): 
                    #print("good point! adding " + str(int(df[filename].iat[i,0])) + " and " + str(int(df[filename].iat[i,1])) + " to file")
                    #print(df[filename].iloc([i]))
            coords = pd.concat([coords, df[filename][(df[filename]["rlnCoordinateX"] > minx) & (df[filename]["rlnCoordinateX"] < maxx) & (df[filename]["rlnCoordinateX"] > miny) & (df[filename]["rlnCoordinateX"] < maxy)]])
        bar()
    
coords.insert(0, "rlnTomoName", "Cry11b_WT_05", True)

############################################################
###DROP EXCESS COLUMNS (contains unimportant information)###
############################################################

coords.drop(coords.columns[[4, 5, 6]], axis=1, inplace = True)    

starfile.write(coords, "coords_tomo.star")
