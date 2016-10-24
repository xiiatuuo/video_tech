#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videotenxunr"
      allowed_domains=[]
      index=0
      start_urls=[]
      tengxun_url=" http://v.qq.com"
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//li[@class="list_item"]'):
                print (len(sell.xpath('//li[@class="list_item"]')))
                item=VideocrawlItem()
                item['title']=sel.xpath('@data-title').extract()
                item['desc']=sel.xpath('@data-title').extract()
                if not sel.xpath('a[@class="figure"]/@href').extract():
                         item['video_url']=self.tengxun_url+sel.xpath('a[@class="figure"]/@href').extract()[0]
                item['date']="null"
                item['duration']=sel.xpath('a/div/div/span[@class="figure_info"]/text()').extract()
                item['classify']=u'母婴育儿'
                yield item 
