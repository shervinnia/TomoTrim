import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys
import math
from skimage.measure import block_reduce
#import skimage as ski
#from alive_progress import alive_bar

def slice(input, outputname, binfac):
    
    print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
    slices = np.arange(0, input.shape[0], 1)
    print("total slices = " + str(slices))
    slicestot = np.max(slices)
    newmrc = block_reduce(input[:, :, :], block_size=(binfac, binfac, binfac),func=np.mean, func_kwargs={'dtype':np.float32})
    #with mrcfile.new_mmap(outputname, shape=[math.ceil(i/binfac) for i in input.shape]) as mrc:

    #for i in input.shape()[2]:
    #    newmrc[:,:,i] = block_reduce(input[:,:,i],block_size=(binfac,binfac),func=np.mean, func_kwargs={'dtype',np.float32})

    #newmrc = block_reduce(newmrc,block_size=(1,1,binfac),func=np.mean,func_kwargs={'dtype',np.float32})

    with mrcfile.new(outputname) as mrc:
        #mrc.set_data(block_reduce(input[:, :, :], block_size=(binfac, binfac, binfac),func=np.mean, func_kwargs={'dtype':np.float32}))
        mrc.set_data(newmrc)
job = sys.argv[1]
#acjob = job.split('.')[0]
binfac = sys.argv[2]
with mrcfile.mmap(str(job), mode='r+') as im:
    slice(im.data, f"{job.split('.')[0]}_iso{binfac}xbin.mrc", int(binfac))
    #slice(im.data, str(job) + str("_iso") + str(binfac) + str("xbin"), int(binfac))
