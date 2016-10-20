#!/usr/bin/python
#coding=utf-8
import os
import sys
import time

import numpy as np
import cv2
try:
    import cv
except Exception, e:
    from cv2 import cv

import frameBasedKFE
import shotBasedKFE
import videoCommon
import utility

"""
the main script. Extract keyframes from video.
@version: 2016/10/20 V1.0
@author: tianxiang
"""

def getKeyframenoList(cap):
    try:
        #fkfe = frameBasedKFE.FKFE(cap)
        #return fkfe.usePixelGrayValue()

        skfe = shotBasedKFE.SKFE(cap)
        return skfe.usingHSVHist()

    except Exception, e:
        print "getKeyframenoList error: %s" % str(e)
        return None

def extractKeyframesFromVideo(videofile, outpath):
    try:
        time_start = time.time()

        cap = cv2.VideoCapture(videofile)       # open video file
        if not cap.isOpened():
            raise Exception("open %s fail!" % videofile)

        videoCommon.showVideoInfo(cap)

        keyframe_no_list = getKeyframenoList(cap)

        if keyframe_no_list and len(keyframe_no_list) > 0:
            videoCommon.saveFramesAsPngs(cap, keyframe_no_list, outpath)
        else:
            print "keyframe_no_list is NULL!"

        cap.release()

        time_all = time.time() - time_start
        print "extractKeyframesFromVideo cost: %.2f s" % time_all
    except Exception, e:
        print "extractKeyframesFromVideo error: %s" % str(e)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "%s usage: <videofile> <outpath>" % sys.argv[0]
        sys.exit(-1)

    videofile = sys.argv[1]
    outpath = sys.argv[2]
    extractKeyframesFromVideo(videofile, outpath)

