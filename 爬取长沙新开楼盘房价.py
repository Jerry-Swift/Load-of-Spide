#coding=utf-8

'''
*-------------------------------------------------*
*          从房天下网站爬取新开楼盘的房价信息
*                 建立进程池爬取
*        域名为cs.newhouse.fang.com/house/s/
*     初步目标为爬取到楼盘、位置、价格、渲染图、单户面积
*          最后引入户型图、联系电话及详情链接
*       目前文件写入存在问题，待完善 --2020.08.11
*-------------------------------------------------*
'''

import xlwt
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from  multiprocessing import Pool, cpu_count
n = 1

def main(url):
    html = request_domain(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)

book = xlwt.Workbook(encoding='utf-8', style_compression=0) #创建表格 将需要统计的信息写入
sheet = book.add_sheet('长沙新开楼盘统计', cell_overwrite_ok=True)
sheet.write(0, 0, '楼盘名')
sheet.write(0, 1, '渲染图')
sheet.write(0, 2, '价格/每平米')
sheet.write(0, 3, '面积')
sheet.write(0, 4, '位置')
sheet.write(0, 5, '详情链接')

def request_domain(url):    #访问网页，返回页面文本内容
    user_agent = UserAgent()
    agent = user_agent.random
    headers = {
        "User-Agent": agent
    }
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            #print("All seems right Now!")
            return response.content.decode('GBK')   #按中文格式解码
    except requests.RequestException:
        print("Response is Null!\nAnd the url is: " + url)
        return None


def save_to_excel(soup):    #定位各元素Xpath，写入表格

    list = soup.find(class_="nhouse_list").find_all('li')   #将当前浏览页面内的所有楼盘信息写入列表
    #print(list[0])
    for item in list:
        try:
            item_name = item.find(class_='nlcd_name').find('a').string.strip()  #楼盘名
            #print(item_name)
            item_img = item.find(class_="nlc_img").find('img').get('src')   #渲染图
            item_price = item.find(class_="nhouse_price").string
            item_area = item.find(class_="house_type clearfix").text
            item_position = item.find(class_="address").find('a').get('title')
            item_detail_url = item.find(class_="address").find('a').get('href')
            global n

            sheet.write(n, 0, item_name)
            sheet.write(n, 1, item_img)
            sheet.write(n, 2, item_price)
            sheet.write(n, 3, item_area)
            sheet.write(n, 4, item_position)
            sheet.write(n, 5, item_detail_url)

            n += 1
            print(n)

        except BaseException:
            pass







if __name__ == '__main__':
    urls = []
    pool = Pool(cpu_count())  #Pool(进程数)  cpu_count()返回CPU内核数量

    for i in range(1,34):
        url = 'https://cs.newhouse.fang.com/house/s/b9' + str(i)
        urls.append(url)

    pool.map(main, urls)
    pool.close()
    pool.join()

    book.save(u'长沙新开楼盘.xlsx')
