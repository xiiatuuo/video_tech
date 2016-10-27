#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
import time
from lxml import etree
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
class VideoSpider(scrapy.Spider):
      name="videoabelow"
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
          driver.get(self.start_urls[0])
          sell=Selector(response)
          time.sleep(3)
          index=0
          while True:
             movis=driver.page_source
             sell=etree.HTML(movis)
             titles=sell.xpath('//div[@class="site-piclist_pic"]')
             i=0
             while(i<len(titles)):
                for i in range(1,10):
                   index=0
                   item=VideocrawlItem()
                   index=index+1
                   if index>10:
                     break
                   item['title']=titles[i].xpath('a/img/@alt')
                   item['desc']=titles[i].xpath('a/img/@alt')
                   item['video_url']=titles[i].xpath('a/@href')
                   item['date']=titles[i].xpath('a/div/div/span/text()')
                   item['duration']="null"
                   item['classify']=u'综艺'
                #yield item 
                   yield item
                break   
             try:
                next_page=driver.find_element_by_xpath('//*[@id="album_pic_paging"]/a[@data-key="down"]') 
                next_page.click()
                time.sleep(3)
                driver.get_screenshot_as_file("3.png")
             except:
                break
