#coding=utf-8
'''
*---------------------------------------------*
*              批量查询域名所属IP
*    查询网站为：http://ip.tool.chinaz.com/
*
*
*
*
*
*
*
*---------------------------------------------*

'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from multiprocessing import Pool, cpu_count
import xlwt
import xlrd


browser = webdriver.Firefox()
WAIT = WebDriverWait(browser, 5)
browser.set_window_size(1400,900)

book = xlrd.open_workbook('td.xlsx')
sheets = []

for i in range(1,11):
    sheets.append(book.sheets()[i])




def request_domain(url):
    pass

def save_to_excel(soup):
    pass

def main():
    pass

if __name__ == '__main__':
    main()