# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from PoemScrapy.dbhelper import DBHelper


class PoemscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


# 将爬取到的作者信息写入数据库
class AuthorSpiderPipeline(object):
    def __init__(self):
        self.mydb = DBHelper()

    def process_item(self, item, spider):
        self.mydb.insert('mydbtest.author',
                         [item['author_info']['author_id'],
                          item['author_info']['author_name'],
                          item['author_info']['dynasty'],
                          item['author_info']['author_pinyin'],
                          item['author_info']['poem_count'],
                          item['author_info']['author_likes'],
                          item['author_info']['author_description'],
                          item['author_info']['author_link'],
                          item['author_info']['poem_first_link']])
        return item


class AuthorSpiderWithoutInsertPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item


# 将爬取到的诗文信息写入数据库
class PoemSpiderPipeline(object):
    def __init__(self):
        self.mydb = DBHelper()

    def process_item(self, item, spider):
        self.mydb.insert('mydbtest.poem',
                         [item['poem_info']['poem_id'],
                          item['poem_info']['poem_no'],
                          item['poem_info']['poem_title'],
                          item['poem_info']['poem_content'],
                          item['poem_info']['author_id'],
                          item['poem_info']['author_name'],
                          item['poem_info']['poem_likes'],
                          item['poem_info']['poem_tags'],
                          item['poem_info']['poem_link']])
        return item
