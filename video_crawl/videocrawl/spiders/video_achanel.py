#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取爱奇艺频道栏目 如http://www.iqiyi.com/u/416391545/v
'''
import scrapy
from videocrawl.items import VideocrawlItem
import time
from date_formate import date_cal
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
class Video_achanel_Spider(scrapy.Spider):
      name="videoahe"
      allowed_domains=[]
      start_urls=[]
      index=1
      def __init__(self, *args, **kwargs):
          super(Video_achanel_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sel_res=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
          driver.get(self.start_urls[0])
          while True:
            time.sleep(5)
            for sel in sel_res.xpath('//li[@j-delegate="colitem"]'):
                item=VideocrawlItem()
                item['title']=sel.xpath('div[1]/a/@data-title').extract()
                item['desc']=sel.xpath('div[1]/a/@data-title').extract()
                item['video_url']=sel.xpath('div[1]/a/@href').extract()
                if not item['video_url']:
                     continue
                item['date']=sel.xpath('div[2]/p[2]/span[2]/text()').extract()
                item['date'][0]=date_cal(item['date'][0])
                item['duration']=sel.xpath('div[1]/a/div/div/span/text()').extract()
                item['classify']=u'综艺'
                yield item
            try: 
                next_page=driver.find_element_by_xpath('//a[@class="a1"]')
                next_page.click()
            except:
                print "next page is over"
                break
