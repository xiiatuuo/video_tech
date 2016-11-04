# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VideocrawlItem(scrapy.Item):
#TODO
        title   =scrapy.Field()#视频标题
        desc    =scrapy.Field()#视频描述
        classify=scrapy.Field()#视频分类
        video_url=scrapy.Field()#视频url
        date  =  scrapy.Field()#视频日期
        duration=scrapy.Field()#视频时长
