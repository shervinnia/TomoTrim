import numpy as np
import matplotlib.pyplot as plt
import mrcfile
import glob
from scipy import ndimage
from dask import delayed
from PIL import Image, ImageOps

# 2DFT and inverse
def fft2c(f):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(f)))

def ifft2c(F):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))

def rotate(array):
    return(np.swapaxes(array, 0, 2))

#Bin the array input
def bin(input, factor):
    array = rotate(input)
    for i in range(1, (array.shape[2] - 1)):
        imsliceraw = I[:, :, i-1]
        binned[:, :, i] = imsliceraw.reshape(array.shape[0] // factor, factor, array.shape[1] // factor, factor)
    return binned

def plotter(input):
    I = rotate(input)
    for i in range(1, (I.shape[2] - 1)):
        imsliceraw = I[:, :, i]
    #   below line is for low pass filtering the tomogram
    #   currently this causes some weird shit to happen, idk why yet
        imslice = ndimage.gaussian_filter(imsliceraw, sigma = 1)
        img_fft = fft2c(imslice)
        plt.subplot(1,2,1)
        plt.imshow(imslice, cmap='gray')
        plt.subplot(1,2,2)
        plt.imshow(np.log(np.abs(img_fft) + 1e-6), cmap='gray')
        plt.show()

def histogram(input):
    input = np.ndarray.flatten(input)
    plt.hist(input, bins=32)
    plt.show()

def segment(input):
    sd = np.std(input)
    mean = np.mean(input)
    threshold = mean - 2.5*sd
    input[input>threshold]=0
    return input


    #for nx in input.shape[0]:
    #    for ny in input.shape[1]:
    #        for nz in input.shape[2]:
    #            if input[nx, ny, nz] < threshold
    #                input[nx, ny, nz] = 0

#im = delayed(mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc'))
#im = mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc')
with mrcfile.open('/data/shervinnia/PNNL/workingstacks/TrimmedTomograms_trimvoltest/01/Cry11b_10min_01_full_recSIRT_TRIMMED.mrc', mode = 'r+') as im:
     segment(im.data)
