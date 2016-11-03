# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideocrawlItem(scrapy.Item):
        title   =scrapy.Field()
        desc    =scrapy.Field()
        classify=scrapy.Field()
        video_url=scrapy.Field()
        date  =  scrapy.Field()
        duration=scrapy.Field()
