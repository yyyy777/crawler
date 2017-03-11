# coding=utf-8

import os
import time
import threading
import multiprocessing
from hashlib import md5
from bs4 import BeautifulSoup
from download import download
from crawler_queue import MongoQueue
from config import *

SLEEP_TIME = 1
down = download()


def meizitu_crawler(max_threads=5):
    crawl_queue = MongoQueue(MONGO_DB, MONGO_QUEUE_TABLE)

    def pageurl_crawler():
        while True:
            try:
                print('1')
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print(u'队列中没有数据')
            else:
                print('2')
                img_urls = []
                resp = down.get(url, 3).text
                title = crawl_queue.pop_title(url)
                mkdir(title)
                max_span = BeautifulSoup(resp, 'lxml').find(
                    'div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) + 1):
                    page_url = url + '/' + str(page)
                    img_url = BeautifulSoup(
                        down.get(
                            page_url, 3).text, 'lxml').find(
                        'div', class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
                crawl_queue.complete(url)

    def save(img_url):
        name = md5(str(img_url).encode(encoding='utf-8')).hexdigest()
        print('正在下载：{0}'.format(img_url))
        img = down.get(img_url, 3)
        with open(str(name) + '.jpg', 'ab')as f:
            f.write(img.content)

    def mkdir(path):
        path = path.strip()
        isExixts = os.path.exists(os.path.join(cwd_path, path))
        if not isExixts:
            print(u'新建文件夹：{0}'.format(path))
            os.mkdir(os.path.join(cwd_path, path))
            os.chdir(os.path.join(cwd_path, path))
            return True
        else:
            print(u'文件夹已经存在了:{0}'.format(path))
            os.chdir(os.path.join(cwd_path, path))
            return False

    threads = []
    while threads or crawl_queue:
        print('6')
        for thread in threads:
            print('7')
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            print('5')
            thread = threading.Thread(target=pageurl_crawler())
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print(u'将启动{0}个进程'.format(num_cpus))
    for i in range(num_cpus):
        p = multiprocessing.Process(target=meizitu_crawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    cwd_path = os.getcwd()
    process_crawler()
