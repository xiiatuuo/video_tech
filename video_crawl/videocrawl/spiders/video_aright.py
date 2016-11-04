#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取爱奇艺列表式布局，例如：http://www.iqiyi.com/playlist300755002.html#vfrm=2-3-0-1
'''
import scrapy
from videocrawl.items import VideocrawlItem
import time
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from lxml import etree
class Video_aright_Spider(scrapy.Spider):
      name="videoaright"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(Video_aright_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          driver=webdriver.PhantomJS()
          driver.get(self.start_urls[0])
          while True:
            page_html=driver.page_source
            selector=etree.HTML(page_html)
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
                print "next_page is over"
                break
