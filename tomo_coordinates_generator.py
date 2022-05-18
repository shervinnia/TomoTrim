
import numpy as np
from scipy import ndimage, signal, misc
import sys
import starfile
import os
import pandas as pd
import mrcfile
from alive_progress import alive_bar



########################
###### Parameters ######
########################

directory = sys.argv[1]
coords_file = sys.argv[2]
mrc_file = sys.argv[3]
pixelSize = float(1.57)
IPD = 70

pixDist = int(IPD / (pixelSize))
print(pixDist)


###################################
######### Import coords ###########
###################################

with open(coords_file) as coords_read:
    csv = coords_read.read()

minX = int(csv.split(',')[0])
maxX = int(csv.split(',')[1])
minY = int(csv.split(',')[2])
maxY = int(csv.split(',')[3])

print(f"MinX = {minX}")
print(f"MaxX = {maxX}")
print(f"MinY = {minY}")
print(f"MaxY = {maxY}")


##################################################
######## Create ndindex and convert to df ########
##################################################

coords = dict()

with mrcfile.mmap(mrc_file, mode='r') as im:
    ind = np.ndindex(int((maxX-minX)/IPD), int((maxY-minY)/IPD), int(np.min(im.data.shape)/IPD))


coords = pd.DataFrame(ind, columns=["rlnCoordinateX", "rlnCoordinateY", "rlnCoordinateZ"])


########################################
### Convert df to proper coords ########
########################################

coords = coords.mul(IPD)
coords["rlnCoordinateX"] = coords["rlnCoordinateX"].add(minX)
coords["rlnCoordinateY"] = coords["rlnCoordinateY"].add(minY)


coords.insert(0, "rlnTomoName", "Cry11b_WT_05", True)

starfile.write(coords, "coords_tomo.star")

