#!/usr/bin/python
#coding=utf-8

import sys
import time

import cv2
from cv2 import cv
import numpy as np

import videoCommon
import utility

# convert the RGB color model to HSV model, 
# then cal histogram of Hue which is quantized as 16 bins 
# normalized the Hue Histogram in [0, 1]
def calHueHist(image):
    try:
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_img)

        h_hist = cv2.calcHist([h], [0], None, [16], [0, 255])

        cv2.normalize(h_hist, h_hist, 0, 1, cv2.NORM_MINMAX)
        return h_hist
    except Exception, e:
        print "getHSVColorHistogram error: %s" % str(e)
        return None

# divide video into shots using shot boundary detection, 
# which is based on HSV color histogram intersection
def divideToShots(cap):
    try:
        shots_list = []                         # list of shots

        pre_hue_hist = None
        cur_shot = []                           # a shot is a list of frames
        while True:
            succ, frame = cap.read()
            if not succ:
                break

            frame_no = int(cap.get(cv.CV_CAP_PROP_POS_FRAMES) - 1)

            cur_hue_hist = calHueHist(frame)

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
        print "divideToShots error: %s" % str(e)
        return shots_list


def calOpticalFlow(frame1, frame2):
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


# @param | list | shot      | A list of frame, like [(frame_no, frame)]
# @return| list | key_frames| A list of keyframes, like [(frame_no, frame)], one element at least and two elements at most
def extractKeyframesFromShot(shot):
    try:
        key_frames = []
        if len(shot) == 1:
            key_frames.append(shot[0])
            return key_frames

        op_min, op_max = None, None
        frame_min, frame_max = None, None
        for i in xrange(1, len(shot) - 1):
            pre_frame_pair = shot[i-1]
            cur_frame_pair = shot[i]

            op_val = calOpticalFlow(pre_frame_pair[1], cur_frame_pair[1])
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

        key_frames.append(frame_min)
        key_frames.append(frame_max)
        return key_frames
    except Exception, e:
        print "extractKeyframesFromShot error: %s" % str(e)
        return keyframes



def extractKeyFrames(video_file, out_path):
    try:
        time_start = time.time()

        cap = cv2.VideoCapture(video_file)      # read video file
        if not cap.isOpened():
            raise Exception("open %s fail!" % video_file)

        videoCommon.showVideoInfo(cap)

        # divide video to shots
        shots_list = divideToShots(cap)
        if len(shots_list) == 0:
            raise Exception("divide %s to shots fail!" % video_file)

        # extract candidate keyframes from shots
        keyframes = []
        for shot in shots_list:
            shot_no_list = [each[0] for each in shot]
            shot_keyframes = extractKeyframesFromShot(shot)
            keyframes.extend(shot_keyframes)

        keyframe_dict = {}
        for each in keyframes:
            frame_no = int(each[0])
            frame = each[1]
            keyframe_dict[frame_no] = frame

        # choose result keyframes using k-means clustering
        keyframe_no_list = keyframe_dict.keys()
        selected_keyframe_no_list = utility.selectKeyframesByKMeans(keyframe_no_list, 9)

        # output result keyframes
        videoCommon.saveFramesAsPngs(cap, selected_keyframes_no_list, out_path)

        cap.release()

        time_end = time.time()
        print "extractKeyFrames cost %.2f s" % (time_end - time_start)

    except Exception, e:
        print "extractKeyFrames error: %s" % str(e)


if __name__ == "__main__":
    video_file = sys.argv[1]
    out_path = sys.argv[2]
    extractKeyFrames(video_file, out_path)
