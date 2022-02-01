import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import matplotlib as mpl
import mrcfile
import glob
from scipy import ndimage, signal, misc
from dask import delayed
from PIL import Image, ImageOps
import time
import sys

# 2DFT and inverse
def fft2c(f):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(f)))

def ifft2c(F):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))

def rotate(array):
    return(np.swapaxes(array, 0, 1))

#Bin the array input
def bin(input, factor):
    array = rotate(input)
    for i in range(1, (array.shape[2] - 1)):
        imsliceraw = I[:, :, i-1]
        binned[:, :, i] = imsliceraw.reshape(array.shape[0] // factor, factor, array.shape[1] // factor, factor)
    return binned

def plotter(input):
     I = rotate(input)
#     I = input
     for i in range(1, (I.shape[2] - 1)):
        imslice = I
    #   below line is for low pass filtering the tomogram
    #   currently this causes some weird shit to happen, idk why yet
    #    imslice = ndimage.gaussian_filter(imsliceraw, sigma = 1)
        img_fft = fft2c(imslice)
        plt.subplot(1,2,1)
        plt.imshow(imslice, cmap='gray')
        plt.subplot(1,2,2)
        plt.imshow(np.log(np.abs(img_fft) + 1e-6), cmap='gray')
        plt.show()

def displayslice(input):
    plt.imshow(input[:, 500, :], cmap='gray')
    plt.show()

def avgslices(input):
    avg = np.zeros((input.shape[0],input.shape[2]))
    #slices = np.linspace(1,input.shape[1], num=100, dtype=int)
    halfpoint = int(input.shape[1]/2)
    span = 100
    slices = np.arange(halfpoint-span,halfpoint+span,100)
    #slice = 500
    for slice in slices:
        #avg = avg + np.flip(input[:, slice, :], axis=0)
        print("Adding slice " + str(slice))
        #avg = avg + np.flip(input[:, slice, :], axis=1)
        avg = avg + input[:, slice, :]
        print("done")
    print("Processing averaged image...")
    imout = avg/slice
    imout = imout - np.min(np.min(imout))
    imout = imout * 256/np.max(np.max(imout))
    print("done")
#    imout[1000:2000, 1000:2000] = 256

#    plt.imshow(imout, cmap='gray')
#    plt.show()

    return(imout)


def plotslice(input):
#     I = rotate(input)
#     I = input
     imslice = input
#   below line is for low pass filtering the tomogram
#   currently this causes some weird shit to happen, idk why yet
#    imslice = ndimage.gaussian_filter(imsliceraw, sigma = 1)
     img_fft = fft2c(imslice)
     plt.subplot(1,2,1)
     plt.imshow(imslice, cmap='gray')
     plt.subplot(1,2,2)
     plt.imshow(np.log(np.abs(img_fft) + 1e-6), cmap='gray')
     plt.show()

#im = delayed(mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc'))
#im = mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc')
#'/backup2/jargroup/batchtest/08-27_10min/Cry11b_10min_01/Cry11b_10min_01_full_recSIRT.mrc'
job = sys.argv[1]
outputname = str(job+".png")
print("Welcome to AvgSlices.py!")
t = time.time()
with mrcfile.mmap(job, mode='r') as im:
    print("input file successfully mapped")
    #im.data = np.flip(im.data, axis=2)
    imout = avgslices(im.data)
    print("saving output file: " + str(outputname))
    image.imsave(outputname, imout, cmap = 'gray')
    print("done")
#print(im.data.shape)
print("slice average created in " + str(int(time.time() - t)) + " seconds")
#plt.imshow(imout, cmap='gray')
#plt.style.use('seaborn')
#plt.imshow(figsize=(12,16))
#plt.show()
