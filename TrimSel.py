import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps, ImageTk
import time
import sys
from alive_progress import alive_bar
import tkinter as tk
import csv

#/backup/jargroup/segmentationTesting/Cry11b_10min_07_full.rec

#function for displaying averagedpng written by martineau on stackoverflow
topx, topy, botx, boty = 0, 0, 0, 0
rectid = None
imagesizeX = 1000
ratio = None

def replace_ending(sentence, old, new):
    if sentence.endswith(old):
        return sentence[:-len(old)] + new
    return sentence

def trim(input, outputname, minx, maxx, miny, maxy):
    sizex = maxx - minx
    sizey = maxy - miny

    with mrcfile.new_mmap(outputname, shape=(input.shape[1], sizey, sizex), mrc_mode=2, overwrite=True) as mrc:
        print("new file successfully mapped")
        slices = np.arange(0, input.shape[1], 1)
#the following "with" loop is for a progress bar
        with alive_bar(input.shape[1]) as bar:
            for slice in slices:
                mrc.data[slice, :, :] = input[miny:maxy, slice, minx:maxx]
                bar()
        print("trimming completed!")

inputpath = sys.argv[1]
directory = sys.argv[2]
outputname = replace_ending(str(inputpath), "full_rec.mrc", "rec.mrc")
print("Welcome to Trimvol.py!")

coords = []
with open(str(directory)+"coords.csv", 'r') as file:
    csvreader = csv.reader(file)
    coords=next(csvreader)

t = time.time()
with mrcfile.mmap(inputpath, mode='r+') as im:
    minx = int(coords[0])
    print("MinX = " + str(minx))
    maxx = int(coords[1])
    print("MaxX = " + str(maxx))
    miny = int(coords[2])
    print("MinY = " + str(miny))
    maxy = int(coords[3])
    print("MaxY = " + str(maxy))
    trim(im.data, outputname, minx, maxx, miny, maxy)
print("trimming completed in " + str(int(time.time() - t)) + "seconds")
