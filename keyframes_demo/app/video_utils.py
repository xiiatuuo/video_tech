#!usr/local/bin/python2.7
#coding:utf-8
#video util-functions by liubo17

import subprocess
import re
import os,glob

# 获取视频总时长
# @param | string | videoname 视频所在位置名称
# @return| string | video_time 视频总时长，类型为%h:%m:%s，其中秒可能不为整数 
def obtain_video_time(videoname):
    video_time = None
    #videopath = videoname
    try:
        child = subprocess.Popen('ffmpeg -i %s 2>&1' % videoname, stdout = subprocess.PIPE, shell = True)
        duration = child.stdout.read()
        print duration
        pattern = re.compile('(?<=Duration: ).*?(?=,)')
        video_time = pattern.search(duration).group()
    except Exception as e:
        print e
        print '读取视频时长出错\n'
    return video_time

# 获取视频分辨率
# @param | string | videoname 视频所在位置名称
# @return| string | video_ratio 视频分辨率,如800x600
def obtain_video_ratio(videoname):
    video_ratio = None
    #videopath = videoname
    try:
        child = subprocess.Popen('ffmpeg -i %s 2>&1' % videoname, stdout = subprocess.PIPE, shell = True)
        duration = child.stdout.read()
        print duration
        pattern = re.compile('(\d{2,}x\d+)')
        video_ratio = pattern.search(duration).group()
    except Exception as e:
        print e
        print '读取视频分辨率出错\n'
    return video_ratio

# 获取视频关键帧
# @param | string | videoname 视频所在位置名称,frame_ratio 视频帧分辨率,frame_path 视频帧文件夹,frame_name 视频帧位置名称（无需后缀）| int | frame_num 视频帧数量
# @return| Bool   | True or False
def obtain_video_keyframes(videoname, frame_ratio, frame_path, frame_name, frame_num):
    try:
        if not os.path.exists(frame_path):
            os.makedirs(frame_path)
        frame_path_name = frame_path + frame_name
        returncode = subprocess.call("ffmpeg -i %s -vf select='eq(pict_type\,I)' -vsync 2 -s %s -f image2 %s" % (videoname,frame_ratio,frame_path_name), shell = True)
        if returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print e.message
        print '获取视频关键帧出错\n'
        return False

# 下载网页链接视频
def obtain_online_video(path, name, url):
    try:
        if path and name:
            returncode = subprocess.call('you-get -o %s -O %s "%s"' % (path, name, url), shell = True)
        elif path:
            returncode = subprocess.call('you-get -o %s "%s"' % (path, url), shell = True)
        elif name:
            returncode = subprocess.call('you-get -O %s "%s"' % (name, url), shell = True)
        else:
            returncode = subprocess.call('you-get "%s"' % (url), shell = True)
        if returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print e.message
        print 'download video error\n'
        return False


# 获取本地视频帧

def obtain_local_frames(rootdir):
    list_path = []
    try:
        for path in sorted(glob.glob(os.path.join(rootdir ,'*.jpg')), key=os.path.getmtime):
            print path
            list_path.append(path)
            if os.path.isdir(path):
                obtain_local_frames(path)
    except Exception as e:
        print e.message
    return list_path
            

if __name__ == "__main__":
    #obtain_online_video('image/', 'downtest.mp4', 'http://weibo.com/p/230444463048de15f7ff201eba91cfff16ec41')
    #obtain_online_video('image/', None, 'http://weibo.com/p/230444097452d6234b993683b96731817bd37c')
    #obtain_online_video(None, None, 'http://weibo.com/p/230444e69f643a554a43cfac99672611703e8a')
    #obtain_online_video(None, 'downtest2.mp4', 'http://weibo.com/p/23044439ab235cfe6e7556b5b4c79d369d9e48')
    video_time = obtain_video_time('test.mp4')
    print video_time
    video_ratio = obtain_video_ratio('test.mp4')
    print video_ratio
    obtain_video_keyframes('test.mp4', video_ratio, 'image/' ,'out_images-%02d.jpg', 0)
    #obtain_local_frames('image/')
