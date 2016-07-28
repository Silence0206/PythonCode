# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import time
from bs4 import BeautifulSoup
import logging

#调用readline()可以每次读取一行内容，调用readlines()一次读取所有内容并按行返回list。
def getFail():
    urls=[]
    with open ('fail_open_resURL.txt', 'r') as f:
        for line in f.readlines():
            if("pageno" in line.split("打开")[0]):
                # print(line.strip().split("打开")[0])
                urls.append(line.strip().split("打开")[0])
    return urls

print(getFail())