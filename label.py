#!/usr/bin/python3
import os
import glob
import cv2
import sys

if (os.path.exists('label') == False):
    os.makedirs('label') #Create folder

files = os.listdir("char")   
for filename in files:
    filename_ts = filename.split(".")[0]
    patt = "label/{}_*".format(filename_ts)
    saved_num = len(glob.glob(patt))
    if saved_num == 1:
        print("{} done".format(patt))
        continue
    filepath = os.path.join("char", filename)
    im = cv2.imread(filepath)
    cv2.imshow("image", im)
    key = cv2.waitKey(0)
    
    if key == 27:
        sys.exit()
    if key == 13:
        os.remove(filepath)
        continue
    char = chr(key)
    filename_ts = filename.split(".")[0]
    outfile = "{}_{}.jpg".format(filename_ts, char)
    outpath = os.path.join("label", outfile)
    cv2.imwrite(outpath, im)    