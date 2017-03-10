# coding=utf-8

import os
import requests
from bs4 import BeautifulSoup
from hashlib import md5

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

class meizitu:

    def __init__(self, url):
        self.url = url

    def request(self, url):
        content = requests.get(url, headers=headers)
        return content

    def html(self, href):
        html = self.request(href)
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()

        for page in range(1, int(max_span)+1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, page_url):
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        name = md5(str(img_url).encode(encoding='utf-8')).hexdigest()
        img = self.request(img_url)
        with open(str(name) + '.jpg', 'ab')as f:
            f.write(img.content)

    def mkdir(self, path):
        path = path.strip()
        isExixts = os.path.exists(os.path.join(cwd_path, path))
        if not isExixts:
            print(u'新建文件夹：{0}'.format(path))
            os.mkdir(os.path.join(cwd_path, path))
            os.chdir(os.path.join(cwd_path, path))
            return True
        else:
            print(u'文件夹已经存在了{0}'.format(path))
            return False

    def all_url(self):
        html = self.request(self.url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print(u'开始保存：', title)
            path = str(title).replace("?", '_')
            self.mkdir(path)
            href = a['href']
            self.html(href)

if __name__ == '__main__':
    url = 'http://www.mzitu.com/all'
    cwd_path = os.getcwd()
    Meizitu = meizitu(url)
    Meizitu.all_url()
