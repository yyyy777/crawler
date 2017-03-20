# coding=utf-8
# !usr/bin/python3

import requests
import re
import functools
from lxml import etree as ET
from .useragent import header


def crawlProxy(func):
    '''
    抓取代理的装饰器，方便输出错误信息
    :param func:
    :return:
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('抓取代理ip失败:%s', e)
    return wrapper


def verifyProxy(proxy):
    '''
    检查代理ip的格式是否正确
    :param proxy:
    :return:
    '''
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    return True if re.findall(verify_regex, proxy) else False


def getHtmlTree(url, xpath=True, **kwargs):
    '''
    获取免费代理ip页面的html树用于解析
    :param url:
    :param kwargs:
    :return:
    '''
    if xpath:
        html = requests.get(url=url, headers=header, timeout=30).content
        return ET.HTML(html)
    else:
        html = requests.get(url=url, headers=header).content
        return html
