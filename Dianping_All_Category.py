# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import time
from bs4 import BeautifulSoup
import logging

class get_Categorys():
    def __init__(self,url,usr, pwd, dbname):
        self.url = url
        self.session = requests.session()
        self.headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "www.dianping.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            'Referer': "http://www.dianping.com/shanghai/life"
        }
        self.conn = mysql.connector.connect(user=usr, password=pwd, database=dbname)
        self.tuples = [] #存所有序列

    def create_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'create table category (category_id varchar(20) primary key, category_name varchar(20),category_link  text(20),add_time datetime default NULL,flag bool )')
            self.conn.commit()
            cursor.close()
            print("餐厅种类表建立成功")
        except BaseException as e:
            print("建立餐厅种类表出问题啦", e)

    def insert_category(self,category_id,category_name,category_link,add_time):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO category (category_id,category_name,category_link,add_time,flag)VALUES (%s, %s, %s, %s, %s);',
                (category_id,category_name,category_link,add_time, False))
            self.conn.commit()
            cursor.close()
            print(category_id,category_name,category_link,add_time, "插入成功")
        except BaseException as e:
            print("插入失败",e)

    def get_category(self):
        html = self.session.get(self.url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        try:
            classfyList = soup.find(id="classfy").find_all("a")
        except BaseException as e:
            print("未找到分类列表")
            classfyList = None
            return
        for item in classfyList:
            try:
                id = item.get("href").split('/')[-1]
                name=item.get_text(strip=True)
                link = "http://www.dianping.com"+item.get("href")
                self.tuples.append((id,name,link))
            except BaseException as e:
                print("解析某条出错",e)






if __name__ == '__main__':
    test=get_Categorys("http://www.dianping.com/search/category/1/10",'root', '58424716', 'dianping')
    test.create_database()
    test.get_category()
    # print(type(test.tuples))
    for item in test.tuples:
        test.insert_category(item[0],item[1],item[2],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



