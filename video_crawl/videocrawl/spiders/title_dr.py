# -*- coding: UTF-8 -*-
'''
@author:duqianjin
@brief:利用结巴分词提取标题关键词，计算标题关键词的simhash，如果海明距离小于3，则认为标题相似
'''
import jieba, codecs
import jieba.analyse
import redis
import os
from  read_config  import get_dbhost,get_dbport
import hashlib
import sys
from optparse import OptionParser
from  hashes.simhash import simhash
reload(sys)
sys.setdefaultencoding("utf-8")
#计算每个分词的sinhash
def get_key_hash(v):
     if v == "":
         return 0
     else:
         x = ord(v[0])<< 7
         m = 1000003
         mask = 2 ** 64 - 1
         for c in v:
              x = ((x * m) ^ ord(c)) & mask
         x ^= len(v)
         if x == -1:
              x = -2
         return x
#计算标题的simhash
def simhash(tokens):
     v = [0] * 128
     for t in [get_key_hash(x) for x in tokens]:
         bitmask = 0
         for i in range(128):
             bitmask = 1 << i
             if t & bitmask:
                  v[i] += 1
             else:
                  v[i] += -1
     fingerprint = 0
     for i in range(128):
          if v[i] >= 0:
              fingerprint += 1 << i
     return fingerprint
#根据hash值计算海明距离
def hamming_distance(hash1, hash2):
     x = (hash1 ^ hash2) & ((1 << 128) - 1)
     tot = 0
     while x:
          tot += 1
          x &= x - 1
     return tot
#计算相似度
def similarity(hash1,hash2):
     a = float(hash1)
     b= float(hash2)
     if a > b: return b / a
     return a / b

#标题MD5计算
def cal_md5(src):
    MD5 = hashlib.md5()
    MD5.update(src)
    return MD5.hexdigest()


#向数据库插入标题
def insert_title(result,title_md5,hash1):
    db = redis.StrictRedis(host=get_dbhost(),port=get_dbport(),db=0) 
    for word in result:
        db.sadd(word,title_md5)
    db.sadd(title_md5,hash1)

#判断标题是否相似
def is_similar(title):
    db = redis.StrictRedis(host=get_dbhost(),port=get_dbport(),db=0)
    result = jieba.analyse.extract_tags(title,topK = 10)
    hash1 = simhash(result)
    title_md5 =cal_md5(title)
    title_set=set()
    for word in result:
        title_set = title_set | db.smembers(word)
    if not title_set:
        insert_title(result,title_md5,hash1) 
        return False
    for every_md5_title in title_set:
        hash_list=db.smembers(every_md5_title) 
        hash2=hash1
        for i in hash_list:
            hash2=int(i)
            break
        if hamming_distance(hash1, hash2)<3:
            return True
    insert_title(result,title_md5,hash1)
    return False
print is_similar(u'tfboys')
