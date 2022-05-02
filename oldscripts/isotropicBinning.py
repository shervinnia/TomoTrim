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

def slice(input, outputname, binfac):
    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
    slicestot = np.max(slices)
    with mrcfile.new(outputname + ".mrc") as mrc:
        mrc.set_data(block_reduce(input[:, :, :], block_size=(binfac, binfac, binfac),func=np.mean, func_kwargs={'dtype':np.float32}))
job = sys.argv[1]
binfac = sys.argv[2]
with mrcfile.mmap(str(job), mode='r+') as im:
    slice(im.data, str(job) + str("_iso") + str(binfac) + str("xbin"), int(binfac))
