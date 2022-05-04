
import numpy as np
from scipy import ndimage, signal, misc
import sys
import starfile
import os
import pandas as pd
from alive_progress import alive_bar



########################
###### Parameters ######
########################

directory = sys.argv[1]
coords_file = sys.argv[2]
pixelSize = float(1.57)
IPD = 70

pixDist = int(IPD / (pixelSize))

coords_read = open(coords_file,"r")
csv = coords_read.readlines()

minX = int(csv.split(',')[0])
maxX = int(csv.split(',')[1])
minY = int(csv.split(',')[2])
maxY = int(csv.split(',')[3])

print("MinX = " + str(minX))
print("MaxX = " + str(maxX))
print("MinY = " + str(minY))
print("MaxY = " + str(maxY))



df = dict()
coords = pd.DataFrame({"rlnCoordinateX": [], "rlnCoordinateY": [], "rlnCoordinateZ": []})

df["rlnCoordinateX"].update(pd.Series(np.arange(minX, maxX, pixDist)))
df["rlnCoordinateX"].update(pd.Series(np.arange(minX, maxX, pixDist)))
