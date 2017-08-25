# Video-Color-Summarizer

This Python script creates a color summary of individual frames from a video. This script was designed to show how color is used and changes throughout a movie, but it could be used for any other videos. (I have only confirmed support for mp4 files, but it might work with other formats as well.)

## Python
The Python script runs through frames from a video and applies a k-means algorithm to each frame to summarize the frame into k colors. The color summaries are then placed in a JSON file.

##### Running the script
    python vcs.py [-h] -v <video> [-k <clusters>] [-f <frame>] [-i] [-s <sample size>]

- Video - the file to be used
- Clusters - summarize to k colors (default is 10)
- Frame - how often to summarize frames (defaults to 60 => one frame summarized for each minute of video)
- Image - show the frame currently being summarized
- Sample size - fraction of pixels to sample (fractions must be input as decimals between 0.0 and 1.0) (default is 0.1)

Example:

    python vcs.py -v "The Empire Strikes Back.mp4" -k 5 -f 30 -s 0.3

This would provide a 5-color summary for a frame taken every 30 second in the movie, and each summary would be based on a sample of 30% of the pixels from the frame.

The Python script uses OpenCV to isolate the frames and uses scikit-learn to run the k-means algorithm. The color summary itself is output as a JSON file.

## Example
Below is a rendering of a color summary of this clip (https://www.youtube.com/watch?v=C-a3lflYOw8) with one frame being sampled for each second of the video and summarized to ten colors.
![Moonlight Example](http://alexmu.com/MoonlightClip.PNG)

The rendering below provides an example with more extreme color variation. The colors summary comes from the opening title sequence to <i>Napoleon Dynamite</i> (https://vimeo.com/5524216).
![Napoleon Dynamite Example](http://alexmu.com/NapoleonDynamite.PNG)

## Future
I will be uploading a JavaScript file that can be used to render a display similar to the example from the JSON file created by the python script. I will also be adding in a feature that will render the same display in matplotlib. Examples will eventually be uploaded to my personal website in the near future.

## Updates
I have changed the method for sampling pixels. Previously, the program would randomly order the pixels and then designate a fraction of them as the sample. The new method samples by choosing every nth pixel. So for example if you choose a 10% sample, it will choose every 10th pixel. This ensures that the pixels are sampled throughout the frame, and because it is no longer necessary to take large samples, run time has been reduced as well.

I also added in a feature where it records the exact frame number and time of the frames sampled.
