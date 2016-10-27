#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="video"
      allowed_domains=[]
      start_urls=["http://i.youku.com/i/UMTI4MzI5MjExMg==/videos"]
      def parse(self,response):
            selector=Selector(response)
            links=selector.xpath('//li[@class="next"]')
            for every_url in links:
                url_front=response.url
                urls=str(self.start_urls[0]+every_url.xpath('a/@href').extract()[0])
                yield Request(urls,callback=self.parse_videoinfo)
      def parse_videoinfo(self,response):
          sell=Selector(response)
          item=VideocrawlItem()
          for sel in sell.xpath('//div[@class="v va"]'):
                item['title']=sel.xpath('div[@class="v-meta"]/div/a/text()').extract()
                item['desc']=sel.xpath('div[@class="v-meta"]/div/a/text()').extract()
                item['video_url']=sel.xpath('div[@class="v-meta"]/div/a/@href').extract()
                item['date']=sel.xpath('div/div/span[@class="v-publishtime"]/text()').extract()
                item['duration']=sel.xpath('div/div/span[@class="v-time"]/text()').extract()
                item['classify']="01"
                yield item
