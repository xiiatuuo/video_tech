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

import utility

"""
@version: 2016/10/20 V1.0
@author: tianxiang
"""

class FKFE:
    """
    FKFE: Frame-based Key Frame Extraction
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        return

    def __convertToGray(self, frame):
        try:
            # Convert to gray
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # scale down to quarter times, using pixel relation resampling
            gray_frame = cv2.resize(gray_frame, None, fx = 0.25, fy = 0.25, interpolation = cv2.INTER_AREA)

            # blur
            gray_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0.0)

            return gray_frame
        except Exception, e:
            print "convertToGray error: %s" % str(e)


    def __cmpConsecutiveFrame(self, pre_frame, cur_frame):
        """
        compare two frames pixel by pixel, result is 'cur_frame - pre_frame'
        """
        try:
            # calculate difference between two frames by element to element
            # output an array of the same size as the input frame
            diff_val = cv2.subtract(cur_frame, pre_frame)

            # count non-zero array elements
            diff_num = cv2.countNonZero(diff_val)

            return diff_num
        except Exception, e:
            print "cmpConsecutiveFrame error: %s" % str(e)
            return -3


    def usePixelGrayValue(self):
        try:
            frame_info_dict = {}
            diff_num_list = []

            pre_frame = None
            diff_val  = 0
            while True:
                frame_no = int(self.__cap.get(cv.CV_CAP_PROP_POS_FRAMES))  # frame No begin with 0
                succ, cur_frame = self.__cap.read()                        # read video by frame
                if not succ:
                    break

                cur_frame = self.__convertToGray(cur_frame)                # convert to gray for comparing

                if frame_no != 0:                                   # if it's not first frame
                    diff_val = self.__cmpConsecutiveFrame(pre_frame, cur_frame)

                diff_num_list.append(diff_val)
                frame_info_dict[frame_no] = {"frame": cur_frame, "diff_val": diff_val}

                # move to next frame
                pre_frame = cur_frame

            diff_num_mean = np.mean(diff_num_list)
            diff_num_std  = np.std(diff_num_list)
            threshold = diff_num_std * 1.85 + diff_num_mean

            cand_keyframe_info_dict = {}
            for frame_no, frame_info_dict in frame_info_dict.iteritems():
                if frame_info_dict["diff_val"] > threshold:
                    cand_keyframe_info_dict[frame_no] = frame_info_dict

            selected_keyframe_no_list = utility.selectKeyframesByKMeans(cand_keyframe_info_dict.keys(), 9) 

            return selected_keyframe_no_list
        except Exception, e:
            print "usePixelGrayValue error: %s" % str(e)

