#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取腾讯右侧列表，如http://v.qq.com/x/cover/8d2dzz0lke8sxo0/b0014x4fdwe.html
'''
import scrapy
from lxml import etree
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from selenium import webdriver
from  selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector
class Video_tenxunr_Spider(scrapy.Spider):
      name="videotenxunr"
      allowed_domains=[]
      index=0
      start_urls=[]
      tengxun_url="http://v.qq.com"
      def __init__(self, *args, **kwargs):
          super(Video_tenxunr_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          driver=webdriver.PhantomJS()
          driver.get(self.start_urls[0])
          element = WebDriverWait(driver, 20).until(lambda x :x.find_element_by_xpath('//li[@class="list_item"]'))
          page_html=driver.page_source
          sell =etree.HTML(page_html)
          titles=sell.xpath('//li[@class="list_item"]')
          i=0
          while (i<len(titles)):
                item=VideocrawlItem()
                item['title']=titles[i].xpath('@data-title')
                if not item['title']:
                    break
                item['desc']=titles[i].xpath('@data-title')
                item['video_url']=titles[i].xpath('a/@href')
                item['video_url'][0]=self.tengxun_url+str(item['video_url'][0])
                item['date']="null"
                item['duration']=titles[i].xpath('a/div/div/span[@class="figure_info"]/text()')
                item['classify']=u'母婴育儿'
                i=i+1
                yield item 
