#!python
import sys
import os
import hashlib
import cv2
import numpy as np

class CopyDetector(object):

    def get_file_md5(self, filename):
        if not os.path.isfile(filename):
            return False
        myhash = hashlib.md5()
        f = file(filename,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def md5_check(self, video_path_a, video_path_b):
        indentity_a = self.get_file_md5(video_path_a)
        indentity_b = self.get_file_md5(video_path_b)
        if indentity_a == indentity_b:
            return True
        else:
            return False


    def sift_match(self, image_a, image_b):
        img_a = cv2.imread(image_a, 0)
        img_b = cv2.imread(image_b, 0)
        
        sift = cv2.SIFT()
        kp_a, des_a = sift.detectAndCompute(img_a, None)
        kp_b, des_b = sift.detectAndCompute(img_b, None)
        #print "KPA:",len(kp_a)
        #print "KPB:",len(kp_b)
        bf  = cv2.BFMatcher()
        matcher = bf.knnMatch(des_a, des_b, k = 2)
        good = []
        for m,n in matcher:
            if m.distance < 0.75*n.distance:
                good.append([m])
        if 1.0*len(good) / min(len(kp_a), len(kp_b)) > 0.25:
            print "MATCH :", len(good), "/", len(kp_a), "|", len(kp_b)
            return True
        else:
            print "NOT MATCH:", len(good), "/", len(kp_a), "|", len(kp_b)
            return False

    def sift_check(self, key_images_list_a, key_images_list_b):
        a_len = len(key_images_list_a)
        b_len = len(key_images_list_b)
        match_num = 0
        for i in key_images_list_a:
            for j in key_images_list_b:
                print i, " vs ", j
                if self.sift_match(i, j):
                    match_num += 1
                    break
        print a_len, b_len, match_num
        if match_num > max(a_len, b_len)/ 2:
            return True
        else:
            return False



if __name__ == "__main__":
    cd = CopyDetector()
    #print cd.md5_check(sys.argv[1], sys.argv[2])
    import glob
    l = glob.glob("static/9955fe8013af83fd6e479d7821302740/*.png")
    a = []
    b = []
    for i in l:
        if i.find("out") == -1:
            a.append(i)
        else:
            b.append(i)
    a = ['./static/265919679fc11bbc6d4d9f0741e778b9/125.png', './static/265919679fc11bbc6d4d9f0741e778b9/374.png', './static/265919679fc11bbc6d4d9f0741e778b9/644.png', './static/265919679fc11bbc6d4d9f0741e778b9/829.png', './static/265919679fc11bbc6d4d9f0741e778b9/919.png', './static/265919679fc11bbc6d4d9f0741e778b9/1009.png', './static/265919679fc11bbc6d4d9f0741e778b9/1127.png', './static/265919679fc11bbc6d4d9f0741e778b9/1282.png', './static/265919679fc11bbc6d4d9f0741e778b9/1484.png', './static/265919679fc11bbc6d4d9f0741e778b9/1523.png']
    b = ['./static/8ad8ada8e9ed81799e7aaa494c5df471/111.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/237.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/474.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/644.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/770.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/829.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/919.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/1124.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/1282.png', './static/8ad8ada8e9ed81799e7aaa494c5df471/1499.png']
    print cd.sift_check(a, b)
