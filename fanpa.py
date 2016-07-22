#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-06-07 07:40:58
# Project: dazhongdianping

from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
from pymongo import MongoClient
import base64
import re

id = 0
count = 0
number = 0
global count
global id
global number


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.dianping.com/search/keyword/3/0_%E4%B8%80%E9%B8%A3%E7%9C%9F%E9%B2%9C%E5%A5%B6%E5%90%A7',
                   callback=self.local_page)

    @config(age=2 * 24 * 60)
    def local_page(self, response):

        self.save_local('remark', response.url, response.doc)
        for each in response.doc('DIV.pic>A').items():
            self.crawl(each.attr.href, callback=self.index_page)

        # 下一页
        for each in response.doc('A.next', ).items():
            self.crawl(each.attr.href, callback=self.local_page)

    @config(age=3 * 24 * 60)
    def index_page(self, response):

        global number

        # 店铺信息
        for each in response.doc('DIV#basic-info').items():

            number += 1

            info = {}
            tmp = BeautifulSoup(str(each))
            name = tmp.find('h1', class_='shop-name')

            # 店铺编号
            info['itemid'] = number

            # 店铺名称
            if re.findall(r'<h1 class="shop-name">[\s]+(.*)', str(name)):
                info['name'] = re.findall(r'<h1 class="shop-name">[\s]+(.*)', str(name))[0]
            else:
                info['name'] = '-'

            #
            if re.findall(r'<a class="branch J-branch">(.*)<i class="icon i-arrow"></i></a>', str(name)):

                info['branch'] = \
                re.findall(r'<a class="branch J-branch">(.*)<i class="icon i-arrow"></i></a>', str(name))[0]
            else:
                info['branch'] = '-'

            #
            info['basic_info'] = []

            basic_info = tmp.find("div", class_="brief-info")

            if basic_info:
                # 星级
                star = basic_info.span.get('class')[1]

                info['level'] = int(re.findall(r'mid-str(.*)', str(star))[0]) * 1.0 / 10
                print
                info['level']
                for td in basic_info.find_all('span', class_="item"):
                    info['basic_info'].append(td.string.encode('utf-8'))
            else:
                info['level'] = '-'
            # 区名
            region = tmp.find('span', itemprop='locality region')

            # 街道信息
            address = tmp.find('span', class_='item', itemprop="street-address")

            if region:
                info['region'] = region.string.encode('utf-8')
            else:
                info['region'] = '-'

            if address:

                info['address'] = address.string.encode('utf-8').strip()

            else:
                info['address'] = '-'

            # 电话
            tel = tmp.find('p', class_="expand-info tel")
            if tel:

                info['telephone'] = tel.find('span', class_='item').string.encode('utf-8')

            else:
                info['telephone'] = '-'

        # 更多评论
        if response.doc('P.comment-all>A'):

            for each in response.doc('P.comment-all>A').items():
                self.crawl(each.attr.href, callback=self.detail_page_all)
        # 如果当前已经显示了所有评论
        else:

            self.crawl(response.url, callback=self.detail_page)

    @config(age=4 * 24 * 60)
    def detail_page(self, response):

        global id

        each = BeautifulSoup(str(response.doc))

        # 获取评论
        tmp = each.find_all('li', class_="comment-item")

        for tr in tmp:

            res = {}

            id += 1

            # 评论id
            res['itemid'] = id

            # 用户名
            if tr.find('p', class_='user-info'):
                res['user'] = tr.find('p', class_='user-info').a.string.encode('utf-8')
            else:
                res['user'] = '-'

            res['comment'] = {}

            # 点赞次数
            date = tr.find('div', class_='misc-info')
            res['time'] = date.find('span', class_='time').string.encode('utf-8')

            # 商店信息
            info = tr.find('p', class_='shop-info')

            # 商店得分情况
            star = info.span.get('class')[1]
            res['level'] = int(re.findall(r'sml-str(.*)', str(star))[0]) * 1.0 / 10
            # 口味环境和服务得分
            if info.find_all('span', class_='item'):

                for thing in info.find_all('span', class_='item'):
                    thing = thing.string.encode('utf-8').split('£º')

                    res['comment'][thing[0]] = thing[1]

            if info.find('span', class_='average'):
                res['price'] = info.find('span', class_='average').string.encode('utf-8').split('£º')[1]
            else:
                res['price'] = '-'

            # 展开评论
            content = tr.find('div', class_='info J-info-all Hide')

            if content:

                res['content'] = content.p.string.encode('utf-8')

            else:
                if tr.find('div', class_='info J-info-short'):

                    res['content'] = tr.find('div', class_='info J-info-short').p.string.encode('utf-8').strip()

                else:
                    res['content'] = '-'

    @config(age=4 * 24 * 60)
    def detail_page_all(self, response):

        global count

        # 得到全部评论
        for each in response.doc('DIV.comment-list').items():

            each = BeautifulSoup(str(each))

            tmp = each.find_all('li')

            for tr in tmp:

                res = {}
                count += 1

                # 点评的id
                res['itemid'] = count

                # 星级
                star = tr.find('div', class_='content')
                if star:

                    rank = star.span.get('class')[1]

                    res['level'] = int(re.findall(r'irr-star(.*)', str(rank))[0]) * 1.0 / 10

                else:
                    continue

                # 点赞次数
                date = tr.find('div', class_='misc-info')
                res['time'] = date.find('span', class_='time').string.encode('utf-8')

                # 用户名
                name = tr.find('div', class_='pic')
                if name:

                    res['user'] = name.find('p', class_='name').string.encode('utf-8')
                else:

                    res['user'] = '-'

                # 口味环境服务
                res['comment'] = {}
                page = tr.find('div', class_='comment-rst')
                if page:

                    info = re.findall('class="rst">(.*)<em class="col-exp">(.*)</em></span>', str(page))

                    if info:

                        for td in info:
                            res['comment'][td[0]] = td[1].strip('(').strip(')')
                # 是否为团购点评
                group = tr.find('div', class_='comment-txt')
                if group.find('a', target='blank'):

                    res['shopping_group'] = group.find('a', target='blank').string.encode('utf-8')

                else:
                    res['shopping_group'] = '-'

                # 人均价格
                price = tr.find('span', class_='comm-per')
                if price:
                    res['price'] = price.string.encode('utf-8')

                else:
                    res['price'] = '-'
                # 简要评论
                if tr.find('div', class_='J_brief-cont'):

                    tmp = str(tr.find('div', class_='J_brief-cont'))
                    res['content'] = re.findall(r'<div class="J_brief-cont">([\w\W]*)</div>', tmp)[0].strip()

                else:
                    res['content'] = '-'

        # 下一页
        for each in response.doc('A.NextPage').items():
            self.crawl(each.attr.href, callback=self.detail_page_all)