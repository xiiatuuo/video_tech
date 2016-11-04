#-*- coding: UTF-8 -*- 
'''
@author:duqianjin
@brief:抓取爱奇艺搜索结果

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
class Video_asearch_Spider(scrapy.Spider):
      name="video_aqiyi_search"
      keys=""
      allowed_domains=[]
      start_urls=["http://so.iqiyi.com/so/q_tfboys?source=hot&sr=498742638455"]
      def __init__(self, *args, **kwargs):
          super(Video_asearch_Spider,self).__init__(*args, **kwargs)
          self.keys=[kwargs.get('keys')]
      def parse(self,response):
          temp=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
          driver.get(self.start_urls[0])
          time.sleep(2)
          driver.find_element_by_id("data-widget-searchword").clear()
          driver.find_element_by_xpath('//input[@id="data-widget-searchword"]').send_keys(self.keys)
          driver.find_element_by_xpath('//input[@class="search_btn"]').click()
          time.sleep(3)
          while True:
                target = driver.find_element_by_xpath('//div[@class="qy_footer"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="logo_wrap"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(3)
                target = driver.find_element_by_xpath('//div[@class="qy_footer"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                movis=driver.page_source
                selector=etree.HTML(movis)
                sel=selector.xpath('//li[@class="list_item"]')
                index=0                
                while(index<len(sel)):
                    item=VideocrawlItem()
                    item['title']=sel[index].xpath('div/h3/a/@title')
                    if  not len(item['title']):
                        index=index+1
                        continue
                    if is_similar(item['title'][0]):
                        index=index+1
                        continue
                    item['desc']=sel[index].xpath('div/h3/a/@title')
                    item['video_url']=sel[index].xpath('a/@href')
                    item['date']=sel[index].xpath('div/div/div/em[@class="result_info_desc"]/text()')
                    if not  item['date']:
                        index=index+1
                        continue
                    item['date'][0]=date_cal(item['date'][0])
                    item['duration']=sel[index].xpath('a/p/span/text()')
                    item['classify']='null'
                    url=str(item['video_url'][0])
                    item['classify']=self.classify(url)
                    index=index+1
                    yield item
                try:
                    next_page=driver.find_element_by_xpath('//a[@data-key="down"]')
                    next_page.click()
                    time.sleep(3)
                except:
                    print "next_page is over"
                    break
      def classify(self,url):
           page_html= urllib2.urlopen(url)
           code=page_html.read() 
           selector=etree.HTML(code)    
           return  selector.xpath('//*[@id="widget-videonav thirdPartyTagList"]/a[2]/text()')

