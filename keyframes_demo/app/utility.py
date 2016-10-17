#!/usr/bin/python
#coding=utf-8

import sys
import cv2
from cv2 import cv
import numpy as np

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
            selected_frame = select_centroid_element(cluster, center)
            selected_frames.append(selected_frame)          
  
        return selected_frames
    except Exception, e:
        print "selectKeyframesByKMeans error: %s" % str(e)
        return []
 
