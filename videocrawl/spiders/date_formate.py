#-*- coding:utf8 -*-
'''
@author:duqianjin
@brief:normal time format
'''
import time
import datetime
import re
import string

#时间串内去电期字，例如2016-10-11期
def sub_date(date):
    pos = pos=date.find(u'期')
    if pos != -1:
        date = date[:pos]
    return date
def sub_load(date_time):
    pos = date_time.find(u'上传')
    if pos!=-1:
        date_time = date_time[:pos]
    return date_time

#变化-为/
def trans_char(date_time):
    return date_time.replace('-','/')


#截取发布日期中的日期，去掉后面的具体时间 例如 09-01 10:23:23
def process_time(date_time):
    pos=date_time.find(' ')
    if pos!=-1:
       date_time=date_time[:pos]
    return date_time

#处理例如 09/01格式
def process_year(date_time):
    if len(date_time)>2:
     if date_time[2]=='/':
       if date_time[3]=='0':
          date_time=date_time[:3]+date_time[4:]
       if date_time[0]=='0':
          date_time=date_time[1:]
       date_year=time.localtime()[0]
       date_time=str(date_year)+'/'+date_time
    return date_time


#处理例如 2016/09/08格式
def sub_zero(date_time):
    if len(date_time)>8:
        if date_time[4]=='/': 
            if date_time[8]=='0':
                date_time=date_time[:8]+date_time[9:]
            if date_time[5]=='0':
                date_time=date_time[:5]+date_time[6:]

    return date_time
 #处理几天前格式
def process_day(date_time):
    if len(date_time)>7:
        return date_time
    number=re.findall(r'\d+',date_time)
    if not number:
        number=['null',]
    day=time.localtime()[2]
    month=time.localtime()[1]
    year=time.localtime()[0]
    for i in date_time:
        if i==u'小':
            break
        if i==u'昨':
           number=number[0].replace('null',str(1))
        if i==u'前':
           number=number[0].replace('null',str(2))
        if i==u'天':
            day=time.localtime()[2]-string.atoi(number[0],10)
            if day<1:
               month=month-1
               day=30+day
               if month<1:
                   month=12+month
                   year=year-1
            break
        if i==u'月':
            month=time.localtime()[1]-string.atoi(number[0],10) 
            if month<1:
                month=12+month
                year=year-1
            break
        if i==u'年':
            year=time.localtime()[0]-string.atoi(number[0],10) or 1999
            break  
    date="%d/%d/%d" %(year,month,day)
    return date

def date_cal(date_time):
    #截取期字
    date_time=sub_date(date_time)
    #截取上传
    date_time =sub_load(date_time)
    #变化-为/    
    date_time=date_time.replace('-','/')
    #截取发布日期中的日期，去掉后面的具体时间 例如 09-01 10:23:23
    date_time=process_time(date_time)
   #处理例如 09/01格式
    date_time = process_year(date_time)
    #处理例如 2016/09/08格式
    date_time = sub_zero(date_time)
    #处理几天前格式
    date_time = process_day(date_time)
    return date_time
