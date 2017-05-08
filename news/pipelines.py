# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import os
import news.spiders.dahebao
from scrapy import signals
import pymysql
import news.spiders.dahebao as nsd
import re


def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='fqy123456',
        charset='utf8',
        use_unicode=False
    )
    return conn

class NewsPipeline(object):
        #self.conn = pymysql.connect(host= "127.0.0.1",port= 3306,user ="root",password ="fqy123456",db = "test",charset ="utf8",cursorclass=pymysql.cursors.DictCursor)

    def __init__(self):
        self.fl = 'tb_'+ nsd.ndate.replace('-','_').replace('/','_')
        creat_table = "CREATE TABLE IF NOT EXISTS {} (" \
                      "id INT(4) NOT NULL AUTO_INCREMENT," \
                      "xuhao CHAR(8) NOT NULL DEFAULT '序号'," \
                      "banming CHAR(8) NOT NULL DEFAULT '版名'," \
                      "ndate CHAR(10) NOT NULL DEFAULT '发行日期'," \
                      "title VARCHAR(45) NOT NULL DEFAULT '新闻标题'," \
                      "body TEXT NOT NULL,PRIMARY KEY (id))".format(self.fl)       #mysql语句中插入变量的实现
        self.conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='fqy123456',
        db = 'test',
        charset='utf8',
        use_unicode=False
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(creat_table)
        self.conn.commit()
    def process_item(self, item, spider):

        sql = 'insert into {}(xuhao,banming,ndate,title,body) values (%s,%s,%s,%s,%s)'.format(self.fl)
        try:
            self.cursor.execute(sql,(item['xuhao'],item['banming'],item['ndate'],item['title'],item['body']))
            self.conn.commit()
            return item
        except Exception as err:
            print(err)
            self.conn.rollback()
    def close_spider(self):
        self.conn.close()


# CREATE TABLE `test`.`news1` (
#   `id` INT(4) NOT NULL AUTO_INCREMENT,
#   `xuaho` CHAR(6) NOT NULL DEFAULT '序号',
#   `banming` CHAR(8) NOT NULL DEFAULT '版名',
#   `ndate` CHAR(10) NOT NULL DEFAULT '发行日期',
#   `title` VARCHAR(45) NOT NULL DEFAULT '新闻标题',
#   `body` TEXT NOT NULL,
#   PRIMARY KEY (`id`))



