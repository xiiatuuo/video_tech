#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取优酷个人主页视频，如http://list.youku.com/albumlist/show?id=3076330&ascending=1&page=1
'''
import scrapy
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
import time
from scrapy.selector import Selector
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys
class Video_yperson_Spider(scrapy.Spider):
      name="videoymeng"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(Video_yperson_Spider,self).__init__(*args, **kwargs)
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
              movis=driver.page_source
              sell=etree.HTML(movis)
              titles=sell.xpath('//div[@class="yk-col4 yk-pack  p-list mb16"]')
          except:
              print "scoll errot"
          index=0
          while (index<len(titles)):
                item=VideocrawlItem()
                item['title']=titles[index].xpath('div/a/@title')
                item['desc']=titles[index].xpath('div/a/@title')
                item['video_url']=titles[index].xpath('div/a/@href')
                if not item['video_url']:
                     continue
                item['date']="null"
                item['duration']=titles[index].xpath('ul/li/span/span/text()')
                item['classify']=u'综艺'
                index=index+1
                yield item
      #识别视频类别
      def parse_classify(self,response):
          
          item=response.meta['item']
          item['classify']=response.xpath('//h1[@class="title"]/a/text()').extract()
          return  item
