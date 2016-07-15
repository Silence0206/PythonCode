# *- coding: utf-8 -*-

import  requests
from bs4 import  BeautifulSoup

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life"
}
res = requests.get("http://www.dianping.com/shopall/1/0", headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
print(soup)
