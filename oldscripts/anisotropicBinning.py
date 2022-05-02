import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys
from skimage.measure import block_reduce
#from alive_progress import alive_bar

def slice(input, outputname, xybinfac, zbinfac):
    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
    slicestot = np.max(slices)
    with mrcfile.new(outputname + ".mrc") as mrc:
        mrc.set_data(block_reduce(input[:, :, :], block_size=(zbinfac, xybinfac, xybinfac),func=np.mean, func_kwargs={'dtype':np.float32}))
job = sys.argv[1]
xybinfac = sys.argv[2]
zbinfac = sys.argv[3]
with mrcfile.mmap(str(job), mode='r+') as im:
    slice(im.data, str(job) + str("_binXY") + str(xybinfac) + str("Z") + (zbinfac) , int(xybinfac), int(zbinfac))
