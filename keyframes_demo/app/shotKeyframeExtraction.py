#!/usr/bin/python
#coding=utf-8
import os
import sys
import time

import math
import numpy as np
import cv2
try:
    import cv
except Exception, e:
    from cv2 import cv


from frameDifferenceMeasures import FDM 

"""
@version: 2016/10/20 V1.0
@author: tianxiang
"""


class SKFE:
    """
    SKFE: Shot Keyframe Extraction
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

    def hueHistKMeansPlus(self, frame_no_list):
        try:
            cluster_list = []
            for frame_no in frame_no_list:
                self.__cap.set(cv.CV_CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = self.__cap.read()
                cur_hue_hist = self.__fdm.getHueHist(frame)

                if len(cluster_list) == 0:              # cluster init
                    cluster_dict = {"center": cur_hue_hist, "frame_list": [(frame_no, cur_hue_hist)]}
                    cluster_list.append(cluster_dict)
                else:
                    index = 0
                    cluster_no, sim_MAX = -1, 0.9       # record max sim and cluster index
                    for cluster_dict in cluster_list:
                        sim = abs(self.__fdm.byHueHist(cluster_dict["center"], cur_hue_hist))
                        if sim > sim_MAX:               # update max sim
                            sim_MAX = sim
                            cluster_no = index
                        index += 1

                    if  cluster_no == -1:               # cluster_no does't change, that means frame isn't close enough to be put in any of the clusters
                        cluster_dict = {"center": cur_hue_hist, "frame_list": [(frame_no, cur_hue_hist)]}
                        cluster_list.append(cluster_dict)
                    else:
                        cluster_dict = cluster_list[cluster_no] 
                        cluster_size = len(cluster_dict["frame_list"])
                        cluster_dict["frame_list"].append((frame_no, cur_hue_hist))
                        cluster_dict["center"] = (cluster_dict["center"] * cluster_size + cur_hue_hist * 1.0) / (cluster_size + 1.0)

            keyframe_no_list = []
            avg_cluster_size = len(frame_no_list) / len(cluster_list) 
            for cluster_dict in cluster_list:
                #if len(cluster_dict["frame_list"]) < avg_cluster_size:
                #    continue
                keyframe_no, sim_MAX = None, 0
                for frame_no, hue_hist in cluster_dict["frame_list"]:
                    sim = self.__fdm.byHueHist(cluster_dict["center"], hue_hist)
                    if sim > sim_MAX:
                        sim_MAX = sim
                        keyframe_no = frame_no
                keyframe_no_list.append(keyframe_no)
            return keyframe_no_list
        except Exception, e:
            print "hueHistKMeansPlus error: %s" % str(e)


    def byShotType(self, shot):
        try:
            fdm = FDM()

            seccessive_diff_list = []

            ref_frame_dict = shot[0][1]
            ref_frame_hist = ref_frame_dict["hist"]
            seccessive_diff_list.append(ref_frame_dict["diff"])
            max_diff, frame_no = 0, None
            for i in xrange(1, len(shot) - 1):
                cur_frame_no, cur_frame_dict = shot[i]
                cur_frame_hist = cur_frame_dict["hist"]
        
                seccessive_diff_list.append(cur_frame_dict["diff"])

                diff = fdm.byBlockGrayHist(cur_frame_hist, ref_frame_hist)
                if diff > max_diff:
                    max_diff = diff
                    frame_no = cur_frame_no

            threshold = np.mean(seccessive_diff_list) + np.std(seccessive_diff_list)
            if max_diff < threshold:
                shot_index = len(shot) / 2
                frame_no = shot[shot_index][0]

            return frame_no
        except Exception, e:
            print "byShotType error: %s" % str(e)
            return None

    def byOpticalFlow(self, shot):
        try:
            keyframes_no_list = []
            if len(shot) == 1:
                keyframes_no_list.append(shot[0])
                return keyframes_no_list

            op_min, op_max = None, None
            frame_min_no, frame_max_no = None, None
            for i in xrange(1, len(shot) - 1):
                pre_frame_no, pre_frame = shot[i-1]
                cur_frame_no, cur_frame = shot[i]

                op_val = self.__calOpticalFlow(pre_frame, cur_frame)
                if op_val == None:
                    continue

                if op_min == None :
                    op_min = op_val
                    frame_min_no = pre_frame_no
                    op_max = op_val
                    frame_max_no = cur_frame_no
                else:
                    if op_val < op_min:
                        op_min = op_val
                        frame_min_no = pre_frame_no
                    if op_val > op_max:
                        op_max = op_val
                        frame_max_no = pre_frame_no

            keyframes_no_list.append(frame_min_no)
            keyframes_no_list.append(frame_max_no)
            return keyframes_no_list
        except Exception, e:
            print "byOpticalFlow error: %s" % str(e)
            return []

    def byEntropy(self, shot):
        try:
            keyframes_no_list = []
            entropy_list = []
            if len(shot) == 1:
                keyframes_no_list.append(shot[0])
                return keyframes_no_list

            for frame_no, frame in shot:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                height, width = gray_frame.shape
                gray_hist = cv2.calcHist([gray_frame], [0], None, [256], [0.0, 255.0])
   
                frame_entropy = 0.0
                for each_bin in gray_hist:
                    p = each_bin[0]/ (height * width)
                    if p > 0:
                        frame_entropy += (math.log(p) * -1 / p)

                entropy_list.append(frame_entropy)
                frame_entropy_dict = {}
                frame_entropy_dict[frame_no] = {"frame": frame, "entropy": frame_entropy}

            avg_entropy = np.mean(entropy_list)

            keyframe_no = shot[0][0]
            MIN_diff = avg_entropy
            for frame_no, frame_info_dict in frame_entropy_dict.iteritems():
                entropy_diff = abs(frame_info_dict["entropy"] - avg_entropy)
                if entropy_diff < MIN_diff:
                    MIN_diff = entropy_diff
                    keyframe_no = frame_no
    
            keyframes_no_list.append(keyframe_no)
            return keyframes_no_list
        except Exception, e:
            print "byEntropy error: %s" % str(e)
            return []

if __name__ == "__main__":
    image1 = cv2.imread(sys.argv[1])
    image2 = cv2.imread(sys.argv[2])
    shot = [(0,image1), (1,image2)]

    skfe = SKFE(None)
    print skfe.byEntropy(shot)
    
