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


class SKE:
    """
    SKE: Shot Keyframe Extraction
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        return

    def __calOpticalFlow(self, frame1, frame2):
        try:
            lk_params = {}
            lk_params["winSize"] = (10, 10)
            lk_params["maxLevel"] = 5
            lk_params["criteria"] = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

            feat_params = {}
            feat_params["maxCorners"] = 3000
            feat_params["qualityLevel"] = 0.1
            feat_params["minDistance"] = 3
            feat_params["blockSize"] = 3

            gray1 = cv2.cvtColor(frame1, cv.CV_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv.CV_BGR2GRAY)

            pt = cv2.goodFeaturesToTrack(gray1, **feat_params)
            p0 = np.float32(pt).reshape(-1, 1, 2)

            p1, st, err = cv2.calcOpticalFlowPyrLK(gray1, gray2, p0, None, **lk_params)

            mean_motion = np.mean(np.absolute(np.subtract(p0, p1)))

            return mean_motion
        except Exception, e:
            print "calOpticalFlow error: %s" % str(e)
            return None

    def useOpticalFlow(self, shot):
        try:
            keyframes_no_list = []
            if len(shot) == 1:
                keyframes_no_list.append(shot[0])
                return keyframes_no_list

            op_min, op_max = None, None
            frame_min, frame_max = None, None
            for i in xrange(1, len(shot) - 1):
                pre_frame_pair = shot[i-1]
                cur_frame_pair = shot[i]

                op_val = self.__calOpticalFlow(pre_frame_pair[1], cur_frame_pair[1])
                if op_val == None:
                    continue

                if op_min == None :
                    op_min = op_val
                    frame_min = pre_frame_pair
                    op_max = op_val
                    frame_max = cur_frame_pair
                else:
                    if op_val < op_min:
                        op_min = op_val
                        frame_min = pre_frame_pair
                    if op_val > op_max:
                        op_max = op_val
                        frame_max = pre_frame_pair

            keyframes_no_list.append(frame_min)
            keyframes_no_list.append(frame_max)
            return keyframes_no_list
        except Exception, e:
            print "useOpticalFlow error: %s" % str(e)
            return []


