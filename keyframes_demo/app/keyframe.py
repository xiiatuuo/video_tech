#!python
#coding=utf-8
from hashlib import md5
import os
import sys
import glob
from video_utils import obtain_online_video
from video_utils import obtain_video_keyframes
from video_utils import obtain_video_ratio 
from entropy_keyframe  import obtain_local_frames
from entropy_keyframe import obtain_all_entropy_list
from entropy_keyframe import obtain_duration_entropy_list
from keyFrame_gray_pixel import  extractKeyFrames
from keyframeExtraction import KFE
from config import basedir

class KeyFrame(object):
    def __init__(self, url):
        self.url = url
        self.key_images_path = []
        self.indentity = md5(url.strip()).hexdigest()
        self.image_path = os.path.join(basedir, 'static', self.indentity)
        self.video = os.path.join(self.image_path, self.indentity + ".mp4")
        self.video_name = self.indentity + ".mp4"
        self.absolute_keyframs_list = []

    def download_video(self):
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        try:
            if not os.path.isfile(self.video):
                obtain_online_video(self.image_path, self.video_name , self.url)
            if not os.path.isfile(self.video):
                return None, "download error"
            image_list  = glob.glob(os.path.join(self.image_path,"*.png"))
            for i in image_list:
                os.remove(i)
        except Exception,data:
            return None, "download error"
        return True, "dwonload succ"


    def entropy_based(self):
        key_images_path = []
        image_list  = glob.glob(os.path.join(self.image_path,"out_images*.png"))
        for i in image_list:
            os.remove(i)
        try:
            ratio = obtain_video_ratio(self.video)
            print "RATIO:",ratio
            #wigth = int(ratio.split("x")[0])/2
            #hight = int(ratio.split("x")[1])/2
            #ratio = str(wigth) + "x" + str(hight)
            obtain_video_keyframes(self.video, ratio ,self.image_path,'/out_images-%03d.png', 200)
        except Exception,data:
            return None, "obtail keyframes error"
        try:
            image_list =  obtain_local_frames(self.image_path)
            keyframs_list = obtain_duration_entropy_list(image_list, 12)
            print keyframs_list
            self.absolute_keyframs_list = keyframs_list[:10]
            for frame in keyframs_list[:10]:
                absolute_path  = frame
                print absolute_path
                start = absolute_path.find("static")
                print start
                relative_path = absolute_path[start-1:]
                key_images_path.append(relative_path)
            print key_images_path
        except Exception,data:
            print data
            return None, "compute entropy error"
        return key_images_path,"Succ"

    def sorted_as_number(self,path, suffix):
        sorted_image_list = []
        image_list  = glob.glob(os.path.join(path,"*."+suffix))
        number_dict = {}
        for i in image_list:
            if i.find("out_image") != -1:
                continue
            compare_num = os.path.basename(i).split(".")[0].split("_")[-1]
            number_dict[i] = int(compare_num)
        sorted_tuple = sorted(number_dict.items() , key = lambda d:d[1])
        for t in sorted_tuple:
            sorted_image_list.append(t[0])
        return sorted_image_list


    #def gray_pixel_based(self):
    #    key_images_path = []
    #    try:
    #        extractKeyFrames(self.video, self.image_path)
    #        keyframs_list = self.sorted_as_number(self.image_path, "png")
    #        self.absolute_keyframs_list = keyframs_list[:10]
    #        for frame in keyframs_list[:10]:
    #            absolute_path  = frame
    #            print absolute_path
    #            start = absolute_path.find("static")
    #            relative_path = absolute_path[start-1:]
    #            key_images_path.append(relative_path)
    #        print key_images_path
    #    except Exception,data:
    #        print data
    #        return None, "compute gray pixel error"

        return key_images_path,"Succ"


    def method1(self):
        try:
            cap = cv2.VideoCapture(self.video)       # open video file
            if not cap.isOpened():
                raise Exception("open %s fail!" % videofile)

            kfe = KFE(cap)
            keyframe_no_list = kfe.usePixelGrayValue()

            videoCommon.saveFramesAsPngs(cap, keyframe_no_list, outpath)

        except Exception, data:
            print data


    def method2(self):
        try:
            cap = cv2.VideoCapture(self.video)       # open video file
            if not cap.isOpened():
                raise Exception("open %s fail!" % videofile)

            kfe = KFE(cap)
            keyframe_no_list = kfe.useBlockGrayHist()

            videoCommon.saveFramesAsPngs(cap, keyframe_no_list, outpath)

        except Exception, data:
            print data



if __name__ == "__main__":
    kf = KeyFrame("test")
    print kf.sorted_as_number(sys.argv[1],"png")

