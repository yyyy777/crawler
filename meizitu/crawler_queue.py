# coding=utf-8

from datetime import datetime, timedelta
from pymongo import MongoClient, errors
from config import MONGO_URL


class MongoQueue(object):

    OUTSTANDING = 1
    PROCESSING = 2
    COMPLETE = 3

    def __init__(self, db, collection, timeout=300):
        self.MongoClient = MongoClient(MONGO_URL, connect=False)
        self.client = self.MongoClient[db]
        self.db = self.client[collection]
        self.timeout = timeout

    def __bool__(self):
        record = self.db.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url, title):
        try:
            self.db.insert({'_id': url, 'status': self.COMPLETE, '主题': title})
            print(u'插入队列成功')
        except errors.DuplicateKeyError as e:
            print('插入队列错误:{0}, {1}可能已经存在于队列之中'.format(e, title))
            pass

    def push_imgurl(self, title, url):
        try:
            self.db.insert(
                {'_id': title, 'status': self.OUTSTANDING, 'url': url})
            print(u'插入图片地址成功')
        except errors.DuplicateKeyError as e:
            print('插入队列错误:{0}, {1}可能已经存在于队列之中'.format(e, url))
            pass

    def pop(self):
        record = self.db.find_and_modify(
            query={
                'status': self.OUTSTANDING}, update={
                '$set': {
                    'status': self.PROCESSING, 'timestamp': datetime.now()}})
        if record:
            return recoed['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one({'_id': url})
        return record['主题']

    def peek(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.update({'_id: url'}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        record = self.db.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print(u'重置URL:{0}的状态'.format(record['_id']))

    def clear(self):
        self.db.drop()
