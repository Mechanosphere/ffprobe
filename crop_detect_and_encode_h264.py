#!/usr/bin/python
import os, sys, subprocess, shlex, re, fnmatch, collections
import shutil
from os.path import basename
from subprocess import call
from subprocess import Popen, PIPE
import datetime
from collections import Counter



# GLOBAL VARIABLES

CROP_DETECT_LINE = "crop="
src_dir = "/Volumes/IDMOSAN/Litterbox/_Jon/incoming"
dest_dir = "/Volumes/IDMOSAN/Litterbox/_Jon/incoming/blackDetect"
output_dir = "/Volumes/IDMOSAN/Litterbox/_Jon/incoming/Done"







def findMoveFile(src_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.startswith('.'):
                print "file is not ready yet"
            elif file.endswith(('.mp4', '.mov', '.mxf', '.mpg')):
                #print "moving %s " % file
                #shutil.move(os.path.join(root, file), os.path.join(dest_dir, file))
                global fpath
                fpath = os.path.join(src_dir, file)
                base = os.path.basename(fpath)
                print "base: %s" % base 
                basefname = os.path.splitext(base)[0] + "_cropped.mp4"
                print "basefname: %s" % basefname 
                global output_fname
                output_fname = output_dir + "/" + basefname
                print "out_fname: %s" % output_fname
                print "fpath = %s " % fpath
                detectCropFile(fpath)
            elif file.endswith('.xml'):
                print "found xml"
            else:
                print "no suitable files found"

# GLOBAL FUNCTIONS - crop detect
def detectCropFile(fpath):
    #fpath = "/Users/mathiesj/desktop/USUV70904030.mpg"
    print "File to detect crop: %s " % fpath
    try:
        p = subprocess.Popen(["ffmpeg", "-i", fpath, "-vf", "cropdetect=24:16:0", "-vframes", "500", "-f", "rawvideo", "-y", "/dev/null"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        infos = p.stderr.read()
        print infos
        allCrops = re.findall(CROP_DETECT_LINE + ".*", infos)
        print allCrops 
        mostCommonCrop = Counter(allCrops).most_common(1)
        print "most common crop: %s" % mostCommonCrop
        print mostCommonCrop[0][0]
        global crop
        crop = mostCommonCrop[0][0]
        cropAndEncode(fpath, output_fname)
    except subprocess.CalledProcessError:
        print "crop detect error"
    


def cropAndEncode(fpath, output_fname):
    #fpath = "/Users/mathiesj/desktop/USUV70904030.mpg"
    print "File to encode: %s " % fpath
    try:
        p = subprocess.Popen(["ffmpeg", "-i", fpath, "-vf", crop, "-codec:v", "libx264", "-profile:v", "high", "-preset", "medium", "-b:v", "8000k", "-threads", "0", "-pass", "1", "-codec:a", "libfaac", "-b:a", "256K", "-f", "mp4", output_fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        infos = p.stderr.read()
        print infos
    except subprocess.CalledProcessError:
        print "encode error"



# Start 
findMoveFile(src_dir)







