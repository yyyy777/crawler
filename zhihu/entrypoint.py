'''
使scrapy可以用pycharmy远程调试
'''

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'zhihuuser'])