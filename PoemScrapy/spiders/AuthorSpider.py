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

    def __init__(self):
        self.allowed_domains = ['so.gushiwen.org']
        self.host = 'https://so.gushiwen.org'
        self.start_urls = [f"{self.host}/{t}" for t in
                           ['/authors/Default.aspx?p=1&c=%e5%85%88%e7%a7%a6',
                            '/authors/Default.aspx?p=1&c=%e4%b8%a4%e6%b1%89',
                            '/authors/Default.aspx?p=1&c=%e9%ad%8f%e6%99%8b',
                            '/authors/Default.aspx?p=1&c=%e5%8d%97%e5%8c%97%e6%9c%9d',
                            '/authors/Default.aspx?p=1&c=%e9%9a%8b%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e5%94%90%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e4%ba%94%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e5%ae%8b%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e9%87%91%e6%9c%9d',
                            '/authors/Default.aspx?p=1&c=%e5%85%83%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e6%98%8e%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e6%b8%85%e4%bb%a3',
                            '/authors/Default.aspx?p=1&c=%e8%bf%91%e7%8e%b0%e4%bb%a3']
                           ]

    def parse(self, response):
        author_item = AuthorItem()
        dynasty = response.xpath(
            '//div[@class="main3"]/div/div/div[@class="son1"]/h1/text()').extract_first()
        resp = response.xpath('//div[@class="sonspic"]')
        for r in resp:
            author_item["author_id"] = r.xpath('.//div/p/a/@href').re_first(r'/authorv_(.*)\.aspx')
            author_item["name"] = r.xpath('.//div/p/a/b/text()').extract_first(default='no_data')
            author_item["dynasty"] = dynasty
            author_item["pinyin"] = ''.join(lazy_pinyin(r.xpath('.//div/p/a/b/text()').extract_first(default=''),
                                                        style=Style.FIRST_LETTER))
            author_item["poem_count"] = r.xpath('.//div/p/a/text()').re_first(r'► (.*)篇诗文')
            author_item["introduction"] = r.xpath('.//div/p[@style=" margin:0px;"]/text()').extract_first(
                default='no_data')
            author_item["link"] = response.urljoin(r.xpath('.//div/p/a/@href').extract_first(default='no_data'))
            author_item["poem_link"] = response.urljoin(r.xpath(
                './/div/p[@style=" margin:0px;"]/a/@href').extract_first(default='no_data'))
            yield author_item
        next_page = response.xpath('//a[@class="amore"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, self.parse)
