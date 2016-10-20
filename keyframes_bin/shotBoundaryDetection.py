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

"""
@version: 2016/10/20 V1.0
@author: tianxiang
"""


class SBD:
    """
    SBD: Shot Boundary Detection
    detect the shot boundarys of video, return a shot list that each shot is represented as frame number list.
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        return

    # convert the RGB color model to HSV model, 
    # then cal histogram of Hue which is quantized as 16 bins 
    # normalized the Hue Histogram in [0, 1]
    def __getHueHist(self, image):
        try:
            hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            h, s, v = cv2.split(hsv_img)

            h_hist = cv2.calcHist([h], [0], None, [16], [0, 255])

            cv2.normalize(h_hist, h_hist, 0, 1, cv2.NORM_MINMAX)
            return h_hist
        except Exception, e:
            print "getHueHist error: %s" % str(e)
            return None

    def useLikelihood(self):
        """
        A region-based method
        """
        try:
            return []
        except Exception, e:
            print "useLikelihood error: %s" % str(e)
            return None

    def useECR(self):
        """ECR: Edge Change Ratio"""
        try:
            return []
        except Exception, e:
            print "useECR error: %s" % str(e)
            return None

    def useHSVHist(self):
        """
        cal the hsv histogram for each frame,
        then compare them in sequence.
        @return | list | like '[[(frame_no, frame)], [(frame_no, frame)]]'
        """
        try:
            shots_list = []                         # list of shots

            pre_hue_hist = None
            cur_shot = []                           # a shot is a list of frames
            
            while True:
                succ, frame = self.__cap.read()
                if not succ:
                    break

                frame_no = int(self.__cap.get(cv.CV_CAP_PROP_POS_FRAMES) - 1)

                cur_hue_hist = self.__getHueHist(frame)

                if frame_no != 0:
                    sim = cv2.compareHist(pre_hue_hist, cur_hue_hist, cv.CV_COMP_CORREL)
                    if sim > 0.7:                   # the greater of the value is, the more similarity it's
                        cur_shot.append((frame_no, frame))
                    else:                           # shot boundary, move to next shot
                        if len(cur_shot) > 0:
                           shots_list.append(cur_shot)
                        cur_shot = []
                        cur_shot.append((frame_no, frame))

                pre_hue_hist = cur_hue_hist

            if len(cur_shot) > 0:                   # the last shot
                shots_list.append(cur_shot)

            return shots_list
        except Exception, e:
            print "useHSVHist error: %s" % str(e)
            return None

        
