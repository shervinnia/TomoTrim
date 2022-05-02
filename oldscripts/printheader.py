import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import mrcfile
import glob
from scipy import ndimage, signal, misc
from PIL import Image, ImageOps
import time
import sys

def header(input, outputname):
    with open(outputname + 'header.txt', 'w') as headobj:
        headobj.write(str(header))


with mrcfile.open('/data/shervinnia/PNNL/workingstacks/Cry11b-08-27-21_10min_PhasePlate/TrimmedTomograms_trimvoltest/01/Cry11b_10min_01_full_recSIRT_TRIMMED.mrc', mode='r+') as im:
    #header(im.header, '/data/shervinnia/PNNL/workingstacks/Cry11b-08-27-21_10min_PhasePlate/TrimmedTomograms_trimvoltest/01/slices/')
    im.print_header()
