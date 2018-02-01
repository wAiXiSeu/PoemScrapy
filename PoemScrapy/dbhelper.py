#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 13:56
# @Author  : wAiXi
# @Site    : 
# @File    : dbhelper.py
# @Software: PyCharm Community Edition

import pymysql as mysql
from scrapy.utils.project import get_project_settings


# MySQL数据库帮助类
class DBHelper():
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.db = self.settings['MYSQL_DBNAME']
        self.user = self.settings['MYSQL_USER']
        self.password = self.settings['MYSQL_PASSWORD']
        self.port = self.settings['MYSQL_PORT']
        self.charset = self.settings['MYSQL_CHARSET']

    def connect_mysql(self):
        connection = mysql.connect(host=self.host, user=self.user, passwd=self.password, db=self.db,
                                   port=self.port, charset=self.charset)
        return connection

    def execute(self, sql, *params):
        conn = self.connect_mysql()
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows

    def insert(self, table, params):
        sql = 'insert into ' + table + ' values (' + ','.join(['%s']*len(params)) + ')'
        self.execute(sql, *params)

    def update_by_id(self, table, entity_id=1, **params):
        sql = 'update ' + table + ' set '
        for p in params.items():
            sql += p[0] + " = '" + p[1] + "',"
        sql = sql[:-1] + " where id = %s"
        self.execute(sql, entity_id)

    def select(self, table, **params):
        sql = 'select * from ' + table + ' where 1=1'
        for p in params.items():
            sql += ' and ' + p[0] + " = '" + p[1] + "'"
        print(sql)
        rows = self.execute(sql)
        return rows


if __name__=='__main__':
    mydb = DBHelper()
    # mydb.insert('mydbtest.author', ["9", "小王", "xw", "诗人", "erwrwe", "hehe"])
    # mydb.update_by_id('mydbtest.author', '3', name='xxxx', pinyin='xxxx')
    result = mydb.select('mydbtest.author')
    for r in result:
        print(r)
