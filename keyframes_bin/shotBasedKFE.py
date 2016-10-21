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

import shotBoundaryDetection
import shotKeyframeExtraction
import utility

"""
@version: 2016/10/20 V1.0
@author: tianxiang
"""


class SKFE:
    """
    SKFE: Shot-based Key Frame Extraction
    step1: detect shot boundaries of video, then divide video into serveral shots
    step2: extract key frames from each video shot
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        self.sbd = shotBoundaryDetection.SBD(self.__cap)
        self.ske = shotKeyframeExtraction.SKE(self.__cap)
        return

    def usingHSVHist(self):
        try:
            keyframe_no_list = []

            shot_list = self.sbd.useHSVHist()
            for shot in shot_list:
                shot_keyframe_no_list = self.ske.useOpticalFlow(shot)
                keyframe_no_list.extend(shot_keyframe_no_list)

            selected_keyframe_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 9)
            return selected_keyframe_no_list
        except Exception, e:
            print "usingHSVHist error: %s" % str(e)
            return None



