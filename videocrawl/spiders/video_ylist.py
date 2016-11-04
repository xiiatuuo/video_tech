#-*- coding: UTF-8 -*-
'''
@author:duqianjin
@brief:抓取优酷自媒体频道，例如：http://i.youku.com/i/UMjAwOTkwOTM2/videos
'''
from  date_formate import date_cal
import scrapy
import time
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class Video_ylist_Spider(scrapy.Spider):
      name="video"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(Video_ylist_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          res_sel=Selector(response)
          for sel in res_sel.xpath('//div[@class="v va"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div[@class="v-meta"]/div/a/text()').extract()
                item['desc']=sel.xpath('div[@class="v-meta"]/div/a/text()').extract()
                item['video_url']=sel.xpath('div[@class="v-meta"]/div/a/@href').extract()
                item['date']=sel.xpath('div/div/span[@class="v-publishtime"]/text()').extract()
                item['date'][0]=date_cal(item['date'][0])
                item['duration']=sel.xpath('div/div/span[@class="v-time"]/text()').extract()
                item['classify']="01"
                yield Request(url=str(item['video_url'][0]), meta={'item':item},callback=self.parse_classify)
          #进入下一页页面
          links=response.xpath('//li[@class="next"]')
          for every_url in links:
                        url=str(self.start_urls[0]+every_url.xpath('a/@href').extract()[0])
                        yield Request(url, callback=self.parse)
      #抓取视频类别
      def parse_classify(self,response):
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
            
