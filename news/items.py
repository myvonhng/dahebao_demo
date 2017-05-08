# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    xuhao = scrapy.Field()
    banming = scrapy.Field()
    ndate = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
