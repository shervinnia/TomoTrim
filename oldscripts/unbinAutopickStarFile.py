import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys
import starfile
import os
from alive_progress import alive_bar

def mult(x, n):
    return x * n

def unbin(df, unbinfac, zUnbinFac):

    df["rlnCoordinateX"] = df["rlnCoordinateX"].apply(mult, n = unbinfac)
    df["rlnCoordinateY"] = df["rlnCoordinateY"].apply(mult, n = unbinfac)
    df["rlnCoordinateZ"] = df["rlnCoordinateZ"].apply(mult, n = zUnbinFac)
    
    return df


origBin =   sys.argv[1]
finalBin =  sys.argv[2]
zOrigBin =  sys.argv[3]
zFinalBin = sys.argv[4]
output =    sys.argv[5]
directory = sys.argv[6]


unbinfac = int(origBin)/int(finalBin)
zUnbinFac = int(zOrigBin)/int(zFinalBin)

with alive_bar(len(os.listdir(directory))) as bar:
    for filename in os.listdir(directory):
        df = starfile.read(str(directory) + str(filename))
        starfile.write(unbin(df, unbinfac, zUnbinFac), filename)
        del df
        bar()
