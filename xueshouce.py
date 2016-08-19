# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
import time
from bs4 import BeautifulSoup
import logging
import  codecs

def get_txt_data(filepath, para):
    if para == 'lines':
        txt_file1 = codecs.open(filepath, 'r',encoding='utf-8')
        txt_tmp1 = txt_file1.readlines()
        print(type(txt_tmp1[0]))
        print(txt_tmp1)
        txt_tmp2 = ''.join(txt_tmp1)
        print((txt_tmp2))
        txt_data1 = txt_tmp2.split('\r\n')
        print(type(txt_data1))
        txt_file1.close()
        return txt_data1
    elif para == 'line':
        txt_file2 = open(filepath, 'r')
        txt_tmp = txt_file2.readline()
        txt_data2 = txt_tmp
        txt_file2.close()
        return txt_data2

print(get_txt_data('ha.txt',"lines"))

