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

from frameDifferenceMeasures import FDM
from shotBoundaryDetection import SBD
from shotKeyframeExtraction import SKFE
import utility
import videoCommon

"""
@version: 2016/10/28 V2.0
@author: tianxiang
"""


class KFE:
    """
    KFE: Key Frame Extraction
    step1: detect shot boundaries of video, then divide video into serveral shots
    step2: extract key frames from each video shot
    """

    def __init__(self, cap):
        """@param: cap. cv2.VideoCapture object"""
        self.__cap = cap
        self.fdm = FDM()
        self.sbd = SBD(self.__cap)
        self.skfe = SKFE(self.__cap)


    def usePixelGrayValue(self):
        """
        [2014] https://github.com/tafsiri/filmstrip
        step1: compare the gray value of pixel to measure the difference of successive frames.
        step2: Threshold is calculated by the mean and std of frame difference value
        step3: get candidate keyframes by threshold
        step4: use frame No. based k-means clustering to select specified number of keyframes
        merits: fast
        demerits: no theoretical basis
        """
        try:
            frame_info_dict = {}
            diff_num_list = []

            pre_gray_frame = None
            diff_val  = 0
            while True:
                frame_no = int(self.__cap.get(cv.CV_CAP_PROP_POS_FRAMES))   # frame No begin with 0
                succ, cur_frame = self.__cap.read()                         # read video by frame
                if not succ:
                    break

                cur_gray_frame = self.fdm.convertToGray(cur_frame)

                if frame_no > 0:
                    diff_val = self.fdm.byPixelGray(pre_gray_frame, cur_gray_frame)

                diff_num_list.append(diff_val)
                frame_info_dict[frame_no] = {"frame": cur_gray_frame, "diff_val": diff_val}

                # move to next frame
                pre_gray_frame = cur_gray_frame

            diff_num_mean = np.mean(diff_num_list)
            diff_num_std  = np.std(diff_num_list)
            threshold = diff_num_std * 1.85 + diff_num_mean

            keyframe_no_list = [ frame_no for frame_no, frame_dict in frame_info_dict.iteritems() if frame_dict["diff_val"] > threshold]

            selected_keyframe_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 10)

            return selected_keyframe_no_list
        except Exception, e:
            print "usePixelGrayValue error: %s" % str(e)
            return None


    def useHueHist(self):
        """
        [2014] https://github.com/FilippoC/pke/tree/master/src/pke
        step1: divide video into shots using hue(16 bins) hist based comparision 
        step2: extract keyframe from each shot by optical flow
        step3: use frame No. based k-means clustering to select specified number of keyframes
        merits: 
        demerits: ineffectiveness
        """
        try:
            keyframe_no_list = []

            shot_list = self.sbd.byHueHist()

            for shot in shot_list:
                shot_keyframe_no_list = self.skfe.byOpticalFlow(shot)
                keyframe_no_list.extend(shot_keyframe_no_list)

            selected_keyframe_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 10)
            return selected_keyframe_no_list
        except Exception, e:
            print "useHSVHist error: %s" % str(e)
            return None


    def useBlockGrayHist(self):
        """
        [2013] An Algorithm for Shot Boundary Detection and Key Frame Extraction Using Histogram Difference
        step1: convert frame to gray, then divide the gray image into 3 * 3 blocks. calculate the hist for each block
        step2: compute square histogram difference between two conseutive frames
        step3: adaptive threshold is caclulated using frame window, and then video is divided into shots
        step4: extract keyframe from each shot by shot type
        step5: use frame No. based k-means clustering to select specified number of keyframes
        merits: effective, robust
        demerits: fail to elimiate motion blur
        """
        try:
            keyframe_no_list = []
            
            shots_list = self.sbd.byBlockGrayHist()

            for shot in shots_list:
                frame_no = self.skfe.byShotType(shot)
                keyframe_no_list.append(frame_no)

            selected_keyframe_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 10)
            return selected_keyframe_no_list
        except Exception, e:
            print "useGrayHist error: %s" % str(e)
            return None

    
    def useEntropy(self):
        """
        [2016] Video Key-Frame Extraction using Entropy value as Global and Local Feature
        step1: divide video into shots using template matching
        step2: extract keyframe from each shot by entropy
        merits: 
        demerits: very slow, difficult to set the threshold of SBD
        """
        try:
            keyframe_no_list = []
            shots_list = self.sbd.byTemplateMatching()
            for shot in shots_list:
                shot_keyframe_no_list = self.skfe.byEntropy(shot)
                keyframe_no_list.extend(shot_keyframe_no_list)

            selected_keyframe_no_list = keyframe_no_list
            return selected_keyframe_no_list
        except Exception, e:
            print "useEntropy error: %s" % str(e)
            return None


if __name__ == "__main__":
    videofile = sys.argv[1]
    outpath = sys.argv[2]

    cap = cv2.VideoCapture(videofile)       # open video file
    if not cap.isOpened():
        raise Exception("open %s fail!" % videofile)

    videoCommon.showVideoInfo(cap)

    time_begin = time.time()
    kfe = KFE(cap)
    #keyframe_no_list = kfe.usePixelGrayValue()
    #keyframe_no_list = kfe.useHueHist()
    #keyframe_no_list = kfe.useBlockGrayHist()
    keyframe_no_list = kfe.useEntropy()
    print "cost %.2f s" % (time.time() - time_begin)

    videoCommon.saveFramesAsPngs(cap, keyframe_no_list, outpath)
