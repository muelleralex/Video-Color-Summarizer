from __future__ import division
import vcs_core as vc
import cv2,random,argparse,json,math,sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from os.path import isdir
from os import mkdir

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to video", metavar="<video>")
ap.add_argument("-k", "--clusters", required=False, type=int, metavar="<clusters>", help="# of clusters", default=10)
ap.add_argument("-f", "--frame", required=False, type=int, metavar="<frame>", help="Set granularity", default=60)
ap.add_argument("-i", "--image", required=False, action="store_true", help="Display frames")
ap.add_argument("-si", "--store_image", required=False, action="store_true", help="Store sampled frames as images")
ap.add_argument("-s", "--sample", required=False, type=vc.restrict_float, metavar="<sample size>", help="Set fraction of sample size", default=0.1)
ap.add_argument("-c", "--complete", required=False, action="store_true", help="Run on clusters from 1 to 10")
args = vars(ap.parse_args())

## SET VARIABLES ##
# find the version of opencv
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# set videofile destination
video_file = args["video"]
# create output folder
output_folder = video_file.split('.')[0]
if not isdir(output_folder):
    mkdir(output_folder)
# create image ouput folder
# frames that are examined will be put in this folder
img_output_folder = output_folder + '/' +  "imgs_" + str(args["frame"])
if not isdir(img_output_folder):
    mkdir(img_output_folder)
# extract video from file
vidcap = cv2.VideoCapture(video_file)
success,image = vidcap.read()
# find fps of the video
if int(major_ver) < 3:
    fps = round(vidcap.get(cv2.cv.CV_CAP_PROP_FPS))
    total_frames = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
else:
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
# number of clusters
k = args["clusters"]
# number of frames to skip
granularity = fps*args["frame"]
# total pixels in frame * sample = number of pixels to sample from frame
sample_percent = args["sample"]
# calculate number of pixels to sample per ten pixels
sample = int(1/sample_percent)
# whether to show frames while executing
show_image = args["image"]
# whether to store frames as images
store_image = args["store_image"]
# whether to run on clusters 1 through 10
all_clusters = args["complete"]

if all_clusters:
    print "Running through clusterings of 1 through 10"
    for i in range(1,11):
        vc.summarize_colors(i, granularity, sample_percent, show_image, fps,
            video_file, total_frames, store_image, img_output_folder)
else:
    vc.summarize_colors(k, granularity, sample_percent, show_image, fps,
        video_file, total_frames, store_image, img_output_folder)
