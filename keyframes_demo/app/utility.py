#!/usr/bin/python
#coding=utf-8

import sys
import cv2
from cv2 import cv
import numpy as np

def getExtremeMaxValue(value_list):
    try:
        value_list = np.array(value_list)
        cv2.normalize(value_list, value_list, 0, 100, cv2.NORM_MINMAX)

        local_maxinum_list = []

        index = 0
        pre_value = value_list[0]
        upward_trend = True
        for value in value_list:
            if upward_trend:
                if value < pre_value:       # local maximum
                    local_maxinum_list.append((index-1, pre_value))
                    trend_up_flag = False
            else:
                if value >= pre_value:      # local minimum
                    trend_up_flag = True

            pre_value = value
            index += 1

        sorted_local_maxinum_list = sorted(local_maxinum_list, key = lambda ele:ele[1], reverse = True)
        value_index_list = [each[0] for each in sorted_local_maxinum_list[:9]]
        value_index_list = sorted(value_index_list)

        return value_index_list
    except Exception, e:
        print "getExtremeMaxValue error: %s" % str(e)
        return None



def select_centroid_element(cluster, center):
    try:
        result = cluster[0]
        distance_to_center_min = abs(result - center)
    
        for each in cluster:
            distance = abs(each - center)
            if distance < distance_to_center_min:
                distance_to_center_min = distance
                result = each
        return result
    except Exception, e:
        print "select_centroid_element error: %s" % str(e)
        return result

# select specified number of keyframes using k-means clustering
# @param | list | frame_list
# @param | int  | cluster_number
# @return| list | selected_frames
def selectKeyframesByKMeans(frame_list, cluster_number):
    try:
        if len(frame_list) < cluster_number:
            return frame_list

        selected_frames = []

        frame_list_np = np.float32(np.vstack(frame_list))

        # set parameters of clustering
        max_iter_num = 10
        epsilon = 1.0
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter_num, epsilon)

        # clustering
        compactness, labels, centers = cv2.kmeans(frame_list_np, cluster_number, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        for i in xrange(cluster_number):
            cluster = frame_list_np[labels==i]
            center = centers[i][0]
            #print i, cluster
            selected_frame = select_centroid_element(cluster, center)
            selected_frames.append(selected_frame)          
  
        return selected_frames
    except Exception, e:
        print "selectKeyframesByKMeans error: %s" % str(e)
        return []
 
