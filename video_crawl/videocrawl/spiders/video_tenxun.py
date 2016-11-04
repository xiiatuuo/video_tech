#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class Video_tenxun_Spider(scrapy.Spider):
      name="videotenxun"
      allowed_domains=[]
      index=0
      start_urls=[]
      tengxun_url=" http://v.qq.com"
      def __init__(self, *args, **kwargs):
          super(Video_tenxun_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//span[@class="item item_half"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('a/@title').extract()
                item['desc']=sel.xpath('a/@title').extract()
                item['video_url']=self.tengxun_url+sel.xpath('a/@href').extract()[0]
                item['date']="null"
                item['duration']="null"
                item['classify']=u'动物萌宠'
                yield item 
