# coding=utf-8

from sqlalchemy import Column, String, Integer,Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Novel(Base):

    __tablename__ = 'novel'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    author = Column(String(255))
    category = Column(String(255))
    novel_id = Column(Integer)

class Content(Base):

    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    chapter_name = Column(String(255))
    chapter_content = Column(Text)
    content_id = Column(Integer)
    num_id = Column(Integer)
    url = Column(String(255))