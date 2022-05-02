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

#/backup/jargroup/segmentationTesting/Cry11b_10min_07_full.rec

#function for displaying averagedpng written by martineau on stackoverflow
topx, topy, botx, boty = 0, 0, 0, 0
rectid = None
imagesizeX = 1000
ratio = None
def selector(WIDTH, HEIGHT, path):
    global ratio
    global topx, topy, botx, boty
    global rectid
    global imagesizeX

    #this function is called to get the top-left corner of the rectangle on mouse click
    def get_mouse_posn(event):
        global topy, topx

        topx = event.x
        topy = event.y
    #this function is called to get the bottom-right corner of the rectangle on mouse click-and-move
    def update_sel_rect(event):
        global rectid
        global topy, topx, botx, boty

        botx, boty = event.x, event.y
        canvas.coords(rectid, topx, topy, botx, boty)

    #create and store ratio for resizing image to screen
    ratio = imagesizeX/WIDTH
    imagesizeY = int(HEIGHT*ratio)

    window = tk.Tk()
    window.title("Select Area")
    window.geometry('%sx%s' % (imagesizeX, imagesizeY))
    window.configure(background='grey')
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print("RATIO IS "+str(ratio))
    print("WIDTH IS "+str(WIDTH))
    print("HEIGHT IS "+str(HEIGHT))
    print("IMAGESIZEX IS "+str(imagesizeX))
    print("IMAGESIZEY IS "+str(imagesizeY))
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    #open and resize image to previously discovered values
    img = Image.open(path)
    img = img.resize((imagesizeX,imagesizeY))
    img = ImageTk.PhotoImage(img)
    print("IMG.WIDTH IS "+str(img.width()))
    print("IMG.HEIGHT IS "+str(img.height()))

    canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                       borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True)
    canvas.img = img  # Keep reference in case this code is put into a function.
    canvas.create_image(0, 0, image=img, anchor=tk.NW)

    # Create selection rectangle (invisible since corner points are equal).
    rectid = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline='white')
    canvas.bind('<Button-1>', get_mouse_posn)
    canvas.bind('<B1-Motion>', update_sel_rect)

    window.mainloop()



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
outputname = sys.argv[2]
print("Welcome to Trimvol.py!")
t = time.time()
with mrcfile.mmap(inputpath, mode='r+') as im:
    selector(im.data.shape[2], im.data.shape[0], inputpath+'.png')
    minx = int(topx/ratio)
    print("MinX = " + str(minx))
    maxx = int(botx/ratio)
    print("MaxX = " + str(maxx))
    miny = int(topy/ratio)
    print("MinY = " + str(miny))
    maxy = int(boty/ratio)
    print("MaxY = " + str(maxy))
    trim(im.data, outputname, minx, maxx, miny, maxy)
print("trimming completed in " + str(int(time.time() - t)) + "seconds")
