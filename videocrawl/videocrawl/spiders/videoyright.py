#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoyyright"
      allowed_domains=[]
     #start_urls=["http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos","http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos","http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos"]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//div[@class="inner active"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/a/@title').extract()
                item['desc']=sel.xpath('div/a/@title').extract()
                item['video_url']=sel.xpath('div/a/@href').extract()
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=sel.xpath('div/a/div/span[@class="c-time"]/span/text()').extract()
                item['classify']="01"
                #yield item 
               # yield item
                yield Request(url=str(item['video_url'][0]),meta={'item':item},callback=self.parse_classify)
      def parse_classify(self,response):
          
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
            
           # item=response.meta['item']
           # item['classify']=response.xpath('//*h1[@class="title"]/a/text()')
           # return item
