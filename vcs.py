"""
TODO:
-   need to find a way to deal with missing frames and opencv errors
-   need method for dealing with unfinished color summaries

NOTES:
-   apparently the letterboxing is already taken care of => no need to remove it
-   nvm might need to do something with the letterboxing after all
"""


from __future__ import division

import cv2,random,argparse,json,math,sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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

def generate_color_count(k, kmeans):
    colorCount = {}
    labels = kmeans.predict(image_array)
    # convert labels into python list
    colorIndices = list(labels)
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

    return colorCount

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to video", metavar="<video>")
ap.add_argument("-k", "--clusters", required=False, type=int, metavar="<clusters>", help="# of clusters", default=10)
ap.add_argument("-f", "--frame", required=False, type=int, metavar="<frame>", help="Set granularity", default=60)
ap.add_argument("-i", "--image", required=False, action="store_true", help="Display frames")
ap.add_argument("-s", "--sample", required=False, type=restrict_float, metavar="<sample size>", help="Set fraction of sample size", default=0.1)
ap.add_argument("-c", "--complete", required=False, action="store_true", help="Run on clusters from 1 to 10")
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
# total pixels in frame * sample = number of pixels to sample from frame
sample_percent = args["sample"]
# calculate number of pixels to sample per ten pixels
sample = int(1/sample_percent)
# whether to show frames while executing
showImage = args["image"]
# whether to run on clusters 1 through 10
all_clusters = args["complete"]
# number of frames looked at
count = 0
success = True
initial_read = False
# number of frames summarized
bars = 0
# head of JSON data
data = [{'granularity' : granularity, 'clusters' : k, 'sampling' : sample_percent, 'fps' : fps}]
all_pixels = []

print "Frames Per Second:",fps
print "Clusters:",k
print "Sampling:",sample_percent
print

## initial test

## SUMMARIZE VIDEO ##
while success:
    success,image = vidcap.read()
    if success and (count % granularity) == 0:
        # initial read was successful
        initial_read = True
        # calculate time of frame
        seconds = count/fps
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time = "%d:%02d:%02d" % (h,m,s)
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
        # reshape image to one dimensional array
        image_array = np.reshape(image, (totalPixels, d))
        # sample pixels
        image_array_sample = image_array[0::sample]
        # testing to remove black
        # for i in range(len(image_array_sample)-1,-1,-1):
        #     # find RGB values
        #     R = image_array_sample[i][0]
        #     G = image_array_sample[i][1]
        #     B = image_array_sample[i][2]
        #
        #     if not R and not G and not B:
        #         image_array_sample = np.delete(image_array_sample, i, 0)

        all_pixel += image_array_sample.tolist()
        # run the k-means algorithm to find k colors on the sample pixels
        kmeans = KMeans(n_clusters=k, random_state=0).fit(image_array_sample)
        # generate color counts and clusters
        color_count = generate_color_count(k, kmeans)
        # add color information for frame to data
        data.append({'colors' : color_count, 'time' : time, 'frame' : count})
    # increment total number of frames passed over so far
    count += 1

if not initial_read:
    print "Could not read video"
    quit()

progress(1,1, "Finished summarizing colors!")
print

# add number of frames summarized to head of data
all_frame_colors = []
for i in range(1, bars):
    # print data[i]['colors']
    for j in range(k):
        color = data[i]['colors'][j]
        R = color["R"]
        G = color["G"]
        B = color["B"]
        all_frame_colors.append(np.array([R,G,B]))

all_frame_colors = np.array(all_frame_colors) / 255
all_frame_kmeans = KMeans(n_clusters=k, random_state=0).fit(all_frame_colors)
all_frame_color_count = generate_color_count(k, all_frame_kmeans)

# all_pixels = np.array(all_pixels)
# all_px_kmeans = KMeans(n_clusters=k, random_state=0).fit(all_pixels)
# all_px_color_count = generate_color_count(k, all_px_kmeans)
# labels = all_px_kmeans.predict(all_pixels)
# colorIndices = list(labels)
# all_frame_colorCount = {}
#
# for c in range(k):
#     RGBvals = []
#     for i in range(3):
#         RGBvals.append(round(kmeans.cluster_centers_[c][i]*255))
#     colorCount[c] = {
#         "percent" : colorIndices.count(c) / totalPixels,
#         "R" : RGBvals[0],
#         "G" : RGBvals[1],
#         "B" : RGBvals[2]
#     }

# data[0]['all_px'] = all_px_color_count

data[0]['bars'] = bars
data[0]['all_frame'] = all_frame_color_count

## OUTPUT FILE ##
# create file name off of video title
colorFile = videoFile.split('.')[0] + "_" + str(k)+ '.json'
# convert data to JSON file
print "Packaging into JSON file..."
with open(colorFile, 'w') as outfile:
    json.dump(data, outfile)
