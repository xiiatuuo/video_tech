#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
import time
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoyhistory"
      allowed_domains=[]
     #start_urls=["http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos","http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos","http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos"]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
         # self.driver=webdriver.PhantomJS()
      def parse(self,response):
          sell=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
         #driver.get(self.start_urls[0])
         # driver.get("http://jilupian.youku.com/index/fengyunlishi")
          try:
              driver.get('http://jilupian.youku.com/index/fengyunlishi')
          except:
                  print "**************************************************"
         #while True:
          for sel in sell.xpath('//div[@class="v"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div/a/@title').extract()
                item['desc']=sel.xpath('div/a/@title').extract()
                item['video_url']=sel.xpath('div/a/@href').extract()
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=sel.xpath('div/div/span[@class="v-time"]/text()').extract()
                item['classify']=u'军事'
                #yield item 
                yield item 
         # next_page=driver.find_element_by_xpath('//span[@class="next"]/a')
         # next_page.click()
         # time.sleep(5)
      
