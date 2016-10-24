#-*- coding: UTF-8 -*-  
import scrapy
import time
from videocrawl.items import VideocrawlItem
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from lxml import etree
from  selenium.webdriver.support.ui import WebDriverWait
class VideoSpider(scrapy.Spider):
      name="videosohu"
      allowed_domains=[]
      index=0
     #start_urls=["http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos","http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos","http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos"]
      start_urls=[]
      sohu_url=u'http://my.tv.sohu.com/user/media/video.do'
      def __init__(self, *args, **kwargs):
          super(VideoSpider,self).__init__(*args, **kwargs)
          self.start_urls=[kwargs.get('start_url')]
      def parse(self,response):
          driver=webdriver.PhantomJS()
          driver.get(self.start_urls[0])
          #item=VideocrawlItem()
          while True:
            js="var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            time.sleep(3)
            element = WebDriverWait(driver, 20).until(lambda x :x.find_element_by_xpath('//p[@class="mB5 lh14"]'))
            movis=driver.page_source
            sell=etree.HTML(movis)
            titles=sell.xpath('//p[@class="mB5 lh14"]')
            i=0
      
            while (i<len(titles)):
                item=VideocrawlItem()
                item['title']=titles[i].xpath('a/text()')
                item['desc']=titles[i].xpath('a/text()')
                item['video_url']=titles[i].xpath('a/@href')
                item['date']="null"#sel.xpath('p/a/span[@class="dr_itime"]/text()').extract()
                item['duration']="null"
                item['classify']=u'数码'
                i=i+1
                yield item 
            try:
              next_page=driver.find_element_by_xpath('//a[@class="a btnR"]')
              next_page.click()
              time.sleep(3)
            except:
                break

