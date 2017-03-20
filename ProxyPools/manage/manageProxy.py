# coding=utf-8
import requests
from multiprocessing import Process
from apscheduler.schedulers.blocking import BlockingScheduler

from crawlProxy.crawlProxy import getProxy
from tools.config import MONGO_TABLE_ALL, MONGO_TABLE_VERIFY
from tools.ext import db
from tools.tools import verifyProxy


class Proxymanager(object):

    def __init__(self):
        '''
        alldb:获取的全部代理的数据库
        verifydb：经过验证后可用的数据库
        '''
        self.alldb = db[MONGO_TABLE_ALL]
        self.verifydb = db[MONGO_TABLE_VERIFY]

    def refesh(self):
        '''
        删除旧数据困并重新获取代理后加入数据库
        :return:
        '''
        self.alldb.drop()
        self.verifydb.drop()

        proxies = getProxy()

        for proxy in proxies.getProxySecond():
            if verifyProxy(str(proxy)):
                proxy_dict = {'proxy': str(proxy)}
                self.alldb.insert(proxy_dict)

        for proxy in proxies.getProxyThird():
            if verifyProxy(str(proxy)):
                proxy_dict = {'proxy': str(proxy)}
                self.alldb.insert(proxy_dict)

        for proxy in proxies.getProxyForth():
            if verifyProxy(str(proxy)):
                proxy_dict = {'proxy': str(proxy)}
                self.alldb.insert(proxy_dict)

        for proxy in proxies.getProxyFifth():
            if verifyProxy(str(proxy)):
                proxy_dict = {'proxy': str(proxy)}
                self.alldb.insert(proxy_dict)

    def getAllProxy(self):
        '''
        获得全部爬取的代理
        :return:
        '''
        for proxy in self.alldb.find():
            yield proxy

    def getVerifyProxy(self):
        '''
        获得一个可用的代理
        :return:
        '''
        return self.alldb.find_one()['proxy']

    def getAllVerifyProxy(self):
        '''
        获得全部可用的代理
        :return:
        '''
        for proxy in self.verifydb.find():
            yield proxy['proxy']

    def valid_proxy(self):
        '''
        验证代理，如果可用则放入verifydb
        :return:
        '''
        print('start valid proxy!')
        for p in self.getAllProxy():
            proxy = {}
            proxy['proxy'] = p['proxy']
            proxies = {"http": "http://{proxy}".format(proxy=proxy['proxy']),
                       "https": "https://{proxy}".format(proxy=proxy['proxy'])}

            try:
                response = requests.get(
                    'https://www.baidu.com',
                    proxies=proxies,
                    timeout=30,
                    verify=False)
                if response.status_code == 200:
                    self.verifydb.insert(proxy)
                    print('Proxy:%s is useful!' % proxy['proxy'])
            except Exception as e:
                print("Error: %s" % e)
                print('Proxy: %s validation fail' % proxy['proxy'])
        print('valid proxy complete!')

    def delete_proxy(self, delproxy):
        self.verifydb.remove({'proxy': delproxy})


def refresh_pool():
    schedules = Proxymanager()
    schedules.valid_proxy()


def main(process_num=10):
    manager = Proxymanager()
    manager.refesh()
    pool = []
    for num in range(process_num):
        proc = Process(target=refresh_pool, args=())
        pool.append(proc)

    for num in range(process_num):
        pool[num].start()

    for num in range(process_num):
        pool[num].join()

if __name__ == '__main__':
    main()
    schedule = BlockingScheduler()
    schedule.add_job(main, 'interval', minutes=10)
    schedule.start()
