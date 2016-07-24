#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import re
import MySQLdb
import time


db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user=‘数据库用户名’,
    passwd=‘数据库密码’,
    db=‘数据库的名字’,
    charset='utf8'
)
cur=db.cursor()

try:
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=17087217199&spuId=230003801&sellerId=1049653664&order=3&currentPage=1'
    cont=requests.get(url)
    myjson = re.findall('\"lastPage\":(.*?)\,',cont.text)[0]
    yeshu = int(myjson)+1
    for i in range(1,yeshu,1):
        print i
        # 小王子12月月销量10826
        # https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.6.FV8XGr&id=17087217199&areaId=310100&cat_id=50021913&rn=b37708f97072a0cfc27656fe374d2daa&user_id=1049653664&is_b=1
        url='https://rate.tmall.com/list_detail_rate.htm?itemId=17087217199&spuId=230003801&sellerId=1049653664&order=3&currentPage='+str(i)

        cont=requests.get(url)
        print "cont:"+cont.text
        myjson = re.findall('\"rateList\":(\[.*?\])\,\"searchinfo\"',cont.text)[0]
        mycont=json.loads(myjson,"utf8")
        count=len(mycont)
        for j in xrange(count):
            comment=mycont[j]['rateContent']
            commentTime = mycont[j]['rateDate']
            comment = comment.encode("utf-8")
            commentTime=commentTime.encode("utf-8")
            sql='insert into commenttxu5_1(comment,commentTime,nowTime) values(%s,%s,%s)'
            cur.execute(sql,(comment,commentTime,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            db.commit()

except Exception :
    print("hello")
    db.rollback()
print("world")
cur.close()
db.close()
