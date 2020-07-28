#coding=utf-8
'''

*-----------------------------------------------------------------------------*
*                                                                             *
*                         尝试编写第三个爬虫代码                                *
*                       爬取目标为B站坤坤的篮球视频                             *
*                              爬取内容为:                                     *
*                标题、UP主、播放次数、弹幕数、上传时间                          *
*                              程序逻辑为：                                    *
*                 访问主页，显式等待搜索框及搜索按钮元素                         *
*             加载完成后立即输入关键词，并提交点击搜索按钮的操作                  *
*    搜索请求提交后会产生新的标签页，通过window_handles获取到搜索结果页面的句柄    *
*                     拿到句柄后，提取出结果页面总数量                           *
*    在搜索结果第一页加载完成后，调用save_to_excel()，过滤出目标内容并写入excel    *
*                      以上操作由函数search()完成                               *
*               之后以循环调用next_page()的形式，请求并过滤2～50的页面            *
*           next_page()负责模拟点击下一页的按钮，并调用save_to_excel()           *
*                                                                             *
*-----------------------------------------------------------------------------*

'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt

browser = webdriver.Firefox()           #创建浏览器驱动实例
WAIT = WebDriverWait(browser, 10)       #页面等待时间
browser.set_window_size(1400,900)       #设置浏览器窗口大小

book = xlwt.Workbook(encoding='utf-8', style_compression=0)     #创建表格
sheet = book.add_sheet('坤坤篮球', cell_overwrite_ok=True)       #创建子表
sheet.write(0, 0, '名称')     #写入第0行各列属性名
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '播放次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1

def search():   #在主页搜索页面输入关键词，模拟点击搜索按钮的操作；显性等待到所有页面数量加载完毕，赋予total变量，并将其作为return值
    try:
        print('开始爬取××××××××××')
        browser.get("https://www.bilibili.com/")

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#nav_searchform > input')))         #定位主页输入框，加载完成即开始执行下一条指令
        submit = WAIT.until(EC.element_to_be_clickable(
                            (By.XPATH,
                             '/html/body/div[2]/div/div[1]/div/div[2]/div/form/div/button')))   #定位主页搜索按钮

        input.send_keys('蔡徐坤 篮球')       #输入框和搜索按钮加载完成后发送搜索关键词
        submit.click()                      #提交点击操作，前往搜索结果页面

        print('跳转新窗口')
        all_h = browser.window_handles      #获取窗口句柄
        browser.switch_to.window(all_h[1])  #拿到新出现的标签页的句柄
        get_source()

        total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
        return int(total.text)      #获取到页面数量
    except TimeoutException:
        return search()

def next_page(page_num):            #模拟点击下一页
    try:
        print('获取下一页××××××××××')
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                    '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'), str(page_num)))   #判断定位器中是否存在指定的文本，返回True或False。在此用于判断是否是当前页面
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):    #过滤当前页面内的目标内容，写入excel文件
    list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')

    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text

        print('爬取：' + item_title)

        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n = n + 1


def get_source():   #提取网页源码，调用save_to_excel函数，过滤出目标内容
    WAIT.until(EC.presence_of_element_located
               ((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))    #等待所有页面加载完成

    html = browser.page_source      #获取网页源代码
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def main():
    try:
        total = search()
        print(total)

        for i in range(2, int(total + 1)):
            next_page(i)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
    book.save('坤坤篮球.xlsx')
