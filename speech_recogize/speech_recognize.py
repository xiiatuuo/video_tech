#!/usr/bin/python
#coding=utf-8
import os
import sys
import json
from baiduapi import recognize
from end_point_split import split_wavs
from utility import req_bin_server
from config import HOST
from config import PORT



def analysis(text):
    host = HOST
    port = PORT 
    req_dict = {}
    req_dict["cmd"] = "text_analyze"
    req_dict["body"] = {}
    req_dict["body"]["text"] = text
    req_dict["body"]["keyword_num"] = 5
    req_dict["body"]["extend_num"] = 10 
    req_dict["body"]["topic_num"] = 2 
    req_dict["body"]["cate_num"] = 2
    result = req_bin_server(host, port, json.dumps(req_dict))
    return result


def speech_to_text(video_file):
    base_dir = os.path.dirname(video_file)
    video_name = os.path.basename(video_file)
    wav_file = os.path.join(base_dir, video_name.split(".")[0]+".wav")
    cmd = "ffmpeg -y -i "  + video_file + " -f wav -vn -ar 16000 -ac 1 " + wav_file 
    os.system(cmd)
    out_file_list  = split_wavs(wav_file, base_dir)
    result_list = []
    for f in out_file_list:
        res = recognize(f)
        result_list.append(res)

    text = " ".join(result_list)
    return text




if __name__ == "__main__":
    speech_to_text(sys.argv[1])
