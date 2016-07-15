# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import request
import json

url = "https://www.zhihu.com/question/23928038"
webheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'cookie':'_zap=05c85782-1b68-4fde-84d3-ac8ffbf42ebc; d_c0="AFAAQmcNsgmPTroDVW5zKTdJPJKrTsFZNQw=|1459347713"; _za=e44d1c7a-6980-4bfb-b193-2344b7a2c296; _zap=b6c2e164-7a6f-49e7-800d-bb03ec5dc82f; q_c1=7343f0c390f64be8a43cfece40eeca29|1468064550000|1459347713000; _xsrf=ddd849ceeb96f3169d822ceb5afe284d; s-q=%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90; s-i=2; sid=luskjq88; s-t=autocomplete; cap_id="NjAyMTBjNGUyYzE1NDM0ZGEwYTU5MGI4Mjk1OWQxNTc=|1468412753|7b9c19a5245479f9ea140f922399c8870316d4a9"; l_cap_id="OWE5NzI3OWQ0MjM2NDdjMGEwZDYwYzNlMTQ3Y2U5MTM=|1468412993|3ec218181b5fc6cefd261b99429b3a06634c093b"; login="YjYwYWY5MzU0ZTFiNGZkYWIxOTU5YjQxMDRkNTQ2MGY=|1468413011|2d73fcaeced216e79dcc6852ba01d817c79f09cf"; a_t="2.0ABBMYS-GaAkXAAAAU8GtVwAQTGEvhmgJAFAAQmcNsgkXAAAAYQJVTVPBrVcArY8czK9zswaMWablztNtyx0Ix-9vXhIC6PWGfFqeIq2oAItikKRcrw=="; z_c0=Mi4wQUJCTVlTLUdhQWtBVUFCQ1p3MnlDUmNBQUFCaEFsVk5VOEd0VndDdGp4ek1yM096Qm94WnB1WE8wMjNMSFFqSDd3|1468413011|14f45b8f442a3f5bb98868cdc8ce1c966f55987a; n_c=1; __utma=51854390.1008111013.1468398575.1468408264.1468413030.4; __utmb=51854390.4.10.1468413030; __utmc=51854390; __utmz=51854390.1468413030.4.4.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/27621722; __utmv=51854390.100--|2=registration_date=20160202=1^3=entry_date=20160202=1',
    'Host': 'www.zhihu.com',
    'Referer': 'www.zhihu.com/question/20899988/answer/35284630',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.8.1000 Chrome/30.0.1599.101 Safari/537.36'
}
re = request.Request(url=url, headers=webheader)
response = request.urlopen(re)
html = response.read().decode("utf-8")
soup = BeautifulSoup(html,"html.parser")
# print(soup)
title = soup.find(id="zh-question-title").get_text(strip=True)
question = soup.find(id="zh-question-detail").get_text(strip=True)
answer_num = soup.find(id="zh-question-answer-num").get_text()

print("问题名称：", title, ' \n问题内容：', question,'\n回答数量：',answer_num)
n = 1
for item in soup.find_all( class_="zm-item-answer  zm-item-expanded"):
    print("\n 回答", n ,": 赞同数",item.find(class_="count").get_text())
    author = item.find(class_="zm-item-answer-author-info")
    author_name = author.find_all("a")[1].string
    author_page= author.find_all("a")[1]["href"]

    content = item.find(class_="zm-editable-content clearfix").get_text(strip=True)
    if author_name is not None:
        print("主页：https://www.zhihu.com",author_page)
    print("===内容如下========== \n", content)
    #print("个人简介", item.find("span")["title"],author)
    n +=1