# crawler
学习python爬虫时的一些代码。

## baidutieba
urllib2爬取百度贴吧某帖子的各楼层的内容

## huaban
selenium爬取花瓣网的图片

## liaoxuefengpdf
request爬取廖雪峰老师网站上的教程并转成pdf

## dingdianxiaoshuo
scrapy爬取顶点小说网全部小说

## meizitu
爬取妹子图全部图片

## weather
scrapy爬取新浪天气

## tickets
获取12306车票信息

## wechat
爬取微信公众号全部文章的链接

## zhihu
scrapy-redis分布式爬取知乎全部用户的信息。使用 scrapy 通过知乎的 API爬取，redis做分布式链接。从一个人的关注列表开始，递归爬取所有关注的人和被关注者，从而实现爬取整个知乎上所有进行过关注和被关注的人的信息。没有关注的人且没有被关注的用户不进行爬取。爬取下来的所有信息存入到 MongoDB 中。