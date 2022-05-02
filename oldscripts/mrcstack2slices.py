import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys

def slice(input, outputname):

    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
    for slice in slices:
        print("starting slice " + str(slice))
        with mrcfile.new(str(str(slice) + ".mrc")) as mrc:
            mrc.set_data(np.zeros((input.shape[1],input.shape[2]), dtype=np.float32))
            mrc.data[:, :] = input[slice, :, :]
            print("finished slice " + str(slice))
job = sys.argv[1]
with mrcfile.open(str(job), mode='r+') as im:
    slice(im.data, str(job))
