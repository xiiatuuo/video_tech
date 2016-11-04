#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取b站搜索结果
'''
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
class Video_bilin_Spider(scrapy.Spider):
      name="video_bili_search"
      keys=""
      allowed_domains=[]
      start_urls=["http://search.bilibili.com/all?keyword=TFBOYS"]
      def __init__(self, *args, **kwargs):
          super(Video_bilin_Spider,self).__init__(*args, **kwargs)
          self.keys=[kwargs.get('keys')]
      def parse(self,response):
          temp=Selector(response)
          try:          
             driver=webdriver.PhantomJS()
          except:
             print "driver error"
          driver.maximize_window()
          driver.get("http://search.bilibili.com/all?keyword=TFBOYS")
          time.sleep(2)
          driver.find_element_by_id("search-keyword").clear()
          driver.find_element_by_xpath('//input[@id="search-keyword"]').send_keys(self.keys)
          driver.find_element_by_xpath('//div[@id="search-button"]').click()
          time.sleep(3)
          index=0
          page=1
          while True:
                #滑动到页面下方
                target = driver.find_element_by_xpath('//a[@id="weixin"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                #滑动到页面上方
                target = driver.find_element_by_xpath('//div[@id="header-search"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                #滑动到页面下方
                target = driver.find_element_by_xpath('//a[@id="weixin"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                page_html=driver.page_source
                selector=etree.HTML(page_html)
                sel=selector.xpath('//li[@class="video matrix "]')
                index=0                
                while(index<len(sel)):
                    item=VideocrawlItem()
                    item['title']=sel[index].xpath('a/@title')
                    if not len(item['title'][0]):
                        index=index+1
                        continue
                    if is_similar(item['title'][0]):
                        index=index+1
                        continue
                    item['desc']=sel[index].xpath('a/@title')
                    item['video_url']=sel[index].xpath('a/@href')
                    item['date']=sel[index].xpath('.//span[@class="so-icon time"]/text()')[1].replace(' ', '').replace('\n','').replace('\t','')
                    item['date']=date_cal(item['date'])
                    item['duration']=sel[index].xpath('a/div/span/text()')
                    item['duration']=item['duration'][0].replace(' ', '').replace('\n','').replace('\t','')
                    item['classify']='null'
                    if not len(item['video_url']):
                        index=index+1
                        continue
                    url=str(item['video_url'][0])
                    item['classify']=self.classify(url)
                    index=index+1
                    yield item
                try:
                    next_page=driver.find_element_by_xpath('//a[@class="nextPage"]')
                    next_page.click()
                    time.sleep(3)
                except:
                    print "nexr page is over"
                    break
     #识别视频分类           
      def classify(self,url):
           page_html = urllib2.urlopen(url)
           code=page_html.read() 
           selector=etree.HTML(code)             
           return  selector.xpath('//a[@class="on"]/text()')

