#-*- coding: UTF-8 -*-  
'''
@author:duqianjin
@brief:抓取搜狐自媒体页面 ，如http://my.tv.sohu.com/user/media/video.do?uid=232799889&page=1&sortType=2
'''
import scrapy
import time
from date_formate import date_cal
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from lxml import etree
from  selenium.webdriver.support.ui import WebDriverWait
class Video_sohu_Spider(scrapy.Spider):
      name="videosohu"
      allowed_domains=[]
      start_urls=[]
      sohu_url=u'http://my.tv.sohu.com/user/media/video.do'
      def __init__(self, *args, **kwargs):
          super(Video_sohu_Spider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          driver=webdriver.PhantomJS()
          driver.get(self.start_urls[0])
          while True:
             #将滚轮滑到最下端
            js="var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            time.sleep(3)
            element = WebDriverWait(driver, 20).until(lambda x :x.find_element_by_xpath('//p[@class="mB5 lh14"]'))
            page_html=driver.page_source
            sell=etree.HTML(page_html)
            #TODO
            titles=sell.xpath('//li[@class="l pl27 pb15 dr_li"]')
            i=0
            while (i<len(titles)):
                item=VideocrawlItem()
                item['title']=titles[i].xpath('p[1]/a/text()')
                item['desc']=titles[i].xpath('p[1]/a/text()')
                item['video_url']=titles[i].xpath('p[1]/a/@href')
                item['date']=titles[i].xpath('p[2]/a[2]/span/text()')
                item['date'][0]=date_cal(item['date'][0])
                item['duration']="null"
                item['classify']=u'数码'
                i=i+1
                yield item 
            try:
                next_page=driver.find_element_by_xpath('//a[@class="a btnR"]')
                next_page.click()
                time.sleep(3)
            except:
                print "next_page is over"
                break

