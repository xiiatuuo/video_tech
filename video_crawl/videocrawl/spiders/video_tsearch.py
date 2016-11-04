#-*- coding: UTF-8 -*- 
'''
@author:duqianjin
@brief:抓取腾讯视频搜索结果
'''
import scrapy
from videocrawl.items import VideocrawlItem
import time
import urllib2  
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from lxml import etree
from date_formate import date_cal
from title_dr import is_similar
from selenium.webdriver.common.keys import Keys 
from  selenium.webdriver.support.ui import WebDriverWait
class Video_youku_Spider(scrapy.Spider):
      name="video_tenxun_search"
      keys=""
      allowed_domains=[]
      start_urls=["http://v.qq.com/x/search/?q=redis&stag=102&smartbox_ab="]
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
          driver.get("http://v.qq.com/x/search/?q=redis&stag=102&smartbox_ab=")
          time.sleep(2)
          driver.find_element_by_id("keywords").clear()
          driver.find_element_by_xpath('//input[@id="keywords"]').send_keys(self.keys)
          driver.find_element_by_xpath('//button[@class="search_btn"]').click()
          time.sleep(3)
          index=0
          page=1
          while True:
                #js="var q=document.documentElement.scrollTop=10000"
                #driver.execute_script(js)
                target = driver.find_element_by_xpath('//div[@class="footermenu"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="site_logo"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="footermenu"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                #WebDriverWait(driver, 20).until(lambda x:x.find_element_by_xpath('//div[@log_prevsend="true"]'))
                time.sleep(3)
                movis=driver.page_source
                selector=etree.HTML(movis)
                sel=selector.xpath('//div[@class="result_item result_item_h"]') 
                index=0                
                while(index<len(sel)):
                    item=VideocrawlItem()
                    item['title']=sel[index].xpath('h2/a/text()')
                    if not len(item['title']):
                        index=index+1
                        continue
                    if len(item['title'])>1:
                        item['title'][0]=item['title'][0]+str(self.keys)+item['title'][1]
                        item['title']=item['title'][:1]
                    if is_similar(item['title'][0]):
                        index=index+1
                        continue
                    item['desc']=sel[index].xpath('h2/a/text()')
                    item['video_url']=sel[index].xpath('a/@href')
                    item['date']=sel[index].xpath('div/div/div/span[@class="content"]/text()')
                    item['date']=date_cal(item['date'][0])
                    item['duration']=sel[index].xpath('a/span/span/text()')
                    item['duration'][0]=item['duration'][0][2:]
                    item['classify']='null'
                    if not len(item['video_url']):
                        index=index+1
                        continue
                    url=str(item['video_url'][0])
                    #item['classify']=self.classify(url)
                    index=index+1
                    yield item
                try:
                    next_page=driver.find_element_by_xpath('//a[@class="page_next"]')
                    next_page.click()
                    time.sleep(3)
                except:
                    print "nexr page is over"
                    break
      def classify(self,url):
           # web_second=webdriver.PhantomJS()
           # web_second.get(url)
           # code=web_second.page_source
           data = urllib2.urlopen(url)
           code=data.read() 
           selector=etree.HTML(code) 
           return  selector.xpath('//a[@class="link_nav"]/text()')

