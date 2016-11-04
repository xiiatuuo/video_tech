#-*- coding: UTF-8 -*-  
import scrapy
from videocrawl.items import VideocrawlItem
import time
import urllib2  
from date_formate import date_cal
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from lxml import etree
from title_dr import is_similar
from selenium.webdriver.common.keys import Keys 
from  selenium.webdriver.support.ui import WebDriverWait
class Video_youku_Spider(scrapy.Spider):
      name="video_youku_search"
      keys=""
      allowed_domains=[]
      start_urls=["http://www.soku.com/search_video/q_qww?f=1&kb=040200000000000__qww&"]
      def __init__(self, *args, **kwargs):
          super(Video_youku_Spider,self).__init__(*args, **kwargs)
          self.keys=[kwargs.get('keys')]
      def parse(self,response):
          temp=Selector(response)
          try:          
             driver=webdriver.PhantomJS()
          except:
             print "driver error"
          driver.maximize_window()
          driver.get("http://www.soku.com/search_video/q_qww?f=1&kb=040200000000000__qww&")
          time.sleep(2)
          driver.find_element_by_id("headq").clear()
          driver.find_element_by_xpath('//input[@id="headq"]').send_keys(self.keys)
          driver.find_element_by_xpath('//button[@class="btn btn_search"]').click()
          time.sleep(3)
          while True:
                target = driver.find_element_by_xpath('//div[@class="about"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="sk_wrap"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="about"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                movis=driver.page_source
                selector=etree.HTML(movis)
                sel=selector.xpath('//div[@class="v"]')
                index=0                
                while(index<len(sel)):
                    item=VideocrawlItem()
                    item['title']=sel[index].xpath('.//div[@class="v-link"]/a/@title')
                    if not len(item['title']):
                        index=index+1
                        continue
                    if is_similar(item['title'][0]):
                        index=index+1
                        continue
                    item['desc']=sel[index].xpath('.//div[@class="v-link"]/a/@title')
                    item['video_url']=sel[index].xpath('div[@class="v-link"]/a/@href')
                    item['date']=sel[index].xpath('.//span[@class="r"]/text()')
                    item['date'][0]=date_cal(item['date'][0])
                    item['duration']=sel[index].xpath('div/div/span[@class="v-time"]/text()')
                    item['classify']='null'
                    if not len(item['video_url']):
                        index=index+1
                        continue
                    url=str(item['video_url'][0])
                    item['classify']=self.classify(url)
                    index=index+1
                    yield item
                try:
                    next_page=driver.find_element_by_xpath('//li[@class="next"]/a')
                    next_page.click()
                    time.sleep(3)
                except:
                    print "nexr page is over"
                    break
     #抓取视频类别
      def classify(self,url):
           data = urllib2.urlopen(url)
           code=data.read() 
           selector=etree.HTML(code) 
            
           return  selector.xpath('//h1[@class="title"]/a/text()')

