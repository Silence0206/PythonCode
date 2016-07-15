# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import request
import requests

url = "http://weibo.com/p/100808d39b6cd18e342b36cd190a45b73c5d17"
webheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'SUB=_2AkMhOy0Bf8NhqwJRmPodzWnnao53wgnEiebDAHzsJxJjHk067K9I-8iE-29j-4-KpEJ5_Ud48Ysq; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhQP84-F0jZKyZKAdUFQMvV; SINAGLOBAL=2757537297438.83.1456917032203; _s_tentry=www.liaoxuefeng.com; Apache=8121454045176.506.1468047286035; ULV=1468047286811:5:2:2:8121454045176.506.1468047286035:1468045288576; YF-V5-G0=447063a9cae10ef9825e823f864999b0; YF-Ugrow-G0=169004153682ef91866609488943c77f; UOR=www.doc88.com,widget.weibo.com,cuiqingcai.com; WBStore=8ca40a3ef06ad7b2|undefined; YF-Page-G0=dc8d8d4964cd93a7c3bfa7640c1bd10c',
    'DNT': '1',
    'Host': 'weibo.com',
    'Pragma': 'no-cache',
    'Referer': 'http://s.weibo.com/weibo/%25E6%2588%2591%25E4%25BB%25A5%25E5%2589%258D%25E4%25B9%259F%25E6%2598%25AF%25E4%25B8%2580%25E4%25B8%25AA%25E7%2598%25A6%25E5%25AD%2590?topnav=1&wvr=6&Refer=top_hot',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.8.1000 Chrome/30.0.1599.101 Safari/537.36'
}
re = request.Request(url=url, headers=webheader)
response = request.urlopen(re)
html = response.read().decode("utf-8")
print(html)

