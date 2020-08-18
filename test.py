#coding=utf-8
'''
完善谷歌批量搜索测试文件
添加多个谷歌服务器
多进程完成搜索任务
自动保存文件
'''

import requests
from bs4 import BeautifulSoup
from random_header import userAgent
from random import choice
from multiprocessing import Pool
import time

class batch_search():
    def __init__(self, key_word_file, domain_file_name):
        self.file = key_word_file

    def request_google(self, url):      #访问谷歌
        headers = userAgent()
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            print('错误请求码： ' + res.status_code)
            pass

    def get_keyWord(self):      #读取搜索关键词文件
        with open(self.file, 'r') as f:
            lists = f.readlines()
        return lists

    def get_google_url(self):   #随机获取一个谷歌服务器
        url_set = set()
        urls = [
                'http://www.google.com',
                'http://www.google.com.hk',
                'http://www.google.ca',
                'http://www.google.com.my',
                'http://www.google.co.za',
                ]
        for url in urls:
            url_set.add(url)
        url_ = choice(url_set) + '/search?hl=en&q='
        return url_

    def get_domain(self,):  #从关键词文件中读取内容，对任意一个谷歌服务器发起请求，定位出对应域名
       key_word_list =  self.get_keyWord()
       for item in key_word_list:
           url = self.get_google_url() + '%s' % item.replace(' ', '%20')
           html = self.request_google(url)
           soup = BeautifulSoup(html, 'lxml')
           try:
               domain = soup.find(class_="iUh30 tjvcx").text
               return domain
           except AttributeError:
               print('未定位到域名！')
               pass

    def mulproc(self):  #多进程搜索
        pass