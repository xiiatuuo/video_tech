#-*- coding: UTF-8 -*-  
'''
@brief:抓取优酷类别下

'''
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class VideoSpider(scrapy.Spider):
      name="videoygbelow"
      allowed_domains=[]
      index=0
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//div[@class="yk-row"]/div'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/div/a/@title').extract()
                item['desc']=sel.xpath('div/div/a/@title').extract()
                item['video_url']=sel.xpath('div/div/a/@href').extract()
                item['date']="null"
                item['duration']=sel.xpath('div/ul/li/span/span/text()').extract()
                item['classify']="01" 
                yield Request(url=str(item['video_url'][0]), meta={'item':item},callback=self.parse_classify)
          links=response.xpath('//li[@class="next"]')
          for every_url in links:
                url=str(every_url.xpath('a/@href').extract()[0])
                yield Request(url, callback=self.parse)
      def parse_classify(self,response):
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
