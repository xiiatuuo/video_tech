#-*- coding: UTF-8 -*- 
'''
@author:duqianjin
@brief:抓取爱奇艺综艺节目，如http://www.iqiyi.com/a_19rrgi9w1l.html#vfrm=2-3-0-1
'''
from date_formate import date_cal
import scrapy
from videocrawl.items import VideocrawlItem
import time
from lxml import etree
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
class Video_abelow_Spider(scrapy.Spider):
      name="videoabelow"
      allowed_domains=[]
      start_urls=[]
      def __init__(self, *args, **kwargs):
          super(Video_abelow_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          sell=Selector(response)
          driver=webdriver.PhantomJS()
          driver.maximize_window()
          driver.get(self.start_urls[0])
          sell=Selector(response)
          time.sleep(3)
          while True:
             movis=driver.page_source
             sell=etree.HTML(movis)
             titles=sell.xpath('//div[@class="site-piclist_pic"]')
             i=0
             for i in range(10):
                   item=VideocrawlItem()
                   item['title']=titles[i].xpath('a/img/@alt')
                   item['desc']=titles[i].xpath('a/img/@alt')
                   item['video_url']=titles[i].xpath('a/@href')
                   item['date']=titles[i].xpath('a/div/div/span/text()')
                   item['date'][0]=date_cal(item['date'][0])
                   item['duration']="null"
                   item['classify']=u'综艺'
                   yield item
             try:
                next_page=driver.find_element_by_xpath('//*[@id="album_pic_paging"]/a[@data-key="down"]') 
                next_page.click()
                time.sleep(3)
             except:
                print "next_page is over"
                break
