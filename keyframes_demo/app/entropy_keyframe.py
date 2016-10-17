#!usr/local/bin/python2.7
#coding:utf-8
#entropy of keyframes method by liubo17(2016-09-28)

import cv2
import numpy as np
import os,glob
import math
import collections
import time
import video_utils

# 读取图像
def read_images(list_path):
    image_list = []
    if len(list_path) <= 0:
        return image_list
    try:
        for file in list_path:
            try:
                ima = cv2.imread(file, 0)
            except:
                continue
            image_list.append(ima)
    except Exception as e:
        print e.message
        print '读取图像出错\n'
    return image_list

# 获取处理图像尺寸
def obtain_image_size(image):
    width, height = image.shape[:2]
    return width, height

# 获取本地视频帧
def obtain_local_frames(rootdir):
    list_path = []
    try:
        for path in sorted(glob.glob(os.path.join(rootdir ,'*.png')), key=os.path.getmtime):
            print path
            list_path.append(path)
            if os.path.isdir(path):
                obtain_local_frames(path)
    except Exception as e:
        print e.message
    return list_path

# 获取所有视频I帧信息熵由高到低tuple list
def obtain_all_entropy_list(list_path):
    try:
        #list_path = obtain_local_frames(localdir)
        #image_list = read_images(list_path)
        img_dict = {}
        for path in list_path:
            img = cv2.imread(path, 0)
            width, height = img.shape[:2]
            #hist_cv = cv2.calcHist([img],[0],None,[256],[0,256])
            hist_np = np.bincount(img.ravel(),minlength=256)
            print hist_np,type(hist_np),len(hist_np)
            entropy = 0.0
            for i in xrange(len(hist_np)):
                pi = float(hist_np[i]) / float( width * height )
                if pi:  #pi不为0
                    entropy = entropy - math.log(pi) / pi
            entropy_util = round(math.pow(entropy, 2))
            img_dict[path] = entropy_util
        img_tuple_list = sorted(img_dict.iteritems(), key = lambda item:item[1], reverse=True)
        print img_dict
        for img_tuple in img_tuple_list:
            print img_tuple[0],img_tuple[1]
        return img_tuple_list
    except Exception as e:
        print e.message
        return []

# 获取各时间区间里视频信息熵高的I帧tuple list
# @param | list | list_path 本地图片帧所在位置及名称list | int | pick_num 选择帧数量
# @return| list | pick_list 包含所需要挑选的帧位置名称list
# todo
def obtain_duration_entropy_list(list_path, pick_num):
    try:
        tuple_list_list = []
        pick_list = []
        image_num = len(list_path)
        print image_num
        batch_num = image_num / pick_num
        remainder_num = image_num % pick_num
        # 如果帧除挑选帧数量余数不为0，那么前几批中帧图片数量相应增加1
        if remainder_num:
            batch_num += 1
        for_num = 0
        img_dict = {}
        for path in list_path:
            if for_num == 0:
                img_dict = {}
            for_num += 1
            img = cv2.imread(path, 0)
            width, height = img.shape[:2]
            hist_np = np.bincount(img.ravel(),minlength=256)
            entropy = 0.0
            for i in xrange(len(hist_np)):
                pi = float(hist_np[i]) / float( width * height )
                if pi:  #pi不为0
                    entropy = entropy - math.log(pi) / pi
            entropy_util = round(math.pow(entropy, 2))
            img_dict[path] = entropy_util
            if for_num == batch_num:
                img_tuple_list = sorted(img_dict.iteritems(), key = lambda item:item[1], reverse=True)
                tuple_list_list.append(img_tuple_list)
                for_num = 0
                remainder_num -= 1
                if remainder_num == 0:
                    batch_num -= 1
        for tuple_list in tuple_list_list:
            print tuple_list[0][0],tuple_list[0][1],len(tuple_list)
            print tuple_list
            pick_list.append(tuple_list[0][0])
        #去除头尾帧
        if len(pick_list) > 2:
            del pick_list[0]
            del pick_list[-1]
        print pick_list
        return pick_list
    except Exception as e:
        print e.message
        return []

if __name__ == "__main__":
    start = time.time()
    video_utils.obtain_video_keyframes('guxia.mp4', '180*120', 'guxia/', 'out_images-%02d.jpg', 0)
    video_utils.obtain_video_keyframes('guxia.mp4', '180*120', 'guxia/', 'out_images-%02d.png', 0)
    middle = time.time()
    middle_period = middle - start
    #obtain_all_entropy_list('image/')
    list_path = obtain_local_frames('guxia/')
    #obtain_all_entropy_list(list_path)
    obtain_duration_entropy_list(list_path, 8)
    end = time.time()
    period = end - start
    print middle_period,period
