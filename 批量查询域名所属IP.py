#coding=utf-8
'''
*---------------------------------------------*
*             批量查询域名所属IP
*    查询网站为：http://ip.tool.chinaz.com/
*         暂时写个初步的模板，待完成
*                        --2020.08.11
*      主体功能已完成，等待完善表格追写功能
*                        --2020.08.12
*
*
*
*---------------------------------------------*

'''
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from multiprocessing import Pool, cpu_count
import xlwt
import xlrd
from xlutils.copy import copy


class batch_query_domain():
    def __init__(self, url):
        self.url = url
        # self.file = file
        self.domains = []

    # def web_driver(self):   #创建web驱动
    #     self.browser = webdriver.Firefox()
    #     self.browser.set_window_size(1400, 900)
    #     self.wait = WebDriverWait(self.browser, 5)

    # def read_xlsx(self):    #读取各子表域名数据
    def read_xlsx(self, sheet, nrows): #读取当前子表内域名数据
        # self.table = xlrd.open_workbook(self.file)
        # self.sheets = []
        # for i in range(0, 10):
        #     self.sheets.append(self.table.sheets()[i])    #读取表格文件内所有子表
        # for i in range(0, 10):  #读取子表内的有效行数

        self.domains = sheet.col_values(1, 1, nrows) #将域名添加进domains列表
        #print(self.domains)
        return self.domains


    def request_domain(self, query_url):   #请求指定url

            # self.browser.get('http://ip.tool.chinaz.com/')
            # for i in self.domains:
            #     input = self.wait.until(ec.presence_of_element_located(By.CSS_SELECTOR, '#address'))
            #     input.send_keys('')
            user_agent = UserAgent()
            agent = user_agent.random
            headers = {
                "User-Agent": agent
            }
            url = self.url+ query_url     #构造get请求直接查询
            print("开始访问： " + url)
            try:
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    print(url + ' 访问正常')
                    #print(res.text)
                    return res.text

            except res.RequestException:
                print('请求错误!')
                return None


    def get_ip(self, soup):
        ips = []
        ip_list = soup.find(class_="WhoIpWrap jspu").find_all(class_="WhwtdWrap bor-b1s col-gray03")
        for item in ip_list:
            ips.append(item.find_all(class_="Whwtdhalf w15-0")[1].text)
        return ips


def main():
    url = 'http://ip.tool.chinaz.com/'
    file = 'tt.xlsx'
    # sheets = []
    batch_query = batch_query_domain(url)
    table = xlrd.open_workbook(file)
    sheets = table.sheets()
    nrows = []
    for sheet in sheets:
        nrows.append(sheet.nrows)
    write_table = copy(table)
    write_sheets = []

    for i in range(0, 10):
        write_sheets.append(write_table.get_sheet(i))


    print(write_sheets)

    for sheet in write_sheets:
        print(sheet)
        n = 0
        domains = batch_query.read_xlsx(sheet, nrows)
        print(domains)
        for domain in domains:
            html = batch_query.request_domain(domain)
            soup = BeautifulSoup(html, 'lxml')
            ips = batch_query.get_ip(soup)
            _ = 0
            for ip in ips:
                sheet.write(n, 5 + _, ip)
                _ = _ + 1
            n = n + 1
    table.save(u'td.xlsx')


if __name__ == '__main__':
    main()