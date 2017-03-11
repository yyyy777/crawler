# coding=utf-8

from bs4 import BeautifulSoup
from download import download
from crawler_queue import MongoQueue
from config import *

spider_queue = MongoQueue(MONGO_DB, MONGO_QUEUE_TABLE)
down = download()

def start(url):
    resp = down.get(url, 3)
    soup = BeautifulSoup(resp.text, 'lxml')
    all_a = soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        print('写入URL:{0}到队列中'.format(url))
        spider_queue.push(url, title)
    print('URL已经全部写入队列')

if __name__ == '__main__':
    start('http://www.mzitu.com/all')
