# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PoemscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AuthorItem(scrapy.Item):
    author_id = Field()
    name = Field()
    dynasty = Field()
    pinyin = Field()
    poem_count = Field()
    introduction = Field()
    link = Field()
    poem_link = Field()


class PoemItem(scrapy.Item):
    poem_info = Field()
