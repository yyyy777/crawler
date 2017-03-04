# coding=utf-8

import urllib2

from bs4 import BeautifulSoup


class BDTB:

    def __init__(self, baseurl, seeLZ, floorTag):

        self.baseurl = baseurl

        self.seeLZ = '?see_lz=' + str(seeLZ)

        self.file = None

        self.floor = 1

        self.floorTag = floorTag

        self.defaultTitle = u"百度贴吧"

    def getpage(self, pagenum):

        try:

            url = self.baseurl + self.seeLZ + '&pn=' + str(pagenum)

            request = urllib2.Request(url)

            response = urllib2.urlopen(request)

            page = BeautifulSoup(response, "html5lib")

            return page

        except urllib2.URLError, e:

            if hasattr(e, 'reason'):

                print u"连接百度贴吧失败，错误原因", e.reason

                return None

    def getTitle(self):

        page = self.getpage(1)

        tag = page.h3

        title = tag['title']

        print title

        return title

    def getPageNum(self):

        page = self.getpage(1)

        num = page.find_all(attrs={"class": "red"})

        pagenum = num[1].string

        return int(pagenum)

    def getcontent(self):

        pagenum = self.getPageNum() + 1

        contents = []

        for num in range(1, pagenum):

            page = self.getpage(num)

            num = page.find_all('cc')

            for item in num:

                content = item.get_text()

                contents.append(content.encode('utf-8'))

        return contents

    def getFileTitle(self):

        title = self.getTitle()

        if title is not None:

            self.file = open(title + ".txt", "w+")

        else:

            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self):

        contents = self.getcontent()

        for item in contents:

            if self.floorTag == '1':

                floorLine = '\n' + \
                    str(self.floor) + \
                    u'---------------------------------------------\n'

                self.file.write(floorLine)

            self.file.write(item)

            self.floor += 1

    def start(self):

        self.getFileTitle()

        pagenum = self.getPageNum()

        if pagenum == None:

            print "URL已失效，请重试"

            return

        try:

            print "该帖子共有" + str(pagenum) + "页"

            self.writeData()

        except IOError, e:

            print "写入异常，原因" + e.message

        finally:

            print "写入成功"


print u"请输入帖子代号"

baseurl = 'http://tieba.baidu.com/p/' + \
    str(raw_input(u'http://tieba.baidu.com/p/'))

seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")

floorTag = raw_input("是否写入楼层信息，是输入1否输入0\n")

bdtb = BDTB(baseurl, seeLZ, floorTag)

bdtb.start()
