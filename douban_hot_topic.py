#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib
import shutil
import codecs
import os,os.path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36','Cookie':'bid="P6gBxQpuYps"; gr_user_id=18e12ac5-279d-4dc3-a8d4-d6f6dcea5ea5; viewed="1870268_26586492"; _ga=GA1.2.1751007425.1447316458; ll="108296"; ps=y; ue="henk1025@sina.com"; ct=y; dbcl2="9660099:hGpbxIydfrQ"; ck="MmgU"; ap=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1453961273%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DvrtLPJzCtmD-1GQpCWNHFd8ph7X-U3qG1_ynykb8vRiRYFjA00lJTdi8bj9GT5Nf%26wd%3D%26eqid%3Dc81c18e50001e0600000000456a86744%22%5D; push_noty_num=2; push_doumail_num=8; _pk_id.100001.8cb4=d335db68e62e01c0.1447316457.41.1453962589.1453958953.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.1751007425.1447316458.1453958928.1453961273.43; __utmb=30149280.26.10.1453961273; __utmc=30149280; __utmz=30149280.1453879433.36.21.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.966'}
res = requests.get("http://www.douban.com/group/explore")
soup = BeautifulSoup(res.text,'lxml')

for item in soup.select('.channel-item'):
	likes = item.select('.likes')[0].text
	title = item.select('.bd > h3')[0].text
	title = title.replace(',','，')
	links = item.select('.bd > h3 > a')[0]['href']
	ctt = likes+','+title+','+links
	print ctt
	with open('douban_hot_topic.csv','a+') as file:
		file.write(codecs.BOM_UTF8)
		file.write(ctt.encode('utf-8')+'\n')