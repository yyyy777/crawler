#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pymongo
import os

MONGO_URI = 'localhost'
MONGO_DATABASE = 'AppStoreCrawler'
COLL_NAME = 'GooglePlayApp'

client = pymongo.MongoClient(MONGO_URI)
coll = client[MONGO_DATABASE][COLL_NAME]


file = os.path.join(os.path.dirname(os.getcwd()), 'GooglePlayRank.txt')


def trans():
    with open(file, 'a+', encoding='utf-8') as f:
        for item in coll.find():
            line = item['pkg'] + '\n'
            f.write(line)


if __name__ == '__main__':
    trans()
