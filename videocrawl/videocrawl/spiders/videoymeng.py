#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
import time
from scrapy.selector import Selector
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys
class VideoSpider(scrapy.Spider):
      name="videoymeng"
      allowed_domains=[]
     #start_urls=["http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos","http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos","http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos"]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          time.sleep(5)
          sell=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
          driver.get(self.start_urls[0])
          try:
              js="var q=document.documentElement.scrollTop=10000"
              driver.execute_script(js)
              time.sleep(10)
              driver.get_screenshot_as_file("qqqqqqqqqqq1.png")
              print driver.page_source
              movis=driver.page_source
              sell=etree.HTML(movis)
              titles=sell.xpath('//div[@class="yk-col4 yk-pack  p-list mb16"]')
          except:
              print "IIIIIIIIIIIIIIIIIIIIIIIIIII"
          i=0
          
          while (i<len(titles)):
                item=VideocrawlItem()
                item['title']=titles[i].xpath('div/a/@title')
                item['desc']=titles[i].xpath('div/a/@title')
                item['video_url']=titles[i].xpath('div/a/@href')
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=titles[i].xpath('ul/li/span/span/text()')
                item['classify']=u'综艺'
                i=i+1
                yield item
               # yield Request(url=str(item['video_url'][0]),meta={'item':item},callback=self.parse_classify)
      def parse_classify(self,response):
          
          item=response.meta['item']
          item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
          return  item
