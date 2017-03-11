# coding=utf-8

import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from ..items import DingdianItem, ContentItem


class Myspider(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['www.23us.com']
    base_url = 'http://www.23us.com/class/'
    end_Url = '.html'

    def start_requests(self):

        for i in range(1, 11):
            url = self.base_url + str(i) + '_1' + self.end_Url
            yield Request(url, self.parse)  # 各类小说的连接

        yield Request('http://www.23us.com/quanben/1', self.parse)  # 全本小说的连接

    def parse(self, response):

        max_num = BeautifulSoup(response.text, 'lxml').find(
            'div', class_='pagelink').find_all('a')[-1].get_text()
        baseurl = str(response.url)[:27]
        for num in range(1, int(max_num) + 1):
            if baseurl == 'http://www.23us.com/quanben':
                url = baseurl + '/' + str(num)
            else:
                url = baseurl + '_' + str(num) + self.end_Url
            yield Request(url, callback=self.get_name)

    def get_name(self, response):

        tds = BeautifulSoup(
            response.text,
            'lxml').find_all(
            'tr',
            bgcolor="#FFFFFF")
        for td in tds:
            novelname = td.find_all('a')[1].get_text()
            novelIntroductionUrl = td.find('a')['href']
            yield Request(novelIntroductionUrl, callback=self.get_chapterurl, meta={'name': novelname,
                                                                                    'url': novelIntroductionUrl})

    def get_chapterurl(self, response):

        resp = BeautifulSoup(response.text, 'lxml')
        item = DingdianItem()
        tds = resp.find('table').find_all('td')

        category = resp.find('table').find('a').get_text()
        author = tds[1].get_text()
        base_url = resp.find(
            'p', class_='btnlinks').find(
            'a', class_='read')['href']
        novel_id = str(base_url)[-6:-1].replace('/', '')
        serialstatus = tds[2].get_text()
        serialnumber = tds[4].get_text()

        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('\xa0', '')
        item['novel_id'] = novel_id
        item['serialstatus'] = str(serialstatus).replace('\xa0', '')
        item['serialnumber'] = str(serialnumber).replace('\xa0', '')

        yield item
        yield Request(url=base_url, callback=self.get_chapter, meta={'novel_id': novel_id})

    def get_chapter(self, response):

        urls = re.findall(
            r'<td class="L"><a href="(.*?)">(.*?)</a></b>',
            response.text)
        num = 0
        for url in urls:
            num += 1
            chapterurl = response.url + url[0]
            chaptername = url[1]
            yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num': num,
                                                                         'novel_id': response.meta['novel_id'],
                                                                         'chaptername': chaptername,
                                                                         'chapterurl': chapterurl
                                                                         })

    def get_chaptercontent(self, response):

        item = DingdianItem()
        item['num'] = response.meta['num']
        item['novel_cont_id'] = response.meta['novel_id']
        item['chapterurl'] = response.meta['chapterurl']
        item['chaptername'] = str(
            response.meta['chaptername']).replace(
            '\xa0', '')
        content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        return item
