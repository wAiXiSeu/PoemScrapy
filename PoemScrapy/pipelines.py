# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from PoemScrapy.dbhelper import MongoHelper


# 将爬取到的作者信息写入数据库
class AuthorSpiderPipeline(object):
    def __init__(self):
        self.collection = MongoHelper().get_collection("author")

    def process_item(self, item):
        self.collection.insert_one(item["author_info"])


class AuthorSpiderWithoutInsertPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item

