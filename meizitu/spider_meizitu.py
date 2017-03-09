# coding=utf-8

import os
import requests
from bs4 import BeautifulSoup
from hashlib import md5

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://www.mzitu.com/all'
html = requests.get(all_url, headers=headers)
Soup = BeautifulSoup(html.text, 'lxml')
all_a = Soup.find('div', class_='all').find_all('a')

for a in all_a:
    title = a.get_text()
    href = a['href']
    html = requests.get(href, headers=headers)
    html_soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_soup.find(
        'div', class_='pagenavi').find_all('span')[-2].get_text()
    for page in range(1, int(max_span) + 1):
        page_url = href + '/' + str(page)
        img_html = requests.get(page_url, headers=headers)
        img_soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_soup.find('div', class_='main-image').find('img')['src']
        # print(img_url)
        name = md5(str(img_url).encode(encoding='utf-8')).hexdigest()
        img = requests.get(img_url, headers=headers)
        # f = open(name+'.jpg', 'ab')
        with open(str(name) + '.jpg', 'ab')as f:
            f.write(img.content)
