# coding=utf-8

import scrapy

from weather.items import WeatherItem

from bs4 import BeautifulSoup

class WeatherSpider(scrapy.Spider):

    name = "localweather"

    #allowed_domains = ["sina.com.cn"]

    start_urls = ['http://weather.sina.com.cn/']

    def parse(self, response):

        item = WeatherItem()

        resp = response.body

        soup = BeautifulSoup(resp, "html5lib")

        itemTemp = {}

        itemTemp['city'] = soup.find(id='slider_ct_name')

        tenDay = soup.find(id='blk_fc_c0_scroll')
        #print tenDay

        itemTemp['date'] = tenDay.findAll("p", class_="wt_fc_c0_i_date")

        itemTemp['dayDesc'] = tenDay.findAll("img", class_="icons0_wt")

        itemTemp['dayTemp'] = tenDay.findAll("p", class_="wt_fc_c0_i_temp")

        for att in itemTemp:

            item[att] = []

            if att == 'city':
                item[att] = itemTemp.get(att).text
                continue

            for obj in itemTemp.get(att):

                if att == 'dayDesc':
                    item[att].append(obj['title'])

                else:
                    item[att].append(obj.text)

        return item





