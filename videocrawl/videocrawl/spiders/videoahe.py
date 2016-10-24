#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
import time
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoahe"
      allowed_domains=[]
      start_urls=[]
      index=1
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
         # self.driver=webdriver.PhantomJS()
      def parse(self,response):
          sell=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
          driver.get(self.start_urls[0])
          while True:
            time.sleep(5)
            for sel in sell.xpath('//div[@class="site-piclist_pic"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('a/@data-title').extract()
                item['desc']=sel.xpath('a/@data-title').extract()
                item['video_url']=sel.xpath('a/@href').extract()
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=sel.xpath('a/div/div/span/text()').extract()
                item['classify']=u'综艺'
                yield item
            try: 
                next_page=driver.find_element_by_xpath('//a[@class="a1"]')
                print next_page
                next_page.click()
            except:
                break
