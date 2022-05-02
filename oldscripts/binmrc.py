import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import image
import mrcfile
#import glob
#from scipy import ndimage, signal, misc
#from PIL import Image, ImageOps
#import time
import sys
from skimage.measure import block_reduce
#from alive_progress import alive_bar

#def slice(input, outputname, binfac):
    #input = np.rot90(input, axes=(0, 1))
    #print("input shape = " + str(input.shape[0]) + ' ' + str(input.shape[1]) + ' ' + str(input.shape[2]))
  #  with mrcfile.new(str(str(outputname) + "_bin" + str(binfac) + ".mrc")) as mrc:
     #   mrc.set_data(block_reduce(input, block_size=(binfac, binfac),func=np.mean))
        #mrc.set_data(block_reduce(input, block_size=(binfac, binfac),func=np.mean, func_kwargs={'dtype':np.float32}))
            #print("finished slice " + str(slice) + " of " + str(slicestot))
            
def bin(im, job, binfac):
    with mrcfile.new(str(str(job) + "_bin" + str(binfac) + ".mrc")) as mrc:
        mrc.set_data(block_reduce(im[:,:], block_size=(binfac, binfac),func=np.mean))            
            
            
job = sys.argv[1]
binfac = sys.argv[2]
with mrcfile.mmap(str(job), mode='r+') as im:
    bin(im.data, str(job), int(binfac))
    

