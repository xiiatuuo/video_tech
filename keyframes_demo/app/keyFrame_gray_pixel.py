#!/usr/bin/python
# coding=utf-8
import os
import sys
import time

import numpy as np
import cv2
from cv2 import cv

import videoCommon
import utility

def convertToGray(frame):
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


# compare two frames pixel by pixel
# Using subtract function, so the order of frame need to be considered
# @return | int | diff_num | result is 'cur_frame - pre_frame'
def cmpConsecutiveFrame(pre_frame, cur_frame):
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


# @param | object| cap             | VideoCapture object
# @return| dict  | frame_info_dict | like {0:{"frame": frame, "diff_val": 0}} 
def calFrameStats(cap):
    try:
        frame_info_dict = {}
        pre_frame = None
        diff_val  = 0
        while True:
            frame_no = int(cap.get(cv.CV_CAP_PROP_POS_FRAMES))  # frame No begin with 0
            succ, cur_frame = cap.read()                        # read video by frame
            if not succ:
                break

            cur_frame = convertToGray(cur_frame)                # convert to gray for comparing

            if frame_no != 0:                                   # if it's not first frame
                diff_val = cmpConsecutiveFrame(pre_frame, cur_frame)

            frame_info_dict[frame_no] = {"frame": cur_frame, "diff_val": diff_val}

            # move to next frame
            pre_frame = cur_frame

        return frame_info_dict
    except Exception, e:
        print "calFrameStats error: %s" % str(e)
        return None

def extractKeyFrames(video_file, out_path):
    try:
        time_start = time.time()

        cap = cv2.VideoCapture(video_file)          # open video file
        if not cap.isOpened():
            raise Exception("open %s fail!" % video_file)

        videoCommon.showVideoInfo(cap)

        # prcoess video frame by frame
        frames_info_dict = calFrameStats(cap)

        # set frame difference threshold
        time_begin = time.time()
        diff_num_list = [frame_info_dict["diff_val"] for frame_no, frame_info_dict in frames_info_dict.iteritems()]
        diff_num_mean = np.mean(diff_num_list)
        diff_num_std  = np.std(diff_num_list)       # standard deviation

        threshold = diff_num_std * 1.85 + diff_num_mean

        # select candidate keyframes based on threshold, then choose result keyframes using k-means clustering
        keyframe_no_list = [ frame_no for frame_no, frame_info_dict in frames_info_dict.iteritems() if frame_info_dict["diff_val"] > threshold ]
        selected_keyframes_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 10) 

        # output result keyframes
        videoCommon.saveFramesAsPngs(cap, selected_keyframes_no_list, out_path)

        cap.release()

        time_all = time.time() - time_start

        print "extractKeyFrames cost: %.2f s" % (time_all)
    except Exception, e:
        print "extractKeyFrame error: %s" % str(e)


if __name__ == "__main__":
    video_file = sys.argv[1]
    out_path   = sys.argv[2]
    extractKeyFrames(video_file, out_path)

