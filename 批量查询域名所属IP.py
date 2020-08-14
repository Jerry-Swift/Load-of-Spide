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
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
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
    # def read_xlsx(self, sheet, nrows): #读取当前子表内域名数据
    #      self.table = xlrd.open_workbook(self.file)
    #      # self.sheets = []
    #      for i in range(0, 10):
    #          sheets.append(self.table.sheets()[i])    #读取表格文件内所有子表
    #      for i in range(0, 10):  #读取子表内的有效行数
    #
    #     self.domains = sheet.col_values(1, 1, nrows) #将域名添加进domains列表
    #     #print(self.domains)
    #     return self.domains

    def read_xlsx(self, sheet, nrow):       #从表格读取域名数据，在下一版本准备更新为数据库查询
        domains = sheet.col_values(1, 1, nrow)
        return domains



    def request_domain(self, query_url):   #请求目标url，IP查询网站基本可以通用

            # self.browser.get('http://ip.tool.chinaz.com/')
            # for i in self.domains:
            #     input = self.wait.until(ec.presence_of_element_located(By.CSS_SELECTOR, '#address'))
            #     input.send_keys('')
            user_agent = UserAgent()      #构造随机的User-Agent请求头，避免被反爬检测到导致拒绝访问
            agent = user_agent.random
            headers = {
                "User-Agent": agent
            }
            self.final_url = self.url+ query_url     #构造get请求直接查询
            #print("开始访问： " + self.url)
            try:
                res = requests.get(self.final_url, headers=headers)
                if res.status_code == 200:
                    print('访问正常: ' + self.final_url)
                    #print(res.text)
                    return res.text

            except res.RequestException:
                print('请求错误!')
                return None
        

    def get_ip(self, soup):     #从返回的页面中过滤出IP内容，需要根据不同网站重写子类函数，此函数仅适用于chinaz.com
        ips = []
        try:
            ip_list = soup.find(class_="WhoIpWrap jspu").find_all(class_="WhwtdWrap bor-b1s col-gray03")
            for item in ip_list:
                ips.append(item.find_all(class_="Whwtdhalf w15-0")[1].text)
        except BaseException:
            print(self.url)

        return ips
    
    
class batch_query_ip138(batch_query_domain):    #针对ip138.com重写子类
    def __init__(self, url):
        super.__init__(url)     #super()继承父类init
        
        
    def get_ip(self, soup):     #根据IP138.com返回的页面重写过滤函数
        ips = []
        try:
            ip_list = soup.find()
    
    
    
    
    
def main():
    url = 'http://ip.tool.chinaz.com/'
    file = 'tt.xlsx'
    # sheets = []
    batch_query = batch_query_domain(url)   #创建类实例
    table = xlrd.open_workbook(file)        #读取表格
    sheets = table.sheets()                 #获取所有的字表对象
    name_sheets = table.sheet_names()       #获取字表名称用于新建TXT文档
    print('***********表格名************')
    print(name_sheets)
    print('****************************')


    nrows = []                              #用于存储各字表的有效行数
    item = 0
    for sheet in sheets:

        nrows.append(sheet.nrows)           #获取字表行数并写入nrows
        nrow = sheet.nrows
        domains = batch_query.read_xlsx(sheet, nrow)
        print(domains)

        for domain in domains:
            html = batch_query.request_domain(domain)
            try:
                soup = BeautifulSoup(html, 'lxml')
            except BaseException:
                print('错误: ' + domain)
                print('!!!!!!!!!!!!!')
            ips = batch_query.get_ip(soup)
            with open(name_sheets[item] + '.txt', 'a') as f:
                print('写入： ' + name_sheets[item] + '.txt')
                f.write(str(ips))

        item += 1

        print(item)

    # write_table = copy(table)
    # write_sheets = []



    # print(write_sheets)
    #
    # for sheet in write_sheets:
    #     print(sheet)
    #     n = 0
    #     domains = batch_query.read_xlsx(sheet, nrows)
    #     print(domains)
    #     for domain in domains:
    #         html = batch_query.request_domain(domain)
    #         soup = BeautifulSoup(html, 'lxml')
    #         ips = batch_query.get_ip(soup)
    #         _ = 0
    #         for ip in ips:
    #             sheet.write(n, 5 + _, ip)
    #             _ = _ + 1
    #         n = n + 1
    # table.save(u'td.xlsx')


if __name__ == '__main__':
    main()