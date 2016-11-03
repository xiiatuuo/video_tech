#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoiasearch"
      allowed_domains=[]
      index=0
     #start_urls=["http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos","http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos","http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos"]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          #item=VideocrawlItem()
          for sel in sell.xpath('//li[@class="list_item"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/h3/a/@title').extract()
                item['desc']=sel.xpath('div/h3/a/@title').extract()
                item['video_url']=sel.xpath('a/@href').extract()
                item['date']=sel.xpath('div/div/div/em[@class="result_info_desc"]/text()').extract()
                item['duration']=sel.xpath('a/p/span/text()').extract()
                item['classify']=sel.xpath('@data-widget-searchlist-catageory').extract()
                #yield item 
               # yield Request(url=str(item['video_url'][0]), meta={'item':item},callback=self.parse_classify)
                #links=sell.xpath('//li[@class="next"]')
          links=response.xpath('//li[@class="next"]')
          for every_url in links:
                        url=str(self.start_urls[0]+every_url.xpath('a/@href').extract()[0])
                        yield Request(url, callback=self.parse)
      def parse_classify(self,response):
          
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
            
           # item=response.meta['item']
           # item['classify']=response.xpath('//*h1[@class="title"]/a/text()')
           # return item
