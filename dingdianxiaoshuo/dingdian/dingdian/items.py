# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 小说名字
    name = scrapy.Field()
    # 小说作者
    author = scrapy.Field()
    # 小说地址
    novelurl = scrapy.Field()
    # 小说连载状态
    serialstatus = scrapy.Field()
    # 小说连载字数
    serialnumber = scrapy.Field()
    # 小说类别
    category = scrapy.Field()
    # 小说编号
    novel_id = scrapy.Field()



class ContentItem(scrapy.Item):

    # 小说编号
    novel_cont_id = scrapy.Field()
    # 小说内容
    chaptercontent = scrapy.Field()
    # 用于绑定章节顺序，防止错乱
    num = scrapy.Field()
    # 章节的地址
    chapterurl = scrapy.Field()
    # 章节的名字
    chaptername = scrapy.Field()