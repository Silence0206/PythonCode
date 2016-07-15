# -*- coding: utf-8 -*-
from urllib import request, parse
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup


print('Login to weibo.cn...')
url='https://passport.weibo.cn/sso/login'

login_data = parse.urlencode([
    ('username', "732379020@qq.com"),
    ('password', "5842HERO"),
    ('entry', 'mweibo'),
    ('client_id', ''),
    ('savestate', '1'),
    ('ec', ''),
    ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
])
filename = 'cookie.txt'
data=login_data.encode('utf-8')
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cookie = http.cookiejar.CookieJar()
pro = urllib.request.HTTPCookieProcessor(cookie)
openner = urllib.request.build_opener(pro)
urllib.request.install_opener(openner)#安装opener作为urlopen()使用的全局URL opener ，即以后调用urlopen()时都会使用安装的opener对象
openner.addheaders=[('Origin', 'https://passport.weibo.cn')]
openner.addheaders=[('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')]
openner.addheaders=[('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')]

with openner.open(url ,login_data.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        if k == "Set-Cookie" and v is not None:
            print('%s: %s' % (k, v))
    # print('Data:', f.read().decode('utf-8'))
    print("========接下来打开其他页面===========")

# 打开主页测试
response = openner.open("http://weibo.cn/")
for k, v in f.getheaders():
    if k == "Set-Cookie" and v is not None:
        print('%s: %s' % (k, v))

html = response.read().decode('utf-8')
soup = BeautifulSoup(html,"html.parser")
print(soup.prettify())




