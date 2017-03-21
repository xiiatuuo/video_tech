#!python
#coding=utf-8
import os
import sys
import json
import wave

class Speech(object):
    def __init__(self, filename):
        self.filename  = filename
        self.__parse_info()


    def __parse_info(self):
        cmd =  'ffprobe -v quiet -print_format json -show_format -show_streams -i "' +  self.filename + '"' 
        res = os.popen(cmd).read()
        try:
            result_dict = json.loads(res)
            print result_dict
            self.channel = result_dict["streams"][0]["channels"]
            self.rate = result_dict["streams"][0]["sample_rate"]
            self.size = result_dict["format"]["size"]
            self.format = result_dict["format"]["format_name"].encode("utf-8")
            self.fp = wave.open(self.filename, 'rb')  
            self.data =  self.fp.readframes(self.fp.getnframes())

        except Exception,data:
            print Exception,data





if __name__ == "__main__":
    s = Speech(sys.argv[1])
    print s.channel
    print s.rate
    print s.size
    print s.format
