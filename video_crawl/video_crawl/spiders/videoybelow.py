#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class VideoSpider(scrapy.Spider):
      name="videoybelow"
      allowed_domains=[]
      index=0
      start_urls=[]
      youku_url=u'http://www.soku.com/search_video/q_剧能扯放胆喷2016?f=1&kb=04114010kv41000__剧&_rp=1469184968791oFNZA7'
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          for sel in sell.xpath('//div[@class="v"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div[@class="v-meta va"]/div/a/@title').extract()
                item['desc']=sel.xpath('div[@class="v-meta va"]/div/a/@title').extract()
                item['video_url']=sel.xpath('div[@class="v-meta va"]/div/a/@href').extract()
                item['date']=sel.xpath('div/div/div/span[@class="r"]/text()').extract()
                item['duration']=sel.xpath('div/div/span[@class="v-time"]/text()').extract()
                item['classify']=u'电视剧'
                yield Request(url=str(item['video_url'][0]), meta={'item':item},callback=self.parse_classify)
          links=response.xpath('//li[@class="next"]')
          for every_url in links:
                url=str(self.youku_url+every_url.xpath('a/@href').extract()[0])
                yield Request(url, callback=self.parse)
      def parse_classify(self,response):
           item=response.meta['item']
           item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
           return  item
            
