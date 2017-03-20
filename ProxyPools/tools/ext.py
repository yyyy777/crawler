# coding=utf-8

import pymongo

from tools.config import MONGO_URL, MONGO_DB

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
