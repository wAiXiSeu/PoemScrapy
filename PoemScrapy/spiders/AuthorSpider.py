#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/31 16:17
# @Author  : wAiXi
# @Site    : 
# @File    : AuthorSpider.py
# @Description: 用于爬取作者信息

import scrapy
from pypinyin import lazy_pinyin, Style

from PoemScrapy.items import AuthorItem


# 爬取作者信息
class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['http://so.gushiwen.org/authors/Default.aspx?p=1&c=%E5%94%90%E4%BB%A3']

    def parse(self, response):
        author_item = AuthorItem()
        dynasty = response.xpath('//div[@class="titletype"]/div/h1/text()').extract_first()
        resp_entity = response.xpath('//div[@class="sonspic"]')
        for r in resp_entity:
            author_item['author_info'] = {
                'author_id': r.xpath('.//div/p/a/@href').re_first(r'/author_(.*)\.aspx'),
                'author_name': r.xpath('.//div/p/a/b/text()').extract_first(default='no_data'),
                'dynasty': dynasty,
                'author_pinyin': ''.join(lazy_pinyin(r.xpath('.//div/p/a/b/text()').extract_first(default=''),
                                                     style=Style.FIRST_LETTER)),
                'poem_count': r.xpath('.//div/p/a/text()').re_first(r'► (.*)篇诗文'),
                'author_likes': r.xpath('.//div/div/a/span/text()').extract_first(default='no_data').strip(),
                'author_description': r.xpath('.//div/p[@style=" margin:0px;"]/text()').extract_first(
                                          default='no_data'),
                'author_link': 'http://so.gushiwen.org' +
                               r.xpath('.//div/p/a/@href').extract_first(default='no_data'),
                'poem_first_link': 'http://so.gushiwen.org' +
                                   r.xpath('.//div/p[@style=" margin:0px;"]/a/@href').extract_first(default='no_data')
            }
            yield author_item
        next_page = response.xpath('//a[@style="width:60px;"]/@href').extract()
        if next_page is not None:
            yield response.follow(next_page[-1], self.parse)
