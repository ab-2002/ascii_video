# MP4 Video to ASCII Video. 
![alt text](https://i.imgur.com/mzS9aYy.png)
## How it works:
This python script enables you to "convert" any .mp4 video to an ascii video and save it if you want.
The script extracts all of the frames from the .mp4 file, then for each frame it generates an adequate ascii representation based on the pixel data. 
Then it goes and prints all of the generated ascii images in your console in the frame rate of the original video.
After it's done, you can save the "ascii video" and then replay it whenever you want.
Here is an example of some random converted animation video.
[![IMAGE ALT TEXT](http://img.youtube.com/vi/j4fib_BHzdc/0.jpg)](http://www.youtube.com/watch?v=j4fib_BHzdc "ASCII Video")

## Requirements:
- You need to be running a Windows machine.
- You need python 3.* installed
- You need to have the OpenCV package installed (https://pypi.org/project/opencv-python/).
- You need to have the Pillow package installed (https://pypi.org/project/Pillow/)
## How to download:
You can either download the executable from the releases section
```
https://github.com/b-aleksa/ascii_video/releases/tag/release
```
or follow the steps bellow if want to mess with the source code.
### Step - 1:
Download the repository by opening your cmd and executing this
```
git clone https://github.com/b-aleksa/ascii_video.git
```
### Step - 2: (if missing python)
Download and install python from their website https://www.python.org/
### Step - 3: (if missing packages)
You can install the OpenCV package by running this in your terminal:
```
pip install opencv-python 
```
You can install the Pillow package by running this in your terminal:
```
pip install Pillow
```
## How to use:
### Step - 1:
Download the mp4 file you want to convert and place it at the same place where the executable/script is located at.
### Step - 2:
If you have downloaded the executable, just run it.
If you have downloaded the script, you need to open your terminal and execute it like this:
```
python <PATH_TO_SCRIPT>/ascii_video.py
```
### Step - 3:
That's it. There's nothing more to it. Just follow the script's lead and you should be fine.
