# Pedestrian Detection
Author:Yan Wang  <dieqi317@gmail.com> <br>
Date: 2018 10 11 <br>
## Introduction
The program is used to locate the people in the vedio. <br>
Though we need to locate the people in the vedio, we can find people is the only kind of
moving object in the 4 test vedio,so the work we should do really is finding the moving
object in the vedio. What's more,we should clean the noise generated by background changes,
such as the moving trees and the Camera jitter.

## Test vedio
There are 4 test vedios. The first and the second are the videos shooting indoors, others
are videos shooting outdoors. People in videos shooting indoors are distinct,people in other
test vedios are blurry.<br>

## Method
I find a frame which has the minimum area of people in the aim vedio as the standard background.
Then use each frame to compare with the background.After that, I use eroding and dilating to
clean the noise

## Details
Photos for testing is in the "Date" .The test vedio is big,so I just put one frame in test2 and
one frame in test3 to the "data"
"humanMotionDetection_frame.py" is used to check the effect of fixed operation on each frame.<br>
"humanMotionDetection_video.py" is used to locate the moving people in the test video.<br>
"test_output2.avi" is the resule of the test2.
You can see more detalls in [SuperYanyann's Blog](superyanyann.github.io)