### by shervin nia ###

import numpy as np
from scipy import ndimage, signal, misc
import sys
import starfile
import os
import pandas as pd
from alive_progress import alive_bar

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


directory = sys.argv[1]
origPixelSize = float(1.57)       #original pixel size of tomogram, IN ANGSTROMS
ZBinFac = int(1)                 #binning factor of Z-direction of tomogram/slices
IPD = 100                         #interparticle distance in Z-direction IN ANGSTROMS

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
        if int(filename.split('_')[0]) in goodZ:
            df[filename] = starfile.read(str(directory) + str(filename))
            df[filename].insert(2, "rlnCoordinateZ", int(filename.split('_')[0]), True)
            coords = pd.concat([coords, df[filename]])
        bar()
    
coords.insert(0, "rlnTomoName", "Cry11b_WT_05", True)

############################################################
###DROP EXCESS COLUMNS (contains unimportant information)###
############################################################

coords.drop(coords.columns[[4, 5, 6]], axis=1, inplace = True)    

starfile.write(coords, "coords_tomo.star")
