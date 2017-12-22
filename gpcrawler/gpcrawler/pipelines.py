# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
file = os.path.join(os.path.dirname(os.getcwd()), 'GooglePlayRank.txt')
import pymongo


class GooglePlayPipeline(object):
    def process_item(self, item, spider):
        if not item:
            return
        with open(file, 'a+', encoding='utf-8') as f:
            pkg = item['pkg']
            for line in f.readlines():
                if pkg in line:
                    return item
            # catagory = item['catagory']
            # down_max = item['down_max']
            # down_min = item['down_min']
            # line = pkg + ' ' + catagory + ' ' + down_max + ' ' + down_min + '\n'
            line = pkg + '\n'
            f.write(line)
            return item


class MongoPipeline(object):
    collection_name = 'GooglePlayApp'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update(
            {'pkg': item['pkg']}, dict(item), True)
        return item
