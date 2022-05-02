import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys


# 2DFT and inverse
def fft2c(f):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(f)))


def ifft2c(F):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))


def rotate(array):
    return (np.swapaxes(array, 0, 1))


# Bin the array input
def bin(input, factor):
    array = rotate(input)
    for i in range(1, (array.shape[2] - 1)):
        imsliceraw = I[:, :, i - 1]
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
        plt.subplot(1, 2, 1)
        plt.imshow(imslice, cmap='gray')
        plt.subplot(1, 2, 2)
        plt.imshow(np.log(np.abs(img_fft) + 1e-6), cmap='gray')
        plt.show()


def displayslice(input):
    plt.imshow(input[:, 500, :], cmap='gray')
    plt.show()


def plotslice(input):
    I = rotate(input)
    #     I = input
    imslice = I
    #   below line is for low pass filtering the tomogram
    #   currently this causes some weird shit to happen, idk why yet
    #    imslice = ndimage.gaussian_filter(imsliceraw, sigma = 1)
    img_fft = fft2c(imslice)
    plt.subplot(1, 2, 1)
    plt.imshow(imslice, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.imshow(np.log(np.abs(img_fft) + 1e-6), cmap='gray')
    plt.show()


def trim(input, outputname, minx, maxx, miny, maxy):
    sizex = maxx - minx
    sizey = maxy - miny
#    print(miny)
#    print(maxy)
#    print(sizey)
#    print(maxy - miny)
#    print(np.shape(input[:, :, :]))
#    print(np.shape(np.flip(np.swapaxes(np.swapaxes(input[:, miny:maxy, minx:maxx], 1, 2), 0, 1))))

    with mrcfile.new_mmap(outputname, shape=(input.shape[1], sizey, sizex), mrc_mode=2) as mrc:
        print("new file successfully mapped")
        slices = np.arange(0, input.shape[1], 1)
#        print(input.shape[1])
#        print(slices)
        for slice in slices:
#          print(slice)
            print("mapping slice " + str(slice))
#            mrc.data[slice, :, :] = np.flip(input[miny:maxy, slice, minx:maxx], axis=1)
            mrc.data[slice, :, :] = input[miny:maxy, slice, minx:maxx]
            print("done")
        print("trimming completed!")
 #           print(np.flip(input[miny:maxy, slice, minx:maxx], axis=1))
 #           print(' ')
 #           print(mrc.data[slice, :, :])
     #   print("trimmed vol is " + str(np.dtype.type(mrc.data[10])))


#    mrc.data[:, :, :] = np.flip(np.swapaxes(input[miny:maxy, : , minx:maxx], 0, 1), axis = 1)
# im = delayed(mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc'))
# im = mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc')
# '/backup2/jargroup/batchtest/08-27_10min/Cry11b_10min_01/Cry11b_10min_01_full_recSIRT.mrc'

input = sys.argv[1]
outputname = sys.argv[2]
print("Welcome to Trimvol.py!")
minx = int(sys.argv[3])
print("MinX = " + str(minx))
maxx = int(sys.argv[4])
print("MaxX = " + str(maxx))
miny = int(sys.argv[5])
print("MinY = " + str(miny))
maxy = int(sys.argv[6])
print("MaxY = " + str(maxy))
t = time.time()
with mrcfile.mmap(input, mode='r+') as im:
    trim(im.data, outputname, minx, maxx, miny, maxy)
# print(im.data.shape)
print("trimming completed in " + str(int(time.time() - t)) + "seconds")
#print("original vol is " + str(np.dtype.type(im.data[10])))
