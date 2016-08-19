## *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import time
from bs4 import BeautifulSoup
import logging
#根据店铺地址爬评论
SleepNum = 1     # 抓取页面的间隔时间，可为0
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Connection":"keep-alive",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life",
    # 'Cookie':'_hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=1.273426386.1469369064.1469369064.1469369064.1; __utmz=1.1469369064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dper=5529c55bfbd478e8c1613429bfde641841a70874a3484cd0259f2c34696bdc02; ua=15651383078; PHOENIX_ID=0a017429-1562227b555-ae953b6; ll=7fd06e815b796be3df069dec7836c3df; JSESSIONID=B596AEA7C9E6A9AF4B51AFD1AC85FFC9; aburl=1; cy=1; cye=shanghai'
    'Cookie':'m_rs=5a23972d-921a-4d46-9ff8-d385d3381dbd; _hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=1.273426386.1469369064.1469369064.1469369064.1; __utmz=1.1469369064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dper=79e1190dfef09628df10db9edd2c9590a25d955f69a85bfe684d4a4ff5d2ef02; ua=13816174065; PHOENIX_ID=0a65026a-1562272a84d-126c111; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; JSESSIONID=6043782DB8A392CA09529A51163D3CA0; aburl=1; cy=1; cye=shanghai'
}
proxies = {
"http":"180.169.5.20:1920",
"http":"119.188.94.145:80",
"http":"180.161.16.166:8118",
"http":"183.161.248.119:8118",
"http":"60.185.209.157:8998",
"http":"120.36.164.143:8118",
"http":"122.239.26.137:8998",
"http":"123.7.177.20:9999",
"http":"119.165.239.81:8118",
"http":"58.214.229.228:8118",
"http":"123.119.18.138:8118",
"http":"61.52.247.229:3128",
"http":"183.129.178.14:8080",
"http":"121.236.212.99:8998",
"http":"222.211.65.72:8080",
"http":"60.167.23.20:8118",
"http":"122.96.59.105:843",
"http":"123.168.109.150:2226",
"http":"121.10.240.45:80",
"http":"116.231.192.22:2226",


}
req = requests.get("http://www.dianping.com/shop/11556193/review_more?pageno=236", headers=headers)
soup = BeautifulSoup(req.text, 'lxml')
print(req.encoding)
print(req.json())