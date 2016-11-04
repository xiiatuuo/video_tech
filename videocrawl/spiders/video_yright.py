#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取优酷视频右侧列表
'''
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class Video_yright_Spider(scrapy.Spider):
      name="videoyright"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(Video_yright_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          res_sel=Selector(response)
          for sel in res_sel.xpath('//div[@class="item"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/div/@title').extract()
                item['desc']=sel.xpath('div/div/@title').extract()
                item['video_url']=sel.xpath('div/div/a/@href').extract()
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=sel.xpath('div/div/a/div/span[@class="c-time"]/span/text()').extract()
                item['classify']=""
                yield Request(url=str(item['video_url'][0]),meta={'item':item},callback=self.parse_classify)
      #抓取视频类别
      def parse_classify(self,response):
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
