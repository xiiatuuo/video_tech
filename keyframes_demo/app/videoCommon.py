#!/usr/bin/python
#coding=utf-8

import sys
import cv2
from cv2 import cv

def showVideoInfo(cap):
    try:
        frame_count   = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
        frate_per_sec = cap.get(cv.CV_CAP_PROP_FPS)
        video_width   = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        video_height  = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        
        print "video frame num: %d" % frame_count
        print "video fps: %f" % frate_per_sec
        print "video duration: %d s" % (frame_count / frate_per_sec)
        print "video size: %d X %d" % (video_width, video_height)

        return frame_count
    except Exception, e:
        print "showVideoInfo error: %s" % str(e)


# save frame with 480 * 320
def saveFramesAsPngs(cap, frame_no_list, out_path, withScale = False):
    try:
        max_width, max_height = 480.0, 320.0

        # out frame size is video frame size by default
        out_width  = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        out_height = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))

        if withScale:
            scale = 1.0
            if out_width > max_width:
                scale = max_width / out_width
                out_width   = max_width
                out_height *= scale
            if out_height > max_height:
                scale = max_height / out_height
                out_width *= scale
                out_height = max_height

        for frame_no in frame_no_list:
            try:
                cap.set(cv.CV_CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()

                out_name = "%s/%d.png" % (out_path, frame_no)

                if withScale:
                    cv2.resize(frame, (out_width, out_height), interpolation = cv2.INTER_AREA)

                cv2.imwrite(out_name, frame)
            except Exception, e:
                print "save frame %d fail!" % frame_no
                continue
    except Exception, e:
        print "saveFrameAsPng error: %s" % str(e)


