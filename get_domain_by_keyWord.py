#coding=utf-8

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def get_keyWord(file):
    with open(file, 'r') as f:
        lists = f.readlines()
    return lists

def query_domain(url):
    user_agent = UserAgent().random

    headers = {
        "User-Agent": user_agent
    }
    proxies = {
        'http': 'http://116.196.85.150:3128',
        'http': 'http://61.9.82.34:54351',
        'http': 'http://60.188.16.15:8928',
        'http': 'http://113.195.18.3:9999',
        'https': 'https://116.196.85.150:3128',
        'https': 'https://61.9.82.34:54351',

    }
    ses = requests.session()
    requests.adapters.DEFAULT_RETRIES = 5
    ses.keep_alive = False
    ses.headers = headers
    ses.get(url)
    try:
        if ses.status_code == 200:
            return ses.text
    except BaseException:
        print('请求错误： ' + url)
        return None

def get_domain(soup):
    domain = soup.find(class_="iUh30 tjvcx").text
    return domain


def main():
    lists = get_keyWord('us_target.txt')
    for item in lists:
        # url = 'https://www.google.com.hk/search?hl=en&q=%s' % item.lstrip()
        url = 'http://www.google.com.hk/search?hl=en&q=hello'
        print(url)
        html = query_domain(url)
        soup = BeautifulSoup(html, 'lxml')
        domain = get_domain(soup)
        with open('us_domain.txt', 'a') as file:
            file.write(domain)
        time.sleep(1)

if __name__ == '__main__':
    main()