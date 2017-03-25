# Video-Color-Summarizer

These Python and JavaScript scripts create and display a color summary of individual frames from a video. These scripts were designed to show how color is used and changes throughout a movie, but it could be used for any other videos. (I have only confirmed support for mp4 files, but it might work with other formats as well.)

## Python
The Python script runs through frames from a video and applies the k-means algorithm to each frame to summarize the frame into k colors. The color summaries are then placed in a JSON file. The script assumes there are 24 frames per second.

##### Running the script
    python cm2.py [-h] -v <video> [-c <clusters>] [-f <frame>] [-i <image>] [-s <sample size>]

- Video - the file to be used
- Clusters - summarize to k colors (default is 10)
- Frame - how often to summarize frames (defaults to 60 => frame summarized for each minute of video)
- Image - show the frame being summarized
- Sample size - fraction of pixels to sample (default is 3 => 1/3 of pixels sampled)

Example:

    python cm2.py -v "The Empire Strikes Back.mp4" -c 5 -f 30 -s 2

This would provide a 5-color summary for a frame taken every 30 second in the movie, and each summary would be based on a sample of 50% of the pixels from the frame.

The Python script uses OpenCV to isolate the frames and uses scikit-learn to run the k-means algorithm.

## JavaScript
