#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
import time
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from lxml import etree
class VideoSpider(scrapy.Spider):
      name="videoaright"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          driver=webdriver.PhantomJS()
          driver.get(self.start_urls[0])
          while True:
            movis=driver.page_source
            selector=etree.HTML(movis)
            sel=selector.xpath('//div[@class="site-piclist_pic"]')
            index=0
            while (index<len(sel)):
                item=VideocrawlItem()
                item['title']=sel[index].xpath('a/@title')
                item['desc']=sel[index].xpath('a/@title')
                item['video_url']=sel[index].xpath('a/@href')
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=sel[index].xpath('a/div/div/span/text()')
                item['classify']=u'综艺'
                index=index+1
                yield item
            try:    
                next_page=driver.find_element_by_xpath('//a[@data-key="down"]')
                next_page.click()
                time.sleep(5)
            except:
                break
