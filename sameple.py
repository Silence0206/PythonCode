# import urllib.request
# import html
# import json
# from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import request
import json

url = "http://weibo.com/p/10080894bc9b5594697988610ffbdfe1268b0a"
webheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
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
soup = BeautifulSoup(html)
for link in soup.find_all("script"):
    if("FM.view" in link.string):
        if("\"html\"" in link.string):
              link.string = link.string.replace('FM.view(', "")
              link.string = link.string.replace("})", "}")
              #print(link.string)
              s = json.loads(link.string)
              soups = BeautifulSoup(s["html"])
              for links in soups.findAll("div", attrs={'class': 'WB_detail'}):
                  print(links.div.a.get("nick-name"))
                  for linkss in links.find_all("div", attrs={'class': 'WB_text W_f14'}):
                      for string in linkss.stripped_strings:
                          print(string)
                  print("------------------------------------------------------")








# weburl = "http://weibo.com/p/100808d39b6cd18e342b36cd190a45b73c5d17"
# webheader = {"Upgrade-Insecure-Requests": "1",
#              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
#              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#              "Host": "www.weibo.com",
#              "Cookie": "SINAGLOBAL=9389872080646.455.1448627975345; un=18030124710; SCF=AsLwLQ2XdtS8EaumVF1BzPRCkIc1YPOErfsjRwQkqu2n337xIsWsRYqeiVD6zWkW7auP-bBzLqhdC5YPu1UJ7UQ.; SUHB=0cSXD9a8qkdELk; SUB=_2AkMg3GeedcNhrABRnPoQyWngZIlH-jzEiebBAn7uJhMyAxgv7noDqSVSv0ED8McptMGQXnVazFAEGP2R4A..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh8BY0IJ3s7Mm_GCo8vIvho5JpVho2Rehe7eKzXS027TJSV; YF-Ugrow-G0=169004153682ef91866609488943c77f; WBStore=8ca40a3ef06ad7b2|undefined; _s_tentry=-; Apache=2888217715080.8276.1468070754528; ULV=1468070754580:35:9:7:2888217715080.8276.1468070754528:1468066678534; UOR=,,www.yibei.com If-Modified-Since: Sat, 09 Jul 2016 13:25:51 GMT"
#              }
# re = urllib.request.Request(url=weburl, headers=webheader)
# response = urllib.request.urlopen(re)
# data = response.read().decode("utf-8")
# print(data)

# weburl = "http://weibo.com/aj/v6/comment/small?ajwvr=6&act=list&mid=3954416413072107&isMain=true&dissDataFromFeed=%5Bobject%20Object%5D&ouid=1746575865&location=page_100505_home&comment_type=0&_t=0&__rnd=1468076136737"
# webheader = {"Upgrade-Insecure-Requests": "1",
#              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
#              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#              "Host": "www.weibo.com",
#              "Cookie": "SINAGLOBAL=9389872080646.455.1448627975345; un=18030124710; SCF=AsLwLQ2XdtS8EaumVF1BzPRCkIc1YPOErfsjRwQkqu2n337xIsWsRYqeiVD6zWkW7auP-bBzLqhdC5YPu1UJ7UQ.; SUHB=0cSXD9a8qkdELk; SUB=_2AkMg3GeedcNhrABRnPoQyWngZIlH-jzEiebBAn7uJhMyAxgv7noDqSVSv0ED8McptMGQXnVazFAEGP2R4A..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh8BY0IJ3s7Mm_GCo8vIvho5JpVho2Rehe7eKzXS027TJSV; YF-Ugrow-G0=169004153682ef91866609488943c77f; WBStore=8ca40a3ef06ad7b2|undefined; _s_tentry=-; Apache=2888217715080.8276.1468070754528; ULV=1468070754580:35:9:7:2888217715080.8276.1468070754528:1468066678534; UOR=,,www.yibei.com If-Modified-Since: Sat, 09 Jul 2016 13:25:51 GMT"
#              }
# re = urllib.request.Request(url=weburl, headers=webheader)
# response = urllib.request.urlopen(re)
# data = response.read().decode()
# s = json.loads(data)
# soup = BeautifulSoup(s["data"]["html"], "html.parser")
# for link in soup(class_ = "list_li S_line1 clearfix"):
#     for links in link.findAll('div', attrs={'class': 'WB_text'}):
#         print(links.a.string)
#         print(links.a.get("usercard"))

#print(s["data"]["html"])

# datas = data.decode('unicode_escape')
# #ss = html.unescape(datas)
# datas = datas.replace('\\', "")
# soup = BeautifulSoup(datas)
# print(soup)

#for link in soup.find_all("div"):
#    print(link.get("href"))


