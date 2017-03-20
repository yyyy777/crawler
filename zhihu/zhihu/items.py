# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    headline = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    url_token = scrapy.Field()
    gender = scrapy.Field()
    cover_url = scrapy.Field()
    type = scrapy.Field()
    badge = scrapy.Field()

    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    commercial_question_count = scrapy.Field()
    favorite_count = scrapy.Field()
    favorited_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_columns_count = scrapy.Field()
    following_count = scrapy.Field()
    pins_count = scrapy.Field()
    question_count = scrapy.Field()
    thank_from_count = scrapy.Field()
    thank_to_count = scrapy.Field()
    thanked_count = scrapy.Field()
    vote_from_count = scrapy.Field()
    vote_to_count = scrapy.Field()
    voteup_count = scrapy.Field()
    following_favlists_count = scrapy.Field()
    following_question_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    marked_answers_count = scrapy.Field()
    mutual_followees_count = scrapy.Field()
    hosted_live_count = scrapy.Field()
    participated_live_count = scrapy.Field()

    locations = scrapy.Field()
    educations = scrapy.Field()
    employments = scrapy.Field()
