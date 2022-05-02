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
from alive_progress import alive_bar

def slice(input, outputname, binfac):
    input = np.rot90(input, axes=(0, 1))
    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
    slicestot = np.max(slices)
    with alive_bar(int(slicestot)) as bar:
        for slice in slices:
            with mrcfile.new(str(str(slice) + ".mrc")) as mrc:
                mrc.set_data(block_reduce(input[slice, :, :], block_size=(binfac, binfac),func=np.mean, func_kwargs={'dtype':np.float32}))
            #print("finished slice " + str(slice) + " of " + str(slicestot))
            bar()
job = sys.argv[1]
binfac = sys.argv[2]
with mrcfile.mmap(str(job), mode='r+') as im:
    slice(im.data, str(job), int(binfac))
