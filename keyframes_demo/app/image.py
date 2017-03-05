#!python
#coding=utf-8
from hashlib import md5
import os
import sys
import cookielib
import urllib2
from config import basedir

class Image(object):
    def __init__(self, url):
        self.url = url
        self.indentity = md5(url.strip()).hexdigest()
        self.image_name = self.indentity + ".img"
        self.image_file = os.path.join(basedir, 'static', self.image_name)
        #self.image_file = os.path.join(os.path.abspath("."), './static', self.indentity + ".img")
        self.score = 0.0

    def download_image(self):
        try:
            if not os.path.isfile(self.image_file):
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
                headers = { 'User-Agent' : user_agent }  
                req  = urllib2.Request(self.url, headers=headers)
                res  = urllib2.urlopen( req )
                data= res.read()
                if data:
                    file=open(self.image_file, "wb")
                    file.write(data)
            if not os.path.isfile(self.image_file) or not os.path.getsize(self.image_file):
                return None, "download error"
            else:
                return True,"download succ"
        except Exception,data:
            print data
            return None,str(data)


    def is_porn(self):
        # settled docker image path is /data1/xiatuo/video_tech/keyframes_demo/app/static
        cmd="docker exec open_nsfw python /opt/open_nsfw/classify_nsfw.py --model_def /opt/open_nsfw/nsfw_model/deploy.prototxt --pretrained_model /opt/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel " + self.image_name + " 2>/dev/null"
        result = os.popen(cmd).read()
        print result
        self.score = float(result.strip().split(" ")[-1])*100
        if self.score > 60:
            return True
        else:
            return False

    def classify(self):
        cmd = "cd /usr/local/python27/lib/python2.7/site-packages/tensorflow/models/image/imagenet;  sh short_tf_image.sh " + self.image_file 
        result = os.popen(cmd).read()

        print cmd
        print result
        return result


if __name__ == "__main__":
    pi = Image(sys.argv[1])
    pi.download_image()
    print pi.classification()

