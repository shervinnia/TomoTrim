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

def mult(x, n):
    return x * n


job = sys.argv[1]
origBin = sys.argv[2]
finalBin = sys.argv[3]
df = starfile.read(str(job))

unbinfac = int(origBin)/int(finalBin)


df["optics"]["rlnMicrographOriginalPixelSize"] = df["optics"]["rlnMicrographOriginalPixelSize"].apply(mult, n = 1/unbinfac)
df["optics"]["rlnImagePixelSize"] = df["optics"]["rlnImagePixelSize"].apply(mult, n = 1/unbinfac)
df["optics"]["rlnImageSize"] = df["optics"]["rlnImageSize"].apply(mult, n = unbinfac)
df["particles"]["rlnCoordinateX"] = df["particles"]["rlnCoordinateX"].apply(mult, n = unbinfac)
df["particles"]["rlnCoordinateY"] = df["particles"]["rlnCoordinateY"].apply(mult, n = unbinfac)


starfile.write(df, str(job[:-5] + "_binnedBy" + str(finalBin) + ".star"))
