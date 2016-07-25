# *- coding: utf-8 -*-
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
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life",
    'Cookie':'_hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0.146908663; __utma=205923334.275296798.1469082376.1469082376.1469109403.2; __utmz=205923334.1469082376.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a650c81-15610b18a16-8a1918; _dp.ac.v=d0884a6b-b29b-4748-90a4-4f71e1bc8535; dper=4dcc94bf30f951ac9a83cfdc9df8d32056c8aab3926eb9220b40603ad7c444ff; ll=7fd06e815b796be3df069dec7836c3df; ua=732379010%40qq.com; ctu=b33af298f0f018b44702e07460c6750f2148460b1f3f12d2a2a92cf0e629162e; s_ViewType=10; aburl=1; cy=1; cye=shanghai; _hc.s=\"\\\"00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663.1469158888.1469159378\\\"\"'
}


#配置日志
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('DpComlog.txt')
# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s  %(funcName)s  %(module)s [line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def create_database(usr, pwd, db):
    global conn
    try:
        conn = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn.cursor()
        cursor.execute(
            'create table comments (comment_Id varchar(20) primary key, res_id varchar(20),'
            '  member_Id  varchar(20),member_name varchar(30),isVIP bool ,'
            'member_rank INT ,given_rank INT ,mean_price INT,'
            'taste INT ,envir INT ,service INT ,comment_text text,'
            ' comment_time datetime,addtime datetime default NULL,flag bool )')
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        logger.error(e)
        print("创建数据库出问题啦", e)

#访问过的店铺做标记
def set_flag(resId):
    global conn
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE restaurants SET flag=TRUE  WHERE res_id =%s'% resId)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print("创建数据库出问题啦", e)
        logger.error(e)
        error_resIdLog = open('error_resId.txt', 'a')
        error_resIdLog.writelines("时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"做标记失败的店铺："+resId+"\n")
        conn.rollback

# 更新一条记录的状态（某家店的某条评论）
def insert_rescomments (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,
            taste  ,envir  ,service  ,comment_text , comment_time ,addtime   ):
    global conn
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO comments (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,taste  ,envir  ,service  ,comment_text , comment_time ,addtime,flag)'
        'VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);',
        (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,taste  ,envir  ,service  ,comment_text , comment_time ,addtime, False))
    conn.commit()
    cursor.close()
    print(comment_Id, res_id, member_Id, member_name,isVIP, member_rank, given_rank, mean_price, taste, envir, service,comment_text, comment_time, addtime ,"插入成功")

def find_comment_onePage(url):
    resId= url.split("/")[4]
    if("review_more" not  in url):
        url += "/review_more"
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        # 页码
        pageDiv = soup.find(class_="Pages").find(class_="Pages")
        if ( pageDiv is not None):
            curr_pageNum = pageDiv.find(class_="PageSel").get_text()
            print("开始爬", url, "\n该页为第", curr_pageNum, "页")
        else:
            print("开始爬", url, "\n该页为第1页 共1页")
            curr_pageNum = 1
        comts = soup.find(class_="comment-list").find("ul")
    except BaseException as e:
        print(url, "打开出错休息2秒 错误原因：", e)
        error_resIdLog = open('error_resId.txt', 'a')
        error_resIdLog.writelines("打开页面失败的店铺："+resId+"时间："+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"原因：" + str(e) + "=========================\n")
        logger.error(e)
        time.sleep(1)
        return ("")
    # for comt in comts.find_all("li",recursive=False):#只检查子节点！！！
    #     try:
    #         comment_Id = comt["data-id"]
    #         memnber_Id = comt.select(".pic > a")[0]["user-id"]
    #         memnber_name = comt.select(".pic > .name")[0].get_text()
    #         isVIP = False
    #         if(comt.find(class_="icon-vip") is not None):
    #             isVIP = True
    #         rank_span = comt.find(class_="contribution").find("span")
    #         rank = rank_span["class"][1]
    #         mode = re.compile(r'\d+')
    #         member_rank = int(mode.findall(rank)[-1])
    #         content = comt.find(class_="content")
    #         given_rank=content.select(".user-info > .item-rank-rst")[0]["class"][1]
    #         given_rank = int(mode.findall(given_rank)[-1])
    #         mean_price = content.find(class_="comm-per")
    #         if(mean_price is not None):
    #             mean_price =int(mean_price.text.replace("人均 ￥",""))
    #         else:
    #             mean_price = 0
    #         comment_list = content.find(class_="comment-rst")
    #         taste=envir=service=0
    #         if(comment_list is not None):
    #            taste = comment_list.select("span:nth-of-type(1) ")[0].get_text()[2]
    #            envir = comment_list.select("span:nth-of-type(2) ")[0].get_text()[2]
    #            service = comment_list.select("span:nth-of-type(3) ")[0].get_text()[2]
    #         com_text=content.find(class_="J_brief-cont").get_text(strip=True)
    #         addtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         year = datetime.datetime.now().strftime("%Y-")
    #         #处理各种日期情况： 09-07-07  更新于07-07 21:45 ！ 09-07-08！07-24
    #         comment_timeStr = content.find(class_="time").get_text()
    #         if("更新于" not in comment_timeStr ):
    #             if(len(comment_timeStr) == 5):
    #                 comment_time = datetime.datetime.strptime(year+comment_timeStr,"%Y-%m-%d")
    #             elif(len(comment_timeStr) == 8):
    #                 comment_time = datetime.datetime.strptime("20"+comment_timeStr,"%Y-%m-%d")
    #             else:
    #                 comment_time = "0000-00-00 00:00:00"
    #         else:
    #             comment_timeStr =content.find(class_="time").get_text().split("更新于")[1]
    #             if (len(comment_timeStr) == 11):
    #                 comment_time = datetime.datetime.strptime(year + comment_timeStr, "%Y-%m-%d %H:%M")
    #             elif(len(comment_timeStr) == 5):
    #                 comment_time = datetime.datetime.strptime(year+comment_timeStr,"%Y-%m-%d")
    #             elif(len(comment_timeStr) == 8):
    #                 comment_time = datetime.datetime.strptime("20"+comment_timeStr,"%Y-%m-%d")
    #             else:
    #                 comment_time = "0000-00-00 00:00:00"
    #         insert_rescomments(comment_Id, resId, memnber_Id, memnber_name, isVIP, member_rank, given_rank, mean_price,
    #                            taste, envir, service, com_text, comment_time, addtime)
    #         # print(comment_Id, resId, memnber_Id, memnber_name, isVIP, member_rank, given_rank, mean_price,taste, envir, service, com_text, comment_time, addtime)
    #     except BaseException as e:
    #         print("解析该页的某条数据出错啦", e)
    #         error_resIdLog = open('error_resId.txt', 'a')
    #         error_resIdLog.writelines("某条数据解析错误 页面地址：" + url +"评论人" +memnber_name+"\n")
    #         error_resIdLog.writelines("时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"原因：" + str(e) + "=========================\n")
    #         logger.error(e)
    #         time.sleep(1)
    # print("第", curr_pageNum, "页爬取完成")
    # if (pageDiv is not None):
    #     next_page = pageDiv.find(class_="NextPage")
    # else:
    #     next_page = None
    #
    # if(next_page is not None):
    #     return ("http://www.dianping.com/shop/"+resId+"/review_more"+next_page["href"],resId, curr_pageNum, url)
    # else:
    #     return ("", resId,curr_pageNum, url)

def find_all_page(url):
    link = url
    while (link != ""):
        link = find_comment_onePage(link)[0]

def read_list(usr, pwd, db):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute( 'SELECT * FROM restaurants where comm_num >50')
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("出问题啦", e)
        return

n=0
create_database('root', '58424716', 'dianping')
# a=read_list('root', '58424716', 'dianping')
find_comment_onePage("http://www.dianping.com/shop/10010719/review_more?pageno=1")
# for item in a :
#     region_id=item[0] #店铺id 店铺名称 店铺链接
#     region_name=item[1]
#     region_link =item[2]
#     print("========开始爬取 店铺id:",region_id,"店铺名称：",region_name,"店铺链接：",region_link)
#     try:
#         find_all_page(region_link)
#     except BaseException as e:
#         print("爬取该店铺出错啦",e)
#         logger.error(e)
#         error_resIdLog = open('error_resId.txt', 'a')
#         error_resIdLog.writelines("做标记失败的店铺："+region_id+"   "+region_link+"\n")
#     set_flag(region_id)
#     n +=1
#     if(n>50):
#         break
#     time.sleep(3)
# for item in a :
#     region_id=item[0] #店铺id 店铺名称 店铺链接
#     region_name=item[1]
#     region_link =item[2]
#     print("========开始爬取 店铺id:",region_id,"店铺名称：",region_name,"店铺链接：",region_link)
#     try:
#         find_all_page(region_link)
#     except BaseException as e:
#         print("爬取该店铺出错啦",e)
#         logger.error(e)
#         error_resIdLog = open('error_resId.txt', 'a')
#         error_resIdLog.writelines("做标记失败的店铺："+region_id+"   "+region_link+"\n")
#     set_flag(region_id)
#     time.sleep(3)







        # find_all_page("http://www.dianping.com/shop/10333309")

        # # set_flag("3d1dd1")
# a=find_comment_onePage("http://www.dianping.com/shop/3259888/review_more?pageno=1106")
# print(a)
# insert_rescomments("2827101594", "3259888", "2032804", "花卷的妈咪", True, 45, 10, 0,
#                    0, 0, 0, "真的很", "0000-00-00 00:00:00", "2016-07-24 23:36:53")