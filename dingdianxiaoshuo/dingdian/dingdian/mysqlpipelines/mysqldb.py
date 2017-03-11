# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Novel, Content

from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'mysql+mysqlconnector://root:123456789a@localhost:3306/dingdian')

Base = declarative_base()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


DBSession = sessionmaker(bind=engine)
session = DBSession()


class MysqlDB:

    def __init__(self):
        pass

    @classmethod
    def insert_to_db(cls, name, author, category, novel_id):

        new_novel = Novel(
            name=name,
            author=author,
            category=category,
            novel_id=novel_id)
        session.add(new_novel)
        session.commit()
        session.close()

    @classmethod
    def select_name(cls, novel_id):

        isnovel = session.query(Novel).filter(novel_id == novel_id).one()

        if isnovel:
            return True
        return False

    @classmethod
    def insert_chapter(cls, chaptername, chapter_content, content_id, num_id, url):

        new_content = Content(
            chaptername=chaptername,
            chapter_content=chapter_content,
            content_id=content_id,
            num_id=num_id,
            url=url)

        session.add(new_content)
        session.commit()

    @classmethod
    def select_chapter(cls, url):

        iscontent = session.query(Content).filter(url == url).one()

        if iscontent:
            return True
        return False

