#!python
#coding=utf-8
# 主要是一些视频的基本属性
from hashlib import md5
import os
import sys
import json
import glob
import urllib
import urllib2
from video_utils import obtain_online_video
from config import basedir
from config import SOURCE


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../speech_recogize"))
reload(sys)
sys.setdefaultencoding('utf-8')


from speech_recognize import  speech_to_text
from speech_recognize import  analysis



def url_get(url):
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req, timeout=10).read()
    return resp

def query_id(s):
    url  = "http://i.api.weibo.com/statuses/queryid.json?source=%s&mid=%s&type=1&isBase62=1" % (SOURCE, s)
    result = url_get(url)
    result_dict = json.loads(result)
    return result_dict["id"]

def query_mid(s):
    url  = "http://i.api.weibo.com/statuses/querymid.json?source=%s&id=%s&type=1" % (SOURCE, s)
    result = url_get(url)
    result_dict = json.loads(result)
    return result_dict['mid']

def get_weibo_url(mid):
    url = "http://i.api.weibo.com/2/statuses/show_batch.json?source=%s&trim_user=1&ids=%s" % (SOURCE, mid)
    result = url_get(url)
    result_dict = json.loads(result)
    if result.find("删除") != -1:
        return "Deleted"
    for object in result_dict["statuses"][0]["url_objects"]:
        if object["object"]["object_type"] == "video":
            return object["object"]["object"]["stream"]["url"]
    return ""

def get_weibo_text(mid):
    url = "http://i.api.weibo.com/2/statuses/show_batch.json?source=%s&trim_user=1&ids=%s" % (SOURCE, mid)
    result = url_get(url)
    result_dict = json.loads(result)
    return result_dict["statuses"][0]["text"]


def get_weibo_link(mid):
    url = "http://i.api.weibo.com/2/statuses/show_batch.json?source=%s&trim_user=1&ids=%s" % (SOURCE,mid)
    result = url_get(url)
    result_dict = json.loads(result)
    uid = str(result_dict["statuses"][0]["uid"])
    base64_mid = query_mid(mid)
    return "http://weibo.com/"+uid+"/"+base64_mid


def parse_video_url(url):
    result = url_get(url)
    if url.find("miaopai") != -1:
        st = result.find("videoSrc") + 11
        et = result.find(",", st)
        url = result[st:et-1]
    else:
        st = result.find("flashvars")
        et = result.find("&", st)
        url = result[st: et].split("=")[2]

    return urllib.unquote(url)
 

def url_to_url(url):
    et = url.find("?")
    base62_mid = url[:et].split("/")[-1]
    mid = query_id(base62_mid)
    video_url = get_weibo_url(mid)
    return video_url 

def mid_to_url(mid):
    video_url = get_weibo_url(mid)
    return video_url 


def meta_download(filename, url):
    print filename
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    
    f.close()


class Video(object):
    def __init__(self, init):
        try:
            mid = str(int(init))
            self.mid = mid
        except Exception,data:
            self.mid = ""
            self.url = init
        self.indentity = md5(init.strip()).hexdigest()

        self.image_path = os.path.join(basedir, 'static', self.indentity)
        if not os.path.isdir(self.image_path):
            os.mkdir(self.image_path)
        self.video_file = os.path.join(self.image_path, self.indentity + ".mp4")
        self.video_name = self.indentity + ".mp4"



    def download_video(self):
        if self.mid:
            video_url = mid_to_url(self.mid)
        else:
            video_url  = url_to_url(self.url)

        try:
            if not os.path.isfile(self.video_file):
                #obtain_online_video(self.image_path, self.video_name , self.url)
                meta_download(self.video_file, video_url)
            if not os.path.isfile(self.video_file):
                return None, "download error"
        except Exception,data:
            print Exception,data
            return None, "download error"
        return True, "dwonload succ"


def do_it_by_mid(mid):
    vd = Video(mid)
    vd.download_video()
    text = speech_to_text(vd.video_file)
    print "RESULT","\t", vd.mid, "\t", text
    result = analysis(text)
    result_dict = json.loads(result)
    keywords = [ i["w"]+":"+i["s"] for i in result_dict["cont"]["keywords"] ]
    cate = [ i["c"]+":"+i["s"] for i in result_dict["cont"]["cate"] ]
    print "RESULT","\t", vd.mid, "\t", ",".join(keywords),"\t",",".join(cate)
    result_list = []
    result_list.append(text)
    result_list.append(",".join(keywords))
    result_list.append(",".join(cate))
    return "\n".join(result_list)


def do_it(url):
    vd = Video(url)
    vd.download_video()
    text = speech_to_text(vd.video_file)
    print "RESULT","\t", vd.url, "\t", text
    try:
        result = analysis(text)
        result_dict = json.loads(result)
        if result_dict["ret"] != 0:
            return "can not analysis , with text is ["+text+"]"
    except Exception,data:
        return str(data)
    keywords = [ i["w"]+":"+i["s"] for i in result_dict["cont"]["keywords"] ]
    cate = [ i["c"]+":"+i["s"] for i in result_dict["cont"]["cate"] ]
    print "RESULT","\t", vd.url, "\t", ",".join(keywords),"\t",",".join(cate)
    result_list = []
    result_list.append("TEXT:["+text+"]")
    result_list.append("KEYWORDS:[" + ",".join(keywords) +"]")
    result_list.append("CATE:[" + ",".join(cate) +"]")
    res = "\n".join(result_list)
    return res



def test_mids():
    f = open(sys.argv[1])
    for line in f:
        mid = line.strip()
        try:
            do_it_by_mid(mid)
        except Exception,data:
            print Exception
            print "RESULT","\t", mid, "ERROR"

def test_urls():
    f = open(sys.argv[1])
    for line in f:
        url = line.strip()
        try:
            do_it(url)
        except Exception,data:
            print Exception
            print "RESULT","\t", mid, "ERROR"


def test_get_weibo_text():
    f = open(sys.argv[1])
    for line in f:
        line = line.strip()
        try:
            text = get_weibo_text(line)
            print line,"\t",len(text),"\t",text
        except Exception,data:
            pass


def test_get_urls():
    f = open(sys.argv[1])
    for line in f:
        mid = line.strip()
        try:
            print mid, "\t",mid_to_url(mid)
        except Exception,data:
            print mid, "\tERROR"

if __name__ == "__main__":
    #test_mids()
    #test_get_urls()
    print mid_to_url(sys.argv[1])
