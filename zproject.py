import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys
from alive_progress import alive_bar

def slice(input, outputname):

    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
#    with mrcfile.new(str(job) + "zproj.mrc") as mrc:
#        mrc.set_data(np.zeros((input.shape[1],input.shape[2]), dtype=np.float32))
#        with alive_bar(input.shape[1]) as bar:
#        for slice in slices:
#            mrc.data[:,:] = mrc.data[:,:] + input[slice, : , :]
#            bar()
#        mrc.data[:,:] = mrc.data[:,:] / input.shape[2]
    with mrcfile.new(str(job) + "zmean.mrc") as mrc:
        mrc.set_data(np.zeros((input.shape[1],input.shape[2]), dtype=np.float32))
        mrc.data[:,:] = np.mean(input[:,:,:], axis=0)
    with mrcfile.new(str(job) + "zmedian.mrc") as mrc:
        mrc.set_data(np.zeros((input.shape[1],input.shape[2]), dtype=np.float32))
        mrc.data[:,:] = np.median(input[:,:,:], axis=0)
job = sys.argv[1]
with mrcfile.mmap(job, mode='r') as im:
    slice(im.data, str(job))
