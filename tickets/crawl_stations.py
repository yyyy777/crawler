# coding=utf-8

import re

import requests

from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8999'

resp = requests.get(url, verify=False)

stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', resp.text)

pprint(dict(stations), indent=4)

