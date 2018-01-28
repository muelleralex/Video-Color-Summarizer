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

def generate_color_count(k, sample, totalPixels, original=[]):
    if not len(original):
        original = sample
    kmeans = KMeans(n_clusters=k, random_state=0).fit(sample)
    colorCount = {}
    labels = kmeans.predict(original)
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
            "percent" : colorIndices.count(c) / float(totalPixels),
            "R" : RGBvals[0],
            "G" : RGBvals[1],
            "B" : RGBvals[2]
        }

    return colorCount

def summarize_colors(k, granularity, sample_percent, show_image, fps,
    video_file, total_frames, store_image, img_output_folder):
    count = 0
    success = True
    # number of frames summarized
    bars = 0
    count = 0
    sample = int(1/sample_percent)
    data = [{'granularity' : granularity, 'clusters' : k, 'sampling' : sample_percent, 'fps' : fps}]
    all_pixels = []

    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()

    if not success:
        print "Could not read video"
        return
    print
    print "Frames Per Second:",fps
    print "Clusters:",k
    print "Sampling:",sample_percent
    print

    while success:
        success, image = vidcap.read()
        if success and (count % granularity) == 0:
            # calculate time of frame
            seconds = count/fps
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            time = "%d:%02d:%02d" % (h,m,s)
            file_time = "%d-%02d-%02d" % (h,m,s)
            progress(count,total_frames,"Summarizing colors")
            # colors are stored backwards for some reason
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # increment number of frames summarized
            bars += 1
            # if true => display frame
            if show_image:
                plt.imshow(image)
                plt.xticks([])
                plt.yticks([])
                plt.show()
            # if true => store image in img_output_folder
            if store_image:
                # trying opencv method
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(img_output_folder + "/frame_" + file_time + ".png", image)
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
            all_pixels += image_array_sample.tolist()
            # run the k-means algorithm to find k colors on the sample pixels
            # kmeans = KMeans(n_clusters=k, random_state=0).fit(image_array_sample)
            # generate color counts and clusters
            color_count = generate_color_count(k, image_array_sample, totalPixels, image_array)
            # add color information for frame to data
            data.append({'colors' : color_count, 'time' : time, 'frame' : count})
        # increment total number of frames passed over so far
        count += 1

    progress(1,1, "Finished summarizing colors!")
    print

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
    # all_frame_kmeans = KMeans(n_clusters=k, random_state=0).fit(all_frame_colors)
    all_frame_color_count = generate_color_count(k, all_frame_colors, totalPixels)

    data[0]['bars'] = bars
    data[0]['all_frame'] = all_frame_color_count

    ## OUTPUT FILE ##
    # create file name off of video title
    colorFile = video_file.split('.')[0] + "_" + str(k)+ '.json'
    # convert data to JSON file
    print "Packaging into JSON file..."
    with open(colorFile, 'w') as outfile:
        json.dump(data, outfile)
