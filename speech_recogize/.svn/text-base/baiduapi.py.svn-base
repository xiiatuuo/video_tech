#coding=utf-8
import sys
import base64
import wave
import requests
import json 
from config import CLIENT_ID, CLIENT_SECRET, CUID

def get_token():
    '''
    获取api token
    :return:
    '''
    url = 'http://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(CLIENT_ID,CLIENT_SECRET)
    r = requests.get(url)
    item = r.text
    token = json.loads(item)['access_token']
    return token

def recognize(wav_file):
    '''
    wav格式音频，识别
    :param wav_file:
    :return:
    '''
    f = wave.open(wav_file)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    if sampwidth > 2 or framerate not in (8000, 16000):        #原始音频参数必须符合 8k/16k 采样率、16bit 位深、单声道
        print sampwidth
        return
    str_data = f.readframes(nframes)
    base_data = base64.b64encode(str_data).decode('utf-8')      #base64编码
    data = {"format": "wav",
            "rate": framerate,
            "channel": nchannels,
            "token": get_token(),
            "cuid": CUID,
            'speech': base_data,
            'len': len(str_data)}
    url = 'http://vop.baidu.com/server_api'
    headers = {'Content-type': 'application/json',
               'Content-length': str(len(str(data)))}
    resoonse = requests.post(url,headers=headers,json=data)
    result_dict = json.loads(resoonse.text)
    if result_dict["err_msg"] == "success.":
        return " ".join(result_dict["result"])
    else:
        return ""

if __name__ == '__main__':
    #r = recognize('baidutest.wav')
    r = recognize(sys.argv[1])
    print(r)
