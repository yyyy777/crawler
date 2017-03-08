# coding = utf-8

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import pdfkit

import os

import sys

dcap = dict(DesiredCapabilities.PHANTOMJS)

dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")

js2 = 'window.scrollTo(0, document.body.scrollHeight)'

class crawl_wechat:

    def __init__(self, url):

        self.url = url

        self.old_scroll_height = 0

    def getList(self):

        driver = webdriver.PhantomJS(desired_capabilities=dcap)

        driver.get(self.url)

        for i in range(10):
            if(BeautifulSoup(driver.page_source,
                            'html5lib').find('div',class_="more_wrapper \
                                            no_more").get("style")) == 'display:none':
                driver.execute_script(js2)

        resp = BeautifulSoup(driver.page_source, 'html5lib')
        msg_list = []
        msg_cover = resp.find_all("div", class_="msg_cover")

        for href in msg_cover:
            if href.get("hrefs") is not None:
                msg_list.append(href.get("hrefs"))
            else:
                msg_cover_redirect = resp.find_all("a",class_="cover_appmsg_link_box redirect")
                for tmp in msg_cover_redirect:
                    msg_list.append(tmp.get("hrefs"))

        sub_msg = resp.find_all("h4", class_="flex_msg_title msg_title")

        for sub_href in sub_msg:
            msg_list.append(sub_href.get("hrefs"))

        print(msg_list)


if __name__ == '__main__':

    key = sys.argv[1]

    wechat_url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA3NDk1NjI0OQ==&uin=MjgxMTU0NDM1&key={0}&devicetype=Windows+10&version=6203005d&lang=zh_CN&ascene=7&pass_ticket=vbFYPkG%2FXKNQwJgsf2AF6LH3gE3ceAEvtzrNPxFswjfdlxJ5b5BYLTzxg4iitkHG'.format(key)

    wechat = crawl_wechat(wechat_url)

    wechat.getList()
