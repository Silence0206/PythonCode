'''
程序名：   网络爬虫
功能：    根据"大众点评网"指定酒店的URL地址，自动抓取所有用户的"ID、评分、时间"。
语言：    python3.2
创建时间： 2013-4-01   修改于2014-8-08
作者:     python大菜鸟
'''
import urllib.request
import re
import time
import random

SleepNum = 3     # 抓取页面的间隔时间，可为0

# 获取指定time中的年份
def get_year(time):
    year = time.split('-')[0] 
    return int(year)

# 检查时间列表，查看是否有2010年之前的评论。[网页格式不同，正则表达式无法统一]
def no_previous10(timelist):
    for t in range(0,len(timelist)):
        year = get_year(timelist[t])
        if year<10:
            return False
        else:
            continue
    return True

# 统计所有酒店的评价信息，存入文本
def getRatingAll(fileIn, fileOut="rating.txt"):
    count =0          # 计数，显示进度 
    breaknumber = 0   # 计数，发生异常的url数

    for line in open(fileIn,'r'):     # 逐行读取并处理文件，即hotel的url
        try:
            #酒店编号     
            hotelid = line.strip('\n').split('/')[4]  

            # 拼凑出该酒店第一页"评论页面"的url
            url = line.strip('\n')+"/review_more"
            
            #模拟浏览器,打开url
            headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
            opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            data = opener.open(url).read()
            
            data = data.decode('utf-8','ignore')

            #该页面的评论数目((根据html源码分析，不同时期会发生变化,2014-8-23))
            rate_number = re.compile(r'全部点评</a><em class="col-exp">\((.*?)\)</em></span>',re.DOTALL).findall(data)  #列表形式
            rate_number = int(''.join(rate_number))   #类型转换
            print("测试：第%d家酒店的评论数为%s"%(count+1,rate_number))

            if rate_number == 0:       #如果评论数为0，跳过，处理下一个酒店URL
                count = count+1
                print("----------")
                continue
            else:
                # 解析评分
                pages = int(rate_number/20)+1        #由评论数计算页面数,点评网每页最多20条评论.
                #print(pages)
                for i in range(1,pages+1):
                    # 打开页面
                    add_url = url+'?pageno='+str(i)
                    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
                    opener = urllib.request.build_opener()
                    opener.addheaders = [headers]
                    data = opener.open(add_url).read()
                    #data = data.decode('utf-8')

                    #获取用户ID列表         
                    userid = re.compile(r'<a target="_blank" rel="nofollow".*?user-id="(.*?)" class="J_card">',re.DOTALL).findall(data)

                    #评价时间
                    rate_time = re.compile(r'<span class="time">(.*?)</span>',re.DOTALL).findall(data)    

                    #单项评分   
                    rate_room = re.compile(r'<span class="rst">房间(.*?)<em class="col-exp">',re.DOTALL).findall(data)    
                    rate_env = re.compile(r'<span class="rst">环境(.*?)<em class="col-exp">',re.DOTALL).findall(data)
                    rate_service = re.compile(r'<span class="rst">服务(.*?)<em class',re.DOTALL).findall(data)

                    # 总评分
                    rate_total = re.compile(r'<span title="" class="item-rank-rst irr-star(.*?)0"></span>',re.DOTALL).findall(data)

                    if no_previous10(rate_time):   # 只抓取2010年之后的评论                       

                        # 写入文件； 首先判断，如果每项数目都对应，则认为各项列表正确（一般是20）
                        fileOp = open(fileOut,'a',encoding="utf8")
                        #
                        if len(userid)==len(rate_total)==len(rate_room)==len(rate_env)==len(rate_service)==len(rate_time): #一般每页是20项评论
                            for k in range(0,len(userid)):
                                fileOp.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(hotelid,userid[k],rate_total[k],rate_room[k],rate_env[k],rate_service[k],rate_time[k]))
                        elif len(userid)==len(rate_total):            ## 如果仅仅有用户数和总评分数一致-->有用户没有"单项评分"
                            for k in range(0,len(userid)):
                                fileOp.write('%s\t%s\t%s\n'%(hotelid,userid[k],rate_total[k]))
                        else:
                            print("评分数字、用户数出现不一致，请检查正则表达式!")
            # +1,睡眠
            count = count+1
            time.sleep(SleepNum)
        # 异常处理：若异常，存储该url到新文本中，继续下一行的抓取
        except:
            file_except = open('exception.txt','a')
            file_except.write(line)
            breaknumber = breaknumber+1
            if breaknumber == 20:              #异常url的数目累积到20时，终止程序。
                break
            else:
                continue


#----------------------------------
#------------测试爬虫程序------------
#----------------------------------
if __name__ == "__main__":
    fileIn = ".\hotel.txt"
    getRatingAll(fileIn)

















