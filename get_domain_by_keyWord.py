#coding=utf-8
'''
*---------------------------------------------------------------*
*                      批量化自动获取关键词对应域名
*                  通过谷歌对指定文件内的关键词进行搜索
*                      得到结果后自动过滤出官网域名
*             当请求的结果为空或响应页面格式特殊时返回NULL字符串
*                    目前只是按照页面格式定位到域名
*                    程序逻辑为简单的URL拼接并请求
*                得到响应页面后再过滤出域名，不再详细说明
*                                              --2020.08.18
*                          下一版本计划：
*                      引入进程池，提高搜索速度
*                   创建代理池，避免因多次搜索被封IP
*       加入多个谷歌相关网站进行搜索，降低对单个谷歌服务器的请求次数
*        加入命令行调用格式，直接指定搜索关键词及保存结果的文件名
*                    加入特殊情况处理，增加容错性
*                            最终版本：
*                    加入余弦算法，提高过滤准确度
*---------------------------------------------------------------*
'''

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def get_keyWord(file):      #读取文件内关键词
    with open(file, 'r') as f:
        lists = f.readlines()
    return lists

def query_domain(url):      #创建随机请求头
    user_agent = UserAgent().random

    headers = {
        "User-Agent": user_agent
    }
    # proxies = {       #代理池，需要添加自动化选择代理功能
    #     'http': 'http://116.196.85.150:3128',
    #     'http': 'http://61.9.82.34:54351',
    #     'http': 'http://60.188.16.15:8928',
    #     'http': 'http://113.195.18.3:9999',
    #     'https': 'https://116.196.85.150:3128',
    #     'https': 'https://61.9.82.34:54351',
    #
    # }
    # ses = requests.session()          #创建session，以控制请求会话数量
    # requests.adapters.DEFAULT_RETRIES = 5     #重复请求次数，避免网络不稳定而请求失败
    # ses.keep_alive = False            #拒绝长连接
    # ses.headers = headers
    # ses.get(url)
    res = requests.get(url, headers=headers)

    try:
        #print(ses.)
        if res.status_code == 200:
            return res.text
    except BaseException:
        print('请求错误： ' + url)
        return None

def get_domain(soup):       #定位域名
    try:
        domain = soup.find(class_="iUh30 tjvcx").text
        return domain
    except AttributeError:
        print('URL has no attribute text')
        # with open('us_domain.txt', 'a') as file1:
        #     file1.write('NULL\n')
        pass

def main():
    lists = get_keyWord('us_target.txt')
    for item in lists:
        # url = 'https://www.google.com.hk/search?hl=en&q=%s' % item.repla
        url = 'http://www.google.ca/search?hl=en&q=%s' % item.replace(' ', '%20')   #空格需要转义为%20
        print(url)
        html = query_domain(url)
        soup = BeautifulSoup(html, 'lxml')
        domain = get_domain(soup)
        if domain:
            with open('us_domain.txt', 'a') as file:
                file.write(domain + '\n')
        else:
            with open('us_domain.txt', 'a') as file1:
                file1.write('NULL\n')
        time.sleep(5)

if __name__ == '__main__':
    main()