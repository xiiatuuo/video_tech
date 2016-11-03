#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoyge"
      allowed_domains=[]
      index=0
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//div[@class="lists"]/div'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/div/a/@title').extract()
                item['desc']=sel.xpath('div/div/a/@title').extract()
                item['video_url']=sel.xpath('div/div/a/@href').extract()
                item['date']="null"
                item['duration']=sel.xpath('div/div/a/div/span/span/text()').extract()
                item['classify']=u'音乐'
                yield item 
