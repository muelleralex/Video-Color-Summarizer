# Video Color Summarizer
The Video Color Summarizer (VCS) is a poorly named tool that summarizes the color composition of videos. It does this by sampling individual frames from a video and then running a k-means clustering algorithm on a sample of pixels from each frame. The resulting clustering effectively distils the frame into k colors. The clustering for each frame is recorded in a JSON file, and then each clustering is displayed in chronological order using a D3 visualization. (Examples are below)

This tool is primarily used to analyze how filmmakers use colors throughout their films by creating aesthetically pleasing visualizations but could essentially be used for any video. (I have only confirmed support for mp4 files, but it might work with other formats as well.)

## Dependencies
- Python 2.7
- numpy
- matplotlib
- OpenCV
- scikit-learn

## How it works

OpenCV is used to convert an mp4 into a Python object, and then OpenCV is once again used to iterate through a set of frames from the video.

A collection of pixels is sequentially sampled from each frame. In other words, if you are sampling 10% of the pixels, the program will take every 10th pixel. This strategy won't sample exactly 10% of the pixels, but it does ensure that pixels are sampled evenly throughout the frame. Each sampled pixel is then represented by a 3-dimensional array of it's Red, Blue, Green values.

A k-means algorithm is run on the sample of pixels, and average color of each clustering becomes one of the k colors that summarizes the frame. The program also records the percentage of pixels that fit in each cluster, and these percentages account for how prominent each of the k colors is.

The pixel sampling and k-means algorithm is repeated for each sampled frame.

After all of the frames have been analyzed, all of the colors from the previous clustering are accumulated into one set, and a k-means algorithm is run on this set of colors. This results in an "overall" summary of the color usage in the movie. (This is an incredibly flawed method and will be replaced soon hopefully.)

The resulting color clusterings are stored in a JSON object in chronological order and output to a JSON file. The resulting file can then be used to render a color summary like the ones here http://alexmu.com/vcs and in the example section below.

## Python
The dependencies for the Python script are listed above.

##### Running the script
    python vcs.py [-h] -v <video> [-k <clusters>] [-f <frame>] [-i] [-s <sample size>] [-c]

- Video (-v) : the file to be used
- Clusters (-k) : summarize to k colors (default is 10)
- Frame (-f) : how often to summarize frames (defaults to 60 => one frame summarized for each minute of video)
- Image (-i) : a flag to show the frame currently being summarized
- Sample size (-s) : fraction of pixels to sample (fractions must be input as decimals between 0.0 and 1.0) (default is 0.1)
- Complete (-c) : a flag that will output summaries for clusters 1 through 10

Example:

    python vcs.py -v "The Empire Strikes Back.mp4" -k 5 -f 30 -s 0.3

This would provide a 5-color summary for a frame taken every 30 second in the movie, and each summary would be based on a sample of 30% of the pixels from the frame.

The Python script uses OpenCV to isolate the frames and uses scikit-learn to run the k-means algorithm. The color summary itself is output as a JSON file.

## Output file
The vcs.py script will output a JSON file. The first element of the JSON object contains metadata as well as an overall color summary of the video. The remaining elements are a listing of the clustering from each sampled frame in chronological order. Example output files are included in the viz folder.

## Visualizations
I used JavaScript and D3 to create a tool to visualize the data from vcs.py. The code for the current version is included in the viz folder. I have also included a pre-built index.html file within the folder, so if you run a simple server out of the folder a visualization should appear.

## Example Visualizations
Below is a rendering of a color summary of this clip (https://www.youtube.com/watch?v=C-a3lflYOw8) with one frame being sampled for each second of the video and summarized to ten colors.
![Moonlight Example](http://alexmu.com/MoonlightClip.PNG)

The rendering below provides an example with more extreme color variation. The colors summary comes from the opening title sequence to <i>Napoleon Dynamite</i> (https://vimeo.com/5524216).
![Napoleon Dynamite Example](http://alexmu.com/NapoleonDynamite.PNG)

For more examples, go to http://www.alexmu.com/vcs.
