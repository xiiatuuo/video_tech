#!/usr/bin/python
#coding=utf-8
import os
import sys
import time
import random

import numpy as np
import cv2
try:
    import cv
except Exception, e:
    from cv2 import cv

from frameDifferenceMeasures import FDM
import utility

"""
@version: 2016/10/20 V1.0
@author: tianxiang
"""


class SBD:
    """
    SBD: Shot Boundary Detector
    detect the shot boundarys of video, return a shot list that each shot is represented as frame number list.
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        self.__fdm = FDM()
        return

    def byLikelihood(self):
        """
        A region-based method
        """
        try:
            return []
        except Exception, e:
            print "byLikelihood error: %s" % str(e)
            return None

    def byECR(self):
        """ECR: Edge Change Ratio"""
        try:
            return []
        except Exception, e:
            print "byECR error: %s" % str(e)
            return None

    def byBlockGrayHist(self):
        """
        cal the gray histogram for each frame, then compare them in sequence.
        """
        try:
            frate_per_sec = self.__cap.get(cv.CV_CAP_PROP_FPS)

            diff_list = []
            frame_info_dict = {}

            pre_gray_hist = None
            while True:
                succ, frame = self.__cap.read()
                if not succ:
                    break
                #if random.randint(0, frate_per_sec) > 10:       # down sample at 10 fps
                #    continue

                frame_no = int(self.__cap.get(cv.CV_CAP_PROP_POS_FRAMES) - 1)
                cur_gray_hist = self.__fdm.getBlockGrayHist(frame) 

                if pre_gray_hist != None:
                    diff = self.__fdm.byBlockGrayHist(pre_gray_hist, cur_gray_hist) / len(cur_gray_hist)
                else:
                    diff = 0

                diff_list.append(diff)
                #print "%d: %.2f" % (frame_no, diff)
                frame_info_dict[frame_no] = {"diff": diff, "hist": cur_gray_hist}
                pre_gray_hist = cur_gray_hist

            shot_boundary_frame_no_list = []

            frame_windows_size = int(frate_per_sec * 10)

            window_begin, window_end = 0, frame_windows_size
            while True:
                if window_end >= len(diff_list):
                    window_end = len(diff_list) - 1
                window_diff_list = diff_list[window_begin : window_end]
                diff_avg = np.mean(window_diff_list)
                diff_std = np.std(window_diff_list)
                diff_threshold = diff_avg + 2 * diff_std

                for frame_no in xrange(window_begin, window_end):
                    if frame_info_dict[frame_no]["diff"] > diff_threshold:
                        shot_boundary_frame_no_list.append(frame_no)

                window_begin = window_end
                window_end += frame_windows_size
                if window_begin >= len(diff_list) - 1:
                    break

            if shot_boundary_frame_no_list[-1] < len(diff_list) - 1:
                shot_boundary_frame_no_list.append(len(diff_list) - 1)
            
            shots_list = []
            shot_begin = 0
            for shot_end in shot_boundary_frame_no_list:
                cur_shot = []
                for frame_no in xrange(shot_begin, shot_end):
                    cur_shot.append((frame_no, frame_info_dict[frame_no]))
                shots_list.append(cur_shot)
                shot_begin = shot_end

            #extreme_index_list = utility.getExtremeMaxValue(diff_list)
            #extreme_index_list.append(len(diff_list))
            #shot_begin = 0
            #for shot_end in extreme_index_list:
            #    cur_shot = []
            #    for frame_no in xrange(shot_begin, shot_end):
            #        cur_shot.append((frame_no, frame_info_dict[frame_no]))
            #    shots_list.append(cur_shot)
            #    shot_begin = shot_end

            #cur_shot = []
            #for frame_no, frame_dict in frame_info_dict.iteritems():
            #    if frame_dict["diff"] > diff_threshold:
            #        shots_list.append(cur_shot)
            #        cur_shot = []
            #    cur_shot.append((frame_no, frame_dict))
                
            return shots_list
        except Exception, e:
            print "byBlockGrayHist error: %s" % str(e)
            return None


    def byHueHist(self):
        """
        cal the hsv histogram for each frame, then compare them in sequence.
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

                cur_hue_hist = self.__fdm.getHueHist(frame)

                if frame_no != 0:
                    sim = self.__fdm.byHueHist(pre_hue_hist, cur_hue_hist)
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
            print "byHueHist error: %s" % str(e)
            return None

    def byTemplateMatching(self):
        """
        using Template matching algorithm. 
        Two consecutive frames are compared pixel by pixel and a correlation factor is calculated.
        """
        try:
            shots_list = []
            cur_shot = []

            pre_frame = None
            while True:
                succ, cur_frame = self.__cap.read()
                if not succ:
                    break

                frame_no = int(self.__cap.get(cv.CV_CAP_PROP_POS_FRAMES) - 1)

                if frame_no != 0:
                    res = cv2.matchTemplate(cur_frame, pre_frame, cv2.TM_CCORR_NORMED)
                    #print "%d: %.2f" % (frame_no, res)
                    if res > 0.9:
                        cur_shot.append((frame_no, cur_frame))
                    else:
                        if len(cur_shot) > 0:
                            shots_list.append(cur_shot)
                        cur_shot = []
                        cur_shot.append((frame_no, cur_frame))

                pre_frame = cur_frame

            if len(cur_shot) > 0:
                shots_list.append(cur_shot)

            #for shot in shots_list:
            #    print "shot: ", len(shot), shot[0][0], shot[-1][0]

            return shots_list
        except Exception, e:
            print "byTemplateMatching error: %s" % str(e)
            return None


if __name__ == "__main__":
    videofile = sys.argv[1]
    #outpath = sys.argv[2]

    cap = cv2.VideoCapture(videofile)       # open video file
    if not cap.isOpened():
        raise Exception("open %s fail!" % videofile)

    sbd = SBD(cap)
    time_begin = time.time()
    #result = sbd.byTemplateMatching()
    result, _ = sbd.byGrayHist()
    print "cost: %.2f s" % (time.time() - time_begin)
    cap.release()

