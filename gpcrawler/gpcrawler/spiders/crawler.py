#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import GooglePlayItem

# https://play\.google\.com/store/apps/details\?id=\S+
# from gpcrawler.gpcrawler.items import GooglePlayItem


def parse_pkg(url):
    params = url.split('?')[-1]
    for item in params.split('&'):
        val = item.split('=')
        if val[0] == 'id':
            return val[1]
    return
    # return url.split('id=')[-1]


class GooglePlaySpider(CrawlSpider):
    name = 'googleplay'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/apps', 'https://play.google.com/store/apps/details?id=com.ksmobile.launcher']
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details",)), callback='parse_item', follow=True),
    ]

    # start_urls = ["https://play.google.com/store/apps"]
    # rules = (
    #     Rule(LinkExtractor(allow=('/store/apps',)), follow=True),
    #     Rule(LinkExtractor(allow=('/store/apps/details\?')), follow=True, callback='parse_item')
    # )

    # def parse(self, response):
    #     '''Parse all categories apps'''
    #     hrefs = response.css('.child-submenu-link::attr(href)').extract()
    #     for href in hrefs:
    #         yield Request(
    #             response.urljoin(href),
    #             callback=self.parse_category,
    #         )
    #
    # def parse_category(self, response):
    #     '''Parse specific category apps'''
    #     hrefs = response.css('.single-title-link > a::attr(href)').extract()
    #     for href in hrefs:
    #         yield Request(
    #             response.urljoin(href),
    #             callback=self.parse_apps,
    #         )
    #
    # def parse_apps(self, response):
    #     '''Parse a list of apps'''
    #     hrefs = response.css('a[class="title"]::attr(href)').extract()
    #     for href in hrefs:
    #         yield Request(
    #             response.urljoin(href),
    #             callback=self.parse_item,
    #         )

    def parse_item(self, response):
        print(response.url)
        pkg = parse_pkg(response.url)
        if not pkg:
            return
        # from gpcrawler.gpcrawler.items import GooglePlayItem
        item = GooglePlayItem()
        item['pkg'] = pkg
        item['catagory'] = response.xpath("//a[@class='document-subtitle category']/@href").extract()[0].split('/')[-1].lower()
        down_num = response.xpath("//div[@itemprop='numDownloads']").xpath("text()").extract()[0].strip().split('-')
        if len(down_num) != 2:
            return
        item['down_min'] = str(down_num[0].strip().replace(',', ''))
        item['down_max'] = str(down_num[1].strip().replace(',', ''))
        if not item['down_min'] or not item['down_max']:
            return
        return item
