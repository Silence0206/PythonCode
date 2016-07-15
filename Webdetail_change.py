#挖话题初步
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request
import json
import re

url = "http://weibo.com/p/100808d39b6cd18e342b36cd190a45b73c5d17"
topic="大鱼海棠"
webheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'weibo.com',
    'Referer': 'http://s.weibo.com/weibo/%25E6%2588%2591%25E4%25BB%25A5%25E5%2589%258D%25E4%25B9%259F%25E6%2598%25AF%25E4%25B8%2580%25E4%25B8%25AA%25E7%2598%25A6%25E5%25AD%2590?topnav=1&wvr=6&Refer=top_hot',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.8.1000 Chrome/30.0.1599.101 Safari/537.36',
    "Cookie": 'SINAGLOBAL=1371486447751.522.1445952298263; login_sid_t=69e05d1540aa69dd16c65d92490ce85d; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-Page-G0=8ec35b246bb5b68c13549804abd380dc; _s_tentry=weibo.com; Apache=2465388884186.248.1458369833718; ULV=1458369834611:7:2:1:2465388884186.248.1458369833718:1456924983931; YF-V5-G0=8d795ebe002ad1309b7c59a48532ef7d; wb_bub_hot_1568350187=1; WBtopGlobal_register_version=8a840560e41b693d; WBStore=8ca40a3ef06ad7b2|undefined; UOR=baike.baidu.com,widget.weibo.com,login.sina.com.cn; SCF=AhVmE1Ji-nKS-vHdSiJOPi5SkEXgHD57lEg4aoSk7ik0KRp6WTT19Y_W6HxU2O-b4q1WF-kTCRRk9KdpQaDMxYE.; SUB=_2A256g1FzDeTxGedL7VoS9S7NwzuIHXVZ-cW7rDV8PUNbmtBeLWjbkW-RWeX6Rb9Ieslz3VO-VUH3qCLMbw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W53xk8Gxv.J-BBGKgLly6N95JpX5K2hUgL.Fo2fSon0SK5p1hM2dJLoI7LsdNi_IJDLIJ-t; SUHB=0la0VucngMFcdf; ALF=1500009634; SSOLoginState=1468473635; un=732379020@qq.com; wvr=6; gsid_CTandWM=4uPKCpOz5W2z8Q6wY6rPE6zZY31'
}
re = request.Request(url=url, headers=webheader)
response = request.urlopen(re)
html = response.read().decode("utf-8")
soup = BeautifulSoup(html,"html.parser")
print(soup)

print(soup.find_all('script')[2].string.split(';')[10].split("=")[1][1:-1])
#判断是否登录BeautifulSoup
if soup.find_all('script')[2].string.split(';')[1][-2] == "1":
    print("登录成功")
else:
    print("登录失败",soup.find_all('script')[2].string.split(';')[1][-2])

for link in soup.find_all('script'):
    if "WB_detail" in link.string and (not("主持人推荐" in link.string)):
        link.string = link.string.replace('FM.view(', "")
        link.string = link.string.replace("})", "}")
        s = json.loads(link.string)
        #格式化输出 d1=json.dumps(s, sort_keys=True, indent=4)
        soups = BeautifulSoup(s["html"], "html.parser")
        for links in soups.findAll("div", class_="WB_detail"):
            WB_info = links.find("div", class_="WB_info")
            blog = WB_info.a.get("href").split("?")[0]
            blog1 = WB_info.a.get("href").split("?")[0].split("/")[-1]
            time = links.find("div", class_="WB_from S_txt2").a.string
            WB_txt = links.find("div", class_="WB_text W_f14").stripped_strings
            WB_txt1 = links.find("div", class_="WB_text W_f14").get_text() #直接获取所有文档内容
            # print(links.find("div", class_="WB_text W_f14"))
            # commen = ""
            # for cos in WB_txt:
            #     commen = commen+cos
           # print(commen)
            print("============", "Name：", WB_info.a.get("nick-name"), "TIME：", time, "用户ID", blog1)
            print("内容", WB_txt1)

        print("||||||||||||||||||||||||||||||||||||||||||||")
            #print("Name：", WB_info.a.get("nick-name"), "TIME：", time,"blog", blog,"COMMENT", WB_txt)