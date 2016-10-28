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
@version: 2016/10/21 V1.0
@author: tianxiang
"""

class FDM:
    """
    FDM: Frame Difference Measures
    """

    def convertToGray(self, frame):
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


    def getBlockGrayHist(self, image):
        try:
            block_hist_list = []

            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            height, width = gray_img.shape

            # divide into 3*3 blocks
            width_block, height_block = 3, 3
            width_block_section = width / width_block
            height_block_section = height / height_block

            height_block_begin, height_block_end = 0, height_block_section 
            for i in xrange(height_block):
                if i == height_block - 1:
                    height_block_end = height

                width_block_begin, width_block_end = 0, width_block_section
                for j in xrange(width_block):
                    if j == width_block - 1:
                        width_block_end = width

                    block_img = gray_img[height_block_begin : height_block_end, width_block_begin : width_block_end]

                    # calculate gray histogram for block image
                    block_hist = cv2.calcHist([block_img], [0], None, [256], [0.0, 255.0])
                    #cv2.normalize(block_hist, block_hist, 0, 1, cv2.NORM_MINMAX)
                    block_hist_list.append(block_hist)

                    width_block_begin = width_block_end
                    width_block_end = width_block_end + width_block_section

                height_block_begin = height_block_end
                height_block_end = height_block_end + height_block_section

            return block_hist_list
        except Exception, e:
            print "getBlockGrayHist error: %s" % str(e)
            return None


    def getHueHist(self, image):
        """
        # convert the RGB color model to HSV model, 
        # then cal histogram of Hue which is quantized as 16 bins 
        # normalized the Hue Histogram in [0, 1]
        """
        try:
            hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            h, s, v = cv2.split(hsv_img)

            h_hist = cv2.calcHist([h], [0], None, [16], [0, 255])

            cv2.normalize(h_hist, h_hist, 0, 1, cv2.NORM_MINMAX)
            return h_hist
        except Exception, e:
            print "getHueHist error: %s" % str(e)
            return None

    def byPixelGray(self, pre_gray_frame, cur_gray_frame):
        """
        @param | frame in gray value
        compare two frames pixel by pixel, result is 'cur_frame - pre_frame'
        """
        try:
            # calculate difference between two frames by element to element
            # output an array of the same size as the input frame
            diff_val = cv2.subtract(cur_gray_frame, pre_gray_frame)

            # count non-zero array elements
            diff_num = cv2.countNonZero(diff_val)

            return diff_num
        except Exception, e:
            print "byPixelGray error: %s" % str(e)
            return None


    def byBlockGrayHist(self, pre_gray_hist, cur_gray_hist):
        """
        2009 Key Frame Extraction from MPEG Video Stream
        @param | list | pre_gray_hist | elelment in the list is histogram of block.
        """
        try:
            block_num = len(pre_gray_hist)
            if len(cur_gray_hist) != block_num:
                raise Exception("two hist have different blocks")

            frame_diff = 0.0
            for block in xrange(block_num):
                pre_block_gray_hist = pre_gray_hist[block]
                cur_block_gray_hist = cur_gray_hist[block]
                block_diff = cv2.compareHist(pre_block_gray_hist, cur_block_gray_hist, cv.CV_COMP_CHISQR)   # x^2 hist difference
                frame_diff += block_diff

            return frame_diff
        except Exception, e:
            print "byBlockGrayHist error: %s" % str(e)
            return None


    def byHueHist(self, pre_hue_hist, cur_hue_hist):
        """
        @param | hue histogram
        优点：实现简单
        缺点：sensitive to illumination change
        """
        try:
            hsv_sim = cv2.compareHist(pre_hue_hist, cur_hue_hist, cv.CV_COMP_CORREL) 

            return hsv_sim
        except Exception, e:
            print "byHueHist error: %s" % str(e)
            return None

    def byEdgeOrientation(self):
        """
        优点：robust to illumination change
        """
        try:
            return []
        except Exception, e:
            print "byEdgeOrientation error: %s" % str(e)

    def byCorrelation(self):
        """
        """
        try:
            return []
        except Exception, e:
            print "byCorrelation error: %s" % str(e)


if __name__ == "__main__":
    fdm = FDM()

    img1 = cv2.imread(sys.argv[1])
    img2 = cv2.imread(sys.argv[2])
    hist1 = fdm.getBlockGrayHist(img1)
    hist2 = fdm.getBlockGrayHist(img2)
    print fdm.byBlockGrayHist(hist1, hist2)
    #hue_hist1 = fdm.getHueHist(img1)
    #hue_hist2 = fdm.getHueHist(img2)
    #print fdm.byHueHist(hue_hist1, hue_hist2)

