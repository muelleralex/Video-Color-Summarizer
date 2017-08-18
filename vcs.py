from __future__ import division

import cv2,random,argparse,json,math,sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

def restrict_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to video", metavar="<video>")
ap.add_argument("-k", "--clusters", required=False, type=int, metavar="<clusters>", help="# of clusters", default=10)
ap.add_argument("-f", "--frame", required=False, type=int, metavar="<frame>", help="Set granularity", default=60)
ap.add_argument("-i", "--image", required=False, action="store_true", help="Display frames")
ap.add_argument("-s", "--sample", required=False, type=restrict_float, metavar="<sample size>", help="Set fraction of sample size", default=0.5));
args = vars(ap.parse_args())

## SET VARIABLES ##
# find the version of opencv
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# set videofile destination
videoFile = args["video"]
# extract video from file
vidcap = cv2.VideoCapture(videoFile)
success,image = vidcap.read()
# find fps of the video
if int(major_ver) < 3:
    fps = round(vidcap.get(cv2.cv.CV_CAP_PROP_FPS))
    totalframes = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
else:
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    totalframes = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
# number of clusters
k = args["clusters"]
# number of frames to skip
granularity = fps*args["frame"]
# total pixels * sample = number of pixels to sample from frame
sample = args["sample"]
# whether to show frames while executing
showImage = args["image"]
# number of frames looked at
count = 0
success = True
# number of frames summarized
bars = 0
# head of JSON data
data = [{'granularity' : granularity, 'clusters' : k}]

## PREPARE VIDEO ##


## SUMMARIZE VIDEO ##
while success:
    success,image = vidcap.read()
    # proceeed if success and frame is to be summarized
    if success and (count % granularity) == 0:
        progress(count,totalframes,"Summarizing colors")
        # colors are stored backwards for some reason
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # increment number of frames summarized
        bars += 1
        # if true => display frame
        if showImage:
            plt.imshow(image)
            plt.show()
        # convert image to array of RGB values
        image = np.array(image, dtype=np.float64) / 255
        # set width and height
        w, h, d = tuple(image.shape)
        # calculate total number of pixels
        totalPixels = w*h
        # sample size
        pixelSample = int(math.floor((w*h)/sample))
        # reshape image to one dimensional array
        image_array = np.reshape(image, (totalPixels, d))
        # randomly shuffle elements of the array
        # pick pixelSample number of points from the array
        image_array_sample = shuffle(image_array, random_state=0)[:pixelSample]
        # run the k-means algorithm to find k colors on the sample pixels
        kmeans = KMeans(n_clusters=k, random_state=0).fit(image_array_sample)
        # label each pixel in image
        labels = kmeans.predict(image_array)
        # convert labels into python list
        colorIndices = list(labels)
        colorCount = {}

        # for each cluster...
        for c in range(k):
            RGBvals = []
            # find the mean RGB value
            for i in range(3):
                RGBvals.append(round(kmeans.cluster_centers_[c][i]*255))
            # find percentage of pixels in image of that color
            colorCount[c] = {
                "percent" : colorIndices.count(c) / totalPixels,
                "R" : RGBvals[0],
                "G" : RGBvals[1],
                "B" : RGBvals[2]
            }

        # add color information for frame to data
        data.append(colorCount)
        # print "bar:",bars
    # increment total number of frames passed over so far
    count += 1
progress(1,1, "Finished summarizing colors!")
print

# add number of frames summarized to head of data
data[0]['bars'] = bars

## OUTPUT FILE ##
# create file name off of video title
colorFile = videoFile.split('.mp4')[0] + '.json'
# convert data to JSON file
print "Packaging into JSON file"
with open(colorFile, 'w') as outfile:
    json.dump(data, outfile)
