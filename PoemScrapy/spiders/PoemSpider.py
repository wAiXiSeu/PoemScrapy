#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 14:00
# @Author  : wAiXi
# @Site    : 
# @File    : PoemSpider.py
# @Description: 用于爬取古诗文内容相关信息
import re
import scrapy
from pypinyin import lazy_pinyin, Style

from PoemScrapy.dbhelper import DBHelper
from PoemScrapy.items import PoemItem


class PoemSpider(scrapy.Spider):
    name = 'poem'
    allowed_domains = ['so.gushiwen.org']

    # start_urls = ['http://so.gushiwen.org/authors/authorsw_665A1.aspx']

    def __init__(self):
        self.start_urls = self._get_poem_first_links()

    def _get_poem_first_links(self):
        self.db = DBHelper()
        poem_links = self.db.execute('select poem_first_link from mydbtest.author')
        urls = []
        for pl in poem_links:
            urls.append(pl[0])
        return urls

    def parse(self, response):
        poem_item = PoemItem()
        resp_entity = response.xpath('//div[@class="sons"]')
        cont_entity = response.xpath('//div/textarea/text()').extract()
        for index, val in enumerate(resp_entity):
            poem_item['poem_info'] = {
                'poem_id': val.xpath('.//div[@class="cont"]/p/a/@href').re_first(r'/shiwenv_(.*)\.aspx'),
                'poem_no': val.xpath('.//div[@class="cont"]/div[@class="contson"]/@id').re_first(r'contson(.*)') or '',
                'poem_title': val.xpath('.//div[@class="cont"]/p/a/b/text()').extract_first(default=''),
                'poem_content': cont_entity[index].split('——')[0] or '' if len(
                    cont_entity[index].split('——')[0] or '') <= 750 else (cont_entity[index].split('——')[
                                                                              0] or '')[0:750] + '...',
                'author_id': re.search(r'\d+',
                                       val.xpath('.//div[@class="cont"]/p[@class="source"]/a/@href').
                                       extract()[-1]).group() or '',
                'author_name': val.xpath('.//div[@class="cont"]/p[@class="source"]/a/text()').extract()[-1],
                'poem_likes': val.xpath('.//div[@class="tool"]/div[@class="good"]/a/span/text()').extract_first(
                    default='').strip(),
                'poem_tags': '，'.join(val.xpath('.//div[@class="tag"]/a/text()').extract()),
                'poem_link': 'http://so.gushiwen.org' +
                             val.xpath('.//div[@class="cont"]/p/a/@href').extract_first(default=''),
            }
            yield poem_item
        next_page = response.xpath('//a[@style="width:60px;"]/@href').extract()
        if len(next_page) > 0:
            yield response.follow(next_page[-1], self.parse)
