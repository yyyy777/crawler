# # coding=utf-8
# !usr/bin/python3

import re
from tools.tools import crawlProxy, getHtmlTree


class getProxy(object):

    def __init__(self):
        pass

    @staticmethod
    @crawlProxy
    def getProxyFirst(page=10):
        '''
        抓取:快代理IP http://www.kuaidaili.com/
        :param page:
        :return:
        '''
        url_list = (
            'http://www.kuaidaili.com/proxylist/{page}/'.format(
                page=page) for page in range(
                1, page + 1))
        for url in url_list:
            tree = getHtmlTree(url=url)
            #proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            proxy_list = tree.xpath(
                '//*[@id="index_free_list"]/table/tbody/tr')
            print('1')
            for proxy in proxy_list:
                print('2')
                # print(proxy)
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @crawlProxy
    def getProxySecond(proxy_num=100):
        '''
        抓取:66代理 http://www.66ip.cn/,66代理提供API，可以直接提取,
        :param proxy_num:
        :return:
        '''
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_num)
        html = getHtmlTree(url, xpath=False)
        proxy_list = re.findall(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', str(html))
        for proxy in proxy_list:
            yield proxy

    @staticmethod
    @crawlProxy
    def getProxyThird(days=1):
        '''
        抓取:有代理 http://www.youdaili.net/Daili/http/
        :param days:
        :return:
        '''
        url = "http://www.youdaili.net/Daili/http/"
        tree = getHtmlTree(url)
        page_url_list = tree.xpath(
            './/div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
        for page_url in page_url_list:
            html = getHtmlTree(page_url, xpath=False)
            proxy_list = re.findall(
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', str(html))
            for proxy in proxy_list:
                yield proxy

    @staticmethod
    @crawlProxy
    def getProxyForth():
        '''
        抓取:西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        '''

        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            tree = getHtmlTree(each_url)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @crawlProxy
    def getProxyFifth():
        '''
        抓取:guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        '''

        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            for each_proxy in proxy_list:
                yield ''.join(each_proxy.xpath('.//text()'))

'''
if __name__ == '__main__':
    gg = getProxy()

    for n in gg.getProxyFifth():
        print(n)
'''