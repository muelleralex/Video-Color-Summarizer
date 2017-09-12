from __future__ import division
import vcs_core as vc
import cv2,random,argparse,json,math,sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to video", metavar="<video>")
ap.add_argument("-k", "--clusters", required=False, type=int, metavar="<clusters>", help="# of clusters", default=10)
ap.add_argument("-f", "--frame", required=False, type=int, metavar="<frame>", help="Set granularity", default=60)
ap.add_argument("-i", "--image", required=False, action="store_true", help="Display frames")
ap.add_argument("-s", "--sample", required=False, type=vc.restrict_float, metavar="<sample size>", help="Set fraction of sample size", default=0.1)
ap.add_argument("-c", "--complete", required=False, action="store_true", help="Run on clusters from 1 to 10")
args = vars(ap.parse_args())

## SET VARIABLES ##
# find the version of opencv
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# set videofile destination
video_file = args["video"]
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
# whether to run on clusters 1 through 10
all_clusters = args["complete"]

if all_clusters:
    print "Running through clusterings of 1 through 10"
    for i in range(1,11):
        vc.summarize_colors(i, granularity, sample_percent, show_image, fps,
            video_file, total_frames)
else:
    vc.summarize_colors(k, granularity, sample_percent, show_image, fps,
        video_file, total_frames)
