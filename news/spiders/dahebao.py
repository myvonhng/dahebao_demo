# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
#from scrapy.contrib.spiders import CrawlSpider,Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import re
#import string
from news.items import NewsItem
global ndate
ndate = "2016-02/06"
class DahebaoSpider(scrapy.Spider):
    name = "dahebao"
    global ndate
    #date = "2016-02/17"
    #allowed_domains = ["dahebao.com"]
    start_urls = ['http://newpaper.dahe.cn/dhb/html/' + ndate + '/node_897.htm',
                  'http://newpaper.dahe.cn/dhb/html/' + ndate + '/node_66.htm']

    def parse(self, response):
        global ndate
        for link in response.xpath("//tbody/tr/td[@class='black']/a[@class='black']/@href").extract():
            try:
                next_link = 'http://newpaper.dahe.cn/dhb/html/'+ ndate +'/'+ link
                yield scrapy.Request(next_link,callback=self.parse_ban)
            except:
                continue
    def parse_ban(self,response):
        global ndate
        test_repet=''
        for href in response.xpath("//map/area/@href").extract():
            if test_repet.split('.')[0] == href.split('.')[0]:          #存在相同content_xxx。指向同一个网页内容，故排除
                continue
            else:
                try:
                    url ='http://newpaper.dahe.cn/dhb/html/'+ ndate+ '/' + href
                    yield scrapy.Request(url,callback=self.parse_news)
                except:
                     continue
            test_repet = href
 #response.xpath("//tbody/tr/td[@class='black']/a[@class='black']/@href").extract()
    def parse_news(self,response):
        global date
        for_body = []
        log.msg("当前爬取的是 %s" % response.url)
        item = NewsItem()
        item['xuhao'] = response.xpath('//td[@width="160"]/text()').extract()[0] #序号
        item['banming'] = response.xpath('//td[@width="160"]/strong/text()').extract()[0] #版名
        item['ndate']= ndate #日期
        if response.xpath("/html/head/title/text()").extract()==[]:
            item['title'] = "无"   #存在标题为空的情况
        if  response.xpath("/html/head/title/text()").extract():
            item['title'] = response.xpath("/html/head/title/text()").extract()[0]  #标题
        #item['editor'] = response.xpath("//*[@id='ozoom']/p/text()").extract()[0] #记者
        for_body = ''.join(response.xpath("//*[@id='ozoom']/p/text()").extract()) # 列表格式的新闻内容
        item['body'] = for_body.replace('\xa0\xa0\xa0\xa0','')

        return item
