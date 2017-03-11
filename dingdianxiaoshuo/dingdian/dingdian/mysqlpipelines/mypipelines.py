# coding=utf-8



from ..items import DingdianItem, ContentItem
from .mysqldb import MysqlDB


class MyDingdianPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, DingdianItem):
            novel_id = item['novel_id']
            name = item['name']
            ret = MysqlDB.select_name(novel_id)
            if ret:
                print('{0}已经存入数据库了'.format(name))
                pass
            else:
                author = item['author']
                category = item['category']
                MysqlDB.insert_to_db(name, author, category, novel_id)
                print('存入数据库:{0}'.format(name))

        if isinstance(item, ContentItem):

            url = item['chapterurl']
            content_id = item['novel_cont_id']
            num_id = item['num']
            chaptername = item['chaptername']
            chapter_content = item['chaptercontent']

            ret = MysqlDB.select_chapter(url)
            if ret:
                print('已经存入数据库了')
            else:
                MysqlDB.insert_chapter(chaptername, chapter_content, content_id, num_id, url)
                print('小说内容存储完毕')

            return item
