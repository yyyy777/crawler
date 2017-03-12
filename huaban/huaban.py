# coding=utf-8

import time

from bs4 import BeautifulSoup

from selenium import webdriver

from urllib.request import urlretrieve


class crawl_huaban:

    def __init__(self,url):

        self.url = url

    def getHtml(self, url):

        driver = webdriver.PhantomJS()

        driver.get(url)

        driver.implicitly_wait(3)

        resp = BeautifulSoup(driver.page_source, 'html5lib')

        driver.quit()

        return resp

    def getPage(self):

        driver = webdriver.PhantomJS()

        driver.get(self.url)

        driver.implicitly_wait(3)

        resp = BeautifulSoup(driver.page_source, 'html5lib')

        driver.quit()

        return resp

    def getImage(self):

        resp = self.getPage()

        pins_ids = []

        pins = resp.find_all("a", class_="img x layer-view loaded")

        for pin in pins:

            pins_ids.append(pin.get('href'))

        pins_ids = pins_ids[2:]

        total = 1

        for pinid in pins_ids:

            print('第{0}张照片'.format(total))

            img_url = 'http://huaban.com%s' %(pinid)

            img_html = self.getHtml(img_url)

            img_hold = img_html.find("div", class_="image-holder")


            img_src = img_hold.find("img").get("src")

            #print(img_url)
            #print(img_hold)
            #print(img_src)

            img_src_url = 'http:%s' % img_src

            #print(img_src_url)

            try:

                urlretrieve(img_src_url, '%s.jpg' %pinid)

                print("获取图片：%s成功!" % img_src_url)

            except:

                print("获取图片：%s失败，跳过，获取下一张!" % img_src_url)

            total += 1

        print("获取图片完毕")

if __name__ == '__main__':

    #url = 'http://huaban.com/search/?q=%E7%BE%8E%E8%85%BF'

    for i in range(1,11):

        print('第{0}页'.format(i))

        url = 'http://huaban.com/search/?q=%E7%BE%8E%E8%85%BF&izxnwygj&page={0}&per_page=20&wfl=1'.format(i)

        crawler = crawl_huaban(url)

        start = time.clock()

        crawler.getImage()

        end = time.clock()

        print('总共用时:%03f seconds\n\n' %(end-start))
