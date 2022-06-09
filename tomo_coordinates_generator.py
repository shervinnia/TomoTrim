
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

coords_file = sys.argv[1]
mrc_file = sys.argv[2]
pixelSize = float(1.57)
IPD = 70
IPDpix = int(np.multiply(IPD,pixelSize))
print(IPDpix)
totalpoints = 15000
N = 1  # only keep every N point from generated grid
minZ = 1500
maxZ = 4500


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
    print(int((maxX-minX)/IPDpix))
    print(int((maxY-minY)/IPDpix))
    print(int(np.min(im.data.shape)/IPDpix))
    print(im.data.shape)
    ind = np.ndindex(int((maxX-minX)/IPDpix), int((maxY-minY)/IPDpix), int((im.data.shape[0])/IPDpix))


coords = pd.DataFrame(ind, columns=["rlnCoordinateX", "rlnCoordinateY", "rlnCoordinateZ"])





########################################
### Convert df to proper coords ########
########################################

coords = coords.mul(IPD)
coords["rlnCoordinateX"] = coords["rlnCoordinateX"].add(minX)
coords["rlnCoordinateY"] = coords["rlnCoordinateY"].add(minY)


### Get rid of all points outside of acceptable Z range ###
coords = coords[coords['rlnCoordinateZ'] < maxZ]
coords = coords[coords['rlnCoordinateZ'] > minZ]

coords = coords[coords.reset_index().index % int(N) == 0]

coords.insert(0, "rlnTomoName", "Cry11b_WT_05", True)

starfile.write(coords, "coords_tomo.star")

