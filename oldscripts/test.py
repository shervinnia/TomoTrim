import numpy as np
import matplotlib.pyplot as plt
import mrcfile
from scipy import ndimage, signal
from dask import delayed
from PIL import Image, ImageOps

# 2DFT and inverse
def fft2c(f):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(f)))

def ifft2c(F):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(F)))

def fftfreq(input):
    return np.fft.fftfreq(input.size, 10)

def rotate(array):
    slice = array[:, 500, :]
    plt.imshow(slice, cmap='gray')
    plt.show()

def avgslices(input):
    avg = np.zeros((input.shape[0],input.shape[2]))
    #slices = np.linspace(1,input.shape[1], num=100, dtype=int)
    slices = np.arange(1,input.shape[1],200)
    #slice = 500
    for slice in slices:
        avg = avg + input[:, slice, :]
    imout = avg/slice
    imout = imout - np.min(np.min(imout))
    imout = imout * 256/np.max(np.max(imout))
#    imout = signal.wiener(imout)
#    imout[1000:2000, 1000:2000] = 256
    plt.imshow(imout, cmap='gray')
    plt.show()
    return(imout)

 def trim(input, minx, maxx, miny, maxy):
    sizex = maxx - minx
    sizey = maxy - miny

    mrc = mrcfile.new_mmap(outputname + '_trimmed.mrc', (sizex, sizey, input.shape[1]))
    mrc.data = np.swapaxes(input[minx:maxx, :, miny:maxy], 1, 2)
    mrcfile.close()

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

#im = delayed(mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc'))
#im = mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-07-02-21/05/Cry11b_05_rec.mrc')
job = sys.argv[1]
outputname = sys.argv[2]
t = time.time()
with mrcfile.mmap(job, mode='r') as im:
    #average(im.data)
    imout = avgslices(im.data)
    image.imsave(outputname, imout, cmap = 'gray')
#print(im.data.shape)
print(str(int(time.time() - t)) + "seconds")
