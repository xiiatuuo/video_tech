#!python2.6
#coding=utf-8
import re
import sys
import time
import json
import urllib
import hashlib
import urllib2
import base64
import binascii

def crc32( v):
  """
  Generates the crc32 hash of the v.
  @return: str, the str value for the crc32 of the v
  """
  return '%d' % (binascii.crc32(v) & 0xffffffff)



def download(url):
    m = hashlib.md5()
    m.update(url)
    file_name = m.hexdigest() + ".mp4"
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

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

def get_video_id(url):
    try:
        u  = urllib2.urlopen(url)
        html = u.read()
        videoid = re.search(r'videoid="\w+', html).group()[9:]
        print videoid
        return videoid
    except Exception,data:
        print data
        return None

def get_main_url(videoid, s, random_r):
    base_url = "http://i.snssdk.com/video/urls/v/1/toutiao/mp4"
    url = base_url + "/" + videoid + "?r=" + random_r  + "&s="+str(s) + "&callback=tt_playerhdhl"
    print url
    try:
        u  = urllib2.urlopen(url)
        result = u.read()
        st = result.find("main_url\":\"")
        print result
        print st
        et = result.find("\"", st+11)
        print et
        main_url = result[st+11:et]
        print main_url
        return main_url
    except Exception,data:
        print data
        return None

def main():
    url = sys.argv[1]
    #http://www.toutiao.com/a6357218760184840450/
    if  re.match(r'http://www.toutiao.com/\w{20}/', url):
        print "yes"
        videoid = get_video_id(url)
        if not videoid:
            return
        random_r = str(int(time.time()*1000))
        s  = crc32("/video/urls/v/1/toutiao/mp4/"+videoid+"?r="+random_r)
        print s
        main_url = get_main_url(videoid , s, random_r)
        real_url = base64.b64decode(main_url)
        print real_url
        download(real_url)


if __name__ == "__main__":
    main()
